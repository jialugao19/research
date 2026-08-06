---
id: article-steering-vector
slug: steering-vector
title: Steering Vector：概念、直觉与边界
concepts:
- steering-vector
learning_units:
- steering-vector-overview
domain: llm
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Steering Vector
- llm
- advanced
- hidden state
- linear algebra
- residual stream
- model calibration
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
  id: article-plan-steering-vector
  covered_concepts: 1
  primary_concept: steering-vector
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: Attention Is All You Need
  url: https://arxiv.org/abs/1706.03762
  type: paper
---
# Steering Vector：概念、直觉与边界

在表示空间中用于引导模型行为或语义方向的向量。

关键词：Steering Vector
- llm
- advanced
- hidden state
- linear algebra
- residual stream
- model calibration
- theory

## 为什么需要它

模型内部表示包含行为方向。steering vector 试图用向量方式调节输出。

## 核心直觉

- 输入：Steering Vector 所处理的数据、状态或评价对象。
- 操作：常见做法是从对比样本中估计方向，再在激活中加入或投影该方向。
- 观察结果：模型内部表示包含行为方向。steering vector 试图用向量方式调节输出。

它像在模型思考空间里推一个方向。

例子：用安全和不安全回答的表示差估计一个行为方向。

## 数学定义

### 表达方式

$$
activation' = activation + alpha \cdot  steering_vector
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Steering Vector 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Steering Vector 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Steering Vector 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 向量引导不是可靠控制。强度和层位置会影响结果。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Steering Vector 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Steering Vector 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于模型解释、可控生成和表示编辑研究。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Hidden State
- Linear Algebra

### 关联
- Residual Stream
- Model Calibration

### 延伸
- Residual Stream
- Model Calibration

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Attention Is All You Need**：https://arxiv.org/abs/1706.03762。用途：追溯原始方法、关键假设和实验设定。
