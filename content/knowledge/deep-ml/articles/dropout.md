---
id: article-dropout
slug: dropout
title: Dropout：概念、直觉与边界
concepts:
- dropout
learning_units:
- dropout-overview
domain: deep_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Dropout
- deep learning
- intermediate
- regularization
- neural network
- batch normalization
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
  id: article-plan-dropout
  covered_concepts: 1
  primary_concept: dropout
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
- title: Dropout
  url: https://jmlr.org/papers/v15/srivastava14a.html
  type: paper
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
---
# Dropout：概念、直觉与边界

训练时随机置零中间激活并对保留值缩放、推理时关闭随机性的正则化方法。

关键词：Dropout
- deep learning
- intermediate
- regularization
- neural network
- batch normalization
- theory

## 为什么需要它

神经网络容易依赖少数强特征。dropout 迫使网络学习更分散的表示。

## 核心直觉

Dropout 在每次训练前向中采样不同 mask，使同一组参数形成许多随机子网络。网络因而不能把预测长期绑定在少数固定激活路径上。

Inverted dropout 对保留元素除以 `1-p`，保证训练输出的期望仍等于原激活。保持的是期望，不是每次输出，也不是方差；随机扰动本身正是正则化来源之一。推理时关闭 dropout，直接使用完整网络。

Dropout 先改变前向计算图，梯度随后自然沿这张随机图传播。它不是在 backward 后修改梯度，也不是永久删除权重。

## 数学定义

### 表达方式

`h_drop = mask * h / keep_prob 是一种常见训练形式`

此处保留 Dropout 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Dropout 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Dropout 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Dropout 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- Dropout 不是归一化、剪枝或梯度裁剪；它改变前向计算图，且只在存在过拟合余量时值得增加。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Dropout 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Dropout 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分类器、语言模型和小数据任务。大规模模型中常和其它正则策略一起使用。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Regularization
- Neural Network

### 关联
- Batch Normalization

### 延伸
- Batch Normalization

## 延伸阅读

- **Dropout**：https://jmlr.org/papers/v15/srivastava14a.html。用途：追溯原始方法、关键假设和实验设定。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
