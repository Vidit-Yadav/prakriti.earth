const puppeteer = require('puppeteer-core');

const PORT = process.env.PORT || 3005;

const routes = [
  '/',
  '/our-company',
  '/our-tech/amrv',
  '/our-tech/blockchain',
  '/solutions/nature-based',
  '/solutions/supply-chain',
  '/resources/case-studies',
  '/resources/case-studies/turning-regenerative-ag-into-verified-climate-performance',
  '/resources/case-studies/scaling-prakritis-intelligence-with-ai',
  '/resources/research-and-insights',
  '/resources/research-and-insights/prakritis-atmospheric-based-measurement-reporting-and-verification-approach',
  '/resources/news-and-media',
  '/resources/news-and-media/prakritis-atmospheric-based-measurement-reporting-and-verification-approach',
  '/contact',
  '/privacy-policy',
  '/terms-of-use'
];

(async () => {
  const browser = await puppeteer.launch({
    executablePath: '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox']
  });

  const page = await browser.newPage();
  await page.setViewport({ width: 1440, height: 900 });

  console.log(`Testing all ${routes.length} pages in Brave on port ${PORT}:\n`);
  let allPass = true;

  for (const route of routes) {
    const url = `http://localhost:${PORT}` + route;
    let failed = 0;
    const reqFailed = (req) => {
      const u = req.url();
      if (!u.includes('google-analytics') && !u.includes('googletagmanager')) {
        failed++;
      }
    };
    page.on('requestfailed', reqFailed);

    try {
      await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 15000 });
      await new Promise(r => setTimeout(r, 1200));

      const title = await page.title();
      const bodyText = await page.evaluate(() => document.body.innerText);

      const alethiaMatches = bodyText.match(/alethia/gi) || [];
      const prakritiMatches = bodyText.match(/prakriti/gi) || [];
      const foreignLocations = bodyText.match(/buenos aires|logan, utah|jersey city/gi) || [];

      if (alethiaMatches.length > 0) {
        allPass = false;
        console.log(`❌ [FAIL - ALETHIA LEAK] ${route} -> ${alethiaMatches.length} occurrences`);
      } else if (foreignLocations.length > 0) {
        allPass = false;
        console.log(`❌ [FAIL - FOREIGN LOCATION] ${route} -> ${foreignLocations.join(', ')}`);
      } else if (prakritiMatches.length === 0) {
        allPass = false;
        console.log(`⚠️ [WARN - NO PRAKRITI FOUND] ${route}`);
      } else {
        console.log(`✅ [PASS] ${route.padEnd(45)} | Prakriti: ${prakritiMatches.length} | Title: ${title.slice(0, 32)}`);
      }
    } catch (err) {
      console.log(`❌ [ERR]  ${route.padEnd(45)} ${err.message}`);
      allPass = false;
    } finally {
      page.off('requestfailed', reqFailed);
    }
  }

  await browser.close();
  console.log('\n======================================================');
  console.log('Final Route Verification Status:', allPass ? '🎉 ALL 16 ROUTES PASSED (100% CLEAN)' : '❌ SOME ISSUES FOUND');
  console.log('======================================================\n');
  process.exit(allPass ? 0 : 1);
})();
