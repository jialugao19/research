---
id: article-positional-encoding
slug: positional-encoding
title: Positional Encoding：概念、直觉与边界
concepts:
- positional-encoding
learning_units:
- positional-encoding-overview
domain: nlp
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Positional Encoding
- position encoding
- nlp
- intermediate
- tokenization
- linear algebra
- transformer architecture
- attention mechanism
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-positional-encoding
  covered_concepts: 1
  primary_concept: positional-encoding
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
- title: Attention Is All You Need
  url: https://arxiv.org/abs/1706.03762
  type: paper
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
---
# Positional Encoding：概念、直觉与边界

向排列等变的自注意力表示注入绝对或相对顺序信息的方法。

关键词：Positional Encoding
- position encoding
- nlp
- intermediate
- tokenization
- linear algebra
- transformer architecture
- attention mechanism

## 为什么需要它

自注意力本身不天然知道顺序。位置编码让模型区分第一个词和后面的词。

## 核心直觉

不含位置信息的 self-attention 对排列等变：调换 token 顺序，输出只会跟着调换，无法表达顺序差异。

token embedding 表达内容，位置表示补充顺序。原始 Transformer 将二者相加而不改变维度。

不同位置方法的外推行为不同，应明确训练与部署长度。

## 数学定义

### 表达方式

`原始 Transformer 使用 sin 和 cos 在不同频率上编码位置`

此处保留 Positional Encoding 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Positional Encoding 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Positional Encoding 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Positional Encoding 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 相加不是注入位置的唯一方式，只是保持 d_model 不变的简洁设计；位置编码也不自动保证超出训练长度后的外推。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Positional Encoding 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Positional Encoding 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 Transformer、视觉 Transformer 和长上下文模型。长序列外推是常见挑战。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Tokenization
- Linear Algebra

### 关联
- Transformer Architecture
- Attention Mechanism

### 延伸
- Transformer Architecture
- Attention Mechanism

## 延伸阅读

- **Attention Is All You Need**：https://arxiv.org/abs/1706.03762。用途：追溯原始方法、关键假设和实验设定。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
