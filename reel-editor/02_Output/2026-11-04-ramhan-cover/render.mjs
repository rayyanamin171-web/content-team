// node render.mjs --bg plates/<plate>.jpg --out <file>.png [--l1 ..] [--l2 ..] [--l3 ..] [--credit 0]
import { createRequire } from "node:module";
import path from "node:path";
import { fileURLToPath } from "node:url";
const require = createRequire(import.meta.url);
const { chromium } = require("playwright");
const here = path.dirname(fileURLToPath(import.meta.url));
const a = Object.fromEntries(process.argv.slice(2).reduce((acc, v, i, arr) => v.startsWith("--") ? [...acc, [v.slice(2), arr[i + 1]]] : acc, []));
const qs = new URLSearchParams({ bg: a.bg, ...(a.l1 && { l1: a.l1 }), ...(a.l2 && { l2: a.l2 }), ...(a.l3 && { l3: a.l3 }), ...(a.credit && { credit: a.credit }) });
const b = await chromium.launch({ args: ["--allow-file-access-from-files"] });
const p = await b.newPage({ viewport: { width: 1080, height: 1920 } });
await p.goto("file://" + path.join(here, "template.html") + "?" + qs);
await p.evaluate(() => document.fonts.ready);
await p.waitForTimeout(300);
await p.screenshot({ path: a.out });
await b.close();
console.log("wrote", a.out);
