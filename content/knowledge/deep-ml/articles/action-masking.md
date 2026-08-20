---
id: article-action-masking
slug: action-masking
title: Action Masking：概念、直觉与边界
concepts:
- action-masking
learning_units:
- action-masking-overview
domain: reinforcement_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Action Masking
- invalid action mask
- reinforcement learning
- intermediate
- policy gradient
- softmax function
- grammar constrained decoding
- optimal policy extraction
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
  id: article-plan-action-masking
  covered_concepts: 1
  primary_concept: action-masking
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Action Masking：概念、直觉与边界

在策略输出中屏蔽当前状态下非法动作的约束方法。

关键词：Action Masking
- invalid action mask
- reinforcement learning
- intermediate
- policy gradient
- softmax function
- grammar constrained decoding
- optimal policy extraction

## 为什么需要它

许多环境并非每一步都允许所有动作。直接采样可能浪费或出错。

## 核心直觉

- 输入：Action Masking 所处理的数据、状态或评价对象。
- 操作：常见做法是在 logits 上给非法动作加极小值，再做 softmax。
- 观察结果：许多环境并非每一步都允许所有动作。直接采样可能浪费或出错。

它像菜单上把当前不能点的选项灰掉。

例子：棋类游戏中，已经被占用的位置不能再落子。

## 数学定义

### 表达方式

$$
\tilde z_a=\begin{cases}z_a,&m_a=1,\\-\infty,&m_a=0,\end{cases}\qquad \pi(a\mid s)=\operatorname{softmax}(\tilde z)_a
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Action Masking 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Action Masking 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Action Masking 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- mask 要来自环境规则，不能泄露未来答案。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Action Masking 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Action Masking 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于棋类、组合优化、推荐约束和工具调用策略。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Policy Gradient
- Softmax Function

### 关联
- Grammar-Constrained Decoding
- Optimal Policy Extraction

### 延伸
- Grammar-Constrained Decoding
- Optimal Policy Extraction

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
