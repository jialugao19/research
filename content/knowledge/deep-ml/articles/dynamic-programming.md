---
id: article-dynamic-programming
slug: dynamic-programming
title: Dynamic Programming：概念、直觉与边界
concepts:
- dynamic-programming
learning_units:
- dynamic-programming-overview
domain: algorithms
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Dynamic Programming
- DP
- algorithms
- intermediate
- recursion
- time complexity
- bellman equation
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
  id: article-plan-dynamic-programming
  covered_concepts: 1
  primary_concept: dynamic-programming
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
---
# Dynamic Programming：概念、直觉与边界

把重复子问题的结果保存下来，以避免重复计算的算法方法。

关键词：Dynamic Programming
- DP
- algorithms
- intermediate
- recursion
- time complexity
- bellman equation
- theory

## 为什么需要它

递归搜索可能反复解决相同小问题。动态规划用缓存减少浪费。

## 核心直觉

- 输入：Dynamic Programming 所处理的数据、状态或评价对象。
- 操作：动态规划通常需要状态定义、状态转移、初始条件和计算顺序。
- 观察结果：递归搜索可能反复解决相同小问题。动态规划用缓存减少浪费。

它像做题时记草稿。算过的中间答案不用再算一遍。

例子：背包问题中，状态可以表示前 i 个物品和容量 j 下的最好价值。

## 数学定义

### 表达方式

`常见形式是 dp[i] = best(dp[i-1], dp[i-2] + value)`

此处保留 Dynamic Programming 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Dynamic Programming 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Dynamic Programming 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Dynamic Programming 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 动态规划不是套模板。状态定义错了，转移式再漂亮也没用。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Dynamic Programming 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Dynamic Programming 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于路径规划、序列匹配、资源分配和强化学习。状态太多时会遇到维度灾难。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Recursion
- Time Complexity

### 关联
- Bellman Equation

### 延伸
- Bellman Equation

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
