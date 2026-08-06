---
id: article-quadratic-programming
slug: quadratic-programming
title: Quadratic Programming：概念、直觉与边界
concepts:
- quadratic-programming
learning_units:
- quadratic-programming-overview
domain: optimization
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Quadratic Programming
- QP
- optimization
- advanced
- convex optimization
- positive definite matrix
- portfolio variance
- lagrange multipliers
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
  id: article-plan-quadratic-programming
  covered_concepts: 1
  primary_concept: quadratic-programming
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Quadratic Programming：概念、直觉与边界

目标函数为二次型且约束通常为线性的优化问题。

关键词：Quadratic Programming
- QP
- optimization
- advanced
- convex optimization
- positive definite matrix
- portfolio variance
- lagrange multipliers

## 为什么需要它

很多风险、控制和间隔最大化问题都含二次目标和约束。

## 核心直觉

- 输入：Quadratic Programming 所处理的数据、状态或评价对象。
- 操作：凸二次规划在 Hessian 半正定时有良好求解性质。
- 观察结果：很多风险、控制和间隔最大化问题都含二次目标和约束。

它像在弯曲的碗面上，沿约束边界找最低点。

例子：投资组合方差最小化可写成二次规划。

## 数学定义

### 表达方式

`min 0.5 x^T Q x + c^T x, subject to Ax <= b`

此处保留 Quadratic Programming 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Quadratic Programming 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Quadratic Programming 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Quadratic Programming 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 含二次项不一定就是容易问题。非凸 QP 可能很难。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Quadratic Programming 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Quadratic Programming 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于资产配置、SVM、模型预测控制和资源分配。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Convex Optimization
- Positive Definite Matrix

### 关联
- Portfolio Variance
- Lagrange Multipliers

### 延伸
- Portfolio Variance
- Lagrange Multipliers

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
