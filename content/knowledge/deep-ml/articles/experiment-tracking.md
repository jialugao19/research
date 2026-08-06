---
id: article-experiment-tracking
slug: experiment-tracking
title: Experiment Tracking：工程用法与常见坑
concepts:
- experiment-tracking
learning_units:
- experiment-tracking-overview
domain: mlops
level: beginner
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Experiment Tracking
- tracking
- mlops
- beginner
- train validation test split
- model evaluation metrics
- model serving
- data drift
profile:
  required_sections:
  - 问题场景
  - 核心机制
  - 实现要点
  - 常见故障
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-experiment-tracking
  covered_concepts: 1
  primary_concept: experiment-tracking
confidence:
  concept: 0.94
  prerequisite: 0.94
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
---
# Experiment Tracking：工程用法与常见坑

记录实验配置、代码版本、指标和产物的工程流程。

关键词：Experiment Tracking
- tracking
- mlops
- beginner
- train validation test split
- model evaluation metrics
- model serving
- data drift

## 问题场景

实验多了以后，很难知道哪个结果来自哪次运行。实验追踪让结果可复现。

## 核心机制

- 输入：Experiment Tracking 所处理的数据、状态或评价对象。
- 操作：关键记录包括数据版本、代码版本、参数、随机种子、指标和模型文件。
- 观察结果：实验多了以后，很难知道哪个结果来自哪次运行。实验追踪让结果可复现。

它像实验室记录本。每次实验都要留下条件、结果和样本。

例子：比较两个学习率时，追踪系统能显示每次运行的曲线和最终指标。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Experiment Tracking 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- 只保存最好模型不够。没有配置和环境，结果很难复现。

## 相关概念

### 前置
- Train Validation Test Split
- Model Evaluation Metrics

### 关联
- Model Serving
- Data Drift

### 延伸
- Model Serving
- Data Drift

## 延伸阅读

- **MLflow Documentation**：https://mlflow.org/docs/latest/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
