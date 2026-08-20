---
id: article-domain-randomization
slug: domain-randomization
title: Domain Randomization：概念、直觉与边界
concepts:
- domain-randomization
learning_units:
- domain-randomization-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Domain Randomization
- randomization robust policy
- reinforcement learning
- advanced
- simulation environment
- domain adaptation
- robust optimization
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
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-domain-randomization
  covered_concepts: 1
  primary_concept: domain-randomization
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
# Domain Randomization：概念、直觉与边界

在训练中随机改变环境参数，以提升策略对真实变化的鲁棒性。

关键词：Domain Randomization
- randomization robust policy
- reinforcement learning
- advanced
- simulation environment
- domain adaptation
- robust optimization
- curriculum learning

## 为什么需要它

仿真策略迁移到真实环境时，常遇到 sim-to-real gap。

## 核心直觉

- 输入：Domain Randomization 所处理的数据、状态或评价对象。
- 操作：随机化对象可包括视觉、动力学、传感器噪声和初始状态。
- 观察结果：仿真策略迁移到真实环境时，常遇到 sim-to-real gap。

它像训练时故意换光线、摩擦和质量，让策略别依赖细节。

例子：机器人抓取训练可随机化物体质量和桌面摩擦。

## 数学定义

### 表达方式

$$
\xi\sim p(\xi),\qquad \theta^{\star}=\underset{\theta}{\operatorname{arg\,max}}\ \mathbb E_{\xi}[J(\pi_\theta;\xi)]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Domain Randomization 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Domain Randomization 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Domain Randomization 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 随机化范围过大也会让任务变难，甚至学不到有效策略。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Domain Randomization 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Domain Randomization 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于机器人、自动驾驶、仿真训练和鲁棒策略学习。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Simulation Environment
- Domain Adaptation

### 关联
- Robust Optimization
- Curriculum Learning

### 延伸
- Robust Optimization
- Curriculum Learning

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
