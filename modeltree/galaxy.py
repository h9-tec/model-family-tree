"""Lay out the whole ancestry graph as a galaxy: families are clusters, roots are stars,
every descendant is a point around its root. Written as compact binaries for the WebGL view.

Layout, from the inside out:
  1. each root's subtree is a radial tree: depth d lives in an annulus whose area matches the
     number of nodes at that depth, angles are partitioned by subtree size, so a child's
     descendants sit inside its wedge;
  2. the roots of a family are circle-packed (d3's front-chain packSiblings, ported);
  3. the families are circle-packed into the galaxy.
"""

from __future__ import annotations

import json
import math
from collections import deque
from pathlib import Path

import numpy as np

from .graph import Graph, N_REL

GOLDEN = 0.6180339887498949
CHUNK = 32768


# ---- circle packing (port of d3-hierarchy packSiblings) --------------------------------------
class _Node:
    __slots__ = ("i", "next", "previous")

    def __init__(self, i: int):
        self.i = i
        self.next = None
        self.previous = None


def pack_siblings(r: np.ndarray, pad: float = 0.0) -> tuple[np.ndarray, np.ndarray, float]:
    """Pack circles of radius r (in the given order) tightly; returns x, y and the enclosing radius."""
    n = len(r)
    rr = r.astype(np.float64) + pad
    x = np.zeros(n)
    y = np.zeros(n)
    if n == 0:
        return x, y, 0.0
    if n == 1:
        return x, y, float(rr[0] - pad)
    x[0], x[1] = -rr[1], rr[0]
    if n == 2:
        return x, y, float(rr[0] + rr[1] - pad)

    def place(b: int, a: int, c: int) -> None:
        dx, dy = x[b] - x[a], y[b] - y[a]
        d2 = dx * dx + dy * dy
        if d2:
            a2 = (rr[a] + rr[c]) ** 2
            b2 = (rr[b] + rr[c]) ** 2
            if a2 > b2:
                xx = (d2 + b2 - a2) / (2 * d2)
                yy = math.sqrt(max(0.0, b2 / d2 - xx * xx))
                x[c] = x[b] - xx * dx - yy * dy
                y[c] = y[b] - xx * dy + yy * dx
            else:
                xx = (d2 + a2 - b2) / (2 * d2)
                yy = math.sqrt(max(0.0, a2 / d2 - xx * xx))
                x[c] = x[a] + xx * dx - yy * dy
                y[c] = y[a] + xx * dy + yy * dx
        else:
            x[c] = x[a] + rr[c]
            y[c] = y[a]

    def intersects(a: int, b: int) -> bool:
        dr = rr[a] + rr[b] - 1e-6
        dx, dy = x[b] - x[a], y[b] - y[a]
        return dr > 0 and dr * dr > dx * dx + dy * dy

    def score(node: _Node) -> float:
        a, b = node.i, node.next.i
        ab = rr[a] + rr[b]
        dx = (x[a] * rr[b] + x[b] * rr[a]) / ab
        dy = (y[a] * rr[b] + y[b] * rr[a]) / ab
        return dx * dx + dy * dy

    place(1, 0, 2)
    a, b, c = _Node(0), _Node(1), _Node(2)
    a.next = c.previous = b
    b.next = a.previous = c
    c.next = b.previous = a
    i = 3
    while i < n:
        place(a.i, b.i, i)
        c = _Node(i)
        j, k = b.next, a.previous
        sj, sk = rr[b.i], rr[a.i]
        retry = False
        while True:
            if sj <= sk:
                if intersects(j.i, c.i):
                    b = j
                    a.next = b
                    b.previous = a
                    retry = True
                    break
                sj += rr[j.i]
                j = j.next
            else:
                if intersects(k.i, c.i):
                    a = k
                    a.next = b
                    b.previous = a
                    retry = True
                    break
                sk += rr[k.i]
                k = k.previous
            if j is k.next:
                break
        if retry:
            continue
        c.previous = a
        c.next = b
        a.next = b.previous = b = c
        aa = score(a)
        cc = c.next
        while cc is not b:
            ca = score(cc)
            if ca < aa:
                a, aa = cc, ca
            cc = cc.next
        b = a.next
        i += 1
    # enclosing circle: centre at the radius-weighted centroid, radius to the farthest edge; recentre
    cx, cy = float(np.average(x, weights=rr)), float(np.average(y, weights=rr))
    x -= cx
    y -= cy
    R = float(np.max(np.hypot(x, y) + rr)) - pad
    return x, y, R


# ---- radial subtree layout ----------------------------------------------------------------------
def _subtree_layout(g: Graph, root: int, owner: np.ndarray, order_out: list[int], spacing: float = 1.0) -> tuple[list[int], np.ndarray, np.ndarray, float]:
    """BFS from root over children not yet owned; returns (nodes, dx, dy, radius) with root at 0,0."""
    nodes = [root]
    owner[root] = root
    depth = {root: 0}
    parent = {root: -1}
    q = deque([root])
    while q:
        v = q.popleft()
        for c in g.children[v]:
            if owner[c] == -1:
                owner[c] = root
                parent[c] = v
                depth[c] = depth[v] + 1
                nodes.append(c)
                q.append(c)
    m = len(nodes)
    dx = np.zeros(m)
    dy = np.zeros(m)
    if m == 1:
        return nodes, dx, dy, 1.0
    pos = {v: i for i, v in enumerate(nodes)}
    # subtree sizes (reverse BFS order)
    size = np.ones(m)
    for i in range(m - 1, 0, -1):
        size[pos[parent[nodes[i]]]] += size[i]
    # angular spans: children split the parent's span in proportion to subtree size
    a0 = np.zeros(m)
    a1 = np.zeros(m)
    a1[0] = 2 * math.pi
    cursor = np.zeros(m)
    cursor[0] = 0.0
    for i in range(1, m):
        p = pos[parent[nodes[i]]]
        span = (a1[p] - a0[p]) * size[i] / (size[p] - 1)
        a0[i] = a0[p] + cursor[p]
        a1[i] = a0[i] + span
        cursor[p] += span
    # annuli: depth d occupies [R_d, R_{d+1}] with area = count_d * spacing^2 (at least one ring)
    depths = np.array([depth[v] for v in nodes])
    maxd = int(depths.max())
    counts = np.bincount(depths, minlength=maxd + 1)
    R = [0.0, 1.5 * spacing]
    for d in range(1, maxd + 1):
        area = counts[d] * spacing * spacing * 1.6
        R.append(math.sqrt(R[-1] ** 2 + area / math.pi + (2.2 * spacing) ** 2 * 0 + 0.0) + 0.9 * spacing)
    # position: angle at the middle of the span, radius spread across the annulus by a golden-ratio hash
    k = np.arange(m)
    frac = (k * GOLDEN) % 1.0
    ang = (a0 + a1) / 2
    for i in range(1, m):
        d = depths[i]
        r = math.sqrt(R[d] ** 2 + frac[i] * (R[d + 1] ** 2 - R[d] ** 2))
        dx[i] = r * math.cos(ang[i])
        dy[i] = r * math.sin(ang[i])
    return nodes, dx, dy, R[maxd + 1] + spacing


# ---- whole galaxy -------------------------------------------------------------------------------
def layout(g: Graph, root_family: dict[int, str], display: dict[str, str], downloads: np.ndarray) -> dict:
    n = len(g.ids)
    owner = np.full(n, -1, dtype=np.int64)
    roots = g.roots()
    roots = roots[np.argsort(-g.desc_total[roots], kind="stable")]

    # 1. subtrees
    sub = {}  # root -> (nodes, dx, dy, R)
    for r in roots.tolist():
        sub[r] = _subtree_layout(g, r, owner, [])
    # nodes inside cycles never reached from a root: attach them to a synthetic family
    leftovers = [v for v in range(n) if owner[v] == -1 and (g.parents[v] or g.children[v])]
    for v in leftovers:
        if owner[v] == -1:
            sub[v] = _subtree_layout(g, v, owner, [])

    # 2. roots packed per family
    fam_roots: dict[str, list[int]] = {}
    for r in sub:
        fam_roots.setdefault(root_family.get(r, "cycles" if r in leftovers else "misc"), []).append(r)
    fam_pos: dict[str, tuple[np.ndarray, np.ndarray, float]] = {}
    for f, rs in fam_roots.items():
        rs.sort(key=lambda r: -sub[r][3])
        rad = np.array([sub[r][3] for r in rs])
        x, y, R = pack_siblings(rad, pad=1.0)
        fam_pos[f] = (x, y, R)
    # 3. families packed into the galaxy
    fams = sorted(fam_pos, key=lambda f: -fam_pos[f][2])
    fr = np.array([fam_pos[f][2] for f in fams])
    fx, fy, G = pack_siblings(fr, pad=3.0)

    # assemble point arrays, ordered family -> root -> bfs
    total = sum(len(sub[r][0]) for r in sub)
    X = np.zeros(total, dtype=np.float32)
    Y = np.zeros(total, dtype=np.float32)
    REL = np.zeros(total, dtype=np.uint8)
    SZ = np.zeros(total, dtype=np.uint8)
    IDX = np.zeros(total, dtype=np.int64)  # graph index per point
    dl = np.log10(np.maximum(downloads, 0) + 1)
    families_meta, roots_meta = [], []
    p = 0
    for fi, f in enumerate(fams):
        x0, y0 = float(fx[fi]), float(fy[fi])
        rx, ry, R = fam_pos[f]
        members = 0
        for ri, r in enumerate(fam_roots[f]):
            nodes, dx, dy, rr = sub[r]
            m = len(nodes)
            cx, cy = x0 + float(rx[ri]), y0 + float(ry[ri])
            X[p:p + m] = cx + dx
            Y[p:p + m] = cy + dy
            idx = np.array(nodes)
            IDX[p:p + m] = idx
            rel = g.node_rel[idx].astype(np.uint8)
            rel[0] = 5  # root
            ghost = idx >= g.n_real
            rel[ghost] = 6
            REL[p:p + m] = rel
            real = np.where(ghost, 0.0, dl[np.minimum(idx, g.n_real - 1)])
            SZ[p:p + m] = np.clip(real * 36, 0, 255).astype(np.uint8)
            SZ[p] = 255
            if m >= 5 or g.desc_total[r] >= 5:
                roots_meta.append({"i": int(p), "id": g.ids[r], "x": round(cx, 2), "y": round(cy, 2), "r": round(float(rr), 2), "n": int(g.desc_total[r]), "f": fi})
            p += m
            members += m
        families_meta.append({"k": f, "d": display.get(f, f), "x": round(x0, 2), "y": round(y0, 2), "r": round(float(R), 2), "n": members})
    return {"x": X, "y": Y, "rel": REL, "size": SZ, "idx": IDX, "families": families_meta, "roots": roots_meta, "radius": G}


def write_galaxy(g: Graph, lay: dict, out: Path, date: str) -> dict:
    out.mkdir(parents=True, exist_ok=True)
    n = len(lay["x"])
    buf = np.concatenate([lay["x"].view(np.uint8), lay["y"].view(np.uint8), lay["rel"], lay["size"]])
    (out / "points.bin").write_bytes(buf.tobytes())
    ids = [g.ids[i] for i in lay["idx"].tolist()]
    nchunks = (n + CHUNK - 1) // CHUNK
    for c in range(nchunks):
        (out / f"ids-{c:03d}.json").write_text(json.dumps(ids[c * CHUNK:(c + 1) * CHUNK], ensure_ascii=False, separators=(",", ":")))
    # parents (models with descendants) -> point index, for "show in galaxy" and search
    desc = g.desc_total[lay["idx"]]
    parents_index = {ids[i]: [int(i), int(desc[i])] for i in np.flatnonzero(desc > 0).tolist()}
    (out / "parents-index.json").write_text(json.dumps(parents_index, ensure_ascii=False, separators=(",", ":")))
    fams = [f for f in lay["families"] if f["n"] >= 3]
    meta = {"generated_at": date, "n": n, "chunk": CHUNK, "chunks": nchunks, "radius": round(float(lay["radius"]), 2),
            "rel": ["finetune", "adapter", "quantized", "merge", "unknown", "root", "ghost"],
            "families": fams, "roots": sorted(lay["roots"], key=lambda r: -r["n"])[:6000]}
    (out / "meta.json").write_text(json.dumps(meta, ensure_ascii=False, separators=(",", ":")))
    return {"points": n, "families": len(fams), "roots": len(meta["roots"]), "chunks": nchunks, "bytes": len(buf)}
