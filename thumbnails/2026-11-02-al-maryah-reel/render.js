// Render the Abu Dhabi Series Reel cover to a 1080x1920 PNG.
// Usage: node render.js --part 1 --island "Al Maryah Island" [--img photos/x.jpg] [--layout a|b|c] [--tag 0|1] [--safe 1] --out cover.png
// --img is relative to this folder. Needs Playwright (preinstalled in Claude cloud sessions).
const { chromium } = require('playwright');
const path = require('path');

const args = Object.fromEntries(
  process.argv.slice(2).reduce((acc, a, i, arr) => (a.startsWith('--') ? [...acc, [a.slice(2), arr[i + 1]]] : acc), [])
);
const out = path.resolve(args.out || 'cover.png');
delete args.out;
const url = 'file://' + path.join(__dirname, 'template.html') + '?' + new URLSearchParams(args).toString();

(async () => {
  const browser = await chromium.launch();
  const page = await browser.newPage({ viewport: { width: 1080, height: 1920 } });
  await page.goto(url);
  await page.evaluate(() => document.fonts.ready);
  await page.screenshot({ path: out, clip: { x: 0, y: 0, width: 1080, height: 1920 } });
  await browser.close();
  console.log('Saved', out);
})();
