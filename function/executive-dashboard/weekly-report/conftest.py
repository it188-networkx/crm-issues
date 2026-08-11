"""
conftest.py - CRM 销售周报 feature 级登录 fixture
用 admin 账号登录一次，后续所有用例复用。
"""
import os
import pytest
from playwright.sync_api import Page

CRM_BASE_URL = "http://test.it188.com"
CRM_ADMIN_USER = "admin"
CRM_ADMIN_PASS = "admin1234"
POST_LOGIN_URL = f"{CRM_BASE_URL}/#/decision-board/weekly-report"  # 周报首页


@pytest.fixture(scope="session")
def crm_session(page: Page):
    """CRM 统一登录——整个 session 只登录一次。"""
    print("[CONFTEST] 开始 CRM 登录...")
    page.goto(f"{CRM_BASE_URL}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    # 填写登录表单
    page.locator('input[placeholder*="账号"]').fill(CRM_ADMIN_USER)
    page.locator('input[placeholder*="密码"]').fill(CRM_ADMIN_PASS)

    # 获取验证码图片的 alt/src 属性尝试读取
    captcha_img = page.locator('img[src*="captcha"]')
    if captcha_img.count() > 0:
        src = captcha_img.first.get_attribute("src") or ""
        print(f"[CONFTEST] 验证码图片: {src[:80]}...")

    # 尝试填充验证码（开发环境可能为固定值）
    captcha_input = page.locator('input[placeholder*="验证码"]')
    if captcha_input.count() > 0:
        captcha_input.fill(os.getenv("CRM_CAPTCHA", "1234"))

    # 点击登录
    page.locator('button:has-text("登 录")').click()
    page.wait_for_timeout(5000)

    current_url = page.url
    print(f"[CONFTEST] 登录后 URL: {current_url}")

    # 如果还在登录页，说明验证码失败
    if "login" in current_url:
        print("[CONFTEST] ⚠️ 可能仍在登录页，请检查验证码")
        # 尝试直接导航到周报页
        page.goto(POST_LOGIN_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

    yield page
    print("[CONFTEST] CRM 测试完成")
