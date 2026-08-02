# Jialu Gao Research

面向同事、同行与研究管理者的静态研究项目主页。网站把项目目标、研究线、
实验快照、量化结果和经过明确筛选的报告组织在一起；源项目、数据与
`0-report-html` 报告归档不会被构建过程修改。

内容分为三层：

- `content/projects.yaml`：项目、研究线和子项目的公开说明；
- `content/studies.yaml`：带证据边界的实验结论与指标快照；
- `content/reports.yaml`：明确批准发布的不可变 HTML 报告清单。

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

Publishing is event-driven. Project directories are never watched or published
automatically. Use the `publish-research-site` Codex skill for audits and report
publication.
