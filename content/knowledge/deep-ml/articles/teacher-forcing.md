---
id: article-teacher-forcing
slug: teacher-forcing
title: Teacher Forcing：概念、直觉与边界
concepts:
- teacher-forcing
learning_units:
- teacher-forcing-overview
domain: nlp
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Teacher Forcing
- nlp
- intermediate
- sequence to sequence
- language modeling
- causal mask
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
  id: article-plan-teacher-forcing
  covered_concepts: 1
  primary_concept: teacher-forcing
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Teacher Forcing：概念、直觉与边界

训练自回归序列模型时，把真实上一个 token 作为下一步输入的方法。

关键词：Teacher Forcing
- nlp
- intermediate
- sequence to sequence
- language modeling
- causal mask
- theory

## 为什么需要它

序列生成训练需要稳定对齐目标。teacher forcing 能让训练更快收敛。

## 核心直觉

- 输入：Teacher Forcing 所处理的数据、状态或评价对象。
- 操作：训练时使用真实历史。推理时使用模型自己生成的历史。
- 观察结果：序列生成训练需要稳定对齐目标。teacher forcing 能让训练更快收敛。

它像练习写句子时，每一步都给正确前文作参考。

例子：机器翻译训练常用目标句子的前一个 token 作为 decoder 输入。

## 数学定义

### 表达方式

$$
decoder_input_t = target_{t-1}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Teacher Forcing 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Teacher Forcing 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Teacher Forcing 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- teacher forcing 会带来训练和推理不一致。暴露偏差需要关注。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Teacher Forcing 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Teacher Forcing 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于翻译、摘要和语言模型训练。可配合 scheduled sampling。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Sequence-to-Sequence
- Language Modeling

### 关联
- Causal Mask

### 延伸
- Causal Mask

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
