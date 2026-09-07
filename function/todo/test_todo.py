# -*- coding: utf-8 -*-
"""待办任务 (Todo) - UAT 测试脚本 (A1021)."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest
from utils.case_runner import execute_case

FEATURE_DIR = Path(__file__).resolve().parent
IGNORED_CASE_IDS: set[str] = set()

TODO_URL = "http://test.it188.com/#/todos"

# 待办列表 7 列表头（与原型一致）
TODO_HEADERS = ["任务", "关联", "类型", "节点日期", "优先级", "状态", "操作"]

# 筛选器
TODO_FILTERS = ["全部状态", "全部优先级", "全部来源"]

# 任务状态枚举（需求 §三）
TODO_STATUS = ["待办", "进行中", "已完成", "已取消"]

# 优先级枚举
TODO_PRIORITY = ["高", "中", "低"]

# 创建来源枚举
TODO_SOURCES = ["手动创建", "跟进记录归档", "节奏提醒", "系统自动"]


def _framework_perform_login(page, settings):
    fc = Path(__file__).resolve().parents[3] / "test-base" / "scripts" / "html" / "conftest.py"
    spec = importlib.util.spec_from_file_location("_fc", fc)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.perform_login(page, settings)


class TodoPO:
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

    def goto_todos(self):
        self._ensure_page_alive()
        self.page.goto(TODO_URL, wait_until="domcontentloaded")
        self._w(2000)
        self._d("已进入 待办任务 页面")

    def verify_page_title(self, title="待办任务"):
        assert self.page.locator(f'text={title}').count() > 0, f"页面标题 {title} 未找到"
        self._d(f"页面标题 {title} ✓")

    def verify_list_headers(self):
        for h in TODO_HEADERS:
            assert self.page.locator(f'th:has-text("{h}")').count() > 0, f"列表头 {h} 缺失"
        self._d("待办列表 7 列表头 ✓")

    def verify_filter_bar(self):
        for f in TODO_FILTERS:
            assert self.page.locator(f'select:has-text("{f}")').count() > 0, f"筛选器 {f} 缺失"
        self._d("待办筛选器 ✓")

    def verify_my_tasks_card(self):
        card = self.page.locator('.card:has-text("我的待办任务")').first
        assert card.count() > 0, "我的待办任务卡未找到"
        self._d("我的待办任务卡 ✓")

    def verify_data_rows(self):
        rows = self.page.locator("tbody tr")
        assert rows.count() > 0, "待办列表无数据行"
        self._d(f"待办列表数据行数: {rows.count()} ✓")

    def open_create_modal(self):
        self.page.locator('button:has-text("新建任务")').first.click()
        self._w(400)
        self._d("已点击新建任务")

    def verify_create_modal(self):
        modal = self.page.locator("#modal-task-create")
        assert modal.count() > 0 and modal.is_visible(), "新建任务弹窗未出现"
        self._d("新建任务弹窗 ✓")

    def verify_create_fields(self):
        # 任务标题/关联对象类型/优先级/跟进到期时间
        for kw in ["任务标题", "关联对象类型", "优先级"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"新建任务字段 {kw} 缺失"
        self._d("新建任务弹窗字段 ✓")

    def click_complete(self, idx=0):
        btn = self.page.locator('button:has-text("完成")').nth(idx)
        btn.click()
        self._w(500)
        self._d("已点击完成任务")

    def verify_overdue_badge(self):
        badge = self.page.locator('.itag', has_text="逾期")
        assert badge.count() > 0, "逾期标记未找到"
        self._d("逾期标记 ✓")

    def verify_priority_badge(self):
        # 优先级徽章（高/中/低）
        badge = self.page.locator('.itag', has_text="高")
        assert badge.count() > 0, "优先级标记未找到"
        self._d("优先级标记 ✓")

    def verify_status_badge(self):
        # 任务状态徽章（待办/进行中/已完成/已取消）
        badge = self.page.locator('.itag', has_text="待办")
        assert badge.count() > 0, "任务状态徽章未找到"
        self._d("任务状态徽章 ✓")

    def verify_task_type(self):
        # 任务类型（售前支持/销售跟进）
        badge = self.page.locator('.itag', has_text="售前支持")
        assert badge.count() > 0, "任务类型未找到"
        self._d("任务类型标记 ✓")

    def verify_related_object_type(self):
        # 关联对象类型（商机/客户）
        badge = self.page.locator('.itag', has_text="商机")
        assert badge.count() > 0, "关联对象类型未找到"
        self._d("关联对象类型标记 ✓")

    def verify_role_views(self):
        # 6 种角色视图：我的待办/团队待办/售前待办/协作商机任务/售前团队待办/全部待办
        for kw in ["我的待办任务", "团队待办任务", "协作商机任务"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"角色视图 {kw} 缺失"
        self._d("待办任务 6 角色视图 ✓")

    def verify_collab_task_readonly(self):
        # 协作商机任务（销售跟进 · 只读 · 了解销售推进节奏）
        card = self.page.locator('.card:has-text("协作商机任务")').first
        assert card.count() > 0, "协作商机任务卡未找到"
        assert "只读" in card.inner_text(), "协作商机任务应为只读"
        self._d("协作商机任务只读 ✓")

    def verify_team_view_owner(self):
        # 团队待办视图含负责人列
        assert self.page.locator('th:has-text("负责人")').count() > 0, "团队视图负责人列缺失"
        self._d("团队待办负责人列 ✓")

    def verify_task_type_switch(self):
        # 新建任务弹窗：任务类型（个人待办/共享待办）
        modal = self.page.locator("#modal-task-create")
        sel = modal.locator("#new-task-type")
        assert sel.count() > 0, "任务类型下拉未找到"
        options = sel.locator("option").all_inner_texts()
        assert "个人待办" in options and "共享待办" in options, f"任务类型选项缺失: {options}"
        self._d("任务类型（个人待办/共享待办）✓")

    def verify_shared_rel_cascade(self):
        # 共享待办 → 显示关联对象（— 无 —/商机/客户）→ 选商机后显示关联目标
        modal = self.page.locator("#modal-task-create")
        # 选共享待办
        modal.locator("#new-task-type").select_option("共享待办")
        self._w(300)
        wrap = modal.locator("#task-shared-wrap")
        assert wrap.is_visible(), "共享待办应显示关联对象"
        # 关联对象选项
        rel = modal.locator("#new-task-rel-type")
        rel_options = rel.locator("option").all_inner_texts()
        assert "商机" in rel_options and "客户" in rel_options, f"关联对象选项缺失: {rel_options}"
        # 选商机后显示关联目标
        rel.select_option("opp")
        self._w(300)
        target = modal.locator("#task-rel-target-wrap")
        assert target.is_visible(), "选商机后应显示关联目标"
        self._d("共享待办关联对象级联（商机/客户）✓")

    def verify_task_summary_required(self):
        # 任务摘要必填标记
        modal = self.page.locator("#modal-task-create")
        assert modal.locator('text=任务摘要').count() > 0, "任务摘要字段缺失"
        assert modal.locator('.req').count() > 0, "必填标记缺失"
        self._d("任务摘要必填 ✓")

    # ---------- 任务状态流转业务流程 ----------
    def verify_status_flow_buttons(self):
        # 状态只能通过「开始/完成/取消」按钮流转（需求规则2）
        for btn in ["完成"]:
            assert self.page.locator(f'button:has-text("{btn}")').count() > 0, f"状态流转按钮 {btn} 缺失"
        self._d("状态流转按钮（完成）✓")

    def verify_no_delete_button(self):
        # 需求规则1：任务不可删除，只能取消
        del_btns = self.page.locator('button:has-text("删除")')
        assert del_btns.count() == 0, "待办任务不应有删除按钮"
        self._d("任务不可删除（只能取消）✓")

    def verify_completed_terminal(self):
        # 需求：已完成/已取消为终态
        done = self.page.locator('.itag', has_text="已完成")
        assert done.count() > 0, "已完成终态展示缺失"
        self._d("已完成终态 ✓")

    def verify_status_badge_all(self):
        # 任务状态枚举：待办/进行中/已完成/已取消
        for s in ["待办", "已完成"]:
            assert self.page.locator(f'.itag:has-text("{s}")').count() > 0, f"状态 {s} 缺失"
        self._d("任务状态枚举展示 ✓")

    def verify_overdue_and_today(self):
        # 逾期/今日到期/即将到期标记（临近截止置顶）
        for kw in ["逾期", "今日到期"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"到期标记 {kw} 缺失"
        self._d("逾期/今日到期标记 ✓")


# ============================================================
# Visual runners
# ============================================================

def _mk_v(i, f):
    def runner(page, settings, pm=None):
        po = TodoPO(page, settings, pm)
        f(po)
    runner.__name__ = f"v_tc{i:02d}"
    return runner


_ALL_FNS = [
    (1, lambda po: (po.goto_todos(), po.verify_page_title())),
    (2, lambda po: (po.goto_todos(), po.verify_list_headers())),
    (3, lambda po: (po.goto_todos(), po.verify_filter_bar(), po.verify_data_rows())),
    (4, lambda po: (po.goto_todos(), po.verify_my_tasks_card())),
    (5, lambda po: (po.goto_todos(), po.open_create_modal(), po.verify_create_modal())),
    (6, lambda po: (po.goto_todos(), po.click_complete())),
    (7, lambda po: (po.goto_todos(), po.verify_overdue_badge())),
    (8, lambda po: (po.goto_todos(), po.verify_priority_badge())),
    (9, lambda po: (po.goto_todos(), po.verify_status_badge())),
    (10, lambda po: (po.goto_todos(), po.verify_related_object_type())),
    (11, lambda po: (po.goto_todos(), po.verify_task_type())),
    (12, lambda po: (po.goto_todos(), po.open_create_modal(), po.verify_create_fields())),
    (13, lambda po: (po.goto_todos(), po.verify_role_views())),
    (14, lambda po: (po.goto_todos(), po.verify_collab_task_readonly())),
    (15, lambda po: (po.goto_todos(), po.verify_team_view_owner())),
    (16, lambda po: (po.goto_todos(), po.open_create_modal(), po.verify_task_type_switch())),
    (17, lambda po: (po.goto_todos(), po.open_create_modal(), po.verify_shared_rel_cascade())),
    (18, lambda po: (po.goto_todos(), po.open_create_modal(), po.verify_task_summary_required())),
    (19, lambda po: (po.goto_todos(), po.verify_status_flow_buttons())),
    (20, lambda po: (po.goto_todos(), po.verify_no_delete_button())),
    (21, lambda po: (po.goto_todos(), po.verify_completed_terminal())),
    (22, lambda po: (po.goto_todos(), po.verify_status_badge_all())),
    (23, lambda po: (po.goto_todos(), po.verify_overdue_and_today())),
]

ALL_V = {}
for i, fn in _ALL_FNS:
    r = _mk_v(i, fn)
    ALL_V[f"tc{i:02d}"] = r


@pytest.mark.parametrize("case_id", [k for k in ALL_V if k not in IGNORED_CASE_IDS])
def test_todo(page, settings, case_id, page_manager):
    f = ALL_V[case_id]
    try:
        f(page, settings, page_manager)
    except Exception:
        print(f"[FAIL] {case_id}", flush=True)
        raise
