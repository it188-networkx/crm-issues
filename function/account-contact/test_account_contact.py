# -*- coding: utf-8 -*-
"""客户/联系人 (Account & Contact) - UAT 测试脚本 (A1020)."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest
from utils.case_runner import execute_case

FEATURE_DIR = Path(__file__).resolve().parent
IGNORED_CASE_IDS: set[str] = set()

ACCOUNT_URL = "http://test.it188.com/#/accounts"

# 客户列表 9 列表头（与原型一致）
ACCOUNT_HEADERS = ["公司简称", "行业", "客户类型", "状态", "获客来源", "负责人", "合作情况", "归属生效时间", "操作"]

# 详情页 3 Tabs
ACCOUNT_TABS = ["基础信息", "联系人", "跟进时间线"]

# 决策链角色枚举（需求 §三）
DECISION_ROLES = ["最终拍板人", "核心决策人", "关键影响人", "技术评估人", "采购执行人", "信息提供人", "一般联系人"]

# 决策权重枚举
DECISION_WEIGHTS = ["高", "中", "低"]

# 联系人状态枚举
CONTACT_STATUS = ["活跃", "已离职", "已失联", "休眠"]


def _framework_perform_login(page, settings):
    fc = Path(__file__).resolve().parents[3] / "test-base" / "scripts" / "html" / "conftest.py"
    spec = importlib.util.spec_from_file_location("_fc", fc)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.perform_login(page, settings)


class AccountContactPO:
    def __init__(self, page, settings=None, page_manager=None):
        self.page = page
        self.settings = settings
        self.page_manager = page_manager

    def _d(self, msg):
        print(f"[TC] {msg}", flush=True)

    def _w(self, ms=300):
        self.page.wait_for_timeout(ms)

    def _ensure_page_alive(self):
        try:
            if not self.page.is_closed():
                return
        except Exception:
            pass
        if self.page_manager:
            self.page = self.page_manager.page

    def goto_accounts(self):
        self._ensure_page_alive()
        self.page.goto(ACCOUNT_URL, wait_until="domcontentloaded")
        self._w(2000)
        self._d("已进入 客户管理 页面")

    def verify_page_title(self, title="客户管理"):
        assert self.page.locator(f'text={title}').count() > 0, f"页面标题 {title} 未找到"
        self._d(f"页面标题 {title} ✓")

    def verify_list_headers(self):
        for h in ACCOUNT_HEADERS:
            assert self.page.locator(f'th:has-text("{h}")').count() > 0, f"列表头 {h} 缺失"
        self._d("客户列表 9 列表头 ✓")

    def verify_filter_bar(self):
        for f in ["行业", "客户类型", "状态"]:
            assert self.page.locator(f'select:has-text("{f}")').count() > 0, f"筛选器 {f} 缺失"
        self._d("客户列表筛选器 ✓")

    def verify_data_rows(self):
        rows = self.page.locator("tbody tr")
        assert rows.count() > 0, "客户列表无数据行"
        self._d(f"客户列表数据行数: {rows.count()} ✓")

    def open_create_modal(self):
        self.page.locator('button:has-text("新增")').first.click()
        self._w(400)
        self._d("已点击新增客户")

    def verify_create_modal(self):
        modal = self.page.locator("#modal-account-create")
        assert modal.count() > 0 and modal.is_visible(), "新增客户弹窗未出现"
        self._d("新增客户弹窗 ✓")

    def click_row_detail(self, idx=0):
        self.page.locator("tbody tr").nth(idx).click()
        self._w(800)
        self._d("已点击客户行进入详情")

    def verify_detail_tabs(self):
        for t in ACCOUNT_TABS:
            assert self.page.locator(f'.tab-item:has-text("{t}")').count() > 0, f"Tab {t} 缺失"
        self._d("客户详情 3 Tabs ✓")

    def verify_core_info(self):
        # 核心信息卡：客户编码/企业名称/客户状态/客户类型等
        for kw in ["客户编码", "企业名称", "客户状态", "客户类型"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"核心信息 {kw} 缺失"
        self._d("核心信息卡 ✓")

    def verify_business_info(self):
        # 归属与商务卡：归属来源/客户等级/细分赛道/合同年收入
        for kw in ["归属来源", "客户等级", "细分赛道"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"归属与商务 {kw} 缺失"
        self._d("归属与商务卡 ✓")

    def verify_insight_collapse(self):
        # 补充洞察折叠展开
        header = self.page.locator('text=补充洞察').first
        assert header.count() > 0, "补充洞察卡未找到"
        header.click()
        self._w(400)
        self._d("补充洞察折叠展开 ✓")

    def verify_change_log(self):
        assert self.page.locator('text=修改日志').count() > 0, "修改日志卡未找到"
        self._d("修改日志卡 ✓")

    def verify_related_opp(self):
        assert self.page.locator('text=关联商机').count() > 0, "关联商机表未找到"
        self._d("关联商机表 ✓")

    def goto_contact_create(self):
        # 联系人 Tab → 新建联系人（原型通过账号详情页进入）
        self.page.locator('.tab-item:has-text("联系人")').first.click()
        self._w(500)
        self.page.locator('button:has-text("新建联系人"), button:has-text("+ 新建")').first.click()
        self._w(800)
        self._d("已进入新建联系人页面")

    def verify_contact_form(self):
        # 联系人新建页：基本信息 + 决策链信息
        for kw in ["姓名", "职位", "决策链角色", "决策权重"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"联系人表单 {kw} 缺失"
        self._d("联系人新建表单字段 ✓")

    def verify_decision_roles(self):
        # 决策链角色下拉（枚举：最终拍板人/核心决策人/关键影响人/技术评估人/采购执行人/信息提供人/一般联系人）
        sel = self.page.locator('select').filter(has_text="最终拍板人").first
        assert sel.count() > 0, "决策链角色下拉未找到"
        self._d("决策链角色下拉 ✓")

    def verify_decision_weights(self):
        # 决策权重下拉（高/中/低）
        sel = self.page.locator('select').filter(has_text="高").first
        assert sel.count() > 0, "决策权重下拉未找到"
        self._d("决策权重下拉 ✓")

    def verify_contact_status(self):
        # 联系人状态下拉（活跃/已离职/已失联/休眠）
        sel = self.page.locator('select').filter(has_text="已离职").first
        assert sel.count() > 0, "联系人状态下拉未找到"
        self._d("联系人状态下拉 ✓")

    def verify_account_status_badge(self):
        # 客户状态徽章（商机推进中）
        badge = self.page.locator('.itag', has_text="商机推进中")
        assert badge.count() > 0, "客户状态徽章未找到"
        self._d("客户状态徽章 ✓")

    def switch_to_contacts_tab(self):
        self.page.locator('.tab-item:has-text("联系人")').first.click()
        self._w(500)
        self._d("已切换到联系人 Tab")

    def verify_contacts_tab(self):
        # 联系人 Tab：联系人卡片列表（姓名/职位/决策链角色/客情状态）
        self.switch_to_contacts_tab()
        # 联系人卡片（王明/李华/赵敏）
        assert self.page.locator('text=王明').count() > 0, "联系人王明未找到"
        self._d("联系人 Tab 卡片列表 ✓")

    def switch_to_timeline_tab(self):
        self.page.locator('.tab-item:has-text("跟进时间线")').first.click()
        self._w(500)
        self._d("已切换到跟进时间线 Tab")

    def verify_timeline_tab(self):
        # 跟进时间线 Tab：时间线 + 新建跟进按钮
        self.switch_to_timeline_tab()
        assert self.page.locator('button:has-text("新建跟进")').count() > 0, "时间线新建跟进按钮缺失"
        self._d("跟进时间线 Tab ✓")

    def verify_ownership_panel(self):
        # 归属与状态面板：当前责任人/客户等级/标签
        for kw in ["当前责任人", "客户等级", "客户状态"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"归属与状态 {kw} 缺失"
        self._d("归属与状态面板 ✓")

    def verify_contact_detail(self):
        # 联系人详情页：基本信息 + 决策链信息 + 客情状态
        for kw in ["姓名", "决策链角色", "决策权重", "客情状态"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"联系人详情 {kw} 缺失"
        self._d("联系人详情页 ✓")

    def verify_tag_button(self):
        # 归属与状态面板「+ 打标签」按钮
        btn = self.page.locator('button:has-text("打标签")')
        assert btn.count() > 0, "打标签按钮缺失"
        self._d("打标签按钮 ✓")

    def verify_new_contact_button(self):
        # 联系人 Tab「+ 新建联系人」按钮
        self.switch_to_contacts_tab()
        btn = self.page.locator('button:has-text("新建联系人")')
        assert btn.count() > 0, "新建联系人按钮缺失"
        self._d("新建联系人按钮 ✓")

    # ---------- 业务流程 ----------
    def verify_account_create_fields(self):
        # 客户建档流程：企业简称(必填)/全称/行业/客户类型
        modal = self.page.locator("#modal-account-create")
        assert modal.count() > 0 and modal.is_visible(), "新增客户弹窗未出现"
        for kw in ["企业简称", "全称", "行业", "客户类型"]:
            assert modal.locator(f'text={kw}').count() > 0, f"建档字段 {kw} 缺失"
        # 企业简称必填
        assert modal.locator('.req').count() > 0, "必填标记缺失"
        self._d("客户建档表单字段 + 必填 ✓")

    def verify_account_industry_enum(self):
        # 行业枚举
        modal = self.page.locator("#modal-account-create")
        opts = modal.locator('select').first.locator("option").all_inner_texts()
        assert "金融" in opts and "制造" in opts, f"行业枚举缺失: {opts}"
        self._d(f"行业枚举 ✓ ({opts})")

    def verify_contact_status_effect(self):
        # 需求规则2：联系人状态「已离职/已失联」触发客情阶段自动降级
        # UI 层验证：联系人状态下拉含 已离职/已失联，客情状态下拉存在
        self.goto_contact_create()
        sel = self.page.locator('select').filter(has_text="已离职").first
        assert sel.count() > 0, "联系人状态（已离职/已失联）缺失"
        assert self.page.locator('text=客情状态').count() > 0, "客情状态字段缺失"
        self._d("联系人状态联动客情降级（观察项）✓")

    def verify_contact_phone_email(self):
        # 需求：手机号/邮箱二选一必填
        self.goto_contact_create()
        assert self.page.locator('text=手机号').count() > 0, "手机号字段缺失"
        assert self.page.locator('text=邮箱').count() > 0, "邮箱字段缺失"
        self._d("手机号/邮箱二选一必填字段 ✓")

    def verify_customer_status_flow(self):
        # 客户状态流转：潜客→商机推进中→签约中→交付中→续约中→风险客户→流失
        # UI 层验证：客户列表状态徽章 + 详情状态展示
        assert self.page.locator('text=商机推进中').count() > 0, "客户状态展示缺失"
        self._d("客户状态流转展示（潜客/商机推进中/签约中...）✓")


# ============================================================
# Visual runners
# ============================================================

def _mk_v(i, f):
    def runner(page, settings, pm=None):
        po = AccountContactPO(page, settings, pm)
        f(po)
    runner.__name__ = f"v_tc{i:02d}"
    return runner


_ALL_FNS = [
    (1, lambda po: (po.goto_accounts(), po.verify_page_title())),
    (2, lambda po: (po.goto_accounts(), po.verify_list_headers())),
    (3, lambda po: (po.goto_accounts(), po.verify_filter_bar(), po.verify_data_rows())),
    (4, lambda po: (po.goto_accounts(), po.open_create_modal(), po.verify_create_modal())),
    (5, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_detail_tabs())),
    (6, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_core_info())),
    (7, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_business_info())),
    (8, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_insight_collapse())),
    (9, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_change_log())),
    (10, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_related_opp())),
    (11, lambda po: (po.goto_accounts(), po.click_row_detail(), po.goto_contact_create(), po.verify_contact_form())),
    (12, lambda po: (po.goto_accounts(), po.click_row_detail(), po.goto_contact_create(), po.verify_decision_roles())),
    (13, lambda po: (po.goto_accounts(), po.click_row_detail(), po.goto_contact_create(), po.verify_decision_weights())),
    (14, lambda po: (po.goto_accounts(), po.click_row_detail(), po.goto_contact_create(), po.verify_contact_status())),
    (15, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_account_status_badge())),
    (16, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_contacts_tab())),
    (17, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_timeline_tab())),
    (18, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_ownership_panel())),
    (19, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_tag_button())),
    (20, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_new_contact_button())),
    (21, lambda po: (po.goto_accounts(), po.open_create_modal(), po.verify_account_create_fields())),
    (22, lambda po: (po.goto_accounts(), po.open_create_modal(), po.verify_account_industry_enum())),
    (23, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_contact_status_effect())),
    (24, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_contact_phone_email())),
    (25, lambda po: (po.goto_accounts(), po.click_row_detail(), po.verify_customer_status_flow())),
]

ALL_V = {}
for i, fn in _ALL_FNS:
    r = _mk_v(i, fn)
    ALL_V[f"tc{i:02d}"] = r


@pytest.mark.parametrize("case_id", [k for k in ALL_V if k not in IGNORED_CASE_IDS])
def test_account_contact(page, settings, case_id, page_manager):
    f = ALL_V[case_id]
    try:
        f(page, settings, page_manager)
    except Exception:
        print(f"[FAIL] {case_id}", flush=True)
        raise
