---
id: article-action-value-function
slug: action-value-function
title: Action Value Function：概念、直觉与边界
concepts:
- action-value-function
learning_units:
- action-value-function-overview
domain: reinforcement_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Action Value Function
- action value
- q function
- reinforcement learning
- beginner
- state value function
- q learning
- sarsa
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
  id: article-plan-action-value-function
  covered_concepts: 1
  primary_concept: action-value-function
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Action Value Function：概念、直觉与边界

表示在某状态先采取某动作后，继续按策略行动的期望回报。

关键词：Action Value Function
- action value
- q function
- reinforcement learning
- beginner
- state value function
- q learning
- sarsa

## 为什么需要它

智能体不仅要评估状态，还要比较动作。动作价值函数直接支持选择动作。

## 核心直觉

- 输入：Action Value Function 所处理的数据、状态或评价对象。
- 操作：Q 函数以状态和动作作为输入。很多控制算法围绕它更新。
- 观察结果：智能体不仅要评估状态，还要比较动作。动作价值函数直接支持选择动作。

它像问在这个局面下，每一步棋分别有多好。

例子：Q-learning 会学习每个状态动作对的价值。

## 数学定义

### 表达方式

$$
Q_pi(s,a) = E_pi[G_t | S_t=s, A_t=a]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Action Value Function 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Action Value Function 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Action Value Function 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- Q 值不是即时奖励。它包含未来影响。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Action Value Function 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Action Value Function 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 Q-learning、SARSA 和离线策略评估。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- State Value Function

### 关联
- Q-Learning
- SARSA

### 延伸
- Q-Learning
- SARSA

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
