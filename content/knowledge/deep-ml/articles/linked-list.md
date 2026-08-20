---
id: article-linked-list
slug: linked-list
title: Linked List：概念、直觉与边界
concepts:
- linked-list
learning_units:
- linked-list-overview
domain: data_structures
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Linked List
- linked lists
- data structures
- beginner
- stack and queue
- lru cache
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
  id: article-plan-linked-list
  covered_concepts: 1
  primary_concept: linked-list
confidence:
  concept: 0.94
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
# Linked List：概念、直觉与边界

由节点和指针连接起来的线性数据结构。

关键词：Linked List
- linked lists
- data structures
- beginner
- stack and queue
- lru cache
- theory

## 为什么需要它

数组适合随机访问，但中间插入删除成本高。链表提供另一种组织方式。

## 核心直觉

- 输入：Linked List 所处理的数据、状态或评价对象。
- 操作：链表节点通常包含值和 next 指针。双向链表还包含 prev 指针。
- 观察结果：数组适合随机访问，但中间插入删除成本高。链表提供另一种组织方式。

它像一串纸条。每张纸条都指向下一张。

例子：实现 LRU 缓存时，双向链表可快速移动节点。

## 数学定义

### 表达方式

$$
\operatorname{node}_i=(v_i,p_{i+1}),\qquad p_{i+1}\in\{\varnothing,\operatorname{addr}(\operatorname{node}_{i+1})\}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Linked List 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Linked List 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Linked List 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 链表不是数组替代品。它随机访问较慢。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Linked List 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Linked List 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于缓存、队列、图邻接表和算法题训练。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- 暂无明确结构化关系。

### 关联
- Stack and Queue
- LRU Cache

### 延伸
- Stack and Queue
- LRU Cache

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
