const puppeteer = require('puppeteer-core');
const path = require('path');
const fs = require('fs');

const SCREENSHOT_DIR = '/Users/vidit/.gemini/antigravity-ide/brain/f3869e55-1db6-4654-a806-ac7f3fdd8cd5/screenshots';

const VIEWPORTS = [
  { name: 'desktop-1440', width: 1440, height: 900 },
  { name: 'laptop-1024', width: 1024, height: 768 },
  { name: 'tablet-768', width: 768, height: 1024 },
  { name: 'mobile-390', width: 390, height: 844, isMobile: true, hasTouch: true }
];

async function runQA() {
  console.log('====================================================');
  console.log('🔬 STARTING PRAKRITI PRODUCTION QA TEST SUITE');
  console.log('====================================================\n');

  const browser = await puppeteer.launch({
    executablePath: '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser',
    headless: 'new',
    args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-gpu']
  });

  let totalErrors = 0;

  for (const vp of VIEWPORTS) {
    console.log(`\n--- Testing Viewport: ${vp.name} (${vp.width}x${vp.height}) ---`);
    const page = await browser.newPage();
    await page.setViewport(vp);

    const consoleErrors = [];
    page.on('console', msg => {
      const txt = msg.text();
      // Ignore benign external analytics aborts
      if (msg.type() === 'error' && !txt.includes('google-analytics') && !txt.includes('favicon')) {
        consoleErrors.push(txt);
      }
    });

    const failedRequests = [];
    page.on('requestfailed', req => {
      const url = req.url();
      if (!url.includes('google-analytics') && !url.includes('googletagmanager')) {
        failedRequests.push({ url, error: req.failure().errorText });
      }
    });

    const httpErrors = [];
    page.on('response', res => {
      const url = res.url();
      if (res.status() >= 400 && !url.includes('google-analytics')) {
        httpErrors.push({ url, status: res.status() });
      }
    });

    // 1. Navigate to homepage
    await page.goto('http://localhost:3000', { waitUntil: 'load', timeout: 20000 });
    await new Promise(r => setTimeout(r, 3500));

    // 2. Check Horizontal Overflow
    const overflowInfo = await page.evaluate(() => {
      const docW = document.documentElement.scrollWidth;
      const winW = window.innerWidth;
      return {
        docWidth: docW,
        winWidth: winW,
        hasOverflow: docW > winW
      };
    });

    if (overflowInfo.hasOverflow) {
      console.error(`  ❌ Layout Overflow: scrollWidth (${overflowInfo.docWidth}) > innerWidth (${overflowInfo.winWidth})`);
      totalErrors++;
    } else {
      console.log(`  ✅ Layout width perfectly contained (${overflowInfo.winWidth}px)`);
    }

    // 3. Capture Hero Screenshot
    const heroPath = path.join(SCREENSHOT_DIR, `${vp.name}-hero.png`);
    await page.screenshot({ path: heroPath, clip: { x: 0, y: 0, width: vp.width, height: Math.min(vp.height, 900) } });
    console.log(`  📸 Hero screenshot captured: ${heroPath}`);

    // 4. Scroll through page to verify canvas / scrubbing animations
    await page.evaluate(async () => {
      const totalH = document.body.scrollHeight;
      const step = 800;
      for (let y = 0; y < totalH; y += step) {
        window.scrollTo(0, y);
        await new Promise(r => setTimeout(r, 100));
      }
    });
    await new Promise(r => setTimeout(r, 1000));

    // 5. Capture Footer Screenshot (showing bespoke PRAKRITI wordmark)
    const footerElem = await page.$('#contact') || await page.$('#contact-mob') || await page.$('.framer-Ex2bJ');
    if (footerElem) {
      const footerPath = path.join(SCREENSHOT_DIR, `${vp.name}-footer.png`);
      await footerElem.screenshot({ path: footerPath });
      console.log(`  📸 Footer wordmark screenshot captured: ${footerPath}`);
    }

    // 6. Test Interactive Anchors
    console.log('  Testing navigation anchors:');
    const anchorsToTest = ['#solutions', '#technology', '#impact', '#contact'];
    for (const a of anchorsToTest) {
      const scrollPosBefore = await page.evaluate(() => window.scrollY);
      await page.evaluate((targetId) => {
        const el = document.querySelector(targetId);
        if (el) el.scrollIntoView();
      }, a);
      await new Promise(r => setTimeout(r, 400));
      const scrollPosAfter = await page.evaluate(() => window.scrollY);
      console.log(`    Anchor ${a}: scrolled from ${scrollPosBefore.toFixed(0)}px to ${scrollPosAfter.toFixed(0)}px`);
    }

    // 7. Check errors
    if (consoleErrors.length > 0) {
      console.warn(`  ⚠️ Console errors (${consoleErrors.length}):`, consoleErrors);
    } else {
      console.log(`  ✅ 0 Console errors`);
    }

    if (failedRequests.length > 0) {
      console.error(`  ❌ Failed requests (${failedRequests.length}):`, failedRequests);
      totalErrors += failedRequests.length;
    } else {
      console.log(`  ✅ 0 Failed requests`);
    }

    if (httpErrors.length > 0) {
      console.error(`  ❌ HTTP 4xx/5xx responses (${httpErrors.length}):`, httpErrors);
      totalErrors += httpErrors.length;
    } else {
      console.log(`  ✅ 0 HTTP 4xx/5xx responses`);
    }

    await page.close();
  }

  await browser.close();

  console.log('\n====================================================');
  console.log(`🏁 QA TEST SUITE COMPLETED: Total Errors: ${totalErrors}`);
  console.log('====================================================\n');

  return totalErrors;
}

runQA()
  .then(errors => {
    if (errors > 0) process.exit(1);
    process.exit(0);
  })
  .catch(err => {
    console.error('QA Runner Exception:', err);
    process.exit(1);
  });
