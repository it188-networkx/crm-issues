"""
conftest.py - CRM 商机模块 feature 级登录 fixture
"""
import os
import pytest
from playwright.sync_api import Page

CRM_BASE_URL = "http://test.it188.com"
CRM_ADMIN_USER = "admin"
CRM_ADMIN_PASS = "admin1234"
POST_LOGIN_URL = f"{CRM_BASE_URL}/#/opportunities"


@pytest.fixture(scope="session")
def crm_session(page: Page):
    """CRM 统一登录——整个 session 只登录一次。"""
    print("[CONFTEST] 开始 CRM 登录...")
    page.goto(f"{CRM_BASE_URL}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    page.locator('input[placeholder*="账号"]').fill(CRM_ADMIN_USER)
    page.locator('input[placeholder*="密码"]').fill(CRM_ADMIN_PASS)

    captcha_input = page.locator('input[placeholder*="验证码"]')
    if captcha_input.count() > 0:
        captcha_input.fill(os.getenv("CRM_CAPTCHA", "1234"))

    page.locator('button:has-text("登 录")').click()
    page.wait_for_timeout(5000)

    if "login" in page.url:
        print("[CONFTEST] ⚠️ 可能仍在登录页，请检查验证码")
        page.goto(POST_LOGIN_URL, wait_until="domcontentloaded")
        page.wait_for_timeout(3000)

    yield page
    print("[CONFTEST] CRM 商机模块测试完成")
