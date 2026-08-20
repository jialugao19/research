---
id: article-vocabulary
slug: vocabulary
title: Vocabulary：概念、直觉与边界
concepts:
- vocabulary
learning_units:
- vocabulary-overview
domain: nlp
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Vocabulary
- vocabulary size
- nlp
- beginner
- tokenization
- byte pair encoding
- token frequency
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
  id: article-plan-vocabulary
  covered_concepts: 1
  primary_concept: vocabulary
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Vocabulary：概念、直觉与边界

分词器可使用的 token 集合及其 ID 映射。

关键词：Vocabulary
- vocabulary size
- nlp
- beginner
- tokenization
- byte pair encoding
- token frequency
- theory

## 为什么需要它

模型只能处理有限 token ID。词表定义文本如何变成数字。

## 核心直觉

- 输入：Vocabulary 所处理的数据、状态或评价对象。
- 操作：词表大小影响表示能力、序列长度和输出层成本。
- 观察结果：模型只能处理有限 token ID。词表定义文本如何变成数字。

它像模型认识的字典。

例子：BPE 训练后会得到子词词表和 merge 规则。

## 数学定义

### 表达方式

$$
V:\mathcal T\leftrightarrow\{0,1,\ldots,|\mathcal V|-1\}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Vocabulary 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Vocabulary 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Vocabulary 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 词表越大不一定越好。大词表会增加参数和稀疏性。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Vocabulary 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Vocabulary 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分词、语言模型、检索和多语言处理。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Tokenization

### 关联
- Byte Pair Encoding
- Token Frequency

### 延伸
- Byte Pair Encoding
- Token Frequency

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
