---
intention: 说明研究网站的内容来源、报告发布边界与本地验证方式.
---

# JG Research Lab

面向同事、同行与研究管理者的静态研究项目主页。网站把项目目标、研究线、
实验快照、量化结果和经过明确筛选的报告组织在一起；源项目、数据与
`0-report-html` 报告归档不会被构建过程修改。

内容分为以下几部分：

- `content/research-flow.yaml`：Research 区统一的六环节顺序、名称与公开说明；
- `content/research-taxonomy.yaml`：从 `mindmap-data/research.md` 固化的完整研究分类树；
- `content/projects.yaml`：独立项目、六环节状态、旧专题重定向和 Infrastructure 的公开说明；
- `content/studies.yaml`: 研究问题、当前结论和跨项目的证据关联.
- `content/experiments.yaml`: 方法、模型、数据范围、测量结果、比较合同和报告引用.
- `content/highlights.yaml`：首页指标、精选研究门槛、审计图表和淘汰结论；
- `content/reports.yaml`：明确批准发布的报告清单，兼容历史 HTML 与新版
  Markdown 内容包；
- `content/report-docs/<project>/<report>/`：新版报告的 `report.md` 与本地
  `images/`，构建时统一套用站点文档外壳。
- `content/knowledge/deep-ml/`：经过校验并带逐文件 SHA-256 清单的 DeepML
  发布快照，包含 Concept、Article、Relation、Learning Path 和自动编辑质量记录；
- `content/knowledge/quant-knowledge/`：经过校验并带逐文件 SHA-256 清单的
  Quant Knowledge 章节快照；
- `content/knowledge/ontology.yaml`：统一知识图谱的 Domain、Topic、来源映射和
  research bridge。DeepML 与 Quant Knowledge 是 source metadata，不作为一级导航。

报告文件不会因为出现在工作区或 `0-report-html` 中就被自动发布。

## 报告来源审计

`scripts/audit_projects.py` 只识别归档报告的归属, 不发布或重生成报告.
普通项目从 `content/projects.yaml` 的 `source_refs` 扫描 workspace 内的 HTML.
NN 项目用 `registry_experiments` 明确声明 experiment ID, 再从中央 registry 的
`report-index.yaml` 读取 `path` 与 `repo_mirror_path`. 两种位置分别核验,
允许报告位于实验 repo 或 `/data-cache` 中; 不遍历整个 cache.

本地 registry 入口由 `$RESEARCH_NN_REGISTRY_ROOT` 指定
(默认 `$RESEARCH_WORKSPACE_ROOT/exp-nn/0-select&report`, workspace 默认 home).
迁移 registry 后修改该入口, 并更新登记的现存报告位置. registry 文件缺失会报错;
登记的报告文件可以缺失, `status` 不替代实际文件检查. 默认只匹配不超过 25 MiB
的 HTML/MHTML 来源文件.

报告通过文件 SHA-256 匹配. 已批准的 `reports.yaml` 归属优先; 同一 hash 命中多个
项目时不会自动选项目. NN evidence 使用 `nn-registry/<experiment-id>/<report-id>`,
不包含本机 artifact 路径. 已发布报告仍由 `reports.yaml` 与独立报告归档决定,
网站构建不需要访问 registry、实验 checkout 或训练产物.

```bash
python3 -m pip install -e '.[test]'
python3 scripts/validate_catalog.py
python3 scripts/sync_knowledge.py \
  --deepml-source /home/maomao/deep-ml/content \
  --quant-source /home/maomao/knowledge
python3 scripts/build_site.py --base-url / --output _preview
python3 scripts/validate_site.py --base-url / --output _preview
python3 -m http.server 8888 --bind 127.0.0.1 --directory _preview
```

在容器环境中，把容器的 `8888` 端口转发到宿主机，再访问
`http://localhost:8888/`。本地预览使用根路径 `/`；部署流程使用
`/research/` 构建 `_site`，以匹配未来 GitHub Pages 的项目仓库路径。

要让预览脱离开发容器常驻运行，先按上面的命令构建并验证 `_preview`，然后在
宿主机的项目目录启动独立 Nginx 服务：

```bash
docker compose up -d
docker compose ps
```

服务通过 `http://x99.local:8088/` 提供，健康检查地址为
`http://x99.local:8088/healthz`。Nginx 只读挂载项目目录且只提供其中的
`_preview`。构建器先在同级 staging 目录完成全量渲染和校验，再原子替换 `_preview`；
构建失败时 Nginx 继续提供上一份成功结果，不需要重启。其 `restart: unless-stopped`
策略使服务不依赖开发容器或当前终端。查看日志
和停止服务分别使用：

```bash
docker compose logs -f web
docker compose down
```

研究问题、实验关联及共享视觉的维护规则见 [研究组织说明](docs/research-organization.md).

主要页面结构为：

```text
/
├── projects/<project>/
│   ├── <research-stage>/
│   └── <legacy-topic>/  # 重定向到阶段页中的 taxonomy 锚点
├── studies/<study>/
├── experiments/<experiment>/
├── knowledge/
│   ├── <domain>/
│   └── <domain>/<topic>/<node>/
└── reports/<project>/<report>/
```

Knowledge 是独立顶层板块，不计入研究项目与实验数量。界面导航使用英文，文章
正文保留中文；展示公式在构建时转为静态 MathML。站点构建只读取仓内快照，
不会在 CI 或 GitHub Pages 环境依赖相邻的 `deep-ml` 或 `knowledge` 工作区。
公开 URL 只使用 ontology 路径；来源项目保留在节点 metadata 中。更新知识库时先在
DeepML / Quant Knowledge 源项目完成校验，再显式执行 `sync_knowledge.py`；同步器
只接受全部 DeepML 文章已发布且编辑阻塞队列为空的内容包，并校验 Quant Knowledge
章节清单与哈希。

更新项目说明或实验结果时，先修改 YAML 并保留指标的口径、样本和限制，
然后重新运行目录校验、测试、构建和站点校验。只有需要公开新报告时才运行
报告发布脚本；不要把源项目目录、训练产物或整个报告归档复制进本站。

## Research 逻辑链

Research 区以独立项目为入口，每个项目固定按以下顺序组织公开研究事实：

```text
Data → Data Engineering → Feature Engineering → Model
     → Prediction Evaluation → Strategy
```

每个项目必须为六个环节声明 `documented`、`in-progress`、`gap` 或
`not-applicable` 状态。每个阶段页按统一 taxonomy 完整显示所有标题，Study 表达研究问题, Experiment 通过一个
主要 `taxonomy_path` 稀疏挂载；没有实验的节点只显示标题。跨主题关系使用可选的
`related_taxonomy_paths`，不会复制实验。报告同时保留在按时间排列的 Publications
总索引中。Prediction-NN 的 1min 与 1s 合同是两个独立项目，旧项目和专题入口提供
重定向，既有 `/reports/prediction-nn/...` URL 保持不变。
Snapshot Visualizer、Factor Research Platform 和 IP Check 属于独立的 Research
Infrastructure，不强行映射到六环节。

## 新版 Markdown 报告

从 `content/report-docs/_template/report.md` 复制固定骨架。正文不写一级标题，
二级标题必须依次为：`摘要`、`研究背景与目标`、`数据与方法`、`主要结果`、
`限制与适用边界`、`结论`；需要时可在末尾增加 `附录`。三级标题用于扩展
“主要结果”和“附录”，不要嵌入原始 HTML。

每份报告至少包含一张图片或一张 Markdown 表格. 图片只能放在同一报告目录的
`images/` 下, 并使用有意义的替代文本:

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

首页精选研究由 `content/reports.yaml` 顶层的 `featured_report` 手工指定，
必须引用当前修订链中的公开报告；`content/highlights.yaml` 只能引用目录中已登记的
experiment、metric 和该精选报告。首页图表数据必须来自公开报告中的明确数值，并在
`source_note` 中标注口径；不会根据日期或报告 front matter 自动选择或推断指标。

项目需要分别登记六环节状态；Research 实验使用完整 `taxonomy_path` 归入主要研究
问题，stage 从路径首段派生。Infrastructure 实验不声明 taxonomy。
实验快照中的指标以紧凑文本呈现，不再为少量重复指标生成
摘要图。首页可把正式报告中已经公开、口径明确的少量数值重绘为统一的内联 SVG，
但正式图形证据仍须在研究报告中保留完整口径、图注和上下文。

发布由用户请求触发, 不自动监控或发布项目目录. 使用 `$publish-research-site 同步这份报告`
或 `$publish-research-site 同步刚才的结论`. Skill 将内容整理为 Markdown 报告并关联
Study 和 Experiment, 对照源内容检查全部图片和表格, 在独立预览通过浏览器验收后更新本机网站,
并创建远端 PR 供审查. 同步不自动合并 PR; 本机网站访问与远端审查状态分别报告.

## 共享视觉和报告字节

页面继承 x99.local 的 Docusaurus 文档站风格. `assets/styles/` 保存 tokens、shared shell
和 Research 扩展, 构建器统一生成 `assets/site.css`; Markdown 报告内联同一份样式.
新增页面不重复定义全局视觉变量. legacy HTML 的公开 hash 记录在 `published_sha256`,
既有报告内容和永久 URL 保留.
