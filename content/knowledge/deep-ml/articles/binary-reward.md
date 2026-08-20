---
id: article-binary-reward
slug: binary-reward
title: Binary Reward：概念、直觉与边界
concepts:
- binary-reward
learning_units:
- binary-reward-overview
domain: reinforcement_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Binary Reward
- binary rewards
- reinforcement learning
- beginner
- verifiable reward
- reward shaping
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
  id: article-plan-binary-reward
  covered_concepts: 1
  primary_concept: binary-reward
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
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Binary Reward：概念、直觉与边界

只取成功或失败两个值的奖励信号。

关键词：Binary Reward
- binary rewards
- reinforcement learning
- beginner
- verifiable reward
- reward shaping
- theory

## 为什么需要它

有些任务只能判断结果是否正确。二值奖励是最简单反馈。

## 核心直觉

- 输入：Binary Reward 所处理的数据、状态或评价对象。
- 操作：二值奖励清晰但稀疏。探索和信用分配会更难。
- 观察结果：有些任务只能判断结果是否正确。二值奖励是最简单反馈。

它像只给通过或不通过。

例子：数学题最终答案正确给 1，错误给 0。

## 数学定义

### 表达方式

$$
R_t\in\{0,1\}\quad\text{or}\quad R_t\in\{-1,1\}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Binary Reward 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Binary Reward 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Binary Reward 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 二值奖励简单，不代表训练容易。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Binary Reward 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Binary Reward 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于验证式训练、游戏胜负、单元测试和任务完成评估。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Verifiable Reward

### 关联
- Reward Shaping

### 延伸
- Reward Shaping

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
