# Jialu Gao Research

面向同事、同行与研究管理者的静态研究项目主页。网站把项目目标、研究线、
实验快照、量化结果和经过明确筛选的报告组织在一起；源项目、数据与
`0-report-html` 报告归档不会被构建过程修改。

内容分为以下几部分：

- `content/projects.yaml`：项目、研究线和子项目的公开说明；
- `content/studies.yaml`：带研究背景、方法、证据边界和指标快照的实验结论；
- `content/reports.yaml`：明确批准发布的报告清单，兼容历史 HTML 与新版
  Markdown 内容包；
- `content/report-docs/<project>/<report>/`：新版报告的 `report.md` 与本地
  `images/`，构建时统一套用站点文档外壳。

报告文件不会因为出现在工作区或 `0-report-html` 中就被自动发布。

```bash
python3 -m pip install -e '.[test]'
python3 scripts/validate_catalog.py
python3 scripts/build_site.py --base-url / --output _preview
python3 scripts/validate_site.py --base-url / --output _preview
python3 -m http.server 8888 --bind 0.0.0.0 --directory _preview
```

在容器环境中，把容器的 `8888` 端口转发到宿主机，再访问
`http://localhost:8888/`。本地预览使用根路径 `/`；部署流程使用
`/research/` 构建 `_site`，以匹配未来 GitHub Pages 的项目仓库路径。

主要页面结构为：

```text
/
├── projects/<project>/
│   ├── <track>/
│   └── topics/<subproject>/
└── reports/<project>/<report>/
```

更新项目说明或实验结果时，先修改 YAML 并保留指标的口径、样本和限制，
然后重新运行目录校验、测试、构建和站点校验。只有需要公开新报告时才运行
报告发布脚本；不要把源项目目录、训练产物或整个报告归档复制进本站。

## 新版 Markdown 报告

从 `content/report-docs/_template/report.md` 复制固定骨架。正文不写一级标题，
二级标题必须依次为：`摘要`、`研究背景与目标`、`数据与方法`、`主要结果`、
`限制与适用边界`、`结论`；需要时可在末尾增加 `附录`。三级标题用于扩展
“主要结果”和“附录”，不要嵌入原始 HTML。

图片只能放在同一报告目录的 `images/` 下，并使用有意义的替代文本：

```markdown
![验证集 IC 变化](images/validation-ic.png "验证集 IC 变化")
```

构建器会把图片内联进最终 HTML，按正文宽度单列排列，自动编号并使用标题或
替代文本作为图注；表格也会按文档顺序自动编号。报告元数据、正文、表格和
所有被引用图片共同形成 `bundle_sha256`。内容变化必须新建报告 id，并用
`revision_of` 指向上一版；共享模板、导航和 CSS 可以独立改进，不改变内容包
哈希。

`content/reports.yaml` 中的 Markdown 记录使用 `format: markdown`、
`content_file` 和 `bundle_sha256`；首页精选报告可以额外声明 `hero_image`，
但只能指向该报告正文已经引用的 `images/` 资源。历史 HTML 记录继续使用
`source_file` 与 `source_sha256`，其公开字节和原有 URL 均保持不变。目录页
默认只展示每条修订链的最新版，旧 URL 仍可直接访问。

研究线需要分别登记展开后的目标、数据结构和当前结论；实验专题使用 `group`
按研究问题组织。实验快照中的指标以紧凑文本呈现，不再为少量重复指标生成
摘要图；需要图形证据时，应在正式研究报告中提供完整的口径、图注和上下文。

Publishing is event-driven. Project directories are never watched or published
automatically. Use the `publish-research-site` Codex skill for audits and report
publication.
