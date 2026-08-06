---
id: article-epsilon-greedy-policy
slug: epsilon-greedy-policy
title: Epsilon-Greedy Policy：概念、直觉与边界
concepts:
- epsilon-greedy-policy
learning_units:
- epsilon-greedy-policy-overview
domain: reinforcement_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Epsilon-Greedy Policy
- epsilon greedy
- reinforcement learning
- beginner
- exploration exploitation
- q learning
- multi armed bandit
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
  id: article-plan-epsilon-greedy-policy
  covered_concepts: 1
  primary_concept: epsilon-greedy-policy
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Epsilon-Greedy Policy：概念、直觉与边界

以小概率随机探索，以大概率选择当前最优动作的策略。

关键词：Epsilon-Greedy Policy
- epsilon greedy
- reinforcement learning
- beginner
- exploration exploitation
- q learning
- multi armed bandit
- theory

## 为什么需要它

智能体需要在探索和利用之间权衡。epsilon-greedy 是最简单方法之一。

## 核心直觉

- 输入：Epsilon-Greedy Policy 所处理的数据、状态或评价对象。
- 操作：epsilon 控制随机探索概率。训练中常逐渐降低 epsilon。
- 观察结果：智能体需要在探索和利用之间权衡。epsilon-greedy 是最简单方法之一。

它像大多数时候走熟路，偶尔试一条新路。

例子：Q-learning 早期可以用较高 epsilon 收集经验。

## 数学定义

### 表达方式

`以 epsilon 概率随机选动作，否则选 argmax Q`

此处保留 Epsilon-Greedy Policy 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Epsilon-Greedy Policy 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Epsilon-Greedy Policy 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Epsilon-Greedy Policy 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- epsilon 过低会早熟。过高会长期浪费回报。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Epsilon-Greedy Policy 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Epsilon-Greedy Policy 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 bandit、Q-learning 和教学实验。复杂环境常需要更细探索策略。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Exploration and Exploitation

### 关联
- Q-Learning
- Multi-Armed Bandit

### 延伸
- Q-Learning
- Multi-Armed Bandit

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
