---
id: article-scaling-law
slug: scaling-law
title: Scaling Law：概念、直觉与边界
concepts:
- scaling-law
learning_units:
- scaling-law-overview
domain: deep_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Scaling Law
- scaling laws
- deep learning
- advanced
- model evaluation metrics
- compute optimal training
- training compute estimation
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
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-scaling-law
  covered_concepts: 1
  primary_concept: scaling-law
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Scaling Law：概念、直觉与边界

描述模型规模、数据规模、计算量和损失之间经验关系的规律。

关键词：Scaling Law
- scaling laws
- deep learning
- advanced
- model evaluation metrics
- compute optimal training
- training compute estimation
- theory

## 为什么需要它

训练大模型成本高。需要在开训前估计规模收益。

## 核心直觉

- 输入：Scaling Law 所处理的数据、状态或评价对象。
- 操作：常见 scaling law 用幂律关系拟合 loss 随参数、数据和计算变化。
- 观察结果：训练大模型成本高。需要在开训前估计规模收益。

它像用历史实验拟合一条预算和效果之间的曲线。

例子：预训练前可用小规模实验外推更大规模训练效果。

## 数学定义

### 表达方式

`loss ≈ a * compute^{-b} + c`

此处保留 Scaling Law 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Scaling Law 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Scaling Law 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Scaling Law 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- scaling law 是经验规律，不保证跨数据和架构恒定成立。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Scaling Law 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Scaling Law 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于大模型预算、数据规划、模型规模选择和研究报告。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Model Evaluation Metrics

### 关联
- Compute-Optimal Training
- Training Compute Estimation

### 延伸
- Compute-Optimal Training
- Training Compute Estimation

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
