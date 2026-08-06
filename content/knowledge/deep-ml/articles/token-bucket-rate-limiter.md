---
id: article-token-bucket-rate-limiter
slug: token-bucket-rate-limiter
title: Token Bucket Rate Limiter：工程用法与常见坑
concepts:
- token-bucket-rate-limiter
learning_units:
- token-bucket-rate-limiter-overview
domain: software_engineering
level: intermediate
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Token Bucket Rate Limiter
- token bucket
- rate limiter
- software engineering
- intermediate
- concurrency control
- web crawler
- model serving
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
  id: article-plan-token-bucket-rate-limiter
  covered_concepts: 1
  primary_concept: token-bucket-rate-limiter
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
- title: Python Data Structures Tutorial
  url: https://docs.python.org/3/tutorial/datastructures.html
  type: official_docs
- title: MLflow Documentation
  url: https://mlflow.org/docs/latest/index.html
  type: official_docs
---
# Token Bucket Rate Limiter：工程用法与常见坑

用令牌生成和消耗机制限制请求速率的算法。

关键词：Token Bucket Rate Limiter
- token bucket
- rate limiter
- software engineering
- intermediate
- concurrency control
- web crawler
- model serving

## 问题场景

服务需要防止请求突增压垮系统。令牌桶允许一定突发但限制长期速率。

## 核心机制

- 输入：Token Bucket Rate Limiter 所处理的数据、状态或评价对象。
- 操作：桶容量控制突发量，令牌生成速率控制平均速率。
- 观察结果：服务需要防止请求突增压垮系统。令牌桶允许一定突发但限制长期速率。

它像一个定速加币的桶。有币才能发请求。

例子：API 网关可用 token bucket 限制每个用户每分钟请求数。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Token Bucket Rate Limiter 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- 限流不是鉴权。它只控制访问频率。

## 相关概念

### 前置
- Concurrency Control

### 关联
- Web Crawler
- Model Serving

### 延伸
- Web Crawler
- Model Serving

## 延伸阅读

- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **MLflow Documentation**：https://mlflow.org/docs/latest/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
