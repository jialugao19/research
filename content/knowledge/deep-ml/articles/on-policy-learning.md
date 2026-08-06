---
id: article-on-policy-learning
slug: on-policy-learning
title: On-Policy Learning：概念、直觉与边界
concepts:
- on-policy-learning
learning_units:
- on-policy-learning-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- On-Policy Learning
- on-policy
- on policy
- reinforcement learning
- intermediate
- policy optimization
- off policy learning
- sample efficiency
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
  id: article-plan-on-policy-learning
  covered_concepts: 1
  primary_concept: on-policy-learning
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
# On-Policy Learning：概念、直觉与边界

用当前正在执行的策略产生的数据来学习同一个策略的方法。

关键词：On-Policy Learning
- on-policy
- on policy
- reinforcement learning
- intermediate
- policy optimization
- off policy learning
- sample efficiency

## 为什么需要它

有些算法必须让采样行为和被优化策略保持一致。

## 核心直觉

- 输入：On-Policy Learning 所处理的数据、状态或评价对象。
- 操作：on-policy 方法的数据新鲜但复用率低。策略更新太大时可能破坏稳定性。
- 观察结果：有些算法必须让采样行为和被优化策略保持一致。

它像边按当前计划行动，边改进这份计划。

例子：SARSA 和 PPO 都是典型 on-policy 风格算法。

## 数学定义

### 表达方式

$$
data ~ pi_theta, update pi_theta
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- On-Policy Learning 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 On-Policy Learning 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 On-Policy Learning 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- on-policy 不等于不能探索。探索通常包含在当前策略中。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 On-Policy Learning 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 On-Policy Learning 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于策略梯度、PPO、在线控制和安全约束场景。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Policy Optimization

### 关联
- Off-Policy Learning
- Sample Efficiency

### 延伸
- Off-Policy Learning
- Sample Efficiency

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Proximal Policy Optimization Algorithms**：https://arxiv.org/abs/1707.06347。用途：追溯原始方法、关键假设和实验设定。
