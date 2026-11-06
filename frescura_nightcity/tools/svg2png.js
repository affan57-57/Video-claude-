const { chromium } = require('playwright'); const fs = require('fs'); const path = require('path');
(async () => {
  const b = await chromium.launch(); const p = await b.newPage({ viewport: { width: 1200, height: 1920 }, deviceScaleFactor: 1.5 });
  for (const f of process.argv.slice(2)) {
    await p.setContent(`<html><body style="margin:0;background:#000">${fs.readFileSync(f, 'utf8')}</body></html>`);
    await p.screenshot({ path: f.replace(/\.svg$/, '.png'), clip: { x: 0, y: 0, width: 1200, height: 1920 } });
    console.log('png', path.basename(f));
  }
  await b.close();
})();
