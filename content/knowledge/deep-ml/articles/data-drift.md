---
id: article-data-drift
slug: data-drift
title: Data Drift：工程用法与常见坑
concepts:
- data-drift
learning_units:
- data-drift-overview
domain: mlops
level: intermediate
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Data Drift
- distribution drift
- mlops
- intermediate
- probability
- model evaluation metrics
- model serving
- experiment tracking
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
  id: article-plan-data-drift
  covered_concepts: 1
  primary_concept: data-drift
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: MLflow Documentation
  url: https://mlflow.org/docs/latest/index.html
  type: official_docs
---
# Data Drift：工程用法与常见坑

模型服务时输入数据分布相对训练时期发生变化的现象。

关键词：Data Drift
- distribution drift
- mlops
- intermediate
- probability
- model evaluation metrics
- model serving
- experiment tracking

## 问题场景

模型假设未来数据和训练数据相似。分布变化会让这个假设变弱。

## 核心机制

- 输入：Data Drift 所处理的数据、状态或评价对象。
- 操作：漂移可以发生在特征分布、标签关系或业务流程中。监控要结合统计和业务解释。
- 观察结果：模型假设未来数据和训练数据相似。分布变化会让这个假设变弱。

它像考试题型变了。学生原来学得很好，也可能突然失分。

例子：节假日用户行为变化，可能让平日训练的推荐模型效果下降。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Data Drift 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- 指标下降不一定都是漂移。也可能是服务故障、数据缺失或标签延迟。

## 相关概念

### 前置
- Probability
- Model Evaluation Metrics

### 关联
- Model Serving
- Experiment Tracking

### 延伸
- Model Serving
- Experiment Tracking

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **MLflow Documentation**：https://mlflow.org/docs/latest/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
