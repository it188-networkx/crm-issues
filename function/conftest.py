"""
conftest.py - CRM 功能测试 pytest 配置
复用 test-base/scripts/html/ 全局框架的所有 fixtures & hooks。
注意：Python 路径已由 pytest.ini 的 pythonpath 选项自动注入，无需手动 sys.path。
"""
from pathlib import Path
import os

# ── 多环境切换 ──────────────────────────────────────────────────────────────
# 用法: pytest --env=dev|staging|prod
#     dev: 本地开发环境（默认）
#     staging: 预发布环境
#     prod: 生产环境（仅限只读冒烟，禁止写操作）
# 各模块 conftest 里用 os.getenv("BASE_URL") 即可获取对应环境地址。
#
# CRM 登录模式：
#   系统使用统一的 EMS 登录入口，账号体系为邮箱 + 密码 + 验证码。
#   不同角色（MKT Leader / Sales / Admin）通过功能级权限控制可访问模块。
#   Feature 级 conftest 需设置 POST_LOGIN_URL 指向对应功能页面。
_ENV_MAP = {
    "dev":  "http://dev.dms",
    "staging": "http://staging.dms",
    "prod": "https://crm.example.com",
}

def pytest_addoption(parser):
    parser.addoption("--env", default="dev", help=f"测试环境: {'|'.join(_ENV_MAP.keys())}")

def pytest_configure(config):
    env = config.getoption("--env", default="dev")
    base_url = _ENV_MAP.get(env, _ENV_MAP["dev"])
    os.environ["BASE_URL"] = base_url
    os.environ["CRM_BASE_URL"] = base_url

# ── 全局框架路径（仅用于加载 conftest，路径注入已由 pytest.ini pythonpath 完成）──
_FRAMEWORK = Path(__file__).resolve().parents[2] / "test-base" / "scripts" / "html"
if not _FRAMEWORK.exists():
    raise RuntimeError(f"全局框架目录不存在: {_FRAMEWORK}")

# ── 复用全局框架的所有 fixtures & hooks ────────────────────────────────────
import importlib.util

_spec = importlib.util.spec_from_file_location("_html_conftest", _FRAMEWORK / "conftest.py")
_mod = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(_mod)

for _name in dir(_mod):
    if not _name.startswith("__"):
        globals()[_name] = getattr(_mod, _name)
