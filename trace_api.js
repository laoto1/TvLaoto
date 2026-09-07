const puppeteer = require('puppeteer');

(async () => {
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();
  
  page.on('request', request => {
    const url = request.url();
    if (url.includes('api') || url.includes('ajax')) {
      console.log('API Request:', url);
    }
  });

  await page.goto('https://vtvgo.vn/xem-truc-tuyen-kenh-vtv1-1.html', { waitUntil: 'networkidle2' });
  await browser.close();
})();
