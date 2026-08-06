---
id: article-class-imbalance
slug: class-imbalance
title: Class Imbalance：概念、直觉与边界
concepts:
- class-imbalance
learning_units:
- class-imbalance-overview
domain: machine_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Class Imbalance
- imbalanced data
- machine learning
- intermediate
- confusion matrix
- model evaluation metrics
- focal loss
- roc auc
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
  id: article-plan-class-imbalance
  covered_concepts: 1
  primary_concept: class-imbalance
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
# Class Imbalance：概念、直觉与边界

不同类别样本数量差异很大的数据现象。

关键词：Class Imbalance
- imbalanced data
- machine learning
- intermediate
- confusion matrix
- model evaluation metrics
- focal loss
- roc auc

## 为什么需要它

模型可能偏向多数类。少数类表现会被整体准确率掩盖。

## 核心直觉

- 输入：Class Imbalance 所处理的数据、状态或评价对象。
- 操作：处理方法包括重采样、类别权重、阈值调整和更合适的评估指标。
- 观察结果：模型可能偏向多数类。少数类表现会被整体准确率掩盖。

它像班里大多数人选同一答案。只猜多数，也能看起来分数不低。

例子：欺诈检测中，欺诈样本可能远少于正常样本。

## 数学定义

### 表达方式

`少数类 recall 常比 overall accuracy 更有信息`

此处保留 Class Imbalance 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Class Imbalance 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Class Imbalance 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Class Imbalance 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 简单复制少数类不一定解决问题。过采样可能带来过拟合。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Class Imbalance 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Class Imbalance 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于风控、医学检测和异常识别。业务代价决定指标选择。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Confusion Matrix
- Model Evaluation Metrics

### 关联
- Focal Loss
- ROC AUC

### 延伸
- Focal Loss
- ROC AUC

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
