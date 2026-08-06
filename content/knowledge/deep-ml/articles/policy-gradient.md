---
id: article-policy-gradient
slug: policy-gradient
title: Policy Gradient：概念、直觉与边界
concepts:
- policy-gradient
learning_units:
- policy-gradient-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Policy Gradient
- REINFORCE
- reinforcement learning
- advanced
- markov decision process
- gradient descent
- q learning
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
  id: article-plan-policy-gradient
  covered_concepts: 1
  primary_concept: policy-gradient
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
# Policy Gradient：概念、直觉与边界

直接优化策略参数，使期望回报上升的强化学习方法。

关键词：Policy Gradient
- REINFORCE
- reinforcement learning
- advanced
- markov decision process
- gradient descent
- q learning
- theory

## 为什么需要它

有些任务动作连续，或策略本身需要随机性。只学 Q 值不一定方便。

## 核心直觉

- 输入：Policy Gradient 所处理的数据、状态或评价对象。
- 操作：策略梯度估计回报对策略参数的梯度。常用 baseline 降低方差。
- 观察结果：有些任务动作连续，或策略本身需要随机性。只学 Q 值不一定方便。

它像直接调整行为习惯。带来更高回报的动作概率会被提高。

例子：机器人控制中，策略可以直接输出动作分布，再根据回报调整参数。

## 数学定义

### 表达方式

`目标是最大化 E[return]，更新方向由 log pi(a|s) 与回报信号共同决定`

此处保留 Policy Gradient 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Policy Gradient 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Policy Gradient 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Policy Gradient 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 策略梯度通常方差较大。它不是比价值方法天然更稳定。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Policy Gradient 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Policy Gradient 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于连续控制、游戏和 RLHF 相关训练。样本效率和稳定性是主要挑战。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Markov Decision Process
- Gradient Descent

### 关联
- Q-Learning

### 延伸
- Q-Learning

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
