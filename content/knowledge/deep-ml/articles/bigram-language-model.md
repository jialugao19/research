---
id: article-bigram-language-model
slug: bigram-language-model
title: Bigram Language Model：模型结构与训练要点
concepts:
- bigram-language-model
learning_units:
- bigram-language-model-overview
domain: nlp
level: beginner
content_type: model
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Bigram Language Model
- bigram
- nlp
- beginner
- probability
- tokenization
- language modeling
- model
profile:
  required_sections:
  - 为什么需要它
  - 结构直觉
  - 数学定义
  - 训练与推理
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-bigram-language-model
  covered_concepts: 1
  primary_concept: bigram-language-model
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Bigram Language Model：模型结构与训练要点

用前一个 token 预测下一个 token 的简单语言模型。

关键词：Bigram Language Model
- bigram
- nlp
- beginner
- probability
- tokenization
- language modeling
- model

## 为什么需要它

复杂语言模型难以直接理解。bigram 模型提供最小可解释起点。

## 结构直觉

- 输入：Bigram Language Model 所处理的数据、状态或评价对象。
- 操作：模型学习相邻 token 的条件概率。它不能捕捉长距离上下文。
- 观察结果：复杂语言模型难以直接理解。bigram 模型提供最小可解释起点。

它像只根据上一个词猜下一个词。

例子：统计语料中某词后面最常出现的下一个词。

## 数学定义

### 表达方式

$$
p(x_t | x_{t-1})
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Bigram Language Model 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Bigram Language Model 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 训练与推理

- 记录输入特征、目标变量、损失函数和评价指标。
- 分别检查训练误差、验证误差和线上分布漂移。
- 关注初始化、正则化和学习率对稳定性的影响。

## 常见误区

### 概念误解
- bigram 简单，不代表无用。它适合教学和基线。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Bigram Language Model 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Bigram Language Model 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于语言模型入门、平滑方法教学和快速基线。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability
- Tokenization

### 关联
- Language Modeling

### 延伸
- Language Modeling

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
