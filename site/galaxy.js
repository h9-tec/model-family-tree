/* Model Galaxy: ~1M points in WebGL2, labels on a 2D overlay, nearest-point picking on a grid. */
(async () => {
  const $ = (s) => document.querySelector(s);
  const fmt = (n) => Number(n).toLocaleString("en-US");
  const esc = (s) => String(s).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
  const BASE = "dist/galaxy/";
  const COLORS = [[0.35, 0.66, 1.0], [1.0, 0.62, 0.26], [0.43, 0.9, 0.63], [1.0, 0.42, 0.62], [0.7, 0.7, 0.8], [1.0, 0.84, 0.4], [0.54, 0.54, 0.59]];

  const [meta, buf] = await Promise.all([fetch(BASE + "meta.json").then((r) => r.json()), fetch(BASE + "points.bin").then((r) => r.arrayBuffer())]);
  const n = meta.n;
  const X = new Float32Array(buf, 0, n), Y = new Float32Array(buf, 4 * n, n);
  const REL = new Uint8Array(buf, 8 * n, n), SZ = new Uint8Array(buf, 9 * n, n);
  $("#gstats").textContent = `${fmt(n)} models with an ancestor or a descendant · ${fmt(meta.families.length)} families · ${meta.generated_at}`;

  // ---------- picking grid (CSR) ----------
  const CELL = 6, R = meta.radius + 10, G = Math.ceil((2 * R) / CELL);
  const cellOf = (x, y) => (Math.floor((y + R) / CELL) * G + Math.floor((x + R) / CELL));
  const cellIds = new Int32Array(n), counts = new Int32Array(G * G + 1);
  for (let i = 0; i < n; i++) { const c = cellOf(X[i], Y[i]); cellIds[i] = c; counts[c + 1]++; }
  for (let c = 0; c < G * G; c++) counts[c + 1] += counts[c];
  const order = new Int32Array(n), fill = counts.slice(0, G * G);
  for (let i = 0; i < n; i++) order[fill[cellIds[i]]++] = i;
  function nearest(wx, wy, maxD) {
    const cx = Math.floor((wx + R) / CELL), cy = Math.floor((wy + R) / CELL), span = Math.ceil(maxD / CELL);
    let best = -1, bd = maxD * maxD;
    for (let gy = cy - span; gy <= cy + span; gy++) for (let gx = cx - span; gx <= cx + span; gx++) {
      if (gx < 0 || gy < 0 || gx >= G || gy >= G) continue;
      const c = gy * G + gx;
      for (let k = counts[c]; k < counts[c + 1]; k++) { const i = order[k]; const dx = X[i] - wx, dy = Y[i] - wy, d = dx * dx + dy * dy; if (d < bd) { bd = d; best = i; } }
    }
    return best;
  }

  // ---------- WebGL ----------
  const canvas = $("#gl"), labels = $("#labels"), ctx = labels.getContext("2d");
  const gl = canvas.getContext("webgl2", { antialias: false, alpha: false, premultipliedAlpha: false });
  if (!gl) { $("#loading").textContent = "WebGL2 is not available in this browser."; return; }
  const vs = `#version 300 es
    layout(location=0) in vec2 p; layout(location=1) in float rel; layout(location=2) in float sz;
    uniform vec2 u_scale; uniform vec2 u_offset; uniform float u_k; uniform float u_dpr; uniform vec3 u_colors[7];
    out vec3 v_col; out float v_alpha;
    void main() {
      vec2 s = p * u_k + u_offset;
      gl_Position = vec4(s * u_scale - vec2(1.0, -1.0) * vec2(1.0, 1.0) * vec2(1.0) + vec2(-1.0, 1.0) * 0.0, 0.0, 1.0);
      gl_Position = vec4(s.x * u_scale.x - 1.0, 1.0 - s.y * u_scale.y, 0.0, 1.0);
      float base = rel == 5.0 ? 2.6 : (0.55 + sz / 255.0 * 1.8);
      float ps = base * pow(u_k, 0.5);
      gl_PointSize = clamp(ps, 1.0, rel == 5.0 ? 30.0 : 16.0) * u_dpr;
      v_col = u_colors[int(rel)];
      v_alpha = rel == 5.0 ? 1.0 : clamp(0.35 + 0.25 * log(u_k + 1.0), 0.35, 0.95);
    }`;
  const fs = `#version 300 es
    precision mediump float; in vec3 v_col; in float v_alpha; out vec4 o;
    void main() { vec2 c = gl_PointCoord - 0.5; float d = dot(c, c); if (d > 0.25) discard; float a = smoothstep(0.25, 0.05, d); o = vec4(v_col * a * v_alpha, a * v_alpha); }`;
  const prog = gl.createProgram();
  for (const [t, src] of [[gl.VERTEX_SHADER, vs], [gl.FRAGMENT_SHADER, fs]]) { const sh = gl.createShader(t); gl.shaderSource(sh, src); gl.compileShader(sh); if (!gl.getShaderParameter(sh, gl.COMPILE_STATUS)) console.error(gl.getShaderInfoLog(sh)); gl.attachShader(prog, sh); }
  gl.linkProgram(prog); gl.useProgram(prog);
  const pos = new Float32Array(2 * n); for (let i = 0; i < n; i++) { pos[2 * i] = X[i]; pos[2 * i + 1] = Y[i]; }
  const bind = (loc, data, size, type, norm) => { const b = gl.createBuffer(); gl.bindBuffer(gl.ARRAY_BUFFER, b); gl.bufferData(gl.ARRAY_BUFFER, data, gl.STATIC_DRAW); gl.enableVertexAttribArray(loc); gl.vertexAttribPointer(loc, size, type, norm, 0, 0); };
  bind(0, pos, 2, gl.FLOAT, false); bind(1, REL, 1, gl.UNSIGNED_BYTE, false); bind(2, SZ, 1, gl.UNSIGNED_BYTE, false);
  gl.uniform3fv(gl.getUniformLocation(prog, "u_colors"), new Float32Array(COLORS.flat()));
  gl.enable(gl.BLEND); gl.blendFunc(gl.ONE, gl.ONE_MINUS_SRC_ALPHA);
  const U = { scale: gl.getUniformLocation(prog, "u_scale"), offset: gl.getUniformLocation(prog, "u_offset"), k: gl.getUniformLocation(prog, "u_k"), dpr: gl.getUniformLocation(prog, "u_dpr") };

  // ---------- view ----------
  let W = 0, H = 0, dpr = 1, t = d3.zoomIdentity;
  function resize() {
    dpr = Math.min(window.devicePixelRatio || 1, 2); W = innerWidth; H = innerHeight;
    canvas.width = labels.width = W * dpr; canvas.height = labels.height = H * dpr; gl.viewport(0, 0, W * dpr, H * dpr);
    draw();
  }
  function fitAll() { const k = Math.min(W, H) / (2.1 * meta.radius); return d3.zoomIdentity.translate(W / 2, H / 2).scale(k); }
  function draw() {
    gl.clearColor(0.027, 0.027, 0.047, 1); gl.clear(gl.COLOR_BUFFER_BIT);
    gl.uniform2f(U.scale, 2 / W, 2 / H); gl.uniform2f(U.offset, t.x, t.y); gl.uniform1f(U.k, t.k); gl.uniform1f(U.dpr, dpr);
    gl.drawArrays(gl.POINTS, 0, n);
    drawLabels();
  }
  function drawLabels() {
    ctx.setTransform(dpr, 0, 0, dpr, 0, 0); ctx.clearRect(0, 0, W, H);
    ctx.textAlign = "center"; ctx.textBaseline = "middle";
    const vis = (x, y, r) => x + r > 0 && x - r < W && y + r > 0 && y - r < H;
    // family rings + names (largest first; a label that would overlap one already placed is skipped)
    const placed = [];
    const free = (x, y, w, h) => !placed.some((b) => x < b.x + b.w && x + w > b.x && y < b.y + b.h && y + h > b.y);
    for (const f of meta.families) {
      const sx = f.x * t.k + t.x, sy = f.y * t.k + t.y, sr = f.r * t.k;
      if (sr < 18 || !vis(sx, sy, sr)) continue;
      ctx.beginPath(); ctx.arc(sx, sy, sr, 0, 2 * Math.PI); ctx.strokeStyle = `rgba(255,255,255,${Math.min(0.12, sr / 2000)})`; ctx.lineWidth = 1; ctx.stroke();
      const fs = Math.max(11, Math.min(26, sr / 6));
      ctx.font = `600 ${fs}px ui-sans-serif, system-ui, sans-serif`;
      const w = ctx.measureText(f.d).width + 8, ly = sy - sr - fs * 0.7;
      if (!free(sx - w / 2, ly - fs / 2, w, fs)) continue;
      placed.push({ x: sx - w / 2, y: ly - fs / 2, w, h: fs });
      ctx.fillStyle = sr > 60 ? "rgba(255,255,255,.85)" : "rgba(255,255,255,.55)";
      ctx.fillText(f.d, sx, ly);
    }
    // root names
    ctx.font = `12px ui-monospace, Menlo, monospace`;
    for (const r of meta.roots) {
      const sx = r.x * t.k + t.x, sy = r.y * t.k + t.y, sr = r.r * t.k;
      if (sr < 40 || !vis(sx, sy, sr)) continue;
      const w = ctx.measureText(r.id).width + 6;
      if (!free(sx - w / 2, sy + 8, w, 12)) continue;
      placed.push({ x: sx - w / 2, y: sy + 8, w, h: 12 });
      ctx.fillStyle = "rgba(255,215,102,.95)"; ctx.fillText(r.id, sx, sy + 14);
    }
  }
  const zoom = d3.zoom().scaleExtent([0.05, 400]).on("zoom", (e) => { t = e.transform; draw(); });
  d3.select(canvas).call(zoom);
  window.addEventListener("resize", resize);
  resize();
  d3.select(canvas).call(zoom.transform, fitAll());
  $("#loading").remove();

  // ---------- ids (lazy chunks) ----------
  const chunks = new Map();
  async function idOf(i) {
    const c = Math.floor(i / meta.chunk);
    if (!chunks.has(c)) chunks.set(c, fetch(`${BASE}ids-${String(c).padStart(3, "0")}.json`).then((r) => r.json()));
    return (await chunks.get(c))[i % meta.chunk];
  }
  let parentsIndex = null;
  const loadParentsIndex = () => parentsIndex || (parentsIndex = fetch(BASE + "parents-index.json").then((r) => r.json()));

  // ---------- interactions ----------
  const tip = $("#tip"), card = $("#card");
  let hoverTimer = null, hovered = -1;
  canvas.addEventListener("mousemove", (e) => {
    const [wx, wy] = t.invert([e.clientX, e.clientY]);
    const i = nearest(wx, wy, 10 / t.k);
    hovered = i;
    if (i < 0) { tip.style.display = "none"; return; }
    clearTimeout(hoverTimer);
    hoverTimer = setTimeout(async () => { if (hovered !== i) return; const id = await idOf(i); if (hovered !== i) return; tip.textContent = `${id} · ${meta.rel[REL[i]]}`; tip.style.display = "block"; tip.style.left = `${e.clientX + 14}px`; tip.style.top = `${e.clientY + 14}px`; }, 60);
  });
  canvas.addEventListener("mouseleave", () => (tip.style.display = "none"));
  canvas.addEventListener("click", async (e) => {
    const [wx, wy] = t.invert([e.clientX, e.clientY]);
    const i = nearest(wx, wy, 12 / t.k);
    if (i < 0) { card.hidden = true; return; }
    showCard(i);
  });
  async function showCard(i) {
    const id = await idOf(i);
    const rel = meta.rel[REL[i]];
    const root = meta.roots.find((r) => r.i === i);
    const fam = root ? meta.families[root.f] : null;
    const pi = parentsIndex ? (await parentsIndex)[id] : null;
    const nd = root ? root.n : pi ? pi[1] : 0;
    card.hidden = false;
    card.innerHTML = `<h3>${esc(id)}</h3>
      <div><span class="k">kind</span> ${esc(rel)}${nd ? ` · <span class="k">descendants</span> ${fmt(nd)}` : ""}${fam ? ` · <span class="k">family</span> ${esc(fam.d)}` : ""}</div>
      <div style="margin-top:8px"><a href="index.html#m=${encodeURIComponent(id)}">Open ancestry ↗</a> &nbsp; <a href="https://huggingface.co/${esc(id)}" target="_blank" rel="noopener">Hugging Face ↗</a> &nbsp; <a href="#" id="zoomto">Zoom here</a></div>`;
    $("#zoomto").addEventListener("click", (e) => { e.preventDefault(); flyTo(X[i], Y[i], Math.max(t.k, 40)); });
    history.replaceState(null, "", `#id=${encodeURIComponent(id)}`);
  }
  function flyTo(x, y, k) { d3.select(canvas).transition().duration(1200).call(zoom.transform, d3.zoomIdentity.translate(W / 2, H / 2).scale(k).translate(-x, -y)); }

  // ---------- search (models with descendants) ----------
  const q = $("#gq"), sug = $("#gsuggest");
  let timer = null, sel = -1;
  q.addEventListener("focus", loadParentsIndex);
  q.addEventListener("input", () => { clearTimeout(timer); timer = setTimeout(suggest, 150); });
  q.addEventListener("keydown", (e) => {
    const items = [...sug.querySelectorAll("li")];
    if (e.key === "ArrowDown") { sel = Math.min(sel + 1, items.length - 1); items.forEach((li, i) => li.classList.toggle("on", i === sel)); e.preventDefault(); }
    else if (e.key === "ArrowUp") { sel = Math.max(sel - 1, 0); items.forEach((li, i) => li.classList.toggle("on", i === sel)); e.preventDefault(); }
    else if (e.key === "Enter") { const li = sel >= 0 ? items[sel] : items[0]; if (li) go(li.dataset.id); }
    else if (e.key === "Escape") hide();
  });
  function hide() { sug.hidden = true; sug.innerHTML = ""; sel = -1; }
  async function suggest() {
    const v = q.value.trim().toLowerCase();
    if (v.length < 2) return hide();
    const idx = await loadParentsIndex();
    const hits = [];
    for (const id in idx) { if (id.toLowerCase().includes(v)) { hits.push(id); if (hits.length >= 60) break; } }
    hits.sort((a, b) => a.length - b.length);
    sug.innerHTML = hits.slice(0, 10).map((id) => `<li data-id="${esc(id)}"><span>${esc(id)}</span></li>`).join("");
    sug.hidden = !hits.length; sel = -1;
    sug.querySelectorAll("li").forEach((li) => li.addEventListener("mousedown", () => go(li.dataset.id)));
  }
  async function go(id) {
    hide(); q.value = "";
    const idx = await loadParentsIndex();
    const i = idx[id] ? idx[id][0] : null;
    if (i == null) return;
    flyTo(X[i], Y[i], 30);
    showCard(i);
  }
  document.addEventListener("click", (e) => { if (!e.target.closest("#gq") && !e.target.closest("#gsuggest")) hide(); });

  // deep link
  const m = location.hash.match(/^#id=(.+)$/);
  if (m) go(decodeURIComponent(m[1]));
})();
