---
id: article-reward-normalization
slug: reward-normalization
title: Reward Normalization：概念、直觉与边界
concepts:
- reward-normalization
learning_units:
- reward-normalization-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Reward Normalization
- exponential weighted average rewards
- weighted average rewards
- reinforcement learning
- intermediate
- reward baseline
- normalization
- model calibration
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
  id: article-plan-reward-normalization
  covered_concepts: 1
  primary_concept: reward-normalization
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
- title: Proximal Policy Optimization Algorithms
  url: https://arxiv.org/abs/1707.06347
  type: paper
---
# Reward Normalization：概念、直觉与边界

对奖励或回报做缩放、中心化或裁剪以稳定训练的处理方法。

关键词：Reward Normalization
- exponential weighted average rewards
- weighted average rewards
- reinforcement learning
- intermediate
- reward baseline
- normalization
- model calibration

## 为什么需要它

奖励尺度差异会影响优化步长和训练稳定性。归一化能缓解这个问题。

## 核心直觉

- 输入：Reward Normalization 所处理的数据、状态或评价对象。
- 操作：常见处理包括减均值、除标准差、裁剪和滑动统计。
- 观察结果：奖励尺度差异会影响优化步长和训练稳定性。归一化能缓解这个问题。

它像把不同任务的分数先放到相近刻度上。

例子：并行环境训练时，可用运行统计量归一化奖励。

## 数学定义

### 表达方式

$$
r_norm = (r - mean) / std
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Reward Normalization 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Reward Normalization 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Reward Normalization 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 归一化会改变学习信号尺度。记录原始奖励仍然重要。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Reward Normalization 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Reward Normalization 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 PPO、策略梯度和多任务强化学习。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Reward Baseline
- Normalization

### 关联
- Model Calibration

### 延伸
- Model Calibration

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Proximal Policy Optimization Algorithms**：https://arxiv.org/abs/1707.06347。用途：追溯原始方法、关键假设和实验设定。
