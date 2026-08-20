---
id: article-roofline-analysis
slug: roofline-analysis
title: Roofline Analysis：概念、直觉与边界
concepts:
- roofline-analysis
learning_units:
- roofline-analysis-overview
domain: performance_optimization
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Roofline Analysis
- roofline
- performance optimization
- advanced
- arithmetic intensity
- gpu bottleneck analysis
- cuda occupancy
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
  id: article-plan-roofline-analysis
  covered_concepts: 1
  primary_concept: roofline-analysis
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
# Roofline Analysis：概念、直觉与边界

用算术强度和硬件峰值估计程序性能上限的分析方法。

关键词：Roofline Analysis
- roofline
- performance optimization
- advanced
- arithmetic intensity
- gpu bottleneck analysis
- cuda occupancy
- theory

## 为什么需要它

优化前需要知道瓶颈在哪里。roofline 模型给出可解释的性能上界。

## 核心直觉

- 输入：Roofline Analysis 所处理的数据、状态或评价对象。
- 操作：模型比较计算上限和带宽上限，判断程序是 compute-bound 还是 memory-bound。
- 观察结果：优化前需要知道瓶颈在哪里。roofline 模型给出可解释的性能上界。

它像给程序画一条硬件天花板线。

例子：分析 GPU kernel 时，可以用 roofline 判断是否应优化内存访问。

## 数学定义

### 表达方式

$$
P\le\min\!\left(P_{\mathrm{peak}},\,B_{\mathrm{mem}}I\right)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Roofline Analysis 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Roofline Analysis 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Roofline Analysis 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- roofline 是模型，不是完整 profiler。它忽略部分调度细节。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Roofline Analysis 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Roofline Analysis 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 CUDA、Triton、矩阵乘法和推理性能优化。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Arithmetic Intensity

### 关联
- GPU Bottleneck Analysis
- CUDA Occupancy

### 延伸
- GPU Bottleneck Analysis
- CUDA Occupancy

## 延伸阅读

- **CUDA C++ Programming Guide**：https://docs.nvidia.com/cuda/cuda-c-programming-guide/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Triton Documentation**：https://triton-lang.org/main/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
