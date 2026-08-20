---
id: article-error-dependent-weight-updates
slug: error-dependent-weight-updates
title: Error-Dependent Weight Updates：概念、直觉与边界
concepts:
- error-dependent-weight-updates
learning_units:
- error-dependent-weight-updates-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Error-Dependent Weight Updates
- multiple weight updates
- reinforcement learning
- intermediate
- gradient descent
- td error
- delta rule
- semi gradient td
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
  id: article-plan-error-dependent-weight-updates
  covered_concepts: 1
  primary_concept: error-dependent-weight-updates
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
# Error-Dependent Weight Updates：概念、直觉与边界

根据预测误差大小和方向调整模型权重的学习规则。

关键词：Error-Dependent Weight Updates
- multiple weight updates
- reinforcement learning
- intermediate
- gradient descent
- td error
- delta rule
- semi gradient td

## 为什么需要它

模型需要知道该往哪个方向改，以及改多少。

## 核心直觉

- 输入：Error-Dependent Weight Updates 所处理的数据、状态或评价对象。
- 操作：误差信号可来自监督学习损失、TD error 或其它反馈。
- 观察结果：模型需要知道该往哪个方向改，以及改多少。

它像根据偏差大小调方向盘。

例子：价值函数近似可用 TD error 乘以特征向量更新权重。

## 数学定义

### 表达方式

$$
w_{t+1}=w_t+\alpha\,\delta_t\,x_t
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Error-Dependent Weight Updates 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Error-Dependent Weight Updates 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Error-Dependent Weight Updates 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 误差越大不一定步子越大，学习率和裁剪也会限制更新。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Error-Dependent Weight Updates 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Error-Dependent Weight Updates 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于感知机、TD 学习、线性近似和神经网络训练。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Gradient Descent
- TD Error

### 关联
- Delta Rule
- Semi-Gradient TD

### 延伸
- Delta Rule
- Semi-Gradient TD

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
