# Changelog

## 2026-08-06

- 全量文章改用按内容类型与深度固定的章节结构，并设置 700–1400、1500–2500、3000–5000 字符发布区间。
- 展示公式只保留可由 latex2mathml 解析的纯 TeX；其它表达改为明确标注的结构化文本。
- 发布状态改为 automated_editorial，人工审批保留为可选覆盖，不再作为发布阻塞条件。
- 质量记录改为可解释的结构、完整性、引用、原创性与公式有效性检查，移除自动推断的事实准确率。
- 低于 0.90 的先修边标记为 supplemental，不进入正式学习路径。

- 基于 Datawhale Deep Learning Notes 的目录缺口审计，新增断点续训、梯度检查、AdamW、Muon、InstanceNorm、GroupNorm 与 FlashAttention 专题；正文保持原创归纳并附 CC BY-NC 来源和原始论文。

- 对照 Datawhale Deep Learning Notes 补强 16 个既有概念的定义与教学直觉，重点澄清计算图、分类损失、归一化、Attention、KV cache 和生成模型边界。

- 将 Deep Learning Engineer 主路径重排为 9 个连续 Part，明确从可微计算到训练、架构、生成模型和系统扩展的学习顺序。

## 2026-08-03

- 引入 Article Plan 层，支持一篇文章覆盖多个 Concept 和 Learning Unit。
- 将文章生成升级为 content_type + depth_level 驱动的信息架构，避免固定模板句和固定栏目漂移。
- 增加标准定义、关键词、数学定义、变量解释、推导、算法 Input/Output/Steps、假设限制和实现清单。
- 生成 article_concept_coverage、article_depth_level、article_content_type 等 manifest 指标。
- 为聚合概念补充 part_of 关系，并使用随层级变化的先修置信度。

- 生成 Review Queue，集中收集需要额外判断的条目。
- 生成课程模块文件，把大型课程阶段拆成最多 8 个 required Learning Unit 的学习块。

- 生成增量发布计划，用文章 hash 和知识图谱 hash 支持全量扫描后只发布变化文章。

- 增加持久人工审批文件和 CLI，作为可选的编辑覆盖记录。

## 2026-08-02

- 构建首批可发布中文知识库内容。
- 生成 Knowledge IR、Concept、Learning Unit、Relation、Course Path、Article、Quality 和 Manifest。
- 保持 Deep-ML 来源隔离，不保存题目、题干、题目 ID、题目链接或源题映射。
