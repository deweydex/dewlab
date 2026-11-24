// Downloads, put together in the reader's browser.
//
// The site does not hold its downloadable copies whole: most of every copy is
// the same runtime, stylesheets, fonts and Python tools, and writing them out
// hundreds of times made the site too big to publish. The build keeps each
// repeated piece once in download/shared/ and each page as a skeleton in
// download/parts/, with a <!--dl-part:NAME--> marker where each piece goes
// (the note at the top of builder/downloads.py has the whole story).
//
// A download link carries `data-dl-save-as`. Its href is either a skeleton,
// for one page, or an archive manifest (download/<name>.json), for a series or
// a course. On a click this file fetches what it needs, joins it exactly as
// builder/downloads.py's join_parts() does, and saves the result: one HTML
// file, or a zip built here. It makes no decisions about what a copy holds;
// that is all decided at build time.

const PART_RE = /<!--dl-part:([A-Za-z0-9._-]+)-->/g;

// Each shared piece is fetched once per visit, however many pages need it.
const pieces = new Map();

async function fetchText(url) {
  const response = await fetch(url);
  if (!response.ok) throw new Error(`${url}: ${response.status}`);
  return response.text();
}

function piece(downloadBase, name) {
  const url = new URL(`shared/${name}`, downloadBase).href;
  if (!pieces.has(url)) {
    const pending = fetchText(url);
    // A failed fetch is not kept, so pressing the button again retries it.
    pending.catch(() => pieces.delete(url));
    pieces.set(url, pending);
  }
  return pieces.get(url);
}

// One page's whole copy, from its skeleton's address.
async function joinPage(partUrl) {
  const downloadBase = new URL("../", partUrl);
  const skeleton = await fetchText(partUrl);
  const names = [...new Set([...skeleton.matchAll(PART_RE)].map((match) => match[1]))];
  const texts = await Promise.all(names.map((name) => piece(downloadBase, name)));
  const byName = new Map(names.map((name, i) => [name, texts[i]]));
  // A replacer function, so a `$` inside a piece is never read as a pattern.
  return skeleton.replace(PART_RE, (_, name) => byName.get(name));
}

// --- A zip, written here ---------------------------------------------------

const CRC_TABLE = (() => {
  const table = new Uint32Array(256);
  for (let n = 0; n < 256; n++) {
    let c = n;
    for (let k = 0; k < 8; k++) c = c & 1 ? 0xedb88320 ^ (c >>> 1) : c >>> 1;
    table[n] = c >>> 0;
  }
  return table;
})();

function crc32(bytes) {
  let crc = 0xffffffff;
  for (let i = 0; i < bytes.length; i++) crc = CRC_TABLE[(crc ^ bytes[i]) & 0xff] ^ (crc >>> 8);
  return (crc ^ 0xffffffff) >>> 0;
}

function canDeflate() {
  try {
    new CompressionStream("deflate-raw");
    return true;
  } catch {
    return false;
  }
}

async function deflate(bytes) {
  const stream = new Blob([bytes]).stream().pipeThrough(new CompressionStream("deflate-raw"));
  return new Uint8Array(await new Response(stream).arrayBuffer());
}

function dosTimeAndDate(when) {
  const time = (when.getHours() << 11) | (when.getMinutes() << 5) | (when.getSeconds() >> 1);
  const date = ((when.getFullYear() - 1980) << 9) | ((when.getMonth() + 1) << 5) | when.getDate();
  return [time, date];
}

// A zip of `files`, each { name, text }, as a Blob. Compressed where the
// browser can compress, stored otherwise; either opens anywhere.
async function zipBlob(files, onEach) {
  const encoder = new TextEncoder();
  const compress = canDeflate();
  const [time, date] = dosTimeAndDate(new Date());
  const chunks = [];
  const central = [];
  let offset = 0;
  for (const file of files) {
    const name = encoder.encode(file.name);
    const data = encoder.encode(file.text);
    const crc = crc32(data);
    const body = compress ? await deflate(data) : data;
    const method = compress ? 8 : 0;

    const local = new DataView(new ArrayBuffer(30));
    local.setUint32(0, 0x04034b50, true);
    local.setUint16(4, 20, true);
    local.setUint16(6, 0x0800, true); // names are UTF-8
    local.setUint16(8, method, true);
    local.setUint16(10, time, true);
    local.setUint16(12, date, true);
    local.setUint32(14, crc, true);
    local.setUint32(18, body.length, true);
    local.setUint32(22, data.length, true);
    local.setUint16(26, name.length, true);
    local.setUint16(28, 0, true);
    chunks.push(local, name, body);

    const entry = new DataView(new ArrayBuffer(46));
    entry.setUint32(0, 0x02014b50, true);
    entry.setUint16(4, 20, true);
    entry.setUint16(6, 20, true);
    entry.setUint16(8, 0x0800, true);
    entry.setUint16(10, method, true);
    entry.setUint16(12, time, true);
    entry.setUint16(14, date, true);
    entry.setUint32(16, crc, true);
    entry.setUint32(20, body.length, true);
    entry.setUint32(24, data.length, true);
    entry.setUint16(28, name.length, true);
    entry.setUint32(42, offset, true);
    central.push(entry, name);

    offset += 30 + name.length + body.length;
    onEach();
  }
  const centralSize = central.reduce((sum, part) => sum + part.byteLength, 0);
  const end = new DataView(new ArrayBuffer(22));
  end.setUint32(0, 0x06054b50, true);
  end.setUint16(8, files.length, true);
  end.setUint16(10, files.length, true);
  end.setUint32(12, centralSize, true);
  end.setUint32(16, offset, true);
  return new Blob([...chunks, ...central, end], { type: "application/zip" });
}

// --- The button ------------------------------------------------------------

function save(blob, name) {
  const url = URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = name;
  document.body.append(link);
  link.click();
  link.remove();
  setTimeout(() => URL.revokeObjectURL(url), 60_000);
}

function statusFor(link) {
  let status = link.nextElementSibling;
  if (!status || !status.classList.contains("dl-download-status")) {
    status = document.createElement("span");
    status.className = "dl-download-status";
    status.setAttribute("role", "status");
    link.after(status);
  }
  return status;
}

async function download(link) {
  const url = new URL(link.getAttribute("href"), location.href);
  const saveAs = link.dataset.dlSaveAs;
  const status = statusFor(link);
  link.setAttribute("aria-busy", "true");
  status.textContent = "Preparing your download…";
  try {
    if (url.pathname.endsWith(".json")) {
      const manifest = JSON.parse(await fetchText(url.href));
      const files = [];
      for (const entry of manifest.files) {
        const text = "text" in entry ? entry.text : await joinPage(new URL(entry.part, url).href);
        files.push({ name: entry.name, text });
        status.textContent = `Preparing ${files.length} of ${manifest.files.length}…`;
      }
      let zipped = 0;
      const blob = await zipBlob(files, () => {
        zipped += 1;
        status.textContent = `Zipping ${zipped} of ${files.length}…`;
      });
      save(blob, saveAs);
    } else {
      const page = await joinPage(url.href);
      save(new Blob([page], { type: "text/html" }), saveAs);
    }
    status.textContent = "";
  } catch (error) {
    console.error("[dewlab] download failed", error);
    status.textContent = "The download could not be prepared. Check your connection and try again.";
  } finally {
    link.removeAttribute("aria-busy");
  }
}

document.addEventListener("click", (event) => {
  const link = event.target.closest?.("a[data-dl-save-as]");
  // Every click, a modified one too: the href is a part, not a file to open.
  if (!link || event.button !== 0) return;
  event.preventDefault();
  if (link.getAttribute("aria-busy") === "true") return;
  download(link);
});
