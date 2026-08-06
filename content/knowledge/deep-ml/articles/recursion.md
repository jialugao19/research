---
id: article-recursion
slug: recursion
title: Recursion：概念、直觉与边界
concepts:
- recursion
learning_units:
- recursion-overview
domain: algorithms
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Recursion
- algorithms
- beginner
- time complexity
- dynamic programming
- graph traversal
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
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-recursion
  covered_concepts: 1
  primary_concept: recursion
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
- title: Introduction to Algorithms
  url: https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
  type: textbook
- title: Python Data Structures Tutorial
  url: https://docs.python.org/3/tutorial/datastructures.html
  type: official_docs
---
# Recursion：概念、直觉与边界

函数在解决问题时调用自身的编程和算法思想。

关键词：Recursion
- algorithms
- beginner
- time complexity
- dynamic programming
- graph traversal
- theory

## 为什么需要它

有些问题天然由相同结构的小问题组成。递归能直接表达这种结构。

## 核心直觉

- 输入：Recursion 所处理的数据、状态或评价对象。
- 操作：递归必须有终止条件。每次调用也要让问题规模变小。
- 观察结果：有些问题天然由相同结构的小问题组成。递归能直接表达这种结构。

递归像拆盒子。每打开一层，都遇到一个更小但形状相同的问题。

例子：计算树的深度时，可以先算左子树深度，再算右子树深度。

## 数学定义

### 表达方式

`典型形式是 solve(n) 调用 solve(n-1)，直到 n 达到边界`

此处保留 Recursion 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Recursion 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Recursion 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Recursion 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 递归不一定更快。它更像一种表达方式，可能带来额外调用开销。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Recursion 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Recursion 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 递归用于树、图搜索、分治和动态规划。递归层数太深时要注意栈空间。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Time Complexity

### 关联
- Dynamic Programming
- Graph Traversal

### 延伸
- Dynamic Programming
- Graph Traversal

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
