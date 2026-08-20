---
id: article-running-median
slug: running-median
title: Running Median：概念、直觉与边界
concepts:
- running-median
learning_units:
- running-median-overview
domain: data_structures
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Running Median
- median stream
- data structures
- intermediate
- heap priority queue
- histogram
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
  id: article-plan-running-median
  covered_concepts: 1
  primary_concept: running-median
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
- title: Introduction to Algorithms
  url: https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
  type: textbook
- title: Python Data Structures Tutorial
  url: https://docs.python.org/3/tutorial/datastructures.html
  type: official_docs
---
# Running Median：概念、直觉与边界

在数据流不断到来时动态维护当前中位数的数据结构问题。

关键词：Running Median
- median stream
- data structures
- intermediate
- heap priority queue
- histogram
- theory

## 为什么需要它

全部排序成本高，数据流还在变化。running median 要在线更新。

## 核心直觉

- 输入：Running Median 所处理的数据、状态或评价对象。
- 操作：常用两个堆维护较小一半和较大一半。
- 观察结果：全部排序成本高，数据流还在变化。running median 要在线更新。

它像每来一个新数，就马上知道中间位置在哪里。

例子：实时监控延迟时，可以维护当前延迟中位数。

## 数学定义

### 表达方式

$$
m_t=\begin{cases}\max(H_L),&|H_L|>|H_R|,\\\frac{\max(H_L)+\min(H_R)}{2},&|H_L|=|H_R|,\end{cases}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Running Median 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Running Median 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Running Median 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 平均值不能替代中位数。异常值会显著影响平均值。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Running Median 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Running Median 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于流式统计、监控、金融数据和在线算法。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Heap and Priority Queue

### 关联
- Histogram

### 延伸
- Histogram

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
