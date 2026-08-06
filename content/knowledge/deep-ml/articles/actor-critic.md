---
id: article-actor-critic
slug: actor-critic
title: Actor-Critic：概念、直觉与边界
concepts:
- actor-critic
learning_units:
- actor-critic-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Actor-Critic
- reinforcement learning
- advanced
- policy gradient
- temporal difference learning
- proximal policy optimization
- deep q network
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
  id: article-plan-actor-critic
  covered_concepts: 1
  primary_concept: actor-critic
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
# Actor-Critic：概念、直觉与边界

同时学习策略和价值函数的强化学习方法框架。

关键词：Actor-Critic
- reinforcement learning
- advanced
- policy gradient
- temporal difference learning
- proximal policy optimization
- deep q network
- theory

## 为什么需要它

策略梯度方差较大。价值函数可以帮助策略更新更稳定。

## 核心直觉

- 输入：Actor-Critic 所处理的数据、状态或评价对象。
- 操作：actor 产生动作分布。critic 估计价值或优势函数。
- 观察结果：策略梯度方差较大。价值函数可以帮助策略更新更稳定。

actor 像执行者。critic 像评估者，告诉执行者这一步好不好。

例子：机器人控制中，actor 输出动作，critic 评估当前状态动作质量。

## 数学定义

### 表达方式

`策略更新常使用 advantage 作为权重`

此处保留 Actor-Critic 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Actor-Critic 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Actor-Critic 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Actor-Critic 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- actor-critic 不是单一算法。它是一类方法。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Actor-Critic 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Actor-Critic 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于连续控制、游戏和大模型对齐相关训练。稳定性依赖实现细节。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Policy Gradient
- Temporal Difference Learning

### 关联
- Proximal Policy Optimization
- Deep Q-Network

### 延伸
- Proximal Policy Optimization
- Deep Q-Network

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Proximal Policy Optimization Algorithms**：https://arxiv.org/abs/1707.06347。用途：追溯原始方法、关键假设和实验设定。
