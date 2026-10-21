# 公众号文章制作和手动发布

独立 Codex Skill：`wechat-article-publisher`。本仓库只包含一个Skill；相关文档中的12项状态是原库审计背景，不代表本仓库包含12项。

## 使用

读取 [SKILL.md](SKILL.md)，或将完整仓库目录按当前Codex环境的安装约定安装为同名Skill。保留references、scripts与docs。所有脚本命令从本仓库根目录执行。

```bash
python3 scripts/validate_skills.py
python3 -m unittest discover -s tests -v
python3 scripts/scan_public.py
```

需要Python 3.9+；校验不需要凭证或生产访问。公众号渲染器等业务工具是外部依赖，不随此库打包。工具缺失时按Skill报告BLOCKED。

## 验证边界

本仓库结构和辅助脚本测试见实际执行输出；历史原库测试范围见 [测试记录](docs/TEST_RESULTS.md)，专项状态见 [审计报告](docs/SKILL_AUDIT.md)。格式PASS不等于平台端到端或业务效果PASS。原始业务资料、凭证与客户数据不随库发布。

历史来源为 [脱敏说明](docs/EXPERIENCE_PROVENANCE.md) 与 [指纹索引](docs/evidence-index.json)。生产写入、发送、发布与迁移均需明确授权。
