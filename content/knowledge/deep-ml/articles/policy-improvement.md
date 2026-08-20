---
id: article-policy-improvement
slug: policy-improvement
title: Policy Improvement：概念、直觉与边界
concepts:
- policy-improvement
learning_units:
- policy-improvement-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Policy Improvement
- reinforcement learning
- intermediate
- policy evaluation
- action value function
- policy iteration
- value iteration
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
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-policy-improvement
  covered_concepts: 1
  primary_concept: policy-improvement
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Policy Improvement：概念、直觉与边界

根据当前价值估计构造更好策略的强化学习步骤。

关键词：Policy Improvement
- reinforcement learning
- intermediate
- policy evaluation
- action value function
- policy iteration
- value iteration
- theory

## 为什么需要它

评估策略后，还需要利用价值信息改进行动选择。

## 核心直觉

- 输入：Policy Improvement 所处理的数据、状态或评价对象。
- 操作：常见做法是对动作价值取贪心，或用软策略保留探索。
- 观察结果：评估策略后，还需要利用价值信息改进行动选择。

它像看完每步棋的评分后，改用更高分的走法。

例子：策略迭代中，每轮评估后都会执行 policy improvement。

## 数学定义

### 表达方式

$$
\pi^{\prime}(s)\in\underset{a}{\operatorname{arg\,max}}\ Q_\pi(s,a)\quad\Longrightarrow\quad V_{\pi^{\prime}}(s)\ge V_\pi(s)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Policy Improvement 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Policy Improvement 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Policy Improvement 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 完全贪心可能降低探索。控制算法常保留随机性。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Policy Improvement 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Policy Improvement 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于策略迭代、值迭代和 actor-critic 思路理解。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Policy Evaluation
- Action Value Function

### 关联
- Policy Iteration
- Value Iteration

### 延伸
- Policy Iteration
- Value Iteration

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
