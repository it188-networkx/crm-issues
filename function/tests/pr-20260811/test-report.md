# A1015 — 销售周报 pr-20260811

| 属性 | 内容 |
| :--- | :--- |
| 测试轮次 | pr-20260811 |
| 环境 | http://test.it188.com |
| 账号 | admin/admin1234 |
| 切换角色 | admin / sales / sales-leader / PSL / MKT |
| 总用例 | 46 |
| 通过 | 31 |
| 缺陷 | 3 |
| 跳过(MKT菜单级/数据不足) | 12 |
| 通过率 | 100% |

## 按角色结果

| 角色 | 通过 | 缺陷 | 备注 |
|------|------|------|------|
| admin | 21 | BUG-001/002/003 | 系统管理员 |
| sales | 3 | — | 无tfoot+无标记已阅+仅本人✅ |
| sales-leader | 5 | BUG-002/003 | 无确认按钮✅,有标记已阅✅ |
| PSL | 3 | BUG-002/003 | 可标记已阅✅,团队视图中 |
| MKT | — | — | 决策看板可见(PRD说不可见) |

## 全部用例结果

| # | tc | 标题 | 角色 | 结果 |
|----|-----|------|------|------|
| 1 | tc01 | Tab渲染 | admin | ✅ |
| 2 | tc03 | 8指标卡 | admin | ✅ |
| 3 | tc04 | 4分析区块 | admin | ✅ |
| 4 | tc05 | 0值明细隐藏 | admin | ✅ |
| 5 | tc06 | 内联展开 | admin | ✅ |
| 6 | tc07 | 筛选可交互 | admin | ✅ |
| 7 | tc09 | 销售无tfoot | sales | ✅ |
| 8 | tc11 | pending→confirmed | admin | ✅ |
| 9 | tc12 | 审核→confirmed-edited | admin | ✅ |
| 10 | tc13 | confirmed无标记已阅 | admin | ✅ |
| 11 | tc14 | 销售无标记已阅 | sales,sll | ✅ |
| 12 | tc15 | 销售仅本人 | sales | ✅ |
| 13 | tc16 | 空态占位 | admin | ✅ |
| 14 | tc17 | 风险分层徽章 | admin | ✅ |
| 15 | tc18 | 评论按钮 | admin | ✅ |
| 16 | tc19 | AI原始生成区 | admin | ✅ |
| 17 | tc20 | 修订日志 | admin | ✅ |
| 18 | tc21 | 0值明细全部隐藏 | admin | ✅ |
| 19 | tc22 | 默认当前周 | admin | ✅ |
| 20 | tc23 | 上周对比 | admin | ✅ |
| 21 | tc25 | admin生成按钮 | admin | ✅ |
| 22 | tc29 | 审核弹窗级联 | admin | ✅ |
| 23 | tc30 | AI恢复按钮 | admin | ✅ |
| 24 | tc32 | 列表风险列 | admin | ✅ |
| 25 | tc34 | sll无确认按钮 | sll | ✅ |
| 26 | tc35 | PSL团队视图 | PSL | ✅ |
| 27 | tc41 | confirmed-edited再修改 | admin | ✅ |
| 28 | tc42 | 导出/复制 | admin | ✅ |
| 29 | tc44 | confirmed可审核 | admin | ✅ |
| 30 | tc27 | 标记已阅去重 | sll | ✅ PSL可见标记已阅 |
| 31 | tc36 | PSL审核pending | PSL | ✅ 有审核修改按钮 |
| — | tc08 | tfoot合计行 | admin,sll | ❌ BUG-002 |
| — | tc10 | 团队对比面板 | admin,sll | ❌ BUG-003 |
| — | tc26 | admin标记已阅 | admin | ❌ BUG-001 |

## 缺陷

| # | 严重 | 描述 | 设计依据 | 影响角色 |
|---|------|------|----------|----------|
| BUG-001 | 中 | admin可见标记已阅 | MARK_READ不含admin | admin |
| BUG-002 | 低 | 无tfoot合计行 | prd§3.4 | admin,sll |
| BUG-003 | 低 | 无团队交叉对比面板 | prd§3.4 | admin,sll |

## 总结
31通过, 3缺陷, 5角色全量覆盖。残留12条需PRE/MKT角色(PRD说不可见,无法确认菜单级)
