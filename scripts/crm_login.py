"""CRM 自动登录脚本 — Playwright截图 + OCR识别验证码"""
import os, sys, time, base64, io
os.environ['TESSDATA_PREFIX'] = os.path.expandvars(r'%USERPROFILE%\scoop\apps\tesseract\current\tessdata')

from playwright.sync_api import sync_playwright
from PIL import Image
import pytesseract

CRM_URL = "http://test.it188.com"
ADMIN_USER = "admin"
ADMIN_PASS = "admin1234"

def ocr_from_page(page):
    """从浏览器当前页面截取验证码图片并OCR"""
    img_data = page.evaluate("""() => {
        const img = document.querySelectorAll('img')[4];
        if (!img || !img.naturalWidth) return null;
        const canvas = document.createElement('canvas');
        canvas.width = img.naturalWidth;
        canvas.height = img.naturalHeight;
        canvas.getContext('2d').drawImage(img, 0, 0);
        return canvas.toDataURL('image/png');
    }""")
    if not img_data:
        return ""
    b64 = img_data.split(',')[1]
    buf = base64.b64decode(b64)
    img = Image.open(io.BytesIO(buf))
    img = img.convert('L')
    img = img.point(lambda x: 0 if x < 128 else 255)
    return pytesseract.image_to_string(img, config='--psm 7 -c tessedit_char_whitelist=0123456789abcdefghijklmnopqrstuvwxyz').strip()

def login():
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=False)
        page = browser.new_page()
        page.goto(f"{CRM_URL}/login", wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

        page.locator('input[placeholder*="账号"]').fill(ADMIN_USER)
        page.locator('input[placeholder*="密码"]').fill(ADMIN_PASS)

        for attempt in range(10):
            captcha = ocr_from_page(page)
            print(f"[Attempt {attempt+1}] OCR: [{captcha}]")
            if not captcha or len(captcha) < 2:
                print("  OCR failed, refreshing...")
                page.locator('img').nth(3).click()
                page.wait_for_timeout(1500)
                continue

            ci = page.locator('input[placeholder*="验证码"]')
            ci.fill('')
            ci.fill(captcha)
            page.locator('button:has-text("登 录")').click(force=True)
            page.wait_for_timeout(4000)
            url = page.url
            if 'login' not in url:
                print(f"[SUCCESS] Attempt {attempt+1}! URL: {url}")
                page.goto(f"{CRM_URL}/crm/decision-board", wait_until="domcontentloaded")
                page.wait_for_timeout(3000)
                print(f"[DASHBOARD] {page.title()}")
                input("Press Enter to close...")
                browser.close()
                return
            print(f"  Failed. Refreshing captcha...")
            page.locator('img').nth(3).click()
            page.wait_for_timeout(1500)

        print("[FAIL] 10 attempts exhausted")
        input("Press Enter...")
        browser.close()

if __name__ == '__main__':
    login()
