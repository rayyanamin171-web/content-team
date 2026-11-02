#!/usr/bin/env node
// Render a map scene (JSON) to a 1080x1920 MP4, frame by frame, fully offline.
//   node render_map.mjs --scene scenes/al-maryah-part1.json --out ../../02_Output/map.mp4 [--fps 30] [--workers 4] [--frames 0,90,180 (stills only)]
// Uses the Chromium + Playwright preinstalled in the cloud container (or `npm i playwright && npx playwright install chromium` on a Mac).
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import os from "node:os";
import { spawnSync } from "node:child_process";
import { createRequire } from "node:module";
import { fileURLToPath } from "node:url";

const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const HERE = path.dirname(fileURLToPath(import.meta.url));
const ROOT = path.resolve(HERE, ".."); // toolkit/ (so map.html can reach ../fonts)

const args = Object.fromEntries(process.argv.slice(2).reduce((a, v, i, arr) => (v.startsWith("--") ? [...a, [v.slice(2), arr[i + 1]?.startsWith("--") ? true : arr[i + 1] ?? true]] : a), []));
if (!args.scene || !args.out) { console.error("usage: node render_map.mjs --scene <scene.json> --out <file.mp4|dir> [--fps 30] [--workers 4] [--frames 0,60]"); process.exit(1); }
const scenePath = path.resolve(args.scene);
const scene = JSON.parse(fs.readFileSync(scenePath, "utf8"));
const fps = Number(args.fps || scene.fps || 30);
const total = Math.round((scene.duration || 6) * fps);
const workers = Math.max(1, Math.min(Number(args.workers || Math.min(4, os.cpus().length)), 8));

// --- tiny static server (scene file may live outside toolkit/, so map it to /__scene.json)
const types = { ".html": "text/html", ".js": "text/javascript", ".css": "text/css", ".json": "application/json", ".geojson": "application/json", ".jpg": "image/jpeg", ".png": "image/png", ".woff2": "font/woff2" };
const server = http.createServer((req, res) => {
  let p = decodeURIComponent(req.url.split("?")[0]);
  let file = p === "/__scene.json" ? scenePath : path.join(ROOT, p);
  if (!file.startsWith(ROOT) && file !== scenePath) { res.writeHead(403); return res.end(); }
  fs.readFile(file, (err, buf) => {
    if (err) { res.writeHead(404); return res.end(); }
    res.writeHead(200, { "content-type": types[path.extname(file)] || "application/octet-stream" }); res.end(buf);
  });
});
await new Promise(r => server.listen(0, "127.0.0.1", r));
const base = `http://127.0.0.1:${server.address().port}`;

// scene paths are relative to toolkit/map/
const browser = await chromium.launch({ args: ["--use-gl=angle", "--use-angle=swiftshader", "--enable-unsafe-swiftshader", "--ignore-gpu-blocklist"] });
async function openPage() {
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: 1 });
  page.on("console", m => { if (m.type() === "error") console.error("[page]", m.text()); });
  await page.goto(`${base}/map/map.html?scene=/__scene.json`);
  await page.waitForFunction(() => window.__ready || window.__error, null, { timeout: 120000 });
  const err = await page.evaluate(() => window.__error);
  if (err) throw new Error(err);
  return page;
}

const stills = args.frames && args.frames !== true ? String(args.frames).split(",").map(Number) : null;
const outIsDir = stills || !String(args.out).endsWith(".mp4");
const frameDir = outIsDir ? path.resolve(args.out) : fs.mkdtempSync(path.join(os.tmpdir(), "mapframes-"));
fs.mkdirSync(frameDir, { recursive: true });
const list = stills || Array.from({ length: total }, (_, i) => i);
const t0 = Date.now();
let done = 0;
async function work(chunk) {
  const page = await openPage();
  for (const i of chunk) {
    await page.evaluate(t => window.renderFrame(t), i / fps);
    await page.screenshot({ path: path.join(frameDir, `f${String(i).padStart(5, "0")}.png`), type: "png" });
    done++;
    if (done % 15 === 0 || done === list.length) process.stderr.write(`\rframes ${done}/${list.length}  ${((Date.now() - t0) / 1000).toFixed(0)}s`);
  }
  await page.close();
}
// interleave frames across workers so they all finish together
const chunks = Array.from({ length: Math.min(workers, list.length) }, (_, w) => list.filter((_, i) => i % workers === w));
await Promise.all(chunks.map(work));
process.stderr.write("\n");
await browser.close(); server.close();

if (!outIsDir) {
  const out = path.resolve(args.out);
  fs.mkdirSync(path.dirname(out), { recursive: true });
  const r = spawnSync("ffmpeg", ["-y", "-loglevel", "error", "-framerate", String(fps), "-i", path.join(frameDir, "f%05d.png"),
    "-c:v", "libx264", "-preset", "slow", "-crf", "16", "-pix_fmt", "yuv420p", "-movflags", "+faststart", out], { stdio: "inherit" });
  if (r.status !== 0) process.exit(r.status);
  fs.rmSync(frameDir, { recursive: true, force: true });
  console.log(`wrote ${out} (${list.length} frames @ ${fps} fps, ${((Date.now() - t0) / 1000).toFixed(0)}s)`);
} else console.log(`wrote ${list.length} PNG frames to ${frameDir}`);
