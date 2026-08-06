---
id: article-feature-hashing
slug: feature-hashing
title: Feature Hashing：概念、直觉与边界
concepts:
- feature-hashing
learning_units:
- feature-hashing-overview
domain: machine_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Feature Hashing
- hashing trick
- machine learning
- intermediate
- hash table
- feature engineering
- tf idf
- random projection
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
  id: article-plan-feature-hashing
  covered_concepts: 1
  primary_concept: feature-hashing
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Feature Hashing：概念、直觉与边界

用哈希函数把高维离散特征映射到固定维度向量的方法。

关键词：Feature Hashing
- hashing trick
- machine learning
- intermediate
- hash table
- feature engineering
- tf idf
- random projection

## 为什么需要它

类别或文本特征空间可能巨大，维护完整词典成本高。

## 核心直觉

- 输入：Feature Hashing 所处理的数据、状态或评价对象。
- 操作：Feature hashing 不需要显式词表，但会产生哈希碰撞。
- 观察结果：类别或文本特征空间可能巨大，维护完整词典成本高。

它像把无限多标签投进固定数量的桶。

例子：在线广告特征可用 hashing trick 控制特征维度。

## 数学定义

### 表达方式

$$
index = hash(feature) mod n_features
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Feature Hashing 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Feature Hashing 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Feature Hashing 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 碰撞不是 bug，而是用空间换速度的代价。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Feature Hashing 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Feature Hashing 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于稀疏特征、在线学习、文本分类和大规模推荐。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Hash Table
- Feature Engineering

### 关联
- TF-IDF
- Random Projection

### 延伸
- TF-IDF
- Random Projection

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
