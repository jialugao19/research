---
id: article-tile-coding
slug: tile-coding
title: Tile Coding：概念、直觉与边界
concepts:
- tile-coding
learning_units:
- tile-coding-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Tile Coding
- reinforcement learning
- advanced
- rl function approximation
- one hot encoding
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
  id: article-plan-tile-coding
  covered_concepts: 1
  primary_concept: tile-coding
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Tile Coding：概念、直觉与边界

把连续状态空间用多组错开的网格编码成稀疏特征的方法。

关键词：Tile Coding
- reinforcement learning
- advanced
- rl function approximation
- one hot encoding
- theory

## 为什么需要它

连续状态很难直接用表格法处理。Tile coding 把连续空间离散成可泛化特征。

## 核心直觉

- 输入：Tile Coding 所处理的数据、状态或评价对象。
- 操作：多个 tiling 提供粗编码。线性模型可利用这些稀疏特征学习价值。
- 观察结果：连续状态很难直接用表格法处理。Tile coding 把连续空间离散成可泛化特征。

它像用多层半透明方格覆盖地图，位置会点亮几格。

例子：山地车控制任务可用 tile coding 表示位置和速度。

## 数学定义

### 表达方式

`features(s) 是多个 tile 的 one-hot 组合`

此处保留 Tile Coding 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Tile Coding 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Tile Coding 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Tile Coding 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- Tile coding 是特征工程，不是神经网络结构。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Tile Coding 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Tile Coding 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于经典 RL、连续控制教学和轻量函数近似。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- RL Function Approximation

### 关联
- One-Hot Encoding

### 延伸
- One-Hot Encoding

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
