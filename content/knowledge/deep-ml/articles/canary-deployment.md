---
id: article-canary-deployment
slug: canary-deployment
title: Canary Deployment：工程用法与常见坑
concepts:
- canary-deployment
learning_units:
- canary-deployment-overview
domain: mlops
level: intermediate
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Canary Deployment
- health rollout
- mlops
- intermediate
- model monitoring
- model serving
- experiment tracking
- engineering
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
  id: article-plan-canary-deployment
  covered_concepts: 1
  primary_concept: canary-deployment
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
- title: PostgreSQL Documentation
  url: https://www.postgresql.org/docs/current/
  type: official_docs
---
# Canary Deployment：工程用法与常见坑

先向少量流量发布新版本，再逐步扩大范围的部署策略。

关键词：Canary Deployment
- health rollout
- mlops
- intermediate
- model monitoring
- model serving
- experiment tracking
- engineering

## 问题场景

模型新版本可能有隐藏风险。金丝雀发布降低一次性全量切换的影响。

## 核心机制

- 输入：Canary Deployment 所处理的数据、状态或评价对象。
- 操作：需要监控关键指标，并设置回滚条件。
- 观察结果：模型新版本可能有隐藏风险。金丝雀发布降低一次性全量切换的影响。

它像先让一小部分用户试用，再决定是否推广。

例子：新排序模型先接 5% 流量，观察点击率和错误率。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Canary Deployment 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- 灰度发布不是免审查。指标设计不当仍会漏掉问题。

## 相关概念

### 前置
- Model Monitoring
- Model Serving

### 关联
- Experiment Tracking

### 延伸
- Experiment Tracking

## 延伸阅读

- **MLflow Documentation**：https://mlflow.org/docs/latest/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PostgreSQL Documentation**：https://www.postgresql.org/docs/current/。用途：作为交叉核对材料，确认术语、公式和使用场景。
