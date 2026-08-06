---
id: article-chain-rule
slug: chain-rule
title: Chain Rule：概念、直觉与边界
concepts:
- chain-rule
learning_units:
- chain-rule-overview
domain: calculus
level: foundation
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Chain Rule
- calculus
- foundation
- calculus basics
- backpropagation
- jacobian matrix
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
  id: article-plan-chain-rule
  covered_concepts: 1
  primary_concept: chain-rule
confidence:
  concept: 0.94
  prerequisite: 0.94
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Chain Rule：概念、直觉与边界

计算复合函数导数的基本规则。

关键词：Chain Rule
- calculus
- foundation
- calculus basics
- backpropagation
- jacobian matrix
- theory

## 为什么需要它

神经网络由很多函数嵌套组成。链式法则解释梯度如何逐层传递。

## 核心直觉

- 输入：Chain Rule 所处理的数据、状态或评价对象。
- 操作：复合函数的导数等于外层导数和内层导数的乘积。
- 观察结果：神经网络由很多函数嵌套组成。链式法则解释梯度如何逐层传递。

它像追踪影响链条。外层变化要乘以内层变化。

例子：反向传播会从损失开始，按链式法则把梯度传回每一层。

## 数学定义

### 表达方式

$$
d f(g(x)) / dx = f'(g(x)) g'(x)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Chain Rule 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Chain Rule 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Chain Rule 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 链式法则不是只适用于一维函数。多维情形需要 Jacobian。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Chain Rule 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Chain Rule 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于反向传播、自动微分和矩阵微积分。维度检查很重要。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Calculus Basics

### 关联
- Backpropagation
- Jacobian Matrix

### 延伸
- Backpropagation
- Jacobian Matrix

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
