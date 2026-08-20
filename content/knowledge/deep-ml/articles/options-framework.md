---
id: article-options-framework
slug: options-framework
title: Options Framework：概念、直觉与边界
concepts:
- options-framework
learning_units:
- options-framework-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Options Framework
- temporal abstraction options
- reinforcement learning
- advanced
- markov decision process
- policy optimization
- action mapping
- curriculum learning
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
  id: article-plan-options-framework
  covered_concepts: 1
  primary_concept: options-framework
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
# Options Framework：概念、直觉与边界

把持续多步的高层动作纳入强化学习决策的时间抽象框架。

关键词：Options Framework
- temporal abstraction options
- reinforcement learning
- advanced
- markov decision process
- policy optimization
- action mapping
- curriculum learning

## 为什么需要它

一步一步选原子动作会让长期规划很慢。

## 核心直觉

- 输入：Options Framework 所处理的数据、状态或评价对象。
- 操作：一个 option 包含启动条件、内部策略和终止条件。
- 观察结果：一步一步选原子动作会让长期规划很慢。

它像把多步操作打包成技能，例如走到门口或打开抽屉。

例子：导航任务可把到达某个房间作为一个 option。

## 数学定义

### 表达方式

$$
\omega=(\mathcal I_\omega,\pi_\omega,\beta_\omega),\qquad \beta_\omega(s)=\Pr(\text{terminate}\mid s,\omega)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Options Framework 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Options Framework 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Options Framework 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- option 不是普通动作。它会持续多个时间步。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Options Framework 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Options Framework 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于层级 RL、技能学习、长期规划和任务分解。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Markov Decision Process
- Policy Optimization

### 关联
- Action Mapping
- Curriculum Learning

### 延伸
- Action Mapping
- Curriculum Learning

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
