---
intention: 明确研究问题、实验和报告的登记边界, 保持 Research 页面、样式与证据长期一致.
---

# 研究问题与证据的组织

## 1. 一个实体只登记一次

Project 定义研究目标与责任范围. Research Project 组织预测研究的六阶段链路;
Infrastructure Project 展示系统目标、运行证据和报告, 不强制声明预测阶段.
Knowledge 继续使用独立 ontology 和经过 hash 校验的源快照.

Study 表示研究问题与当前结论. Experiment 表示具体方法、数据范围、状态、测量值和限制.
Report 是完整的公开证据. Experiment 可以是单次运行, 也可以是一组具有明确比较合同的实验臂.
同一组的 arm 仅保存其测量结果, 不重复登记 Project、Study 或 Report.

```text
Project ←→ Study ←→ Experiment ←→ Report
                 └────────────→ Report
```

- `content/projects.yaml` 保存项目身份和六阶段状态.
- `content/studies.yaml` 保存问题、结论及 `project_ids`、`experiment_ids`、`report_ids`.
- `content/experiments.yaml` 保存实验事实、方法属性、结果和证据引用.
- `content/reports.yaml` 保存公开报告清单、内容校验值和修订链.

Study 的多个项目、实验和报告都通过 ID 引用. Experiment 与 Report 各保留一个 `project`
作为 canonical home, 可以用 `related_project_ids` 关联其他项目. canonical home 与既有
`route_project` 一起确定稳定 URL, 增加关联不改变 URL.
一份报告可以关联多个 Experiment 或 Study. 反向链接由 Catalog 派生, 不另存重复清单.
`registry_experiments` 仍只声明来源审计的主要归属, 不代替公开研究实体之间的关联.

加载时验证 ID 唯一性、引用完整性、所属项目、问题分类和孤立实验.
关系入口位于 `research_site/catalog.py` 的 `load_studies` 及 Catalog 查询方法.

## 2. 从研究问题进入结果

预测研究保留 Data → Data Engineering → Feature Engineering → Model →
Prediction Evaluation → Strategy 的顺序和历史 taxonomy anchors.
Study 的标题和 question 表达问题; model、experiment_type、method、dataset
属于 Experiment 属性, 不为每个具体配置复制一份研究问题.

Project 页面展示目标、阶段、当前判断、问题入口和实验表.
`/studies/` 与 `/studies/<id>/` 展示问题和证据比较;
`/experiments/` 与 `/experiments/<id>/` 提供实验筛选、结果、限制、实验臂和报告入口.
原实验 ID 保留, 旧阶段页中的 `#study-<experiment-id>` anchors 也保留.

筛选可组合 question、experiment type、model、status 和文本查询, 查询状态写入 URL.
`not-recorded` 表示源材料没有登记模型, 不根据指标或项目名猜测.
同一实验只出现在表中一次, 相关研究问题和报告由链接复用.

表格保留 metric context、dataset 和 caveats. 不把不同 label、split、universe、budget
或 checkpoint policy 的数字直接排序. `arms` 必须声明 `comparison_scope`;
failed-before-test 和 gated 臂保留记录, 不允许填入 OOS 比较指标.
页面构建与共享表格分别位于 `research_site/build_entities.py` 和
`templates/_research_records.html`.

## 3. 图表与原报告保持可追溯

Experiment 的 `figures` 只能引用其 `report_ids` 中已批准的报告.
Markdown 图片通过 `asset: images/...` 指向内容包内已引用的文件;
legacy HTML 通过零起始 `image_index` 引用原报告中内嵌的 raster image.
图题必须与源证据一致. 不在构建时扫描训练产物或生成新的实验指标.

构建过程保留原始图片字节, 按内容 SHA256 命名, 另生成不超过 480、960、1440px
的 lossless WebP 版本. 页面通过 srcset、sizes、width、height、lazy loading 和
async decoding 加载图片. 点击进入原图 lightbox, 无 JavaScript 时仍可直接访问原图.
每张图都有源报告入口, provenance 写入 `research-images.json`.

图片位于输出目录的 `assets/research-images/`. Nginx 对该 hash 路径设置一年 immutable
cache; GitHub Pages 的 cache header 由托管服务管理. 修改样式不修改源图或报告内容包.
图片构建入口为 `research_site/research_assets.py`.

## 4. 继承 x99 的视觉契约

视觉参考是 x99.local 的 Docusaurus 文档站风格. 仓内 `93c2501` 保存首次继承记录,
作为可复查的代码基线. 本轮环境无法访问 x99.local:80, 因此不声称完成了对在线源站的像素比对.

当前共享设计源码只有三层:

- `assets/styles/tokens.css`: 继承的白底、绿色、system fonts、导航和正文布局参数.
- `assets/styles/shell.css`: 继承的共享 shell、正文和已有组件样式.
- `assets/styles/research.css`: 新研究功能的表格、筛选器、图片和 taxonomy 导航.

`research_site/styles.py` 统一编译为输出的 `assets/site.css`. Markdown 报告内联同一份编译结果.
共享 Header 来自 `templates/_shell.html`, Sidebar 来自 `templates/_navigation.html`.
新增页面引用这些组件, 不复制 header 或重新定义全局 token.

审计识别并移除了后加的 Research 全局字号覆盖、`!important` 标题压平和额外流式 shell
覆盖. 例如二级标题由漂移后的 16px 恢复到继承样式对应的 24px; sidebar、TOC、正文宽度
和绿色品牌标记恢复继承值. 新表格使用同一套颜色与字体, 只增加功能所需的布局规则.
Knowledge 的内容、公式与 ontology 保持原样.

legacy HTML 保留历史公开字节, 不重新套 shared shell. Catalog 登记 `published_sha256`,
构建前验证公开副本, 构建后再核对输出与副本一致. 原始归档的 `source_sha256`
与公开副本的 hash 分别校验. 已发布内容变化需要新 ID 和 revision_of.

## 5. 验证与维护

修改数据后运行 Catalog 校验; 修改模板或样式后运行 tests、生产 base build 和站点校验:

```bash
python scripts/validate_catalog.py
python -m pytest
python scripts/build_site.py --base-url /research/ --output _site
python scripts/validate_site.py --base-url /research/ --output _site
```

本地预览使用 `/` 构建 `_preview`. 构建器先在 staging 渲染并校验, 再替换目标目录.
失败构建不覆盖原站点. 构建只复制 reports 清单批准的 legacy 文件.

`tests/test_research.py` 覆盖关系完整性、多对多查询、失败实验臂、图表 provenance、
响应式资源、原始字节和完整实体路由. 现有 Knowledge、Publications、报告内容包与
atomic build tests 继续运行.

真实页面检查使用已安装 Playwright 的 Python 环境执行 `tests/browser_research.py`.
需要设置 `RESEARCH_PREVIEW_URL` 和 `RESEARCH_CHROMIUM`. 它检查桌面和手机上的
Research、Project、Stage、Study、Experiment、Infrastructure、Knowledge、Publications
和 Markdown report, 并实际操作组合筛选、重置、mobile navigation 和原图 lightbox.
截图与结果只写入被 Git 忽略的 `build-audit/browser/`.
