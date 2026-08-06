---
id: article-policy-evaluation
slug: policy-evaluation
title: Policy Evaluation：概念、直觉与边界
concepts:
- policy-evaluation
learning_units:
- policy-evaluation-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Policy Evaluation
- reinforcement learning
- intermediate
- markov decision process
- bellman equation
- policy iteration
- temporal difference learning
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
  id: article-plan-policy-evaluation
  covered_concepts: 1
  primary_concept: policy-evaluation
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Policy Evaluation：概念、直觉与边界

估计给定策略在各状态下长期价值的过程。

关键词：Policy Evaluation
- reinforcement learning
- intermediate
- markov decision process
- bellman equation
- policy iteration
- temporal difference learning
- theory

## 为什么需要它

改进策略前，常要先知道当前策略好不好。策略评估负责回答这个问题。

## 核心直觉

- 输入：Policy Evaluation 所处理的数据、状态或评价对象。
- 操作：评估可以用动态规划、Monte Carlo 或 TD 方法完成。
- 观察结果：改进策略前，常要先知道当前策略好不好。策略评估负责回答这个问题。

它像先给现有路线打分，再决定要不要换路线。

例子：在网格世界中，可以估计固定移动策略从每个格子出发的期望回报。

## 数学定义

### 表达方式

$$
V_pi(s) = E_pi[G_t | S_t=s]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Policy Evaluation 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Policy Evaluation 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Policy Evaluation 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 评估策略不等于寻找最优策略。它只评价给定策略。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Policy Evaluation 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Policy Evaluation 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于策略迭代、actor-critic 和离线评估。估计误差会影响后续改进。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Markov Decision Process
- Bellman Equation

### 关联
- Policy Iteration
- Temporal Difference Learning

### 延伸
- Policy Iteration
- Temporal Difference Learning

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
