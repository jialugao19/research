---
id: article-time-complexity
slug: time-complexity
title: Time Complexity：概念、直觉与边界
concepts:
- time-complexity
learning_units:
- time-complexity-overview
domain: algorithms
level: foundation
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Time Complexity
- Big O
- algorithms
- foundation
- sorting algorithms
- binary search
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
  id: article-plan-time-complexity
  covered_concepts: 1
  primary_concept: time-complexity
confidence:
  concept: 0.97
  prerequisite: 1.0
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
# Time Complexity：概念、直觉与边界

用输入规模描述算法运行时间增长速度的方法。

关键词：Time Complexity
- Big O
- algorithms
- foundation
- sorting algorithms
- binary search
- theory

## 为什么需要它

同一个任务可能有很多写法。时间复杂度帮助我们判断哪种写法能处理更大的数据。

## 核心直觉

- 输入：Time Complexity 所处理的数据、状态或评价对象。
- 操作：常见记号包括 O(1)、O(log n)、O(n)、O(n log n) 和 O(n^2)。它关注增长趋势，不关注机器细节。
- 观察结果：同一个任务可能有很多写法。时间复杂度帮助我们判断哪种写法能处理更大的数据。

它像看路程增长。输入翻倍时，程序耗时是大致翻倍，还是变成四倍。

例子：遍历一个长度为 n 的数组需要看 n 个元素。它通常是 O(n)。

## 数学定义

### 表达方式

`二重循环常见复杂度是 O(n^2)。二分查找常见复杂度是 O(log n)`

此处保留 Time Complexity 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Time Complexity 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Time Complexity 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Time Complexity 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 复杂度不是精确秒数。常数、缓存和实现语言仍会影响真实耗时。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Time Complexity 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Time Complexity 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于算法选择、面试训练和性能评估。输入很小时，简单方法也可能足够好。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- 暂无明确结构化关系。

### 关联
- Sorting Algorithms
- Binary Search
- Dynamic Programming

### 延伸
- Sorting Algorithms
- Binary Search
- Dynamic Programming

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
