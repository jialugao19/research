---
id: article-decision-tree
slug: decision-tree
title: Decision Tree：概念、直觉与边界
concepts:
- decision-tree
learning_units:
- decision-tree-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Decision Tree
- CART
- machine learning
- beginner
- model evaluation metrics
- random forest
- gradient boosting
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
  id: article-plan-decision-tree
  covered_concepts: 1
  primary_concept: decision-tree
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
# Decision Tree：概念、直觉与边界

通过一系列特征划分形成树状判断规则的模型。

关键词：Decision Tree
- CART
- machine learning
- beginner
- model evaluation metrics
- random forest
- gradient boosting
- theory

## 为什么需要它

模型需要可解释的分支规则。决策树用条件判断逐步缩小预测范围。

## 核心直觉

- 输入：Decision Tree 所处理的数据、状态或评价对象。
- 操作：训练会选择能让节点更纯的划分。常见标准包括信息增益和 Gini impurity。
- 观察结果：模型需要可解释的分支规则。决策树用条件判断逐步缩小预测范围。

它像一张问答流程图。每个节点问一个问题，叶子给出预测。

例子：判断贷款风险时，树可以先看收入，再看负债，再给出风险等级。

## 数学定义

### 表达方式

`分类树常最小化划分后的不纯度`

此处保留 Decision Tree 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Decision Tree 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Decision Tree 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Decision Tree 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 树越深不一定越好。深树容易记住训练数据。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Decision Tree 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Decision Tree 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分类、回归和规则解释。单棵树稳定性较差，常用集成方法增强。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Model Evaluation Metrics

### 关联
- Random Forest
- Gradient Boosting

### 延伸
- Random Forest
- Gradient Boosting

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
