# Skills审计与验收

日期：2026-10-21。对象：原有12个Skill，无新增Skill、无重命名。每项均实际读取初版和修订版。

## 初版发现

- 命名：12项均为小写连字符，frontmatter name与目录一致，未发现重复名称。
- 格式：初版全部通过旧校验器，但触发条件同一句泛化模板，具体操作压在单一长步骤，缺独立工具权限、失败恢复和可执行验收条件。
- 边界：Shopify审计/CRO/发布，增长/自动化，客服/KOL以及公众号/内容拆解存在相邻范围；修订后分别说明只读、实施、发布或草稿范围。
- 来源：交接叙述不等于当前验证；无法核实的AppTask、客服/KOL业绩不作为已证案例。没有依据时保留NOT VERIFIED。

## 逐Skill验收

“结构与内容PASS”指名称、格式、触发、步骤、权限、失败、输出、验收均通过本次审阅与结构校验；不代表工具自动发现、生产或业务效果通过。

| Skill | 结构与内容 | 本次行为验证 | 整体业务验收 |
|---|---|---|---|
| wechat-article-publisher | PASS | 本地真实渲染及包装PASS；缺图负例被门禁拒绝 | BLOCKED：微信导入/视觉/手机预览/发布未验证 |
| codex-qa-gatekeeper | PASS | 6项历史控制器mock测试及证据门禁回归PASS | PASS，限定离线范围；平台/真机NOT VERIFIED |
| shopify-store-auditor | PASS | JS语法与本地快照只读审计PASS | BLOCKED：当前主题、Admin、预览交互/支付未验证 |
| shopify-safe-deployment | PASS | 历史角色/认证阻塞方法证据已读 | NOT VERIFIED：未上传或发布主题 |
| shopify-cro-optimizer | PASS | 历史矩阵、促销清理边界已读 | NOT VERIFIED：无当前转化实验 |
| ecommerce-growth-diagnostician | PASS | 内容索引可读，未采信营销数字 | NOT VERIFIED：无授权经营数据测算 |
| ecommerce-automation-architect | PASS | 同意未持久化的历史阻塞已读 | NOT VERIFIED：未连接/启用自动化 |
| customer-support-copilot | PASS | 无可公开专项案例 | NOT VERIFIED：未查询订单或发送回复 |
| kol-collaboration-manager | PASS | 无可公开专项案例 | NOT VERIFIED：未外联/签约/寄样 |
| ai-product-launch-playbook | PASS | 开发任务、根因与历史QA证据已读 | NOT VERIFIED：未完成新产品试点 |
| content-repurposing-studio | PASS | 真实内容索引方法已读 | NOT VERIFIED：未做素材级拆条 |
| business-document-builder | PASS | 无可公开专项案例 | NOT VERIFIED：未渲染业务文档 |

## 新增内容

三个优先Skill补充缺图阻断、同名素材、API不明回执、证据层级、原文/事实/状态分离、当前主题角色、多视口、配件状态矩阵、促销本地/远程差异和追踪归属。其余9项分别补充数据口径、同意幂等、权益/支付恢复、引用映射、授权台账及可观察交付标准。

历史案例的公开版本仅含去除账号/数据的摘要和来源指纹，见 [来源说明](EXPERIENCE_PROVENANCE.md)。未复制历史代码或业务日志到仓库。

## 后续修复/验证

1. 在授权测试账号完成微信粘贴与手机预览；外部原公众号工具的缺图仅告警/同名图碰撞/回查忽略问题未修改，使用前受本库门禁约束。
2. 在明确授权的非LIVE预览主题补Shopify当前角色、视觉/购物车/事件级追踪证据；支付另行限定环境。
3. 为其余9项各积累一个获授权、脱敏且有实际产物的案例，逐步替代仅文档审计状态。
4. 启发式敏感扫描无法识别所有语义商业秘密；新增案例仍需人工审阅，原始业务数据继续留在本地。
