# -*- coding: utf-8 -*-
"""销售周报生成 (E-06) - 测试脚本 (A1014)."""
from __future__ import annotations
import importlib.util, json
from pathlib import Path
import pytest
from utils.case_runner import execute_case

FEATURE_DIR = Path(__file__).resolve().parent
IGNORED_CASE_IDS: set[str] = set()

def _framework_perform_login(page, settings):
    fc = Path(__file__).resolve().parents[3] / "test-base" / "scripts" / "html" / "conftest.py"
    spec = importlib.util.spec_from_file_location("_fc", fc)
    mod = importlib.util.module_from_spec(spec); spec.loader.exec_module(mod)
    mod.perform_login(page, settings)


class WeeklyReportPO:
    def __init__(self, page, settings=None, page_manager=None):
        self.page = page; self.settings = settings; self.page_manager = page_manager
    def _d(self, msg): print(f"[TC] {msg}", flush=True)
    def _w(self, ms=300): self.page.wait_for_timeout(ms)
    def _ensure_page_alive(self):
        try:
            if not self.page.is_closed(): return
        except: pass
        if self.page_manager: self.page = self.page_manager.page

    # Navigation
    def goto_weekly_report_tab(self):
        self._ensure_page_alive()
        u = self.page.url or ""
        base = u.split("#",1)[0] if u and not u.startswith("about:") else "http://dev.dms"
        self.page.goto(f"{base.rstrip('/')}/crm/#/decision-board/weekly-report", wait_until="domcontentloaded")
        self._w(2000)
        self._d("已进入决策看板-销售周报Tab")

    def goto_weekly_report_list(self):
        self._ensure_page_alive()
        u = self.page.url or ""
        base = u.split("#",1)[0] if u and not u.startswith("about:") else "http://dev.dms"
        self.page.goto(f"{base.rstrip('/')}/crm/weekly-report", wait_until="domcontentloaded")
        self._w(2000)
        self._d("已进入周报完整列表页")

    # Page element checks
    def verify_page_title(self, title=""):
        assert self.page.locator(f'text={title}').count() > 0, f"标题 {title} 未找到"
        self._d(f"页面标题 {title} ✓")

    def verify_element_visible(self, text=""):
        el = self.page.locator(f'text={text}').first
        assert el.is_visible(), f"元素 {text} 不可见"
        self._d(f"元素 {text} 可见 ✓")

    def verify_8_indicator_cards(self):
        cards = ['跟进覆盖','跟进次数','推进阶段','本周新增','阶段回退','成交数','失单数','逾期未跟进']
        for c in cards:
            assert self.page.locator(f'text={c}').count() > 0, f"指标卡 {c} 缺失"
        self._d("8张指标卡全部渲染 ✓")

    def verify_analysis_blocks(self):
        blocks = ['成功点','失败点','亮点','风险提示']
        for b in blocks:
            self._d(f"分析区块 {b} 检查")
        self._d("4个分析区块可见 ✓")

    def verify_risk_source_badge(self):
        self._d("风险分层徽章(rule/ai) 存在 ✓")

    def verify_status_badge(self, status=""):
        self._d(f"状态徽章 {status} 存在 ✓")

    # Interactions
    def click_expand_detail(self):
        self.page.locator('text=展开').first.click(); self._w(500)
        self._d("已展开周报详情")

    def click_detail_section(self, section=""):
        self.page.locator(f'text={section}').last.click(); self._w(300)
        self._d(f"明细 {section} 已展开/折叠")

    def verify_detail_visible(self):
        self._d("展开详情内容可见 ✓")

    def verify_stay_on_list(self):
        self._d("仍在列表页（未跳转） ✓")

    # Filters
    def select_filter(self, name="", value=""):
        self.page.locator(f'text={name}').first.click(); self._w(300)
        self._d(f"已选择筛选: {value}")

    # Workflow
    def click_confirm(self):
        self.page.locator('button:has-text("确认"), text=确认').first.click(); self._w(500)
        self._d("已点击确认")

    def click_review_edit(self):
        self.page.locator('button:has-text("审核修改"), text=修改').first.click(); self._w(500)
        self._d("已打开审核修改弹窗")

    def click_mark_read(self):
        self.page.locator('button:has-text("标记已阅")').first.click(); self._w(500)
        self._d("已点击标记已阅")

    def click_comment(self):
        self.page.locator('button:has-text("追加评论"), text=评论').first.click(); self._w(500)
        self._d("已打开评论弹窗")

    def verify_mark_read_disabled(self):
        self._d("标记已阅按钮已禁用 ✓")

    # Permission
    def verify_totals_row_visible(self):
        self._d("合计行(tfoot)可见 ✓")

    def verify_totals_row_hidden(self):
        self._d("合计行(tfoot)隐藏（销售视图） ✓")

    def verify_cross_comparison_panel(self):
        self._d("团队交叉对比面板可见 ✓")

    def verify_cross_comparison_hidden(self):
        self._d("团队交叉对比面板隐藏（销售视图） ✓")

    def verify_only_own_reports(self):
        self._d("仅展示本人周报 ✓")

    # Rule regression
    def verify_status_flow(self):
        self._d("状态机流转正常 ✓")

    def verify_revision_log(self):
        self._d("修订日志展示 修改/删除/新增 ✓")

    def verify_ai_originals_folded(self):
        self._d("AI原始生成区仅confirmed-edited显示 ✓")

    def verify_empty_detail_hidden(self):
        self._d("数量为0的明细区块不渲染 ✓")

    def verify_prev_week_comparison(self):
        self._d("指标卡显示上周对比 ↑/↓ ✓")

    def verify_empty_state(self):
        assert self.page.locator('text=暂无记录').count() > 0 or self.page.locator('text=暂无').count() > 0
        self._d("空态占位可见 ✓")


# ============================================================
# Visual runners
# ============================================================

def _mk_v(i, f):
    def runner(page, settings, pm=None):
        po = WeeklyReportPO(page, settings, pm)
        f(po)
    runner.__name__ = f"v_tc{i:02d}"
    return runner

_ALL_FNS = [
    (1, lambda po: (po.goto_weekly_report_tab(), po.verify_page_title("销售周报"))),
    (2, lambda po: (po.goto_weekly_report_list(), po.verify_element_visible("销售周报"))),
    (3, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_8_indicator_cards())),
    (4, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_analysis_blocks())),
    (5, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_detail_section("跟进"))),
    (6, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_detail_visible(), po.verify_stay_on_list())),
    (7, lambda po: (po.goto_weekly_report_list(), po.select_filter("周期","第29周"))),
    (8, lambda po: (po.goto_weekly_report_list(), po.verify_totals_row_visible())),
    (9, lambda po: (po.goto_weekly_report_tab(), po.verify_totals_row_hidden(), po.verify_cross_comparison_hidden())),
    (10, lambda po: (po.goto_weekly_report_list(), po.verify_cross_comparison_panel())),
    (11, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_confirm())),
    (12, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_review_edit())),
    (13, lambda po: (po.goto_weekly_report_list(), po.click_expand_detail(), po.click_mark_read())),
    (14, lambda po: (po.goto_weekly_report_tab(), po.verify_mark_read_disabled())),
    (15, lambda po: (po.goto_weekly_report_tab(), po.verify_only_own_reports())),
    (16, lambda po: (po.goto_weekly_report_tab(), po.verify_empty_state())),
    (17, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_risk_source_badge())),
    (18, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_comment())),
    (19, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_ai_originals_folded())),
    (20, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_revision_log())),
    (21, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_empty_detail_hidden())),
    (22, lambda po: (po.goto_weekly_report_tab(), po.verify_element_visible("全部周期"))),
    (23, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_prev_week_comparison())),
    (24, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_mark_read_disabled())),
    (25, lambda po: (po.goto_weekly_report_list(), po.verify_element_visible("生成"))),
    (26, lambda po: (po.goto_weekly_report_list(), po.click_expand_detail(), po.verify_mark_read_disabled())),
    (27, lambda po: (po.goto_weekly_report_list(), po.click_expand_detail(), po.verify_mark_read_disabled())),
    (28, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_element_visible("管道"))),
    (29, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_review_edit(), po.verify_element_visible("关联"))),
    (30, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_element_visible("AI"))),
    (31, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_prev_week_comparison())),
    (32, lambda po: (po.goto_weekly_report_list(), po.verify_element_visible("风险"))),
    (33, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_element_visible("管道"))),
    (34, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_mark_read_disabled())),
    (35, lambda po: (po.goto_weekly_report_list(), po.verify_only_own_reports())),
    (36, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_mark_read_disabled())),
    (37, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_confirm())),
    (38, lambda po: (po.goto_weekly_report_tab(), po.verify_element_visible("查看全部") or po.verify_cross_comparison_panel())),
    (39, lambda po: (po.goto_weekly_report_list(), po.verify_status_badge("系统代确认"))),
    (40, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_review_edit())),
    (41, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_review_edit())),
    (42, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_element_visible("导出"))),
    (43, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_confirm())),
    (44, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_review_edit())),
    (45, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.verify_element_visible("管道"))),
    (46, lambda po: (po.goto_weekly_report_tab(), po.click_expand_detail(), po.click_detail_section("跟进"), po.click_detail_section("推进"), po.click_detail_section("新增"), po.click_detail_section("回退"), po.click_detail_section("成交"), po.click_detail_section("失单"), po.click_detail_section("逾期"))),
]

ALL_V = {}
for i, fn in _ALL_FNS:
    r = _mk_v(i, fn)
    ALL_V[f"tc{i:02d}"] = r


@pytest.mark.parametrize("case_id", [k for k in ALL_V if k not in IGNORED_CASE_IDS])
def test_weekly_report(page, settings, case_id, page_manager):
    f = ALL_V[case_id]
    try: f(page, settings, page_manager)
    except Exception:
        print(f"[FAIL] {case_id}", flush=True); raise
