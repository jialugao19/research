---
id: article-evidence-lower-bound
slug: evidence-lower-bound
title: Evidence Lower Bound：概念、直觉与边界
concepts:
- evidence-lower-bound
learning_units:
- evidence-lower-bound-overview
domain: probabilistic_ml
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Evidence Lower Bound
- ELBO
- probabilistic ml
- advanced
- variational inference
- kl divergence
- variational autoencoder
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
  id: article-plan-evidence-lower-bound
  covered_concepts: 1
  primary_concept: evidence-lower-bound
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
- title: Auto-Encoding Variational Bayes
  url: https://arxiv.org/abs/1312.6114
  type: paper
---
# Evidence Lower Bound：概念、直觉与边界

变分推断中可优化的对数证据下界。

关键词：Evidence Lower Bound
- ELBO
- probabilistic ml
- advanced
- variational inference
- kl divergence
- variational autoencoder
- theory

## 为什么需要它

真实边缘似然常含难积分。ELBO 提供可训练目标。

## 核心直觉

- 输入：Evidence Lower Bound 所处理的数据、状态或评价对象。
- 操作：ELBO 通常由重构项和正则化 KL 项组成。
- 观察结果：真实边缘似然常含难积分。ELBO 提供可训练目标。

它像给难算目标找一个能安全提高的替代下界。

例子：VAE 训练时会最大化 ELBO。

## 数学定义

### 表达方式

$$
\log p(x)\ge\mathcal L(q)=\mathbb{E}_{q(z)}\!\left[\log p(x,z)-\log q(z)\right]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Evidence Lower Bound 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Evidence Lower Bound 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Evidence Lower Bound 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- ELBO 高不一定代表生成样本一定好，还要看模型假设。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Evidence Lower Bound 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Evidence Lower Bound 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 VAE、贝叶斯模型、主题模型和近似后验学习。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Variational Inference

### 关联
- KL Divergence
- Variational Autoencoder

### 延伸
- KL Divergence
- Variational Autoencoder

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Auto-Encoding Variational Bayes**：https://arxiv.org/abs/1312.6114。用途：追溯原始方法、关键假设和实验设定。
