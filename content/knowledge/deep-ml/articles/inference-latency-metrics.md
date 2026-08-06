---
id: article-inference-latency-metrics
slug: inference-latency-metrics
title: Inference Latency Metrics：指标含义与使用边界
concepts:
- inference-latency-metrics
learning_units:
- inference-latency-metrics-overview
domain: inference
level: intermediate
content_type: metric
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Inference Latency Metrics
- TTFT
- ITL
- inference
- intermediate
- latency throughput
- prefill decode
- continuous batching
profile:
  required_sections:
  - 衡量什么
  - 数学定义
  - 指标解释
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-inference-latency-metrics
  covered_concepts: 1
  primary_concept: inference-latency-metrics
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: CUDA C++ Programming Guide
  url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
  type: official_docs
---
# Inference Latency Metrics：指标含义与使用边界

衡量推理服务首 token、单 token 和整体吞吐表现的指标集合。

关键词：Inference Latency Metrics
- TTFT
- ITL
- inference
- intermediate
- latency throughput
- prefill decode
- continuous batching

## 衡量什么

总延迟无法解释用户等待来自哪里。推理指标需要拆阶段看。

## 数学定义

### 表达方式

$$
E2E latency = TTFT + decode_time
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Inference Latency Metrics 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Inference Latency Metrics 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 指标解释

- Inference Latency Metrics 的数值只回答一个特定评价问题。
- 高分不一定代表模型整体更好，必须结合数据分布和错误代价。
- 指标变化要和阈值、样本量、类别比例一起解释。

## 常见误区

### 概念误解
- TPS 高不代表单用户体验好。还要看排队和首 token 延迟。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Inference Latency Metrics 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Inference Latency Metrics 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 LLM 服务、SLA、容量规划和性能回归测试。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Latency and Throughput
- Prefill and Decode

### 关联
- Continuous Batching
- Streaming Inference

### 延伸
- Continuous Batching
- Streaming Inference

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CUDA C++ Programming Guide**：https://docs.nvidia.com/cuda/cuda-c-programming-guide/。用途：作为交叉核对材料，确认术语、公式和使用场景。
