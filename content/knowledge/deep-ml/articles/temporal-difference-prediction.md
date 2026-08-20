---
id: article-temporal-difference-prediction
slug: temporal-difference-prediction
title: Temporal Difference Prediction：概念、直觉与边界
concepts:
- temporal-difference-prediction
learning_units:
- temporal-difference-prediction-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Temporal Difference Prediction
- TD prediction
- TD update
- reinforcement learning
- intermediate
- temporal difference learning
- state value function
- td error
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
  id: article-plan-temporal-difference-prediction
  covered_concepts: 1
  primary_concept: temporal-difference-prediction
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Temporal Difference Prediction：概念、直觉与边界

用当前奖励和下一状态估计更新状态价值的 TD 预测方法。

关键词：Temporal Difference Prediction
- TD prediction
- TD update
- reinforcement learning
- intermediate
- temporal difference learning
- state value function
- td error

## 为什么需要它

不想等完整回合结束时，可以用 bootstrap 提前更新价值。

## 核心直觉

- 输入：Temporal Difference Prediction 所处理的数据、状态或评价对象。
- 操作：TD prediction 用一步目标 r + gamma V(s') 更新 V(s)。
- 观察结果：不想等完整回合结束时，可以用 bootstrap 提前更新价值。

它像一边走路一边修正地图，而不是走完整条路才总结。

例子：网格世界中，每走一步都可以更新当前位置价值。

## 数学定义

### 表达方式

$$
V(S_t)\leftarrow V(S_t)+\alpha\left[R_{t+1}+\gamma V(S_{t+1})-V(S_t)\right]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Temporal Difference Prediction 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Temporal Difference Prediction 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Temporal Difference Prediction 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- TD 目标含估计值，因此有偏但方差较低。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Temporal Difference Prediction 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Temporal Difference Prediction 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于价值预测、策略评估和深度强化学习基础算法。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Temporal Difference Learning
- State Value Function

### 关联
- TD Error
- N-Step TD

### 延伸
- TD Error
- N-Step TD

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
