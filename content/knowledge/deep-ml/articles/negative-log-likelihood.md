---
id: article-negative-log-likelihood
slug: negative-log-likelihood
title: Negative Log Likelihood：概念、直觉与边界
concepts:
- negative-log-likelihood
learning_units:
- negative-log-likelihood-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Negative Log Likelihood
- NLL
- machine learning
- beginner
- maximum likelihood estimation
- cross entropy
- uncertainty estimation
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
  id: article-plan-negative-log-likelihood
  covered_concepts: 1
  primary_concept: negative-log-likelihood
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Negative Log Likelihood：概念、直觉与边界

把模型赋给真实观测的概率取负对数得到的损失。

关键词：Negative Log Likelihood
- NLL
- machine learning
- beginner
- maximum likelihood estimation
- cross entropy
- uncertainty estimation
- theory

## 为什么需要它

概率模型需要可优化目标。NLL 把高概率奖励和低概率惩罚写成损失。

## 核心直觉

- 输入：Negative Log Likelihood 所处理的数据、状态或评价对象。
- 操作：最小化 NLL 等价于最大化数据似然。
- 观察结果：概率模型需要可优化目标。NLL 把高概率奖励和低概率惩罚写成损失。

它像惩罚模型对真实结果不够相信。

例子：分类交叉熵可以看作真实类别的负对数似然。

## 数学定义

### 表达方式

$$
NLL = - log p(y|x)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Negative Log Likelihood 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Negative Log Likelihood 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Negative Log Likelihood 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- NLL 依赖概率假设。分布假设错时，损失解释也会变弱。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Negative Log Likelihood 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Negative Log Likelihood 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分类、概率回归、语言模型和密度估计。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Maximum Likelihood Estimation

### 关联
- Cross Entropy
- Uncertainty Estimation

### 延伸
- Cross Entropy
- Uncertainty Estimation

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
