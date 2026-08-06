---
id: article-latency-throughput
slug: latency-throughput
title: Latency and Throughput：工程用法与常见坑
concepts:
- latency-throughput
learning_units:
- latency-throughput-overview
domain: inference
level: beginner
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Latency and Throughput
- latency
- throughput
- inference
- beginner
- model serving
- dynamic batching
- model quantization
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
  id: article-plan-latency-throughput
  covered_concepts: 1
  primary_concept: latency-throughput
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Latency and Throughput：工程用法与常见坑

衡量服务响应速度和单位时间处理能力的两个指标。

关键词：Latency and Throughput
- latency
- throughput
- inference
- beginner
- model serving
- dynamic batching
- model quantization

## 问题场景

推理系统既要快，也要能处理足够多请求。两个指标常有取舍。

## 核心机制

- 输入：Latency and Throughput 所处理的数据、状态或评价对象。
- 操作：增大 batch 可能提高吞吐，但也可能增加单请求等待时间。
- 观察结果：推理系统既要快，也要能处理足够多请求。两个指标常有取舍。

延迟看单个请求等多久。吞吐看一段时间能处理多少请求。

例子：在线搜索更关注 P95 延迟。离线评分更关注总吞吐。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Latency and Throughput 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- 平均延迟不够。尾部延迟常决定用户体验。

## 相关概念

### 前置
- Model Serving

### 关联
- Dynamic Batching
- Model Quantization

### 延伸
- Dynamic Batching
- Model Quantization

## 延伸阅读

- **MLflow Documentation**：https://mlflow.org/docs/latest/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
