---
id: article-lru-cache
slug: lru-cache
title: LRU Cache：概念、直觉与边界
concepts:
- lru-cache
learning_units:
- lru-cache-overview
domain: data_structures
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- LRU Cache
- LRU
- data structures
- intermediate
- hash table
- linked list
- key value store
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
  id: article-plan-lru-cache
  covered_concepts: 1
  primary_concept: lru-cache
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
# LRU Cache：概念、直觉与边界

淘汰最近最少使用项的缓存策略和数据结构组合。

关键词：LRU Cache
- LRU
- data structures
- intermediate
- hash table
- linked list
- key value store
- theory

## 为什么需要它

缓存空间有限。LRU 用访问时间近似判断哪些数据更值得保留。

## 核心直觉

- 输入：LRU Cache 所处理的数据、状态或评价对象。
- 操作：常见实现结合哈希表和双向链表，兼顾查找和移动效率。
- 观察结果：缓存空间有限。LRU 用访问时间近似判断哪些数据更值得保留。

它像书桌只留最近常看的资料。

例子：网页缓存会淘汰很久没访问的页面。

## 数学定义

### 表达方式

`get and put should be O(1)`

此处保留 LRU Cache 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- LRU Cache 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 LRU Cache 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 LRU Cache 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- LRU 不总是最优。周期访问模式可能让它失效。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 LRU Cache 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 LRU Cache 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于数据库、系统缓存、模型服务和面试算法。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Hash Table
- Linked List

### 关联
- Key-Value Store

### 延伸
- Key-Value Store

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
