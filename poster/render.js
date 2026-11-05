// Render poster.html -> PNG (1080x1920). Usage: node render.js [out.png] [scale]
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const out = process.argv[2] || path.join(__dirname, '../output/frescura_kl_luxury_poster.png');
  const scale = Number(process.argv[3] || 1);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
  await p.goto('file://' + path.join(__dirname, 'poster.html'));
  await p.waitForSelector('body[data-ready]');
  await p.waitForTimeout(300);
  await p.screenshot({ path: out });
  await b.close();
  console.log('saved', out);
})();
