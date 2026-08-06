---
id: article-prioritized-sweeping
slug: prioritized-sweeping
title: Prioritized Sweeping：概念、直觉与边界
concepts:
- prioritized-sweeping
learning_units:
- prioritized-sweeping-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Prioritized Sweeping
- reinforcement learning
- advanced
- dyna q
- temporal difference learning
- environment model
- td error
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
  id: article-plan-prioritized-sweeping
  covered_concepts: 1
  primary_concept: prioritized-sweeping
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
# Prioritized Sweeping：概念、直觉与边界

优先更新预计价值变化最大的状态的模型式强化学习方法。

关键词：Prioritized Sweeping
- reinforcement learning
- advanced
- dyna q
- temporal difference learning
- environment model
- td error
- theory

## 为什么需要它

规划更新预算有限。平均扫所有状态会浪费在变化很小的位置。

## 核心直觉

- 输入：Prioritized Sweeping 所处理的数据、状态或评价对象。
- 操作：算法维护优先队列，把 TD 误差大的前驱状态放到前面更新。
- 观察结果：规划更新预算有限。平均扫所有状态会浪费在变化很小的位置。

它像先修补地图上误差最大的区域。

例子：网格世界中，奖励变化会沿前驱状态快速传播。

## 数学定义

### 表达方式

$$
priority(s)=abs(predicted_value_change)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Prioritized Sweeping 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Prioritized Sweeping 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Prioritized Sweeping 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 优先级计算依赖模型和前驱信息，工程实现更复杂。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Prioritized Sweeping 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Prioritized Sweeping 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于模型式 RL、规划、Dyna 方法和教学环境。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Dyna-Q
- Temporal Difference Learning

### 关联
- Environment Model
- TD Error

### 延伸
- Environment Model
- TD Error

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
