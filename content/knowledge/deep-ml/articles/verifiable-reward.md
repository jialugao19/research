---
id: article-verifiable-reward
slug: verifiable-reward
title: Verifiable Reward：概念、直觉与边界
concepts:
- verifiable-reward
learning_units:
- verifiable-reward-overview
domain: reinforcement_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Verifiable Reward
- RLVR
- reinforcement learning
- advanced
- reward modeling
- answer equivalence checking
- binary reward
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
  id: article-plan-verifiable-reward
  covered_concepts: 1
  primary_concept: verifiable-reward
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Verifiable Reward：概念、直觉与边界

可以由规则、程序或外部检查器自动验证的奖励信号。

关键词：Verifiable Reward
- RLVR
- reinforcement learning
- advanced
- reward modeling
- answer equivalence checking
- binary reward
- theory

## 为什么需要它

开放式奖励难以稳定评估。可验证奖励让训练信号更明确。

## 核心直觉

- 输入：Verifiable Reward 所处理的数据、状态或评价对象。
- 操作：奖励通常来自单元测试、数学校验、格式检查或任务规则。
- 观察结果：开放式奖励难以稳定评估。可验证奖励让训练信号更明确。

它像答案能被判题器直接判对错。

例子：代码生成任务可用测试通过率构造奖励。

## 数学定义

### 表达方式

$$
reward = verifier(output, target)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Verifiable Reward 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Verifiable Reward 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Verifiable Reward 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 可验证不等于覆盖完整质量。规则外的好坏可能看不到。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Verifiable Reward 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Verifiable Reward 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于代码模型、数学推理、RLHF 变体和代理训练。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Reward Modeling

### 关联
- Answer Equivalence Checking
- Binary Reward

### 延伸
- Answer Equivalence Checking
- Binary Reward

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
