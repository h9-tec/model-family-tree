"""Ancestry graph over the Hub: unique-descendant counts for every model that has children.

Models form a DAG (merges have several parents), with the occasional cycle from a
mis-tagged card. Descendant sets are built children-first (Kahn order on the
child->parent direction) so every node's set is the union of its children's sets plus
the children themselves; each node is counted once no matter how many paths reach it.
"""

from __future__ import annotations

from collections import deque
from dataclasses import dataclass, field

import numpy as np
import polars as pl

from .fetch import RELATIONS

REL_CODE = {r: i for i, r in enumerate(RELATIONS)}
REL_CODE["unknown"] = len(RELATIONS)
N_REL = len(RELATIONS) + 1


@dataclass
class Graph:
    ids: list[str]                       # index -> model id (dump nodes first, then ghost parents)
    index: dict[str, int]
    n_real: int                          # ids[:n_real] exist in the dump; the rest are ghosts
    children: list[list[int]]            # parent -> children
    parents: list[list[int]]             # child -> parents
    edge_rel: dict[tuple[int, int], int]  # (child, parent) -> relation code
    node_rel: np.ndarray                 # relation of a node to its (first) parent, N_REL-1 if root
    created_day: np.ndarray              # days since epoch, -1 for ghosts
    desc_total: np.ndarray = field(default=None)
    desc_by_rel: np.ndarray = field(default=None)   # (n, N_REL)
    desc_30d: np.ndarray = field(default=None)
    desc_90d: np.ndarray = field(default=None)
    depth: np.ndarray = field(default=None)         # longest root->node chain below? no: max depth of subtree
    cyclic: set[int] = field(default_factory=set)
    _desc_sets: dict[int, np.ndarray] = field(default_factory=dict, repr=False)

    # ---- construction ---------------------------------------------------------------
    @classmethod
    def build(cls, nodes: pl.DataFrame, edges: pl.DataFrame) -> "Graph":
        ids = nodes["id"].to_list()
        index = {m: i for i, m in enumerate(ids)}
        n_real = len(ids)
        for p in edges["parent"].unique().to_list():
            if p not in index:
                index[p] = len(ids)
                ids.append(p)
        n = len(ids)
        children: list[list[int]] = [[] for _ in range(n)]
        parents: list[list[int]] = [[] for _ in range(n)]
        edge_rel: dict[tuple[int, int], int] = {}
        node_rel = np.full(n, N_REL - 1, dtype=np.int8)
        for c, p, r in zip(edges["child"].to_list(), edges["parent"].to_list(), edges["relation"].to_list()):
            ci, pi = index[c], index[p]
            children[pi].append(ci)
            parents[ci].append(pi)
            code = REL_CODE.get(r, N_REL - 1)
            edge_rel[(ci, pi)] = code
            if node_rel[ci] == N_REL - 1:
                node_rel[ci] = code
        created = nodes["created"].dt.epoch("d").fill_null(-1).to_numpy().astype(np.int64)
        created_day = np.concatenate([created, np.full(n - n_real, -1, dtype=np.int64)])
        return cls(ids, index, n_real, children, parents, edge_rel, node_rel, created_day)

    # ---- descendant closure -----------------------------------------------------------
    def compute(self, today_day: int, keep_sets_for: set[int] | None = None) -> None:
        n = len(self.ids)
        remaining = np.array([len(c) for c in self.children], dtype=np.int64)  # children not yet folded
        self.desc_total = np.zeros(n, dtype=np.int64)
        self.desc_by_rel = np.zeros((n, N_REL), dtype=np.int64)
        self.desc_30d = np.zeros(n, dtype=np.int64)
        self.desc_90d = np.zeros(n, dtype=np.int64)
        self.depth = np.zeros(n, dtype=np.int32)
        sets: dict[int, np.ndarray] = {}
        pending_parents = np.array([len(p) for p in self.parents], dtype=np.int64)
        keep = keep_sets_for or set()

        queue = deque(i for i in range(n) if remaining[i] == 0)
        done = np.zeros(n, dtype=bool)
        cut30, cut90 = today_day - 30, today_day - 90
        while queue:
            v = queue.popleft()
            if done[v]:
                continue
            done[v] = True
            if self.children[v]:
                parts = [np.fromiter(self.children[v], dtype=np.int64, count=len(self.children[v]))]
                for c in self.children[v]:
                    s = sets.get(c)
                    if s is not None and len(s):
                        parts.append(s)
                    pending_parents[c] -= 1
                    if pending_parents[c] == 0 and c not in keep:
                        sets.pop(c, None)
                d = np.unique(np.concatenate(parts)) if len(parts) > 1 else parts[0]
                self._record(v, d, cut30, cut90)
                self.depth[v] = 1 + max(self.depth[c] for c in self.children[v])
                sets[v] = d
            for p in self.parents[v]:
                remaining[p] -= 1
                if remaining[p] == 0:
                    queue.append(p)
        # Nodes left undone sit on or above a cycle. Resolve them by plain BFS.
        for v in np.flatnonzero(~done):
            self.cyclic.add(int(v))
            d = self._bfs_desc(int(v))
            self._record(int(v), d, cut30, cut90)
            sets[int(v)] = d
        self._desc_sets = {k: sets[k] for k in keep if k in sets}

    def _record(self, v: int, d: np.ndarray, cut30: int, cut90: int) -> None:
        self.desc_total[v] = len(d)
        self.desc_by_rel[v] = np.bincount(self.node_rel[d], minlength=N_REL)
        cd = self.created_day[d]
        self.desc_30d[v] = int((cd >= cut30).sum())
        self.desc_90d[v] = int((cd >= cut90).sum())

    def _bfs_desc(self, v: int) -> np.ndarray:
        seen = {v}
        q = deque([v])
        out = []
        while q:
            x = q.popleft()
            for c in self.children[x]:
                if c not in seen:
                    seen.add(c)
                    out.append(c)
                    q.append(c)
        return np.array(sorted(out), dtype=np.int64)

    # ---- queries ----------------------------------------------------------------------
    def descendants(self, v: int) -> np.ndarray:
        s = self._desc_sets.get(v)
        return s if s is not None else self._bfs_desc(v)

    def ancestors(self, v: int, limit: int = 64) -> list[list[int]]:
        """All root-ward chains from v (DAG-aware), each as [v, parent, grandparent, ...]."""
        chains: list[list[int]] = []
        stack = [[v]]
        while stack and len(chains) < limit:
            chain = stack.pop()
            ps = [p for p in self.parents[chain[-1]] if p not in chain]
            if not ps:
                chains.append(chain)
            for p in ps:
                stack.append(chain + [p])
        return chains

    def roots(self) -> np.ndarray:
        return np.array([i for i in range(len(self.ids)) if not self.parents[i] and self.children[i]], dtype=np.int64)

    def is_ghost(self, v: int) -> bool:
        return v >= self.n_real
