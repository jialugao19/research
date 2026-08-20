---
id: article-ngram-model
slug: ngram-model
title: N-gram Model：模型结构与训练要点
concepts:
- ngram-model
learning_units:
- ngram-model-overview
domain: nlp
level: beginner
content_type: model
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- N-gram Model
- n-gram
- ngram
- nlp
- beginner
- tokenization
- token frequency
- bigram language model
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
  id: article-plan-ngram-model
  covered_concepts: 1
  primary_concept: ngram-model
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
# N-gram Model：模型结构与训练要点

用连续 n 个 token 片段表示文本局部统计规律的语言模型。

关键词：N-gram Model
- n-gram
- ngram
- nlp
- beginner
- tokenization
- token frequency
- bigram language model

## 为什么需要它

语言处理中常需要简单统计基线。n-gram 提供可解释的局部上下文方法。

## 结构直觉

- 输入：N-gram Model 所处理的数据、状态或评价对象。
- 操作：n 越大，上下文更丰富，但稀疏性和存储成本也更高。
- 观察结果：语言处理中常需要简单统计基线。n-gram 提供可解释的局部上下文方法。

它像只看最近几个词来猜下一个词。

例子：bigram 模型只用前一个词预测当前词。

## 数学定义

### 表达方式

$$
p(w_{1:T})\approx\prod_{t=1}^{T}p(w_t\mid w_{\max(1,t-n+1):t-1})
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- N-gram Model 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 N-gram Model 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 训练与推理

- 记录输入特征、目标变量、损失函数和评价指标。
- 分别检查训练误差、验证误差和线上分布漂移。
- 关注初始化、正则化和学习率对稳定性的影响。

## 常见误区

### 概念误解
- n-gram 只能捕捉短距离模式，难以表达长程语义。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 N-gram Model 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 N-gram Model 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于语言模型基线、文本相似度、去重和特征工程。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Tokenization
- Token Frequency

### 关联
- Bigram Language Model
- TF-IDF

### 延伸
- Bigram Language Model
- TF-IDF

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
