---
id: article-eligibility-traces
slug: eligibility-traces
title: Eligibility Traces：概念、直觉与边界
concepts:
- eligibility-traces
learning_units:
- eligibility-traces-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Eligibility Traces
- eligibility trace
- TD lambda
- reinforcement learning
- advanced
- td error
- temporal difference learning
- n step td
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
  id: article-plan-eligibility-traces
  covered_concepts: 1
  primary_concept: eligibility-traces
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
# Eligibility Traces：概念、直觉与边界

记录近期状态或动作对当前 TD 误差应承担多少更新责任的机制。

关键词：Eligibility Traces
- eligibility trace
- TD lambda
- reinforcement learning
- advanced
- td error
- temporal difference learning
- n step td

## 为什么需要它

一步 TD 更新传播慢。资格迹让近期经历同时得到更新。

## 核心直觉

- 输入：Eligibility Traces 所处理的数据、状态或评价对象。
- 操作：lambda 控制迹的衰减速度。它连接一步 TD 和 Monte Carlo 方法。
- 观察结果：一步 TD 更新传播慢。资格迹让近期经历同时得到更新。

它像给最近走过的脚印留下可衰减的责任标记。

例子：TD(lambda) 使用 eligibility traces 更新价值函数。

## 数学定义

### 表达方式

$$
e_t=\gamma\lambda e_{t-1}+\nabla_w V_w(S_t),\qquad w_{t+1}=w_t+\alpha\delta_t e_t
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Eligibility Traces 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Eligibility Traces 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Eligibility Traces 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- lambda 越大不一定越好。方差和偏差会同时变化。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Eligibility Traces 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Eligibility Traces 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 TD(lambda)、SARSA(lambda) 和在线 RL。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- TD Error
- Temporal Difference Learning

### 关联
- N-Step TD

### 延伸
- N-Step TD

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
