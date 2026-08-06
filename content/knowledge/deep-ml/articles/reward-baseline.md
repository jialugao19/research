---
id: article-reward-baseline
slug: reward-baseline
title: Reward Baseline：概念、直觉与边界
concepts:
- reward-baseline
learning_units:
- reward-baseline-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Reward Baseline
- baseline reward
- average rewards
- reinforcement learning
- intermediate
- discounted return
- policy gradient
- advantage function
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
  id: article-plan-reward-baseline
  covered_concepts: 1
  primary_concept: reward-baseline
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
- title: Proximal Policy Optimization Algorithms
  url: https://arxiv.org/abs/1707.06347
  type: paper
---
# Reward Baseline：概念、直觉与边界

在策略梯度中减去的参考值，用于降低梯度估计方差。

关键词：Reward Baseline
- baseline reward
- average rewards
- reinforcement learning
- intermediate
- discounted return
- policy gradient
- advantage function

## 为什么需要它

回报噪声会让策略更新不稳定。baseline 能减少无关波动。

## 核心直觉

- 输入：Reward Baseline 所处理的数据、状态或评价对象。
- 操作：baseline 不应改变期望梯度方向。价值函数常用作 baseline。
- 观察结果：回报噪声会让策略更新不稳定。baseline 能减少无关波动。

它像只看表现比平均水平高多少，而不是只看原始分数。

例子：Actor-Critic 用 critic 的价值估计作为策略更新基线。

## 数学定义

### 表达方式

$$
advantage = return - baseline
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Reward Baseline 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Reward Baseline 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Reward Baseline 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- baseline 不是奖励塑形。它主要降低方差。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Reward Baseline 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Reward Baseline 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于策略梯度、优势估计和 RLHF 训练。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Discounted Return
- Policy Gradient

### 关联
- Advantage Function
- Reward Normalization

### 延伸
- Advantage Function
- Reward Normalization

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Proximal Policy Optimization Algorithms**：https://arxiv.org/abs/1707.06347。用途：追溯原始方法、关键假设和实验设定。
