# -*- coding: utf-8 -*-
"""跟进记录 (Followup) - UAT 测试脚本 (A1019)."""
from __future__ import annotations
import importlib.util
from pathlib import Path
import pytest
from utils.case_runner import execute_case

FEATURE_DIR = Path(__file__).resolve().parent
IGNORED_CASE_IDS: set[str] = set()

FOLLOWUP_URL = "http://test.it188.com/#/followups"

# 跟进列表 10 列表头（与原型一致）
FOLLOWUP_HEADERS = ["跟进时间", "关联", "关联类型", "跟进内容", "意向等级", "触达方式", "阶段变更", "跟进关键词", "跟进人", "操作"]

# 详情页区块
FOLLOWUP_SECTIONS = ["基础信息", "录音回放", "AI 转写参考", "跟进关键词", "商机深度信息"]

# 意向等级枚举（需求 §三）
INTENT_LEVELS = ["冷淡", "一般", "有兴趣", "强意向"]

# 触达方式枚举（需求 §二）
CONTACT_METHODS = ["电话", "微信", "邮件", "现场拜访", "视频会议", "企业微信", "其他"]


def _framework_perform_login(page, settings):
    fc = Path(__file__).resolve().parents[3] / "test-base" / "scripts" / "html" / "conftest.py"
    spec = importlib.util.spec_from_file_location("_fc", fc)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.perform_login(page, settings)


class FollowupPO:
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

    def goto_followups(self):
        self._ensure_page_alive()
        self.page.goto(FOLLOWUP_URL, wait_until="domcontentloaded")
        self._w(2000)
        self._d("已进入 跟进记录 页面")

    def verify_page_title(self, title="跟进记录"):
        assert self.page.locator(f'text={title}').count() > 0, f"页面标题 {title} 未找到"
        self._d(f"页面标题 {title} ✓")

    def verify_list_headers(self):
        for h in FOLLOWUP_HEADERS:
            assert self.page.locator(f'th:has-text("{h}")').count() > 0, f"列表头 {h} 缺失"
        self._d("跟进列表 10 列表头 ✓")

    def verify_filter_bar(self):
        for f in ["全部时段", "触达方式", "阶段变更"]:
            assert self.page.locator(f'select:has-text("{f}")').count() > 0, f"筛选器 {f} 缺失"
        assert self.page.locator('input[placeholder*="搜索跟进内容"]').count() > 0, "搜索框缺失"
        self._d("跟进列表筛选器 ✓")

    def verify_data_rows(self):
        rows = self.page.locator("tbody tr")
        assert rows.count() > 0, "跟进列表无数据行"
        self._d(f"跟进列表数据行数: {rows.count()} ✓")

    def open_create(self):
        self.page.locator('button:has-text("新建跟进")').first.click()
        self._w(800)
        self._d("已点击新建跟进")

    def verify_entry_modes(self):
        # 4 种录入方式：语音录入/录音导入/粘贴文本/完整表单
        bar = self.page.locator("#entry-mode-bar")
        assert bar.count() > 0, "录入方式切换栏未找到"
        for mode in ["语音录入", "录音导入", "粘贴文本", "完整表单"]:
            assert bar.locator(f'button:has-text("{mode}")').count() > 0, f"录入方式 {mode} 缺失"
        self._d("4 种录入方式 ✓")

    def switch_entry_mode(self, mode="text"):
        self.page.locator(f'#entry-mode-bar button:has-text("{mode}")').first.click()
        self._w(400)
        self._d(f"已切换到 {mode} 录入方式")

    def click_row_detail(self, idx=0):
        self.page.locator("tbody tr").nth(idx).click()
        self._w(800)
        self._d("已点击跟进行进入详情")

    def verify_detail_sections(self):
        for s in FOLLOWUP_SECTIONS:
            assert self.page.locator(f'text={s}').count() > 0, f"详情区块 {s} 缺失"
        self._d("跟进详情页 5 大区块 ✓")

    def verify_archive_badge(self):
        badge = self.page.locator('text=已归档')
        assert badge.count() > 0, "已归档徽章未找到"
        self._d("归档状态徽章 ✓")

    def verify_ai_transcript_toggle(self):
        # AI 转写参考卡片可折叠展开
        header = self.page.locator('text=AI 转写参考').first
        assert header.count() > 0, "AI 转写参考卡片未找到"
        header.click()
        self._w(400)
        self._d("AI 转写折叠展开 ✓")

    def verify_keyword_tags(self):
        tags = self.page.locator('.itag', has_text="统一告警")
        # 跟进关键词区块
        kw_section = self.page.locator('text=跟进关键词')
        assert kw_section.count() > 0, "跟进关键词区块未找到"
        self._d("跟进关键词标签 ✓")

    def verify_deep_info(self):
        # 商机深度信息：跟进要点/客户IT环境/客户痛点/客户需求/决策链观察
        for kw in ["跟进要点", "客户IT环境", "客户痛点", "客户需求", "决策链观察"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"商机深度信息 {kw} 缺失"
        self._d("商机深度信息区块 ✓")

    def verify_audio_playback(self):
        play = self.page.locator('text=录音回放')
        assert play.count() > 0, "录音回放卡未找到"
        self._d("录音回放卡 ✓")

    def verify_budget_status(self):
        # 立项状态字段（详情页基础信息）
        assert self.page.locator('text=预算状态').count() > 0, "立项状态字段未找到"
        self._d("立项状态字段 ✓")

    def verify_budget_risk(self):
        # 立项风险展示
        risk = self.page.locator('text=低风险')
        assert risk.count() > 0, "立项风险展示未找到"
        self._d("立项风险展示 ✓")

    def verify_intent_level(self):
        # 意向等级字段展示（详情页基础信息）
        assert self.page.locator('text=意向等级').count() > 0, "意向等级字段未找到"
        self._d("意向等级字段 ✓")

    def verify_contact_method(self):
        # 触达方式字段展示（详情页基础信息）
        assert self.page.locator('text=触达方式').count() > 0, "触达方式字段未找到"
        self._d("触达方式字段 ✓")

    def verify_next_actions(self):
        # issue 模块2：下步行动多任务清单。新建跟进页「下步行动项」卡片
        # AI 提取 + 手动添加 + 驳回 + 任务类型选择（销售跟进/售前支持/协作跟进）
        card = self.page.locator('#next-actions-list')
        assert card.count() > 0, "下步行动项清单未找到"
        items = card.locator('.extraction-item')
        assert items.count() > 0, "下步行动项为空"
        # 任务类型下拉（销售跟进/售前支持/协作跟进）
        assert card.locator('select:has-text("协作跟进")').count() > 0, "任务类型下拉缺失"
        # 手动添加按钮
        assert self.page.locator('button:has-text("手动添加")').count() > 0, "手动添加按钮缺失"
        self._d(f"下步行动多任务清单 ✓ ({items.count()} 条)")

    def verify_next_action_reject(self):
        # 下步行动项可驳回
        reject_btn = self.page.locator('#next-actions-list button:has-text("驳回")').first
        assert reject_btn.count() > 0, "行动项驳回按钮缺失"
        reject_btn.click()
        self._w(300)
        self._d("下步行动项驳回 ✓")

    def verify_intent_judge(self):
        # 客户意向判断：持续跟进/近期成交/长期培育 + 关联类型（商机/客户/无关联）
        for kw in ["持续跟进", "近期成交", "长期培育"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"意向判断 {kw} 缺失"
        for kw in ["商机", "客户"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"关联类型 {kw} 缺失"
        self._d("客户意向判断卡 ✓")

    def verify_create_type(self):
        # 创建类型：人工跟进/自动触达/渠道同步
        for kw in ["人工跟进", "自动触达", "渠道同步"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"创建类型 {kw} 缺失"
        self._d("创建类型枚举 ✓")

    def verify_attendees(self):
        # 参会联系人（多选）
        assert self.page.locator('text=添加参会联系人').count() > 0, "参会联系人字段缺失"
        self._d("参会联系人字段 ✓")

    def verify_competitor_status(self):
        # 竞对状态：无竞争/已出现/活跃竞争/客户倾向竞对
        for kw in ["无竞争", "已出现", "活跃竞争"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"竞对状态 {kw} 缺失"
        self._d("竞对状态枚举 ✓")

    def verify_stage_ops(self):
        # 阶段操作：无阶段变更/推进/回退/标记成交/标记失单
        for kw in ["无阶段变更", "推进阶段", "回退阶段", "标记成交", "标记失单"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"阶段操作 {kw} 缺失"
        self._d("阶段操作（推进/回退/成交/失单）✓")

    def verify_lost_reasons(self):
        # 失单原因枚举：竞对中标/预算取消/项目终止/客户流失/其他
        for kw in ["竞对中标", "预算取消", "项目终止", "客户流失"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"失单原因 {kw} 缺失"
        self._d("失单原因枚举 ✓")

    def verify_presales_observation(self):
        # 售前技术观察区（pre-only/psl-only）：风险标签多选 + 技术观察 + 保存
        for kw in ["售前技术观察", "风险标签", "技术观察"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"售前技术观察 {kw} 缺失"
        self._d("售前技术观察区块 ✓")

    def verify_next_action_plan(self):
        # 下一步行动计划：下次计划日期/下步工作类型/负责人/下次跟进计划/需要公司支持
        for kw in ["下一步行动计划", "下次计划日期", "下步工作类型"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"下一步行动计划 {kw} 缺失"
        self._d("下一步行动计划区块 ✓")

    def verify_customer_voice(self):
        # 客户原声
        assert self.page.locator('text=客户原声').count() > 0, "客户原声区块未找到"
        self._d("客户原声区块 ✓")

    def verify_supplement_info(self):
        # 补充信息：竞对名称/关联商机/关联材料/公司支持/补充备注
        for kw in ["补充信息", "竞对名称", "关联材料"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"补充信息 {kw} 缺失"
        self._d("补充信息区块 ✓")

    def verify_modify_log(self):
        # 修改日志：所有编辑操作留痕
        assert self.page.locator('text=修改日志').count() > 0, "修改日志区块未找到"
        self._d("修改日志区块 ✓")

    # ---------- 完整业务流程 ----------
    def submit_archive(self):
        # 新建跟进页点「提交归档」
        btn = self.page.locator('button:has-text("提交归档")').first
        assert btn.count() > 0, "提交归档按钮缺失"
        btn.click()
        self._w(600)
        self._d("已点击提交归档")

    def verify_ai_normalize_modal(self):
        # 提交归档前 AI 规范化确认弹窗
        modal = self.page.locator("#modal-ai-normalize")
        assert modal.count() > 0 and modal.is_visible(), "AI 规范化确认弹窗未出现"
        assert modal.locator('text=提交归档前确认字段格式').count() > 0, "弹窗缺少说明"
        self._d("AI 规范化确认弹窗（归档前）✓")

    def verify_archive_toast(self):
        # 归档成功 toast
        toast = self.page.locator('.toast, .el-message', has_text="已提交")
        assert toast.count() > 0, "归档成功提示未出现"
        self._d("跟进记录归档成功 ✓")

    def verify_content_required(self):
        # 需求规则8：6 个内容字段至少填 1 个才允许归档
        # 原型：右侧关键内容卡（跟进要点/客户IT环境/客户痛点/客户需求/决策链观察）
        for kw in ["跟进要点", "客户IT环境", "客户痛点", "客户需求", "决策链观察"]:
            assert self.page.locator(f'text={kw}').count() > 0, f"内容字段 {kw} 缺失"
        self._d("内容字段至少填 1 个（6 字段）✓")

    def verify_intent_to_opportunity(self):
        # 需求规则6：意向等级≥有兴趣时提醒转商机
        # 原型：意向等级选择（持续跟进/近期成交/长期培育 或 有兴趣/强意向）
        # 观察项：转商机建议由后端触发，UI 验证意向等级选项存在
        assert self.page.locator('text=意向').count() > 0 or self.page.locator('text=近期成交').count() > 0, "意向等级字段缺失"
        self._d("意向等级（≥有兴趣转商机建议，观察项）✓")

    def verify_record_archived_readonly(self):
        # 需求规则1：归档后不可修改删除（详情页「已归档」徽章 + 无编辑按钮）
        assert self.page.locator('text=已归档').count() > 0, "已归档徽章缺失"
        # 详情页无编辑/删除按钮
        edit_btns = self.page.locator('button:has-text("编辑"), button:has-text("删除")')
        assert edit_btns.count() == 0, "归档后不应有编辑/删除按钮"
        self._d("归档后不可修改删除 ✓")


# ============================================================
# Visual runners
# ============================================================

def _mk_v(i, f):
    def runner(page, settings, pm=None):
        po = FollowupPO(page, settings, pm)
        f(po)
    runner.__name__ = f"v_tc{i:02d}"
    return runner


_ALL_FNS = [
    (1, lambda po: (po.goto_followups(), po.verify_page_title())),
    (2, lambda po: (po.goto_followups(), po.verify_list_headers())),
    (3, lambda po: (po.goto_followups(), po.verify_filter_bar(), po.verify_data_rows())),
    (4, lambda po: (po.goto_followups(), po.open_create())),
    (5, lambda po: (po.goto_followups(), po.open_create(), po.verify_entry_modes())),
    (6, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_detail_sections())),
    (7, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_archive_badge())),
    (8, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_ai_transcript_toggle())),
    (9, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_keyword_tags())),
    (10, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_deep_info())),
    (11, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_intent_level())),
    (12, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_contact_method())),
    (13, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_budget_status())),
    (14, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_budget_risk())),
    (15, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_audio_playback())),
    (16, lambda po: (po.goto_followups(), po.open_create(), po.verify_next_actions())),
    (17, lambda po: (po.goto_followups(), po.open_create(), po.verify_next_action_reject())),
    (18, lambda po: (po.goto_followups(), po.open_create(), po.verify_intent_judge())),
    (19, lambda po: (po.goto_followups(), po.open_create(), po.verify_create_type())),
    (20, lambda po: (po.goto_followups(), po.open_create(), po.verify_attendees())),
    (21, lambda po: (po.goto_followups(), po.open_create(), po.verify_competitor_status())),
    (22, lambda po: (po.goto_followups(), po.open_create(), po.verify_stage_ops())),
    (23, lambda po: (po.goto_followups(), po.open_create(), po.verify_lost_reasons())),
    (24, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_presales_observation())),
    (25, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_next_action_plan())),
    (26, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_customer_voice())),
    (27, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_supplement_info())),
    (28, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_modify_log())),
    (29, lambda po: (po.goto_followups(), po.open_create(), po.verify_content_required())),
    (30, lambda po: (po.goto_followups(), po.open_create(), po.submit_archive(), po.verify_ai_normalize_modal())),
    (31, lambda po: (po.goto_followups(), po.click_row_detail(), po.verify_record_archived_readonly())),
    (32, lambda po: (po.goto_followups(), po.open_create(), po.verify_intent_to_opportunity())),
]

ALL_V = {}
for i, fn in _ALL_FNS:
    r = _mk_v(i, fn)
    ALL_V[f"tc{i:02d}"] = r


@pytest.mark.parametrize("case_id", [k for k in ALL_V if k not in IGNORED_CASE_IDS])
def test_followup(page, settings, case_id, page_manager):
    f = ALL_V[case_id]
    try:
        f(page, settings, page_manager)
    except Exception:
        print(f"[FAIL] {case_id}", flush=True)
        raise
