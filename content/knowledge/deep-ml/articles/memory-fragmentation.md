---
id: article-memory-fragmentation
slug: memory-fragmentation
title: Memory Fragmentation：概念、直觉与边界
concepts:
- memory-fragmentation
learning_units:
- memory-fragmentation-overview
domain: performance_optimization
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Memory Fragmentation
- fragmentation LLM serving
- performance optimization
- intermediate
- memory footprint estimation
- kv cache
- continuous batching
- theory
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
  id: article-plan-memory-fragmentation
  covered_concepts: 1
  primary_concept: memory-fragmentation
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
- title: CUDA C++ Programming Guide
  url: https://docs.nvidia.com/cuda/cuda-c-programming-guide/
  type: official_docs
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Memory Fragmentation：概念、直觉与边界

内存被切成许多不连续空洞，导致可用总量和可分配大块不一致的现象。

关键词：Memory Fragmentation
- fragmentation LLM serving
- performance optimization
- intermediate
- memory footprint estimation
- kv cache
- continuous batching
- theory

## 为什么需要它

服务明明还有空闲内存，却可能无法分配足够连续的大块。

## 核心直觉

- 输入：Memory Fragmentation 所处理的数据、状态或评价对象。
- 操作：碎片来自频繁分配释放、不同大小对象和长短生命周期混合。
- 观察结果：服务明明还有空闲内存，却可能无法分配足够连续的大块。

它像停车场还有很多小空位，但停不下一辆大车。

例子：LLM 服务中 KV cache 动态变化可能造成显存碎片。

## 数学定义

### 表达方式

$$
usable_large_block \le total_free_memory
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Memory Fragmentation 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Memory Fragmentation 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Memory Fragmentation 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 碎片不是简单内存泄漏，但也会造成 OOM。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Memory Fragmentation 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Memory Fragmentation 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 GPU 服务、内存池、推理调度和性能诊断。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Memory Footprint Estimation

### 关联
- KV Cache
- Continuous Batching

### 延伸
- KV Cache
- Continuous Batching

## 延伸阅读

- **CUDA C++ Programming Guide**：https://docs.nvidia.com/cuda/cuda-c-programming-guide/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
