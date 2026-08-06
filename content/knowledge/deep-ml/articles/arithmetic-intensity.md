---
id: article-arithmetic-intensity
slug: arithmetic-intensity
title: Arithmetic Intensity：概念、直觉与边界
concepts:
- arithmetic-intensity
learning_units:
- arithmetic-intensity-overview
domain: performance_optimization
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Arithmetic Intensity
- ops byte ratio
- performance optimization
- advanced
- latency throughput
- vectorization
- roofline analysis
- memory coalescing
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-arithmetic-intensity
  covered_concepts: 1
  primary_concept: arithmetic-intensity
confidence:
  concept: 0.94
  prerequisite: 0.9
  prerequisite_path_eligible: true
generated_version:
  model: curated-catalog-v3
  prompt_version: chapter-profile-v3
review:
  state: automated_editorial
  last_review: null
  reviewer: null
  triggers:
  - advanced_or_expert_topic
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: CUDA C++ Programming Guide
  url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
  type: official_docs
- title: Triton Documentation
  url: https://triton-lang.org/main/index.html
  type: official_docs
---
# Arithmetic Intensity：概念、直觉与边界

计算操作量与内存访问量之间的比值。

关键词：Arithmetic Intensity
- ops byte ratio
- performance optimization
- advanced
- latency throughput
- vectorization
- roofline analysis
- memory coalescing

## 为什么需要它

GPU 性能瓶颈可能来自计算，也可能来自内存带宽。算术强度帮助分类瓶颈。

## 核心直觉

- 输入：Arithmetic Intensity 所处理的数据、状态或评价对象。
- 操作：算术强度高的算子更可能受计算峰值限制。低的更可能受带宽限制。
- 观察结果：GPU 性能瓶颈可能来自计算，也可能来自内存带宽。算术强度帮助分类瓶颈。

它像看每搬一字节数据能做多少计算。

例子：矩阵乘法通常比逐元素加法有更高算术强度。

## 数学定义

### 表达方式

$$
arithmetic_intensity = FLOPs / bytes_moved
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Arithmetic Intensity 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Arithmetic Intensity 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Arithmetic Intensity 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 算术强度只是分析入口。实际性能还受并行度和缓存影响。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Arithmetic Intensity 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Arithmetic Intensity 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 GPU 性能分析、算子优化和 roofline 建模。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Latency and Throughput
- Vectorization

### 关联
- Roofline Analysis
- Memory Coalescing

### 延伸
- Roofline Analysis
- Memory Coalescing

## 延伸阅读

- **CUDA C++ Programming Guide**：https://docs.nvidia.com/cuda/cuda-c-programming-guide/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Triton Documentation**：https://triton-lang.org/main/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
