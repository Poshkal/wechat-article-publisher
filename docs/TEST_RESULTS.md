# 实际测试记录

日期：2026-10-21。范围：本地离线检查；无线上业务修改、无微信API、无Shopify Admin写入、无下单或付款。

## 已执行

另已执行 skill-creator 随附 quick_validate.py，12/12 返回 Skill is valid（exit 0）；此结果仅为格式验证。

| 检查 | 结果 | 范围及限制 |
|---|---|---|
| 初版 `python3 scripts/validate_skills.py` | PASS，12个 | 旧脚本只检查部分标题/name/秘密正则，不能证明内容可用 |
| 补强后的同名校验命令 | 见本次证据文件 | 12个数量、名称/目录一致、受限frontmatter格式、完整非空章节、脚手架残留、Markdown相对引用 |
| `python3 -m unittest discover -s tests -v` | 见本次证据文件 | 格式破坏、断链、HTML外部图片/注入、伪PASS、秘密/隐私扫描等回归 |
| 原公众号工具真实本地渲染 | PASS | Node 22.22.0，wenyan 2.0.12；合成文章、1张合成图，渲染exit 0，产物检查PASS。原工具最少两文件复制到隔离目录，不复制凭证或历史文章 |
| 原公众号工具缺图负例 | 见本次证据文件 | 用以验证渲染进程成功不等于导入包完整；平台未参与 |
| 历史 `node --test tests/qa.test.js` | PASS，6/6 | 只读盘原测试加载实际页面控制器，API和wx由测试替身替代；不证明真实后端或真机 |
| 历史配件JS `node --check` | PASS，exit 0 | 仅语法；未执行购物车网络请求 |
| 历史促销模板只读核对 | PASS，范围限本地 | 观察到历史集合handle保留和结束态；不能推出远端折扣已关闭 |
| `python3 scripts/scan_public.py` | 见发布前证据 | 仅待公开文件；私有映射、隔离运行产物不在上传范围。启发式扫描加人工审阅，不是零风险保证 |

本次可复核结构化结果保存在 [LOCAL_TEST_EVIDENCE.json](LOCAL_TEST_EVIDENCE.json)。含命令、环境、退出码、范围和源指纹；不公开历史业务输出或原始素材。

## 尚未验证 / 阻塞

- 微信复制/真实粘贴/手机预览、草稿接口和发布：NOT VERIFIED，本次无正式账号操作授权；不依赖模拟结果升级状态。
- 公众号桌面/窄屏视觉检查：NOT VERIFIED；本次仅HTML结构包装验证。
- Shopify实时主题角色、Admin配置、预览交互、追踪事件、配送/支付：NOT VERIFIED；本次只用历史快照，无生产测试授权。
- 其余9个Skill：完成文档审计，未开展专项业务端到端验证。具体见审计表。
- GitHub Actions：本地通过不代表远程CI通过，以真实运行结果为准。

## QA门禁输入格式

`qa_gate.py`只评估声明与证据文件存在性，不验证证据真实性；操作者仍需审阅原始执行输出。每项PASS要求executed、exit_code=0、command、environment和非空证据文件，路径必须在报告目录内。

```json
{
  "scope": "offline controller mock tests",
  "revision": "record-source-sha256-here",
  "checks": [
    {
      "id": "controller-tests",
      "required": true,
      "status": "PASS",
      "executed": true,
      "command": "node --test tests/qa.test.js",
      "environment": "local with API mocks",
      "exit_code": 0,
      "evidence": "LOCAL_TEST_EVIDENCE.json"
    }
  ]
}
```

这是输入格式示例，不是额外执行结果。必需项NOT VERIFIED/BLOCKED会阻止总PASS；确认缺陷NEED FIX优先。
