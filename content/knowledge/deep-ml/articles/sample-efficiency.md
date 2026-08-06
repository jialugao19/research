---
id: article-sample-efficiency
slug: sample-efficiency
title: Sample Efficiency：概念、直觉与边界
concepts:
- sample-efficiency
learning_units:
- sample-efficiency-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Sample Efficiency
- sample
- reinforcement learning
- intermediate
- markov decision process
- replay buffer
- dyna q
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
  id: article-plan-sample-efficiency
  covered_concepts: 1
  primary_concept: sample-efficiency
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Sample Efficiency：概念、直觉与边界

算法用较少交互样本学到有效策略的能力。

关键词：Sample Efficiency
- sample
- reinforcement learning
- intermediate
- markov decision process
- replay buffer
- dyna q
- theory

## 为什么需要它

真实环境交互昂贵或有风险。样本效率决定训练成本。

## 核心直觉

- 输入：Sample Efficiency 所处理的数据、状态或评价对象。
- 操作：提升方式包括经验回放、模型学习、离线数据和更强先验。
- 观察结果：真实环境交互昂贵或有风险。样本效率决定训练成本。

它像学生用更少练习题掌握同样能力。

例子：机器人训练中，样本效率差会导致真实试验成本过高。

## 数学定义

### 表达方式

$$
performance per environment step
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Sample Efficiency 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Sample Efficiency 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Sample Efficiency 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 样本效率高不等于最终性能最高。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Sample Efficiency 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Sample Efficiency 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于机器人、游戏、离线 RL 和仿真到现实迁移。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Markov Decision Process

### 关联
- Replay Buffer
- Dyna-Q

### 延伸
- Replay Buffer
- Dyna-Q

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
