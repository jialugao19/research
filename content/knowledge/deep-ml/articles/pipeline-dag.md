---
id: article-pipeline-dag
slug: pipeline-dag
title: Pipeline DAG：工程用法与常见坑
concepts:
- pipeline-dag
learning_units:
- pipeline-dag-overview
domain: mlops
level: intermediate
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Pipeline DAG
- DAG scheduler
- mlops
- intermediate
- topological sort
- etl pipeline
- critical path analysis
- resumable processing
profile:
  required_sections:
  - 问题场景
  - 核心机制
  - 实现要点
  - 常见故障
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-pipeline-dag
  covered_concepts: 1
  primary_concept: pipeline-dag
confidence:
  concept: 0.94
  prerequisite: 0.92
  prerequisite_path_eligible: true
generated_version:
  model: curated-catalog-v3
  prompt_version: chapter-profile-v3
review:
  state: automated_editorial
  last_review: null
  reviewer: null
  triggers:
  - routine_auto_check
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: MLflow Documentation
  url: https://mlflow.org/docs/latest/index.html
  type: official_docs
- title: Introduction to Algorithms
  url: https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
  type: textbook
---
# Pipeline DAG：工程用法与常见坑

用有向无环图表示数据或模型流水线任务依赖的结构。

关键词：Pipeline DAG
- DAG scheduler
- mlops
- intermediate
- topological sort
- etl pipeline
- critical path analysis
- resumable processing

## 问题场景

复杂流水线有多个步骤和依赖。DAG 让执行顺序清晰可调度。

## 核心机制

- 输入：Pipeline DAG 所处理的数据、状态或评价对象。
- 操作：节点是任务，边是依赖。DAG 不能有环。
- 观察结果：复杂流水线有多个步骤和依赖。DAG 让执行顺序清晰可调度。

它像一张任务依赖图，前置完成后才能执行后续。

例子：训练流水线可包含抽取、特征、训练、评估和发布节点。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Pipeline DAG 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- DAG 只描述依赖，不自动保证任务正确。

## 相关概念

### 前置
- Topological Sort
- ETL Pipeline

### 关联
- Critical Path Analysis
- Resumable Processing

### 延伸
- Critical Path Analysis
- Resumable Processing

## 延伸阅读

- **MLflow Documentation**：https://mlflow.org/docs/latest/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
