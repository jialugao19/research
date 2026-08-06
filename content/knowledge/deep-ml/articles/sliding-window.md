---
id: article-sliding-window
slug: sliding-window
title: Sliding Window：概念、直觉与边界
concepts:
- sliding-window
learning_units:
- sliding-window-overview
domain: algorithms
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Sliding Window
- window
- algorithms
- beginner
- arrays
- hash table
- two pointers
- prefix sum
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
  id: article-plan-sliding-window
  covered_concepts: 1
  primary_concept: sliding-window
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
# Sliding Window：概念、直觉与边界

维护一个移动区间来处理连续子数组或子串的方法。

关键词：Sliding Window
- window
- algorithms
- beginner
- arrays
- hash table
- two pointers
- prefix sum

## 为什么需要它

很多连续区间问题如果重复扫描会很慢。滑动窗口复用上一步状态。

## 核心直觉

- 输入：Sliding Window 所处理的数据、状态或评价对象。
- 操作：窗口可以固定长度，也可以按条件伸缩。关键是维护窗口内状态。
- 观察结果：很多连续区间问题如果重复扫描会很慢。滑动窗口复用上一步状态。

它像拿一个窗口沿序列移动。每次只加入新元素，移出旧元素。

例子：求长度为 k 的子数组最大平均值，可用固定窗口。

## 数学定义

### 表达方式

`每步更新 left、right 和窗口统计量`

此处保留 Sliding Window 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Sliding Window 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Sliding Window 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Sliding Window 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 滑动窗口需要单调或可维护条件。不是所有子序列问题都适用。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Sliding Window 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Sliding Window 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于字符串、数组、时间序列和流式统计。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Arrays
- Hash Table

### 关联
- Two Pointers
- Prefix Sum

### 延伸
- Two Pointers
- Prefix Sum

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
