---
id: article-semi-gradient-td
slug: semi-gradient-td
title: Semi-Gradient TD：概念、直觉与边界
concepts:
- semi-gradient-td
learning_units:
- semi-gradient-td-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Semi-Gradient TD
- semi-gradient
- semi gradient TD
- reinforcement learning
- advanced
- rl function approximation
- temporal difference prediction
- td error
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
  id: article-plan-semi-gradient-td
  covered_concepts: 1
  primary_concept: semi-gradient-td
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
# Semi-Gradient TD：概念、直觉与边界

在函数近似 TD 更新中，只对当前价值估计求梯度的方法。

关键词：Semi-Gradient TD
- semi-gradient
- semi gradient TD
- reinforcement learning
- advanced
- rl function approximation
- temporal difference prediction
- td error

## 为什么需要它

TD 目标中包含下一状态估计。完整梯度会引入额外复杂性。

## 核心直觉

- 输入：Semi-Gradient TD 所处理的数据、状态或评价对象。
- 操作：semi-gradient 方法忽略目标中参数的梯度，常用于价值函数近似。
- 观察结果：TD 目标中包含下一状态估计。完整梯度会引入额外复杂性。

它像把目标暂时当作固定标签，只更新当前预测。

例子：线性价值函数近似可用 semi-gradient TD(0) 更新权重。

## 数学定义

### 表达方式

$$
w \leftarrow w + alpha delta grad V_w(s)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Semi-Gradient TD 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Semi-Gradient TD 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Semi-Gradient TD 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- semi-gradient 简化计算，但稳定性依赖算法和采样分布。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Semi-Gradient TD 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Semi-Gradient TD 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于函数近似 RL、TD 学习和深度价值方法基础。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- RL Function Approximation
- Temporal Difference Prediction

### 关联
- TD Error
- Deep Q-Network

### 延伸
- TD Error
- Deep Q-Network

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
