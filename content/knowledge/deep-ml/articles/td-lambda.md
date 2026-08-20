---
id: article-td-lambda
slug: td-lambda
title: TD Lambda：概念、直觉与边界
concepts:
- td-lambda
learning_units:
- td-lambda-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- TD Lambda
- TD(lambda)
- TD(λ)
- reinforcement learning
- advanced
- eligibility traces
- temporal difference learning
- n step td
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
  id: article-plan-td-lambda
  covered_concepts: 1
  primary_concept: td-lambda
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# TD Lambda：概念、直觉与边界

用资格迹在一步 TD 和蒙特卡洛回报之间折中的强化学习方法。

关键词：TD Lambda
- TD(lambda)
- TD(λ)
- reinforcement learning
- advanced
- eligibility traces
- temporal difference learning
- n step td

## 为什么需要它

一步 TD 偏差较大，完整回报方差较大。TD(lambda) 提供连续折中。

## 核心直觉

- 输入：TD Lambda 所处理的数据、状态或评价对象。
- 操作：lambda 控制信用分配向过去传播的长度。
- 观察结果：一步 TD 偏差较大，完整回报方差较大。TD(lambda) 提供连续折中。

它像让近期状态按衰减权重共同承担一次反馈。

例子：在表格控制任务中，eligibility traces 可加速价值传播。

## 数学定义

### 表达方式

$$
G_t^{\lambda}=(1-\lambda)\sum_{n=1}^{T-t-1}\lambda^{n-1}G_{t:t+n}+\lambda^{T-t-1}G_t
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- TD Lambda 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 TD Lambda 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 TD Lambda 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- lambda 越大不一定越好，偏差方差权衡会变化。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 TD Lambda 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 TD Lambda 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 TD 学习、SARSA(lambda) 和强化学习教学。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Eligibility Traces
- Temporal Difference Learning

### 关联
- N-Step TD
- Temporal Difference Prediction

### 延伸
- N-Step TD
- Temporal Difference Prediction

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
