---
id: article-successor-representation
slug: successor-representation
title: Successor Representation：概念、直觉与边界
concepts:
- successor-representation
learning_units:
- successor-representation-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Successor Representation
- successor features
- reinforcement learning
- advanced
- state value function
- markov decision process
- feature space
- temporal difference learning
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
  id: article-plan-successor-representation
  covered_concepts: 1
  primary_concept: successor-representation
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
# Successor Representation：概念、直觉与边界

表示当前状态未来会访问哪些状态或特征的强化学习表示方法。

关键词：Successor Representation
- successor features
- reinforcement learning
- advanced
- state value function
- markov decision process
- feature space
- temporal difference learning

## 为什么需要它

价值函数把动态和奖励混在一起。successor representation 可部分拆开。

## 核心直觉

- 输入：Successor Representation 所处理的数据、状态或评价对象。
- 操作：SR 把状态转移结构编码为未来折扣访问频率。
- 观察结果：价值函数把动态和奖励混在一起。successor representation 可部分拆开。

它像从当前位置出发，预估以后会经过哪些地方。

例子：奖励改变但环境结构不变时，SR 可更快重算价值。

## 数学定义

### 表达方式

$$
M(s,s') = E[sum_t gamma^t 1(S_t=s')]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Successor Representation 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Successor Representation 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Successor Representation 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- SR 仍依赖策略。策略改变时表示也可能需要更新。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Successor Representation 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Successor Representation 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于迁移 RL、表示学习、规划和神经科学建模。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- State Value Function
- Markov Decision Process

### 关联
- Feature Space
- Temporal Difference Learning

### 延伸
- Feature Space
- Temporal Difference Learning

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
