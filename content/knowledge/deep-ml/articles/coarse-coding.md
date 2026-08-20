---
id: article-coarse-coding
slug: coarse-coding
title: Coarse Coding：概念、直觉与边界
concepts:
- coarse-coding
learning_units:
- coarse-coding-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Coarse Coding
- reinforcement learning
- intermediate
- rl function approximation
- tile coding
- kanerva coding
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
  id: article-plan-coarse-coding
  covered_concepts: 1
  primary_concept: coarse-coding
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Coarse Coding：概念、直觉与边界

用重叠的粗粒度特征表示连续状态空间的方法。

关键词：Coarse Coding
- reinforcement learning
- intermediate
- rl function approximation
- tile coding
- kanerva coding
- theory

## 为什么需要它

连续状态无法直接用小表格存储每个状态价值。

## 核心直觉

- 输入：Coarse Coding 所处理的数据、状态或评价对象。
- 操作：每个状态会激活多个特征，泛化来自特征覆盖区域的重叠。
- 观察结果：连续状态无法直接用小表格存储每个状态价值。

它像用多个重叠探照灯照亮状态空间。

例子：机器人位置可用多个圆形区域特征编码。

## 数学定义

### 表达方式

$$
\hat V(s,w)=w^{\top}x(s),\qquad x_i(s)=\mathbf 1_{\{s\in F_i\}}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Coarse Coding 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Coarse Coding 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Coarse Coding 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 特征太粗会欠拟合，太细又会失去泛化。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Coarse Coding 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Coarse Coding 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于函数近似 RL、连续控制和可解释特征设计。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- RL Function Approximation

### 关联
- Tile Coding
- Kanerva Coding

### 延伸
- Tile Coding
- Kanerva Coding

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
