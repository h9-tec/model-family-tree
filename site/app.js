/* Open Model Family Tree explorer. Leaderboards come from dist/ (nightly build);
   ancestors, children and search are live from the Hugging Face API. */
(() => {
  const HF = "https://huggingface.co/api";
  const $ = (s, r = document) => r.querySelector(s);
  const $$ = (s, r = document) => [...r.querySelectorAll(s)];
  const fmt = (n) => (n == null ? "–" : Number(n).toLocaleString("en-US"));
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const hfLink = (id) => `<a href="https://huggingface.co/${esc(id)}" rel="noopener" target="_blank">↗</a>`;
  const mLink = (id) => `<a href="#m=${encodeURIComponent(id)}" class="id">${esc(id)}</a>`;

  const state = { lb: null, stats: null, ts: null, parents: null, kind: "models_all_time", fam: "", sort: null, rel: "", model: null, famOff: new Set() };

  // ---------- data ----------
  const json = (u) => fetch(u).then((r) => (r.ok ? r.json() : Promise.reject(new Error(`${u}: ${r.status}`))));
  async function loadCore() {
    [state.lb, state.stats] = await Promise.all([json("dist/leaderboard.json"), json("dist/stats.json")]);
    const s = state.stats;
    $("#stat-line").textContent = `${fmt(s.models)} models · ${fmt(s.edges)} parent links · updated ${s.generated_at}`;
    const sel = $("#fam-filter");
    state.lb.families.slice(0, 60).forEach((f) => {
      const o = document.createElement("option");
      o.value = f.family; o.textContent = `${f.display} (${fmt(f.total)})`; sel.appendChild(o);
    });
  }
  async function loadParents() {
    if (state.parents) return state.parents;
    const p = await json("dist/parents.json");
    const idx = p.columns.reduce((a, c, i) => ((a[c] = i), a), {});
    state.parents = new Map(p.rows.map((r) => [r[0], { direct: r[idx.direct], total: r[idx.total], d90: r[idx.d90], finetune: r[idx.finetune], adapter: r[idx.adapter], quantized: r[idx.quantized], merge: r[idx.merge], family: r[idx.family] }]));
    return state.parents;
  }
  const famDisplay = (key) => (state.lb.families.find((f) => f.family === key) || {}).display || key;

  // ---------- routing ----------
  function route() {
    const h = decodeURIComponent(location.hash.slice(1) || "board");
    let view = "board";
    if (h.startsWith("m=")) { view = "model"; state.model = h.slice(2); }
    else if (h.startsWith("families")) view = "families";
    else if (h.startsWith("board")) { view = "board"; const k = h.split(":")[1]; if (k) state.kind = k; }
    $$(".view").forEach((v) => (v.hidden = v.id !== `view-${view}`));
    $$("nav a[data-view]").forEach((a) => a.classList.toggle("on", a.dataset.view === view));
    if (view === "board") renderBoard();
    if (view === "families") renderFamilies();
    if (view === "model") renderModel(state.model);
  }

  // ---------- leaderboard ----------
  const MODEL_COLS = [
    ["#", null, ""], ["Model", "id", ""], ["Descendants", "total", "num"], ["Direct", "direct", "num"], ["Last 90d", "d90", "num"],
    ["Finetune", "by_rel.finetune", "num"], ["Adapter", "by_rel.adapter", "num"], ["Quantized", "by_rel.quantized", "num"], ["Merge", "by_rel.merge", "num"], ["Family", "family_display", ""],
  ];
  const ORG_COLS = [["#", null, ""], ["Organization", "org", ""], ["Descendants", "total", "num"], ["Last 90d", "d90", "num"], ["Roots", "n_roots", "num"], ["Biggest root", "roots.0.id", ""]];
  const get = (o, path) => path.split(".").reduce((a, k) => (a == null ? a : a[k]), o);

  const REL_COLOR = { finetune: "#4C78A8", adapter: "#F58518", quantized: "#54A24B", merge: "#E45756", unknown: "#9a9aa2" };
  let allRows = null, page = 0;
  async function renderBoard() {
    $$("#kind button").forEach((b) => b.classList.toggle("on", b.dataset.kind === state.kind));
    const isAll = state.kind === "all";
    $("#all-q").hidden = !isAll; $("#pager").hidden = !isAll;
    if (isAll) return renderAll();
    const isOrg = state.kind === "orgs";
    const cols = isOrg ? ORG_COLS : MODEL_COLS;
    let rows = state.lb[state.kind].slice();
    if (!isOrg && state.fam) rows = rows.filter((r) => r.family === state.fam);
    const scoreKey = state.kind === "models_90d" ? "d90" : state.kind === "models_finetune" ? "by_rel.finetune" : "total";
    if (state.sort) rows.sort((a, b) => (get(b, state.sort.key) ?? -1) - (get(a, state.sort.key) ?? -1) * (state.sort.dir));
    const max = Math.max(...rows.map((r) => get(r, scoreKey) || 0), 1);
    const t = $("#board");
    t.innerHTML = `<thead><tr>${cols.map(([l, k, c]) => `<th class="${c} ${state.sort && state.sort.key === k ? "sorted" : ""}" data-key="${k || ""}">${l}</th>`).join("")}</tr></thead>` +
      `<tbody>${rows.map((r, i) => isOrg
        ? `<tr><td class="num">${i + 1}</td><td class="id"><a href="https://huggingface.co/${esc(r.org)}" target="_blank" rel="noopener">${esc(r.org)}</a></td><td class="num"><span class="bar" style="width:${(80 * r.total) / max}px"></span>${fmt(r.total)}</td><td class="num">${fmt(r.d90)}</td><td class="num">${fmt(r.n_roots)}</td><td class="id">${r.roots[0] ? mLink(r.roots[0].id) : ""}</td></tr>`
        : `<tr><td class="num">${i + 1}</td><td class="id">${mLink(r.id)}${r.ghost ? ' <span class="ghost" title="no longer public">†</span>' : ""} ${hfLink(r.id)}</td>` +
          `<td class="num"><span class="bar ${scoreKey === "d90" ? "hot" : ""}" style="width:${(80 * (get(r, scoreKey) || 0)) / max}px"></span>${fmt(r.total)}</td>` +
          `<td class="num">${fmt(r.direct)}</td><td class="num">${fmt(r.d90)}</td><td class="num">${fmt(r.by_rel.finetune)}</td><td class="num">${fmt(r.by_rel.adapter)}</td><td class="num">${fmt(r.by_rel.quantized)}</td><td class="num">${fmt(r.by_rel.merge)}</td><td>${esc(r.family_display || "")}</td></tr>`
      ).join("")}</tbody>`;
    $("#board-note").textContent = { models_all_time: "unique descendants of every kind, all time", models_90d: "sorted by new descendants created in the last 90 days", models_finetune: "sorted by descendants whose relation to their parent is finetune", orgs: "descendants of every root the organization owns" }[state.kind];
    $$("th", t).forEach((th) => th.addEventListener("click", () => {
      const k = th.dataset.key; if (!k) return;
      state.sort = state.sort && state.sort.key === k ? { key: k, dir: -state.sort.dir } : { key: k, dir: 1 };
      renderBoard();
    }));
  }
  async function renderAll() {
    const t = $("#board");
    if (!allRows) {
      t.innerHTML = `<tbody><tr><td class="loading">loading all parents (5 MB)…</td></tr></tbody>`;
      const p = await loadParents();
      allRows = [...p.entries()].map(([id, r]) => ({ id, ...r, by_rel: { finetune: r.finetune, adapter: r.adapter, quantized: r.quantized, merge: r.merge }, family_display: r.family ? famDisplay(r.family) : "" }));
    }
    const q = $("#all-q").value.trim().toLowerCase();
    let rows = q ? allRows.filter((r) => r.id.toLowerCase().includes(q) || (r.family_display || "").toLowerCase().includes(q)) : allRows;
    const key = state.sort ? state.sort.key : "total";
    const dir = state.sort ? state.sort.dir : 1;
    rows = rows.slice().sort((a, b) => key === "id" || key === "family_display" ? String(a[key]).localeCompare(String(b[key])) * dir : ((get(b, key) ?? -1) - (get(a, key) ?? -1)) * dir);
    const PER = 100, pages = Math.max(1, Math.ceil(rows.length / PER));
    page = Math.min(page, pages - 1);
    const slice = rows.slice(page * PER, (page + 1) * PER);
    const max = Math.max(...slice.map((r) => r.total), 1);
    t.innerHTML = `<thead><tr>${MODEL_COLS.map(([l, k, c]) => `<th class="${c} ${key === k ? "sorted" : ""}" data-key="${k || ""}">${l}</th>`).join("")}</tr></thead><tbody>` +
      slice.map((r, i) => `<tr><td class="num">${page * PER + i + 1}</td><td class="id">${mLink(r.id)} ${hfLink(r.id)}</td><td class="num"><span class="bar" style="width:${(80 * r.total) / max}px"></span>${fmt(r.total)}</td><td class="num">${fmt(r.direct)}</td><td class="num">${fmt(r.d90)}</td><td class="num">${fmt(r.finetune)}</td><td class="num">${fmt(r.adapter)}</td><td class="num">${fmt(r.quantized)}</td><td class="num">${fmt(r.merge)}</td><td>${esc(r.family_display)}</td></tr>`).join("") + "</tbody>";
    $("#board-note").textContent = `${fmt(rows.length)} models with at least one declared descendant`;
    $("#pager").innerHTML = `<button id="pg-prev" ${page === 0 ? "disabled" : ""}>‹ prev</button> page ${page + 1} of ${fmt(pages)} <button id="pg-next" ${page >= pages - 1 ? "disabled" : ""}>next ›</button>`;
    $("#pg-prev").onclick = () => { page--; renderAll(); };
    $("#pg-next").onclick = () => { page++; renderAll(); };
    $$("th", t).forEach((th) => th.addEventListener("click", () => { const k = th.dataset.key; if (!k) return; state.sort = state.sort && state.sort.key === k ? { key: k, dir: -state.sort.dir } : { key: k, dir: 1 }; page = 0; renderAll(); }));
  }
  $("#all-q").addEventListener("input", () => { page = 0; renderAll(); });
  $("#kind").addEventListener("click", (e) => { const b = e.target.closest("button"); if (!b) return; state.kind = b.dataset.kind; state.sort = null; location.hash = `board:${state.kind}`; });
  $("#fam-filter").addEventListener("change", (e) => { state.fam = e.target.value; renderBoard(); });

  // ---------- families ----------
  async function renderFamilies() {
    state.ts = state.ts || (await json("dist/timeseries.json"));
    const fams = state.lb.families.filter((f) => state.ts.families[f.family]).slice(0, 12);
    const months = state.ts.months.slice(-24);
    const series = fams.map((f) => {
      const full = state.ts.families[f.family];
      let acc = f.total - full.reduce((a, b) => a + b, 0) + full.slice(0, -24).reduce((a, b) => a + b, 0);
      return { key: f.family, name: f.display, values: full.slice(-24).map((v) => (acc += v)) };
    });
    const W = 1200, H = 480, L = 80, R = 210, T = 24, B = 40;
    const on = series.filter((s) => !state.famOff.has(s.key));
    const ymax = d3.max(on, (s) => d3.max(s.values)) || 1;
    const x = d3.scalePoint().domain(months).range([L, W - R]);
    const y = d3.scaleLinear().domain([0, ymax]).nice().range([H - B, T]);
    const color = d3.scaleOrdinal(["#4C78A8", "#F58518", "#54A24B", "#E45756", "#72B7B2", "#B279A2", "#FF9DA6", "#9D755D", "#BAB0AC", "#8CD17D", "#F1CE63", "#A0CBE8"]).domain(series.map((s) => s.key));
    const svg = d3.create("svg").attr("viewBox", `0 0 ${W} ${H}`);
    svg.append("g").selectAll("line").data(y.ticks(5)).join("line").attr("class", "grid").attr("x1", L).attr("x2", W - R).attr("y1", y).attr("y2", y);
    svg.append("g").selectAll("text").data(y.ticks(5)).join("text").attr("class", "lbl").attr("x", L - 8).attr("y", (d) => y(d) + 4).attr("text-anchor", "end").text(fmt);
    svg.append("g").selectAll("text").data(months.filter((m, i) => i % 3 === 0 || i === months.length - 1)).join("text").attr("class", "lbl").attr("x", x).attr("y", H - B + 18).attr("text-anchor", "middle").text((d) => d);
    const line = d3.line().x((d, i) => x(months[i])).y((d) => y(d));
    svg.append("g").selectAll("path").data(on).join("path").attr("fill", "none").attr("stroke", (s) => color(s.key)).attr("stroke-width", 2.5).attr("d", (s) => line(s.values));
    const lg = svg.append("g").selectAll("g").data(series).join("g").attr("class", (s) => `legend ${state.famOff.has(s.key) ? "off" : ""}`).attr("transform", (s, i) => `translate(${W - R + 14},${T + 14 + i * 22})`)
      .on("click", (e, s) => { state.famOff.has(s.key) ? state.famOff.delete(s.key) : state.famOff.add(s.key); renderFamilies(); });
    lg.append("rect").attr("width", 12).attr("height", 12).attr("rx", 3).attr("y", -10).attr("fill", (s) => color(s.key));
    lg.append("text").attr("x", 18).text((s) => `${s.name} · ${fmt(s.values[s.values.length - 1])}`);
    $("#fam-chart").replaceChildren(svg.node());
    $("#fam-table").innerHTML = `<thead><tr><th>#</th><th>Family</th><th class="num">Descendants</th><th class="num">Last 90d</th><th class="num">Roots</th><th class="num">Finetune</th><th class="num">Adapter</th><th class="num">Quantized</th><th class="num">Merge</th><th>Biggest root</th><th>Orgs</th></tr></thead><tbody>` +
      state.lb.families.slice(0, 100).map((f, i) => `<tr><td class="num">${i + 1}</td><td><b>${esc(f.display)}</b></td><td class="num">${fmt(f.total)}</td><td class="num">${fmt(f.d90)}</td><td class="num">${fmt(f.n_roots)}</td><td class="num">${fmt(f.by_rel.finetune)}</td><td class="num">${fmt(f.by_rel.adapter)}</td><td class="num">${fmt(f.by_rel.quantized)}</td><td class="num">${fmt(f.by_rel.merge)}</td><td class="id">${f.roots[0] ? mLink(f.roots[0].id) : ""}</td><td class="small muted">${f.orgs.map(esc).join(", ")}</td></tr>`).join("") + "</tbody>";
  }

  // ---------- explorer ----------
  const hfModel = (id) => fetch(`${HF}/models/${id}`).then((r) => (r.ok ? r.json() : null)).catch(() => null);
  function basesOf(info) {
    if (!info) return { parents: [], rel: null };
    const tags = info.tags || [];
    const typed = tags.filter((t) => t.startsWith("base_model:") && t.split(":").length === 3);
    if (typed.length) return { parents: [...new Set(typed.map((t) => t.split(":")[2]))], rel: typed[0].split(":")[1] };
    const plain = tags.filter((t) => t.startsWith("base_model:") && t.split(":").length === 2).map((t) => t.slice(11));
    return { parents: [...new Set(plain)], rel: plain.length ? "unknown" : null };
  }
  async function fetchChildren(id, rel, limit = 40) {
    const f = rel ? `base_model:${rel}:${id}` : `base_model:${id}`;
    const r = await fetch(`${HF}/models?filter=${encodeURIComponent(f)}&sort=downloads&direction=-1&limit=${limit}`);
    if (!r.ok) return { rows: [], total: null };
    const rows = await r.json();
    return { rows, total: Number(r.headers.get("X-Total-Count")) || rows.length };
  }
  let renderSeq = 0;
  async function renderModel(id) {
    const seq = ++renderSeq;
    $("#model-head").innerHTML = `<h2>${esc(id)} ${hfLink(id)}</h2><div class="loading">loading…</div>`;
    $("#ancestors").innerHTML = ""; $("#children").innerHTML = ""; $("#tree").innerHTML = "";
    $$("#rel button").forEach((b) => b.classList.toggle("on", b.dataset.rel === state.rel));
    const [parents, info] = await Promise.all([loadParents(), hfModel(id)]);
    if (seq !== renderSeq) return;
    const c = parents.get(id) || {};
    const ghost = !info;
    $("#model-head").innerHTML = `<h2>${esc(id)} ${hfLink(id)}${ghost ? ' <span class="pill">not public (ghost)</span>' : ""}${c.family ? ` <span class="pill">${esc(famDisplay(c.family))}</span>` : ""}${c.total ? ` <a class="pill" href="galaxy.html#id=${encodeURIComponent(id)}">show in galaxy ✦</a>` : ""}</h2>` +
      `<div class="stats">${[["descendants", c.total ?? 0], ["direct children", c.direct ?? 0], ["last 90 days", c.d90 ?? 0], ["finetunes", c.finetune ?? 0], ["adapters", c.adapter ?? 0], ["quantized", c.quantized ?? 0], ["merges", c.merge ?? 0], ["downloads / month", info ? info.downloads : null], ["likes", info ? info.likes : null]].map(([l, v]) => `<div class="stat"><b>${fmt(v)}</b><span>${l}</span></div>`).join("")}</div>`;

    // ancestry: walk first parents live
    const chain = [{ id, rel: null, info }];
    let cur = basesOf(info), seen = new Set([id]);
    while (cur.parents.length && chain.length < 12 && !seen.has(cur.parents[0])) {
      const pid = cur.parents[0]; seen.add(pid);
      chain[chain.length - 1].rel = cur.rel; chain[chain.length - 1].parents = cur.parents;
      const pinfo = await hfModel(pid);
      if (seq !== renderSeq) return;
      chain.push({ id: pid, rel: null, info: pinfo });
      cur = basesOf(pinfo);
    }
    const top = chain.slice().reverse();
    $("#ancestors").innerHTML = top.map((n, i) => {
      const pc = parents.get(n.id) || {};
      const me = n.id === id;
      const rel = n.rel ? `<span class="rel">${esc(n.rel)} of ↓</span>` : "";
      const multi = n.parents && n.parents.length > 1 ? `<span class="rel">+${n.parents.length - 1} more parent${n.parents.length > 2 ? "s" : ""}: ${n.parents.slice(1).map(mLink).join(", ")}</span>` : "";
      return `<li class="${me ? "me" : ""}">${i === 0 ? '<span class="rel">root</span> ' : ""}${me ? `<b>${esc(n.id)}</b>` : mLink(n.id)}${n.info ? "" : ' <span class="ghost">†</span>'} <span class="muted">${pc.total ? fmt(pc.total) + " desc." : ""}</span> ${multi} ${rel}</li>`;
    }).join("");

    // children live
    const { rows, total } = await fetchChildren(id, state.rel);
    if (seq !== renderSeq) return;
    $("#children-note").textContent = total != null ? `${fmt(total)} live${state.rel ? ` (${state.rel})` : ""}` : "";
    const relOf = (m) => ((m.tags || []).find((t) => t.startsWith("base_model:") && t.endsWith(":" + id) && t.split(":").length === 3) || "::").split(":")[1] || "";
    $("#children").innerHTML = rows.length
      ? `<thead><tr><th>Model</th><th>Relation</th><th class="num">Downloads</th><th class="num">Likes</th><th class="num">Descendants</th><th>Task</th></tr></thead><tbody>` +
        rows.map((m) => { const pc = parents.get(m.id) || {}; return `<tr><td class="id">${mLink(m.id)} ${hfLink(m.id)}</td><td class="small muted">${esc(relOf(m))}</td><td class="num">${fmt(m.downloads)}</td><td class="num">${fmt(m.likes)}</td><td class="num">${fmt(pc.total ?? 0)}</td><td class="small muted">${esc(m.pipeline_tag || "")}</td></tr>`; }).join("") + "</tbody>"
      : `<tbody><tr><td class="muted">no declared children${state.rel ? ` with relation ${state.rel}` : ""}</td></tr></tbody>`;

    // pedigree: every ancestor path on the left, top descendants (expandable) on the right
    const anc = await ancestorTree(id, info, parents);
    if (seq !== renderSeq) return;
    const desc = { id, me: true, ghost, kids: rows.slice(0, 30).map((m) => ({ id: m.id, rel: relOf(m), dl: m.downloads || 0, n: (parents.get(m.id) || {}).total || 0, kids: null })), dl: info ? info.downloads : 0, n: c.total || 0 };
    pedigree = { id, anc, desc, parents, seq };
    drawPedigree();
  }

  const infoCache = new Map();
  const cachedModel = (id) => infoCache.get(id) || (infoCache.set(id, hfModel(id)), infoCache.get(id));
  async function ancestorTree(id, info, parents, depth = 0, path = new Set()) {
    const node = { id, info, ghost: !info, dl: info ? info.downloads : 0, n: (parents.get(id) || {}).total || 0, kids: [] };
    if (depth >= 10) return node;
    const { parents: ps, rel } = basesOf(info);
    node.rel = rel;
    for (const pid of ps.slice(0, 6)) {
      if (path.has(pid)) continue;
      const pinfo = await cachedModel(pid);
      const child = await ancestorTree(pid, pinfo, parents, depth + 1, new Set([...path, id]));
      child.edge = rel;
      node.kids.push(child);
    }
    return node;
  }

  let pedigree = null;
  function drawPedigree() {
    if (!pedigree) return;
    const { anc, desc, parents } = pedigree;
    const STEP = 170;
    const A = d3.hierarchy(anc, (d) => d.kids), D = d3.hierarchy(desc, (d) => d.kids || []);
    const sep = (a, b) => (a.parent === b.parent ? 1 : 1.6) / Math.max(a.depth, 1);
    d3.tree().size([Math.PI, Math.max(A.height, 1) * STEP]).separation(sep)(A);
    d3.tree().size([Math.PI, Math.max(D.height, 1) * STEP]).separation(sep)(D);
    const place = (nodes, offset) => nodes.forEach((d) => { const th = (nodes.length === 1 ? Math.PI / 2 : d.x) + offset; d.theta = th; d.px = d.depth === 0 ? 0 : d.y * Math.cos(th); d.py = d.depth === 0 ? 0 : d.y * Math.sin(th); });
    place(A.descendants(), Math.PI / 2);   // left half: angles in [π/2, 3π/2]
    place(D.descendants(), -Math.PI / 2);  // right half: angles in [-π/2, π/2]
    const nodes = [...A.descendants().filter((d) => d.depth > 0), ...D.descendants()];
    const links = [...A.links().map((l) => ({ ...l, side: "anc", rel: l.target.data.edge })), ...D.links().map((l) => ({ ...l, side: "desc", rel: l.target.data.rel }))];
    const rScale = (dl) => 3 + Math.min(9, 2.2 * Math.log10((dl || 0) + 1));
    const xs = nodes.map((d) => d.px), ys = nodes.map((d) => d.py);
    const pad = 150;
    const x0 = Math.min(-300, ...xs) - pad, x1 = Math.max(300, ...xs) + pad, y0 = Math.min(-200, ...ys) - 60, y1 = Math.max(200, ...ys) + 60;
    const svg = d3.create("svg").attr("viewBox", `${x0} ${y0} ${x1 - x0} ${y1 - y0}`);
    const g = svg.append("g");
    svg.call(d3.zoom().scaleExtent([0.3, 6]).on("zoom", (e) => g.attr("transform", e.transform)));
    g.append("text").attr("class", "axis").attr("x", x0 + 20).attr("y", y0 + 24).text("← ancestors");
    g.append("text").attr("class", "axis").attr("x", x1 - 20).attr("y", y0 + 24).attr("text-anchor", "end").text("descendants →");
    const curve = (l) => { const s = l.source, t = l.target; const sx = s.depth === 0 ? 0 : s.px, sy = s.depth === 0 ? 0 : s.py; const mx = (sx + t.px) / 2; return `M${sx},${sy}C${mx},${sy} ${mx},${t.py} ${t.px},${t.py}`; };
    g.selectAll("path.pl").data(links).join("path").attr("class", "pl").attr("d", curve).attr("stroke", (l) => REL_COLOR[l.rel] || REL_COLOR.unknown).attr("stroke-width", (l) => 1 + Math.min(3, Math.log10((l.target.data.dl || 0) + 1) / 2));
    const tip = $("#xtip");
    const n = g.selectAll("g.pn").data(nodes, (d) => d.data.id + (d.side || "")).join("g")
      .attr("class", (d) => `pn ${d.data.me ? "me" : ""} ${d.data.ghost ? "ghost" : ""} ${d.data.kids === null && d.data.n ? "more" : ""} ${(d.data.kids && d.data.kids.length === 0 && d.data.rel === null && d.depth > 0) ? "root" : ""}`)
      .attr("transform", (d) => `translate(${d.px},${d.py})`)
      .on("mousemove", (e, d) => { const r = $("#tree").getBoundingClientRect(); tip.style.display = "block"; tip.style.left = `${e.clientX - r.left + 12}px`; tip.style.top = `${e.clientY - r.top + 12}px`; tip.innerHTML = `<b>${esc(d.data.id)}</b><br>${d.data.rel ? esc(d.data.rel) + " · " : ""}${fmt(d.data.dl || 0)} dl/mo · ${fmt(d.data.n || 0)} descendants${d.data.kids === null && d.data.n ? "<br><i>click to unfold</i>" : ""}`; })
      .on("mouseleave", () => (tip.style.display = "none"))
      .on("click", async (e, d) => { if (d.data.kids === null && d.data.n) { d.data.kids = [{ id: "…", loading: true }]; const { rows } = await fetchChildren(d.data.id, state.rel, 15); d.data.kids = rows.map((m) => ({ id: m.id, rel: ((m.tags || []).find((t) => t.startsWith("base_model:") && t.endsWith(":" + d.data.id) && t.split(":").length === 3) || "::").split(":")[1], dl: m.downloads || 0, n: (parents.get(m.id) || {}).total || 0, kids: null })); drawPedigree(); } })
      .on("dblclick", (e, d) => { e.stopPropagation(); if (!d.data.me && !d.data.loading) location.hash = `m=${encodeURIComponent(d.data.id)}`; });
    n.append("circle").attr("r", (d) => (d.data.me ? 10 : rScale(d.data.dl))).attr("fill", (d) => d.data.ghost ? "none" : d.data.me ? "var(--accent)" : REL_COLOR[d.data.rel] || "#d4a017");
    n.append("text").attr("dy", "0.32em")
      .attr("transform", (d) => { if (d.depth === 0) return "translate(0,-20)"; const deg = (d.theta * 180) / Math.PI; const flip = Math.cos(d.theta) < 0; const lift = d.children && d.children.length ? -13 : 0; return `rotate(${flip ? deg + 180 : deg}) translate(${flip ? -(rScale(d.data.dl) + 6) : rScale(d.data.dl) + 6},${lift})`; })
      .attr("text-anchor", (d) => (d.depth === 0 ? "middle" : Math.cos(d.theta) < 0 ? "end" : "start"))
      .text((d) => (d.data.loading ? "loading…" : d.data.id.length > 36 ? "…" + d.data.id.slice(-35) : d.data.id) + (d.data.kids === null && d.data.n ? ` (+${fmt(d.data.n)})` : ""));
    $("#tree").replaceChildren(svg.node(), tip);
  }
  $("#rel").addEventListener("click", (e) => { const b = e.target.closest("button"); if (!b) return; state.rel = b.dataset.rel; renderModel(state.model); });

  // ---------- search ----------
  const q = $("#q"), sug = $("#suggest");
  let timer = null, sel = -1;
  q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(suggest, 220); });
  q.addEventListener("keydown", (e) => {
    const items = $$("li", sug);
    if (e.key === "ArrowDown") { sel = Math.min(sel + 1, items.length - 1); items.forEach((li, i) => li.classList.toggle("on", i === sel)); e.preventDefault(); }
    else if (e.key === "ArrowUp") { sel = Math.max(sel - 1, 0); items.forEach((li, i) => li.classList.toggle("on", i === sel)); e.preventDefault(); }
    else if (e.key === "Enter") { const id = sel >= 0 && items[sel] ? items[sel].dataset.id : q.value.trim(); if (id) go(id); }
    else if (e.key === "Escape") hide();
  });
  function go(id) { hide(); q.value = ""; location.hash = `m=${encodeURIComponent(id)}`; }
  function hide() { sug.hidden = true; sug.innerHTML = ""; sel = -1; }
  async function suggest() {
    const v = q.value.trim();
    if (v.length < 2) return hide();
    const r = await fetch(`${HF}/models?search=${encodeURIComponent(v)}&sort=downloads&direction=-1&limit=8`).catch(() => null);
    const rows = r && r.ok ? await r.json() : [];
    if (q.value.trim() !== v) return;
    const parents = state.parents;
    sug.innerHTML = rows.map((m) => `<li data-id="${esc(m.id)}"><span>${esc(m.id)}</span><span class="muted">${parents && parents.get(m.id) ? fmt(parents.get(m.id).total) + " desc." : fmt(m.downloads) + " dl"}</span></li>`).join("");
    sug.hidden = !rows.length; sel = -1;
    $$("li", sug).forEach((li) => li.addEventListener("mousedown", () => go(li.dataset.id)));
  }
  document.addEventListener("click", (e) => { if (!e.target.closest(".search-row")) hide(); });

  // ---------- boot ----------
  window.addEventListener("hashchange", route);
  loadCore().then(route).catch((e) => { $("#stat-line").textContent = `failed to load data: ${e.message}`; });
})();
