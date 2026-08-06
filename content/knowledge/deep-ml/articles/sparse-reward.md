---
id: article-sparse-reward
slug: sparse-reward
title: Sparse Reward：概念、直觉与边界
concepts:
- sparse-reward
learning_units:
- sparse-reward-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Sparse Reward
- sparse rewards
- reinforcement learning
- intermediate
- reward shaping
- exploration exploitation
- sample efficiency
- curriculum learning
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
  id: article-plan-sparse-reward
  covered_concepts: 1
  primary_concept: sparse-reward
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
# Sparse Reward：概念、直觉与边界

只有少数状态或任务完成时才提供反馈的奖励设定。

关键词：Sparse Reward
- sparse rewards
- reinforcement learning
- intermediate
- reward shaping
- exploration exploitation
- sample efficiency
- curriculum learning

## 为什么需要它

反馈稀少时，智能体很难知道哪些早期动作有帮助。

## 核心直觉

- 输入：Sparse Reward 所处理的数据、状态或评价对象。
- 操作：稀疏奖励常需要更强探索、奖励塑形、课程学习或示范数据。
- 观察结果：反馈稀少时，智能体很难知道哪些早期动作有帮助。

它像走迷宫时只有到终点才知道自己有没有成功。

例子：机器人抓取任务可能只有成功抓起物体时给奖励。

## 数学定义

### 表达方式

`r_t = 0 for most steps, r_T != 0 at success`

此处保留 Sparse Reward 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Sparse Reward 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Sparse Reward 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Sparse Reward 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 稀疏奖励更客观，但训练难度通常更高。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Sparse Reward 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Sparse Reward 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于机器人、游戏、规划任务和目标导向 RL。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Reward Shaping
- Exploration and Exploitation

### 关联
- Sample Efficiency
- Curriculum Learning

### 延伸
- Sample Efficiency
- Curriculum Learning

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
