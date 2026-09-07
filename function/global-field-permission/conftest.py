"""
conftest.py - CRM 全局字段/权限模块 feature 级登录 fixture
支持角色切换（admin/sales/sales-leader/presales-leader/mkt-leader）
"""
import os
import pytest
from playwright.sync_api import Page

CRM_BASE_URL = "http://test.it188.com"

# 角色账号（邮箱+密码+验证码，验证码开发环境 1234）
ROLE_ACCOUNTS = {
    "admin": ("admin", "admin1234"),
    "sales": ("cuizhibo", "admin123"),
    "sales-leader": ("caizhengli", "admin123"),
    "presales-leader": ("zhangyi", "admin123"),
    "mkt-leader": ("shenjie", "admin123"),
}


@pytest.fixture(scope="session")
def crm_session(page: Page):
    """CRM 统一登录（默认 admin）——整个 session 只登录一次。"""
    user, pwd = ROLE_ACCOUNTS[os.getenv("CRM_ROLE", "admin")]
    print(f"[CONFTEST] 开始 CRM 登录（角色 {os.getenv('CRM_ROLE', 'admin')}）...")
    page.goto(f"{CRM_BASE_URL}/login", wait_until="domcontentloaded")
    page.wait_for_timeout(2000)

    page.locator('input[placeholder*="账号"]').fill(user)
    page.locator('input[placeholder*="密码"]').fill(pwd)

    captcha_input = page.locator('input[placeholder*="验证码"]')
    if captcha_input.count() > 0:
        captcha_input.fill(os.getenv("CRM_CAPTCHA", "1234"))

    page.locator('button:has-text("登 录")').click()
    page.wait_for_timeout(5000)

    if "login" in page.url:
        print("[CONFTEST] ⚠️ 可能仍在登录页，请检查验证码")

    yield page
    print("[CONFTEST] CRM 全局权限模块测试完成")
