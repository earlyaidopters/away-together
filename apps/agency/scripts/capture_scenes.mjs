// Screenshot every filming scene at 1440x900 for the PDF guide. Animated frames are captured at their final state.
import { createRequire } from 'module';
import fs from 'fs';
import { fileURLToPath } from 'url';
import path from 'path';
// Find playwright-core in the nearest parent node_modules.
let dir = path.dirname(fileURLToPath(import.meta.url)), playwright = null;
for (;;) { if (fs.existsSync(path.join(dir, 'node_modules', 'playwright-core'))) { playwright = createRequire(path.join(dir, 'node_modules', '/'))('playwright-core'); break; } if (dir === path.dirname(dir)) break; dir = path.dirname(dir); }
if (!playwright) { console.error('playwright-core not found in a parent node_modules'); process.exit(2); }
const { chromium } = playwright;
const out = fileURLToPath(new URL('../output/qa/scene-shots/', import.meta.url));
fs.mkdirSync(out, { recursive: true });
const browser = await chromium.launch();
const page = await browser.newPage({ viewport: { width: 1440, height: 900 } });
await page.goto('http://127.0.0.1:8770/?capture=1', { waitUntil: 'networkidle' });
await page.waitForTimeout(2000);
const only = process.argv.slice(2);
const ids = (await page.$$eval('section.scene', s => s.map(x => x.id))).filter(id => !only.length || only.includes(id));
for (const id of ids) {
  await page.$eval('#' + id, el => el.scrollIntoView());
  const framed = await page.$eval('#' + id, el => !!el.querySelector('iframe'));
  await page.waitForTimeout(framed ? 18000 : 1800);
  await page.screenshot({ path: `${out}${id}.jpg`, type: 'jpeg', quality: 82 });
  console.log(id, framed ? 'framed' : 'static');
}
await browser.close();
