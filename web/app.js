/* Digital critical edition. The scanned image is always the source of truth.
   EVA/IVTFF files are imported client-side and are never uploaded.
*/
"use strict";

const state = { edition: null, current: 0, viewer: null, corpus: new Map(), sourceName: "", request: 0, toastTimer: null };
const find = id => document.getElementById(id);

function notify(message) {
  const el = find("toast");
  el.textContent = message;
  el.hidden = false;
  clearTimeout(state.toastTimer);
  state.toastTimer = setTimeout(() => { el.hidden = true; }, 3500);
}

function prettyLabel(page) {
  return page.folio ? page.folio.replace(/^f/, "Fólio ") : page.label.replace(/^\[|\]$/g, "");
}

function folioList(searchText = "") {
  const list = find("folioList");
  list.replaceChildren();
  if (!state.edition) return;
  const query = searchText.toLowerCase().trim().replace(/^f(?=\d)/, "");
  const found = state.edition.pages.filter(p =>
    !query || (p.folio || "").toLowerCase().replace(/^f/, "").includes(query) ||
    p.label.toLowerCase().includes(query) || String(p.seq) === query
  );
  if (!found.length) {
    const message = document.createElement("p");
    message.className = "muted loading";
    message.textContent = "Nenhum fólio encontrado.";
    list.append(message);
    return;
  }
  for (const page of found) {
    const index = page.seq - 1;
    const button = document.createElement("button");
    button.type = "button";
    button.className = "folio-item" + (index === state.current ? " active" : "");
    button.dataset.index = String(index);
    button.setAttribute("role", "listitem");
    button.setAttribute("aria-current", String(index === state.current));
    const img = document.createElement("img");
    img.loading = "lazy";
    img.decoding = "async";
    img.alt = "";
    if (page.thumbnail) img.src = page.thumbnail;
    const words = document.createElement("span");
    const name = document.createElement("strong");
    name.textContent = page.folio || "Vista " + page.seq;
    const description = document.createElement("small");
    description.textContent = page.folio ? "Fólio · MS 408" : page.label.replace(/^\[|\]$/g, "");
    words.append(name, description);
    const arrow = document.createElement("span");
    arrow.className = "arrow";
    arrow.textContent = "›";
    button.append(img, words, arrow);
    button.addEventListener("click", () => goTo(index));
    list.append(button);
  }
}

function sourceUrl(page) {
  return page.image_fallback || page.image_info || page.canvas || state.edition.catalog;
}

function viewerFallback(page, cause) {
  const root = find("viewer");
  root.replaceChildren();
  const wrap = document.createElement("div");
  wrap.className = "viewer-fallback";
  if (page.image_fallback || page.thumbnail) {
    const img = document.createElement("img");
    img.src = page.image_fallback || page.thumbnail;
    img.alt = "Imagem original " + prettyLabel(page);
    wrap.append(img);
  } else {
    const p = document.createElement("p");
    p.className = "viewer-loading";
    p.textContent = "Esta vista não tem imagem disponível no índice.";
    wrap.append(p);
  }
  root.append(wrap);
  if (cause) console.warn("IIIF tiled viewer fallback:", cause);
}

function createViewer(page) {
  state.request += 1;
  const token = state.request;
  if (state.viewer) {
    try { state.viewer.destroy(); } catch (_) {}
    state.viewer = null;
  }
  find("viewer").replaceChildren();
  if (!window.OpenSeadragon || !page.image_info) {
    viewerFallback(page, "no tile viewer or IIIF service");
    return;
  }
  try {
    const viewer = window.OpenSeadragon({
      id: "viewer",
      prefixUrl: "https://cdnjs.cloudflare.com/ajax/libs/openseadragon/5.0.1/images/",
      showNavigationControl: false,
      zoomPerClick: 1.7,
      zoomPerScroll: 1.25,
      minZoomImageRatio: .8,
      maxZoomPixelRatio: 3,
      visibilityRatio: .85,
      constrainDuringPan: true,
      animationTime: 0.5,
      gestureSettingsMouse: { scrollToZoom: true, clickToZoom: true, dblClickToZoom: true },
      tileSources: page.image_info
    });
    state.viewer = viewer;
    viewer.addHandler("open-failed", event => {
      if (token === state.request) {
        state.viewer = null;
        try { viewer.destroy(); } catch (_) {}
        viewerFallback(page, event.message);
      }
    });
  } catch (err) {
    viewerFallback(page, err);
  }
}

function saveNote() {
  if (!state.edition) return;
  const page = state.edition.pages[state.current];
  const key = "voynich-note-" + page.id;
  try {
    localStorage.setItem(key, find("noteText").value);
    find("noteStatus").textContent = "Salvo neste navegador";
  } catch (_) {
    find("noteStatus").textContent = "Armazenamento indisponível; exporte suas notas";
  }
}

function readNote(page) {
  try { return localStorage.getItem("voynich-note-" + page.id) || ""; }
  catch (_) { return ""; }
}

function renderTranscription(page) {
  const output = find("transcriptionLines");
  const empty = find("transcriptionState");
  output.replaceChildren();
  const lines = state.corpus.get(page.folio) || [];
  if (!lines.length) {
    empty.hidden = false;
    output.hidden = true;
    return;
  }
  empty.hidden = true;
  output.hidden = false;
  const heading = document.createElement("p");
  heading.className = "muted body-small";
  heading.textContent = lines.length + " registros em " + state.sourceName + ". Texto de transliteração; não é tradução.";
  output.append(heading);
  for (const record of lines) {
    const row = document.createElement("div");
    row.className = "line";
    const marker = document.createElement("span");
    marker.className = "line-id";
    marker.textContent = record.line;
    const raw = document.createElement("span");
    raw.className = "line-text";
    raw.textContent = record.raw;
    row.append(marker, raw);
    output.append(row);
  }
}

function goTo(index, focusSidebar = true) {
  if (!state.edition) return;
  const size = state.edition.pages.length;
  state.current = Math.min(Math.max(index, 0), size - 1);
  const page = state.edition.pages[state.current];
  find("folioHeading").textContent = prettyLabel(page);
  find("folioSubtitle").textContent = page.label + " · Yale Beinecke MS 408";
  find("positionLabel").textContent = String(page.seq).padStart(3,"0") + " / " + size;
  find("imageDimensions").textContent = page.width && page.height
    ? page.width + " × " + page.height + " px · Yale"
    : "Digitalização original · Yale";
  find("openOriginal").href = sourceUrl(page);
  find("previousPage").disabled = state.current === 0;
  find("nextPage").disabled = state.current === size - 1;
  find("noteText").value = readNote(page);
  find("noteStatus").textContent = "Notas deste fólio · local";
  renderTranscription(page);
  folioList(find("folioSearch").value);
  if (focusSidebar) {
    const chosen = find("folioList").querySelector(".active");
    if (chosen) chosen.scrollIntoView({block:"nearest",inline:"nearest"});
  }
  const params = new URLSearchParams(location.search);
  params.set("folio", page.id);
  history.replaceState(null, "", location.pathname + "?" + params.toString() + location.hash);
  createViewer(page);
}

function jump() {
  const query = find("jumpToFolio").value.trim().toLowerCase();
  if (!query || !state.edition) return;
  const clean = query.startsWith("f") ? query : "f" + query;
  const index = state.edition.pages.findIndex(page =>
    page.id.toLowerCase() === clean || page.folio === clean ||
    page.label.toLowerCase() === query
  );
  if (index < 0) {
    notify("Esse fólio não consta do índice digital de Yale.");
    return;
  }
  goTo(index);
}

function parseIvTff(text, filename) {
  const result = new Map();
  const re = /^<([^<>.]+)\.([^,>]+),([^>]+)>\s*(.*)$/;
  for (const line of text.split(/\r?\n/)) {
    if (!line.startsWith("<") || line.startsWith("<!")) continue;
    const match = re.exec(line.trim());
    if (!match) continue;
    const folio = match[1];
    if (!result.has(folio)) result.set(folio, []);
    result.get(folio).push({ line: match[2], type: match[3], raw: match[4] });
  }
  if (result.size < 1) throw new Error("O arquivo não contém loci reconhecíveis em formato IVTFF.");
  state.corpus = result;
  state.sourceName = filename;
  const page = state.edition.pages[state.current];
  renderTranscription(page);
  notify("Transcrição carregada localmente: " + result.size + " identificadores.");
}

async function handleUpload(event) {
  const file = event.target.files && event.target.files[0];
  if (!file) return;
  if (file.size > 10_000_000) {
    notify("Arquivo muito grande: máximo de 10 MB para importar no navegador.");
    return;
  }
  try {
    parseIvTff(await file.text(), file.name);
  } catch (err) {
    notify("Importação não reconhecida: " + err.message);
  }
}

function exportNotes() {
  if (!state.edition) return;
  const notes = state.edition.pages.map(page => ({
    folio: page.folio, canvas: page.canvas, page_id: page.id,
    text: readNote(page)
  })).filter(entry => entry.text.trim());
  const json = {
    schema: "voynich-local-notes-1.0",
    original_manifest_sha256: state.edition.source_sha256,
    export_utc: new Date().toISOString(),
    notices: ["User notes are not an authoritative transcription", "Coordinates and scientific claims require independent verification"],
    entries: notes
  };
  const blob = new Blob([JSON.stringify(json, null, 2)], {type:"application/json"});
  const href = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = href;
  a.download = "voynich-notas-" + new Date().toISOString().slice(0,10) + ".json";
  a.click();
  setTimeout(() => URL.revokeObjectURL(href), 1000);
  notify("Notas exportadas em JSON (" + notes.length + " folios).");
}

function switchTab(button) {
  document.querySelectorAll(".tab").forEach(tab => {
    const active = tab === button;
    tab.classList.toggle("active", active);
    tab.setAttribute("aria-selected", String(active));
    const panel = find(tab.dataset.tab + "Panel");
    if (panel) panel.hidden = !active;
  });
}

function zoom(factor) {
  if (state.viewer && state.viewer.viewport) {
    if (factor === 0) state.viewer.viewport.goHome();
    else state.viewer.viewport.zoomBy(factor);
    state.viewer.viewport.applyConstraints();
  } else if (factor !== 0) {
    notify("Zoom em mosaicos indisponível. Abra a imagem original na fonte.");
  }
}

function bind() {
  find("previousPage").addEventListener("click", () => goTo(state.current-1));
  find("nextPage").addEventListener("click", () => goTo(state.current+1));
  find("folioSearch").addEventListener("input", e => folioList(e.target.value));
  find("jumpButton").addEventListener("click", jump);
  find("jumpToFolio").addEventListener("keydown", e => { if (e.key === "Enter") jump(); });
  find("zoomIn").addEventListener("click", () => zoom(1.4));
  find("zoomOut").addEventListener("click", () => zoom(1/1.4));
  find("resetZoom").addEventListener("click", () => zoom(0));
  find("ivtffUpload").addEventListener("change", handleUpload);
  find("noteText").addEventListener("input", saveNote);
  find("exportNotes").addEventListener("click", exportNotes);
  find("sourceInfoButton").addEventListener("click", () => {
    notify("Acervo Yale · manifesto SHA-256: " + state.edition.source_sha256.slice(0,16) + "…");
  });
  document.querySelectorAll(".tab").forEach(b => b.addEventListener("click", () => switchTab(b)));
  document.addEventListener("keydown", e => {
    const tag = (e.target.tagName || "").toUpperCase();
    if (["INPUT","TEXTAREA","SELECT"].includes(tag) || e.altKey || e.ctrlKey || e.metaKey) return;
    if (e.key === "ArrowRight") goTo(state.current+1);
    if (e.key === "ArrowLeft") goTo(state.current-1);
    if (e.key === "/") { e.preventDefault(); find("folioSearch").focus(); }
  });
}

async function init() {
  bind();
  try {
    const response = await fetch("./data/folios.json", {cache: "no-cache"});
    if (!response.ok) throw new Error("HTTP " + response.status);
    const edition = await response.json();
    if (!Array.isArray(edition.pages) || edition.pages.length < 200 || !edition.source_sha256)
      throw new Error("Índice incompleto ou sem proveniência");
    state.edition = edition;
    find("pageCount").textContent = edition.canvas_count + " vistas";
    const requested = new URLSearchParams(location.search).get("folio");
    let index = requested ? edition.pages.findIndex(p => p.id === requested || p.folio === requested) : -1;
    if (index < 0) index = edition.pages.findIndex(p => p.folio === "f1r");
    goTo(index >= 0 ? index : 0);
  } catch (err) {
    find("folioList").textContent = "Índice digital indisponível. Consulte a fonte institucional Yale.";
    find("viewer").textContent = "Não foi possível acessar o índice: " + err.message;
    notify("Erro de carregamento do índice. Veja o README do site.");
  }
}
init();
