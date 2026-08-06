---
id: article-directional-stripe-tiling
slug: directional-stripe-tiling
title: Directional Stripe Tiling：概念、直觉与边界
concepts:
- directional-stripe-tiling
learning_units:
- directional-stripe-tiling-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Directional Stripe Tiling
- directional stripe tilings
- stripe tilings
- reinforcement learning
- advanced
- tile coding
- feature receptive field
- coarse coding
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
  id: article-plan-directional-stripe-tiling
  covered_concepts: 1
  primary_concept: directional-stripe-tiling
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Directional Stripe Tiling：概念、直觉与边界

用带方向的条纹式覆盖对连续状态空间做特征编码的方法。

关键词：Directional Stripe Tiling
- directional stripe tilings
- stripe tilings
- reinforcement learning
- advanced
- tile coding
- feature receptive field
- coarse coding

## 为什么需要它

某些任务中的价值变化沿特定方向更明显。普通网格未必高效。

## 核心直觉

- 输入：Directional Stripe Tiling 所处理的数据、状态或评价对象。
- 操作：方向性 tiling 通过不同角度和偏移产生泛化模式。
- 观察结果：某些任务中的价值变化沿特定方向更明显。普通网格未必高效。

它像用斜向条纹覆盖地图，让相同方向的区域共享特征。

例子：连续控制中可用多组斜向 tiling 表示状态。

## 数学定义

### 表达方式

`phi_i(s)=1 if s lies inside stripe_i`

此处保留 Directional Stripe Tiling 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Directional Stripe Tiling 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Directional Stripe Tiling 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Directional Stripe Tiling 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 条纹方向是归纳偏置。方向选错会影响学习。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Directional Stripe Tiling 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Directional Stripe Tiling 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于函数近似 RL、tile coding 扩展和特征可视化。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Tile Coding
- Feature Receptive Field

### 关联
- Coarse Coding
- Kanerva Coding

### 延伸
- Coarse Coding
- Kanerva Coding

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
