---
id: article-td-gammon
slug: td-gammon
title: TD-Gammon：概念、直觉与边界
concepts:
- td-gammon
learning_units:
- td-gammon-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- TD-Gammon
- TD Gammon
- reinforcement learning
- advanced
- temporal difference learning
- state value function
- self play
- deep q network
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
  id: article-plan-td-gammon
  covered_concepts: 1
  primary_concept: td-gammon
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# TD-Gammon：概念、直觉与边界

使用时序差分学习训练双陆棋位置评估网络的经典系统。

关键词：TD-Gammon
- TD Gammon
- reinforcement learning
- advanced
- temporal difference learning
- state value function
- self play
- deep q network

## 为什么需要它

游戏状态巨大，人工穷举价值表不可行。

## 核心直觉

- 输入：TD-Gammon 所处理的数据、状态或评价对象。
- 操作：TD-Gammon 用神经网络估计位置价值，并通过 TD 误差更新。
- 观察结果：游戏状态巨大，人工穷举价值表不可行。

它像让神经网络通过自我对弈学会给局面打分。

例子：自我对弈产生的局面可训练评估网络。

## 数学定义

### 表达方式

$$
weights \leftarrow weights + alpha \cdot  TD_error \cdot  gradient V(s)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- TD-Gammon 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 TD-Gammon 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 TD-Gammon 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 它不是现代深度 RL 的全部模板，但奠定了价值近似思想。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 TD-Gammon 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 TD-Gammon 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 RL 历史、游戏 AI 和价值函数教学。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Temporal Difference Learning
- State Value Function

### 关联
- Self-Play
- Deep Q-Network

### 延伸
- Self-Play
- Deep Q-Network

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
