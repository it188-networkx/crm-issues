# CRM 功能 UAT 测试总纲

> 依据 [ops-playbook#1735]（CRM 功能测试与原型一致性验证）建立。

| 属性 | 内容 |
| :--- | :--- |
| 测试依据 | ① 原型（页面/交互） ② 需求/设计文档（字段/规则/口径） ③ AI/Prompt 文档 |
| 验收原则 | 不以线上现有实现为标准；原型与需求冲突时以最新需求/设计结论为准 |
| Last Updated | 2026-08-24 |

## 模块与测试资产对照

| # | 模块 | 需求文档 | 原型页面 | 测试目录 | 状态 |
|---|------|---------|---------|---------|------|
| 1 | 商机 | `field-specs/04-商机.md` + `06-商机跟进功能审核.md` + `requirements/structured-sales-cycle/` | `13-opportunities` / `14-opp-detail` / modals 03/05/06/07 | `opportunity/` | ✅ 已建 |
| 2 | 跟进记录 | `field-specs/01-跟进记录.md` + `05-待办任务.md` + `06-商机跟进功能审核.md` | `04-followups` / `05-followup-detail` / `06-followup-create` | `followup/` | ✅ 已建 |
| 3 | 客户/联系人 | `field-specs/03-客户基础信息.md` + `02-联系人.md` | `09-accounts` / `10-account-detail` / `11-contact-create` / `12-contact-detail` | `account-contact/` | ✅ 已建 |
| 4 | 待办任务 | `field-specs/05-待办任务.md` | `03-todos` | `todo/` | ✅ 已建 |
| 5 | 决策看板/销售周报 | `requirements/executive-dashboard/weekly-report/*` + `field-specs/07-决策驾驶舱.md` | `26-decision-board` / `27-weekly-report-list` | `executive-dashboard/weekly-report/` | ✅ 已有（46 用例，覆盖 8 指标卡/分析区块/下钻/统计口径/状态机/权限） |
| 6 | 全局字段/权限 | `crm-field-mapping-full.md` + `CRM角色权限矩阵.md` + `full-system-menu-design.md` | 全局（角色切换器/菜单/字段） | `global-field-permission/` | ✅ 已建 |

## 执行约定

- 登录：统一 EMS 入口 `http://test.it188.com`，账号体系邮箱+密码+验证码（开发环境验证码 `1234`）
- 测试账号见 `test-accounts`（见用户记忆 `crm-test-accounts.md`）
- 各模块 conftest 需设置 `POST_LOGIN_URL` 直达模块页面
- 执行命令示例：
  ```bash
  cd crm-issues/function && pytest opportunity/test_opportunity.py -v --tb=short --env=dev
  ```

## 问题记录要求（发现缺陷时）

记录：问题模块 / 问题功能 / 实际表现 / 预期表现 / 复现步骤 / 原型对应页面位置 / 关联需求文档章节 / 截图 / 严重程度。

## ⚠️ 提测时待核对项（原型未完整实现，需按线上实际对齐）

| # | 待核对项 | 现状 | 处理方式 |
|---|---------|------|---------|
| 1 | 商机「搁置/唤醒」操作 | issue 写「搁置/唤醒」，需求文档术语为「退回待重启 / 重新激活」，原型仅有「退回原因」字段、无独立搁置按钮 | 已按需求术语实现 tc19~21；若线上有独立「搁置」按钮需补用例 |

> 待办「协作跟进及共享对象」已找到完整原型实现：待办页「协作商机任务」卡（只读）+ 新建任务弹窗「任务类型=共享待办 → 关联对象级联（商机/客户）」，已覆盖（todo tc13/14/16/17、followup tc16）。
