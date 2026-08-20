---
id: article-group-relative-policy-optimization
slug: group-relative-policy-optimization
title: Group Relative Policy Optimization：概念、直觉与边界
concepts:
- group-relative-policy-optimization
learning_units:
- group-relative-policy-optimization-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Group Relative Policy Optimization
- GRPO
- GRPO objective
- reinforcement learning
- advanced
- policy optimization
- reward modeling
- proximal policy optimization
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
  id: article-plan-group-relative-policy-optimization
  covered_concepts: 1
  primary_concept: group-relative-policy-optimization
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
- title: Proximal Policy Optimization Algorithms
  url: https://arxiv.org/abs/1707.06347
  type: paper
---
# Group Relative Policy Optimization：概念、直觉与边界

用同组样本相对表现构造优化信号的策略优化思路。

关键词：Group Relative Policy Optimization
- GRPO
- GRPO objective
- reinforcement learning
- advanced
- policy optimization
- reward modeling
- proximal policy optimization

## 为什么需要它

训练生成策略时，绝对奖励尺度可能不稳。同组相对比较能降低尺度依赖。

## 核心直觉

- 输入：Group Relative Policy Optimization 所处理的数据、状态或评价对象。
- 操作：方法会比较同组候选的奖励，并用相对优势更新策略。
- 观察结果：训练生成策略时，绝对奖励尺度可能不稳。同组相对比较能降低尺度依赖。

它像把同一道题的多个回答放在一起排名。

例子：生成模型训练中，可对同一提示下多个回答做相对优化。

## 数学定义

### 表达方式

$$
\hat A_i=\frac{r_i-\bar r_G}{s_G+\varepsilon},\qquad \bar r_G=\frac1G\sum_{j=1}^{G}r_j
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Group Relative Policy Optimization 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Group Relative Policy Optimization 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Group Relative Policy Optimization 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 相对优化不能替代奖励质量。奖励错误仍会误导训练。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Group Relative Policy Optimization 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Group Relative Policy Optimization 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于生成策略优化、偏好学习和对齐训练研究。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Policy Optimization
- Reward Modeling

### 关联
- Proximal Policy Optimization
- Reward Baseline

### 延伸
- Proximal Policy Optimization
- Reward Baseline

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Proximal Policy Optimization Algorithms**：https://arxiv.org/abs/1707.06347。用途：追溯原始方法、关键假设和实验设定。
