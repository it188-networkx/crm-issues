# Function 测试规范 — CRM

> **前置必读（强制）**
>
> 生成或修改任何 UI 自动化测试用例之前，必须先用 `read_file` 阅读以下文档以理解 CRM 业务逻辑：
> - `crm-product/README.md` — AI Native CRM 产品定义、4 Theme / 19 Epic / 70+ Feature
> - `crm-product/concept/product-definition.md` — 愿景、定位、MVP 范围
> - `crm-product/architecture/architecture.md` — 13 个子系统架构与模块关系
>
> 禁止仅凭需求文字或原型图盲写用例；必须先理解 CRM 以营销闭环和 AI 辅助决策为核心的系统逻辑。

## CRM 产品概要

面向 ICT 运维服务小团队的 **AI Native 内部 CRM**，以 AI 建议替代手工判断。

| 维度 | 说明 |
| :--- | :--- |
| **核心命题** | AI 扩容（覆盖规模 x3）、经验沉淀（客户关系资产）、老板视角（漏斗全链路） |
| **用户角色** | MKT Leader（市场负责人）、Sales（销售）、Pre-sales（售前）、Administrators（管理员） |
| **4 大 Theme** | T-01 营销过程闭环 / T-02 AI 营销管理 / T-03 决策驾驶舱 / T-04 营销知识库 |
| **13 个子系统** | 线索管理、客户管理、销售管道、工作台、客户360、AI辅助、知识库、仪表盘、EDM营销、营销自动化、数据接入、配置、公共服务 |

## 目录结构

> **边界硬约束（必须遵守）**
>
> - `xxx-issues/function/` 仅允许存放业务逻辑资产与轮次执行产物。
> - 任何公共框架、参数模型、工具封装，必须放在 `test-base/scripts/html/` 中。
> - `xxx-issues/scripts/func-test.py` 仅允许作为薄入口转发。

功能测试以 CRM 业务场景为驱动，验证端到端功能，可穿越多个子系统（如线索→跟进→商机→成交）。

```text
function/
├── conftest.py                             # CRM 仓 pytest 桥接（复用全局框架 fixtures）
├── pytest.ini                              # 测试执行配置（pythonpath 指向全局框架）
├── screenshots/                            # 产品 UI 截图（供用例设计与脚本选择器编写参考）
│   └── <theme>/                            #   按主题/feature 组织
│       └── <feature>/
├── tests/                                  # 测试执行目录（按轮次组织）
│   └── <round>/                            #   轮次目录
│       ├── test-cases.json                 #     本轮用例清单（机器可读）
│       ├── test-plan.md                    #     A1013 本轮功能测试计划
│       └── test-report.md                  #     A1015 本轮功能测试报告
├── structured-sales-cycle/                 # T-01 营销过程闭环
│   ├── lead-governance/                   #     线索治理（录入/评分/分级/分配）
│   ├── nurture-followup/                  #     培育跟进（跟进记录/策略/提醒）
│   ├── opportunity-pipeline/              #     商机管道（商机创建/推进/关闭）
│   ├── customer-360/                      #     客户360（画像/关联/历史）
│   └── winloss-retrospective/             #     赢单/丢单复盘
├── ai-augmentation/                        # T-02 AI 营销管理
│   ├── lead-intelligence/                 #     AI 线索评分
│   ├── followup-copilot/                  #     AI 跟进建议
│   └── competitive-alerts/                #     竞品预警
├── executive-dashboard/                    # T-03 决策驾驶舱
│   ├── funnel-analytics/                  #     漏斗分析
│   ├── channel-effectiveness/             #     渠道效能
│   └── opportunity-health/                #     商机健康度
└── knowledge-repository/                   # T-04 营销知识库
    ├── knowledge-ingestion/               #     知识录入
    └── knowledge-retrieval/               #     知识检索
```

> - `<round>` 为测试轮次标识：`pr-<number>`（回归）、`nb-<date>`（每夜构建）、`rel-<version>`（发布门禁）
> - 每个 feature 目录下包含：`README.md`（A1011）、`test_<feature>.py`（A1014）、`conftest.py`（feature 级 fixture）、`tcNN/`（用例目录）

> **🚫 禁止创建维度子目录**：`tcNN/` 必须直接放在 feature 根目录下。维度信息仅通过 `data.json` 的 `dimension` 字段标注。

## 测试维度

| 维度 | 说明 |
| :--- | :--- |
| `01_页面元素冒烟` | 页面/组件是否正常渲染 |
| `02_页面交互` | 点击/悬停/切换/分页等交互行为 |
| `03_控件表单` | 输入框/下拉/日期/开关/上传等表单控件 |
| `04_业务流程` | 端到端业务闭环（线索→跟进→商机→成交） |
| `05_权限鉴权` | MKT Leader / Sales / Admin 不同角色权限 |
| `06_异常处理` | 空数据/超时/错误状态/回退 |
| `07_边界条件` | 输入极值/上限/下限/空值 |
| `08_规则回归` | 业务规则一致性/状态机/评分逻辑 |

## 工作规则

- 新增 feature 时按标准 9 节结构生成 `README.md`（A1011 功能测试大纲）
- 每条用例独立目录：`tcNN/tcNN.md` + `tcNN/data.json`
- 测试脚本遵循 Playwright + Pytest 框架，PO 类方法 + v_tcXX 可视化 runner
- CRM 测试重点覆盖营销闭环场景（线索→跟进→商机→成交），需关注跨子系统的数据流转
