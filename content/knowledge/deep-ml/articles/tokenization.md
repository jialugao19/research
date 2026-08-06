---
id: article-tokenization
slug: tokenization
title: Tokenization：概念、直觉与边界
concepts:
- tokenization
learning_units:
- tokenization-overview
domain: nlp
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Tokenization
- tokenizer
- nlp
- beginner
- probability
- word embeddings
- positional encoding
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
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-tokenization
  covered_concepts: 1
  primary_concept: tokenization
confidence:
  concept: 0.94
  prerequisite: 0.94
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
---
# Tokenization：概念、直觉与边界

把原始文本切分成模型可处理 token 的过程。

关键词：Tokenization
- tokenizer
- nlp
- beginner
- probability
- word embeddings
- positional encoding
- theory

## 为什么需要它

语言模型不能直接理解整段字符串。tokenization 把文本变成离散编号序列。

## 核心直觉

- 输入：Tokenization 所处理的数据、状态或评价对象。
- 操作：常见方法包括 wordpiece、BPE 和 unigram。词表大小会影响长度和表示粒度。
- 观察结果：语言模型不能直接理解整段字符串。tokenization 把文本变成离散编号序列。

它像把句子拆成模型词块。词块不一定等于自然语言里的词。

例子：英文单词 unfamiliar 可能被拆成多个子词 token。

## 数学定义

### 表达方式

`文本会被映射为 token ids，例如 [101, 7592, 102]`

此处保留 Tokenization 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Tokenization 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Tokenization 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Tokenization 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- token 不是字符，也不一定是完整单词。不同 tokenizer 的结果可能不同。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Tokenization 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Tokenization 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于语言模型、检索和文本分类。长文本成本常由 token 数决定。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability

### 关联
- Word Embeddings
- Positional Encoding

### 延伸
- Word Embeddings
- Positional Encoding

## 延伸阅读

- **Attention Is All You Need**：https://arxiv.org/abs/1706.03762。用途：追溯原始方法、关键假设和实验设定。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
