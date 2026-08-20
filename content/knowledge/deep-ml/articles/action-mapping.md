---
id: article-action-mapping
slug: action-mapping
title: Action Mapping：概念、直觉与边界
concepts:
- action-mapping
learning_units:
- action-mapping-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Action Mapping
- hierarchical action space
- reinforcement learning
- intermediate
- markov decision process
- latent action space
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
  id: article-plan-action-mapping
  covered_concepts: 1
  primary_concept: action-mapping
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
# Action Mapping：概念、直觉与边界

把模型输出或抽象动作转换为环境可执行动作的过程。

关键词：Action Mapping
- hierarchical action space
- reinforcement learning
- intermediate
- markov decision process
- latent action space
- theory

## 为什么需要它

模型输出空间和真实环境动作空间可能不同。动作映射连接两者。

## 核心直觉

- 输入：Action Mapping 所处理的数据、状态或评价对象。
- 操作：映射要保持动作语义、边界约束和可执行性。
- 观察结果：模型输出空间和真实环境动作空间可能不同。动作映射连接两者。

它像把策略想法翻译成控制指令。

例子：机器人策略输出归一化数值，再映射到关节控制范围。

## 数学定义

### 表达方式

$$
a_t=g(u_t),\qquad u_t\sim\pi_\theta(\cdot\mid s_t),\quad a_t\in\mathcal A_{\mathrm{env}}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Action Mapping 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Action Mapping 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Action Mapping 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 动作映射错误会让好策略表现很差。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Action Mapping 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Action Mapping 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于机器人、游戏控制、离散化动作和安全约束。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Markov Decision Process

### 关联
- Latent Action Space

### 延伸
- Latent Action Space

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
