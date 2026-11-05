// Render a poster page to PNG at its native size.
// Usage: node render.js [page.html] [out.png] [scale]
//   node render.js                      -> poster.html (1080x1920) -> output/frescura_kl_luxury_poster.png
//   node render.js poster_square.html   -> 1080x1080 -> output/frescura_kl_luxury_poster_square.png
const { chromium } = require('playwright');
const path = require('path');
(async () => {
  const page = process.argv[2] || 'poster.html';
  const defOut = page === 'poster.html' ? 'frescura_kl_luxury_poster.png' : 'frescura_kl_luxury_' + page.replace('.html', '.png');
  const out = process.argv[3] || path.join(__dirname, '../output', defOut);
  const scale = Number(process.argv[4] || 1);
  const b = await chromium.launch();
  const p = await b.newPage({ viewport: { width: 1080, height: 1920 }, deviceScaleFactor: scale });
  await p.goto('file://' + path.join(__dirname, page));
  await p.waitForSelector('body[data-ready]');
  await p.waitForTimeout(300);
  const el = await p.$('#poster');
  await el.screenshot({ path: out });
  await b.close();
  console.log('saved', out);
})();
