// Erzeugt die Kursflyer als Bild (Website) und PDF (Druck, A4 quer).
// Voraussetzung: lokaler Server im Projektordner auf Port 8766 und Playwright.
//   node tools/flyer/render.js
const { chromium } = require('playwright');

const FLYER = [
  ['taping', 'flyer-kinesio-taping-kompakt'],
  ['pinofit', 'flyer-pinofit-kombikurs'],
];

(async () => {
  const browser = await chromium.launch();
  for (const [kurs, name] of FLYER) {
    const page = await browser.newPage({ viewport: { width: 1492, height: 1054 }, deviceScaleFactor: 2 });
    await page.goto(`http://localhost:8766/tools/flyer/flyer.html?kurs=${kurs}`, { waitUntil: 'networkidle' });
    await page.evaluate(() => document.fonts.ready);
    await page.screenshot({ path: `assets/${name}.jpg`, type: 'jpeg', quality: 86 });
    await page.pdf({ path: `assets/${name}.pdf`, format: 'A4', landscape: true, printBackground: true, scale: 1122.52 / 1492, margin: { top: 0, right: 0, bottom: 0, left: 0 } });
    await page.close();
    console.log(name);
  }
  await browser.close();
})();
