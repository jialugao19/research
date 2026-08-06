---
id: article-contrastive-learning
slug: contrastive-learning
title: Contrastive Learning：概念、直觉与边界
concepts:
- contrastive-learning
learning_units:
- contrastive-learning-overview
domain: deep_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Contrastive Learning
- deep learning
- advanced
- word embeddings
- cross entropy
- retrieval augmented generation
- image augmentation
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
  id: article-plan-contrastive-learning
  covered_concepts: 1
  primary_concept: contrastive-learning
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Contrastive Learning：概念、直觉与边界

通过拉近相似样本表示、推远不相似样本表示来学习特征的方法。

关键词：Contrastive Learning
- deep learning
- advanced
- word embeddings
- cross entropy
- retrieval augmented generation
- image augmentation
- theory

## 为什么需要它

标注数据有限时，模型仍可利用样本之间的相似关系学习表示。

## 核心直觉

- 输入：Contrastive Learning 所处理的数据、状态或评价对象。
- 操作：方法通常构造正样本对和负样本对，再用对比损失优化表示空间。
- 观察结果：标注数据有限时，模型仍可利用样本之间的相似关系学习表示。

它像教模型分辨哪些样本应该靠近，哪些应该分开。

例子：同一图片的两种增强视图可以作为正样本对。

## 数学定义

### 表达方式

`InfoNCE 是常见对比损失形式`

此处保留 Contrastive Learning 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Contrastive Learning 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Contrastive Learning 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Contrastive Learning 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 负样本越多不一定总好。假负样本会干扰训练。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Contrastive Learning 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Contrastive Learning 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于视觉预训练、文本表示和多模态对齐。batch 构造很重要。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Word Embeddings
- Cross Entropy

### 关联
- Retrieval-Augmented Generation
- Image Augmentation

### 延伸
- Retrieval-Augmented Generation
- Image Augmentation

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
