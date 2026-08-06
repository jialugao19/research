---
id: article-self-play
slug: self-play
title: Self-Play：概念、直觉与边界
concepts:
- self-play
learning_units:
- self-play-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Self-Play
- self play
- reinforcement learning
- advanced
- multi agent reinforcement learning
- policy optimization
- alphazero
- minimax algorithm
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
  id: article-plan-self-play
  covered_concepts: 1
  primary_concept: self-play
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
- title: Proximal Policy Optimization Algorithms
  url: https://arxiv.org/abs/1707.06347
  type: paper
---
# Self-Play：概念、直觉与边界

让智能体通过和自身或历史版本对战来生成训练数据的方法。

关键词：Self-Play
- self play
- reinforcement learning
- advanced
- multi agent reinforcement learning
- policy optimization
- alphazero
- minimax algorithm

## 为什么需要它

对抗任务中，高质量对手数据昂贵且会过时。

## 核心直觉

- 输入：Self-Play 所处理的数据、状态或评价对象。
- 操作：self-play 需要维护对手池、避免策略崩塌，并保证难度逐步提升。
- 观察结果：对抗任务中，高质量对手数据昂贵且会过时。

它像棋手不断和自己的更强版本练习。

例子：棋类智能体可通过自博弈不断生成新棋局。

## 数学定义

### 表达方式

`policy_t trains against policy_{<=t}`

此处保留 Self-Play 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Self-Play 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Self-Play 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Self-Play 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 只和自己玩可能形成盲点，需要多样化对手和评估。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Self-Play 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Self-Play 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于棋类、博弈、自动课程学习和多智能体 RL。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Multi-Agent Reinforcement Learning
- Policy Optimization

### 关联
- AlphaZero
- Minimax Algorithm

### 延伸
- AlphaZero
- Minimax Algorithm

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Proximal Policy Optimization Algorithms**：https://arxiv.org/abs/1707.06347。用途：追溯原始方法、关键假设和实验设定。
