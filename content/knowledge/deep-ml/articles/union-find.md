---
id: article-union-find
slug: union-find
title: Union-Find：概念、直觉与边界
concepts:
- union-find
learning_units:
- union-find-overview
domain: data_structures
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Union-Find
- disjoint set union
- DSU
- data structures
- intermediate
- arrays
- graph traversal
- minimum spanning tree
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
  id: article-plan-union-find
  covered_concepts: 1
  primary_concept: union-find
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
# Union-Find：概念、直觉与边界

维护元素所属连通集合的数据结构。

关键词：Union-Find
- disjoint set union
- DSU
- data structures
- intermediate
- arrays
- graph traversal
- minimum spanning tree

## 为什么需要它

需要频繁合并集合并查询是否连通时，普通图遍历会重复工作。

## 核心直觉

- 输入：Union-Find 所处理的数据、状态或评价对象。
- 操作：路径压缩和按秩合并能让操作非常接近常数时间。
- 观察结果：需要频繁合并集合并查询是否连通时，普通图遍历会重复工作。

它像给每个小组指定代表。合并时只更新代表关系。

例子：判断无向图中两个节点是否连通，可以用 union-find。

## 数学定义

### 表达方式

`find(x) 返回 x 所在集合代表`

此处保留 Union-Find 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Union-Find 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Union-Find 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Union-Find 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- Union-Find 擅长动态合并，不擅长删除边。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Union-Find 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Union-Find 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于连通性、最小生成树和聚类。初始化和路径压缩要写对。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Arrays
- Graph Traversal

### 关联
- Minimum Spanning Tree

### 延伸
- Minimum Spanning Tree

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Python Data Structures Tutorial**：https://docs.python.org/3/tutorial/datastructures.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
