---
id: article-categorical-encoding
slug: categorical-encoding
title: Categorical Encoding：概念、直觉与边界
concepts:
- categorical-encoding
learning_units:
- categorical-encoding-overview
domain: data_preprocessing
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Categorical Encoding
- category encoding
- label encoding
- data preprocessing
- beginner
- one hot encoding
- data leakage
- word embeddings
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
  id: article-plan-categorical-encoding
  covered_concepts: 1
  primary_concept: categorical-encoding
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: pandas Documentation
  url: https://pandas.pydata.org/docs/
  type: official_docs
---
# Categorical Encoding：概念、直觉与边界

把类别特征转换成模型可使用数值表示的方法。

关键词：Categorical Encoding
- category encoding
- label encoding
- data preprocessing
- beginner
- one hot encoding
- data leakage
- word embeddings

## 为什么需要它

表格模型常遇到城市、行业和类型等类别字段。它们需要编码后才能训练。

## 核心直觉

- 输入：Categorical Encoding 所处理的数据、状态或评价对象。
- 操作：常见方法包括 one-hot、ordinal encoding、target encoding 和 embedding。
- 观察结果：表格模型常遇到城市、行业和类型等类别字段。它们需要编码后才能训练。

编码像给每个类别安排一种数字表达方式。

例子：城市字段可以编码后进入线性模型或树模型。

## 数学定义

### 表达方式

`one-hot 把类别映射到稀疏向量`

此处保留 Categorical Encoding 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Categorical Encoding 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Categorical Encoding 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Categorical Encoding 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 类别编码不能随便引入顺序。无序类别用整数编号可能误导模型。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Categorical Encoding 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Categorical Encoding 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于表格建模、推荐和特征工程。高基数类别要特别处理。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- One-Hot Encoding
- Data Leakage

### 关联
- Word Embeddings
- Feature Scaling

### 延伸
- Word Embeddings
- Feature Scaling

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **pandas Documentation**：https://pandas.pydata.org/docs/。用途：作为交叉核对材料，确认术语、公式和使用场景。
