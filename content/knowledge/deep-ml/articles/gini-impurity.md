---
id: article-gini-impurity
slug: gini-impurity
title: Gini Impurity：概念、直觉与边界
concepts:
- gini-impurity
learning_units:
- gini-impurity-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Gini Impurity
- gini
- apple colors
- machine learning
- beginner
- decision tree
- probability
- entropy
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
  id: article-plan-gini-impurity
  covered_concepts: 1
  primary_concept: gini-impurity
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Gini Impurity：概念、直觉与边界

衡量一个节点中类别混杂程度的决策树指标。

关键词：Gini Impurity
- gini
- apple colors
- machine learning
- beginner
- decision tree
- probability
- entropy

## 为什么需要它

决策树需要选择能最好分开类别的划分。Gini impurity 提供一个简单度量。

## 核心直觉

- 输入：Gini Impurity 所处理的数据、状态或评价对象。
- 操作：节点越纯，Gini 越低。完全同一类别时为零。
- 观察结果：决策树需要选择能最好分开类别的划分。Gini impurity 提供一个简单度量。

它像看一篮水果颜色有多杂。

例子：分类树会比较不同特征切分后的 Gini 下降。

## 数学定义

### 表达方式

$$
Gini = 1 - sum_k p_k^2
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Gini Impurity 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Gini Impurity 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Gini Impurity 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- Gini 和 entropy 都能衡量混杂，但数值含义不同。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Gini Impurity 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Gini Impurity 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于决策树、随机森林和分类特征划分。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Decision Tree
- Probability

### 关联
- Entropy
- Information Gain

### 延伸
- Entropy
- Information Gain

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
