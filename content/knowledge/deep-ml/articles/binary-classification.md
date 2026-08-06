---
id: article-binary-classification
slug: binary-classification
title: Binary Classification：概念、直觉与边界
concepts:
- binary-classification
learning_units:
- binary-classification-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Binary Classification
- binary classifier
- machine learning
- beginner
- classifier
- logistic regression
- binary cross entropy
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
  id: article-plan-binary-classification
  covered_concepts: 1
  primary_concept: binary-classification
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
---
# Binary Classification：概念、直觉与边界

把样本划分到两个类别之一的监督学习任务。

关键词：Binary Classification
- binary classifier
- machine learning
- beginner
- classifier
- logistic regression
- binary cross entropy
- theory

## 为什么需要它

很多决策只有是或否。二分类提供最基础的预测框架。

## 核心直觉

- 输入：Binary Classification 所处理的数据、状态或评价对象。
- 操作：模型输出分数或概率，再通过阈值变成类别。
- 观察结果：很多决策只有是或否。二分类提供最基础的预测框架。

它像在一条边界两侧做判断。

例子：判断邮件是否为垃圾邮件就是二分类。

## 数学定义

### 表达方式

`y_hat = 1 if p >= threshold else 0`

此处保留 Binary Classification 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Binary Classification 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Binary Classification 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Binary Classification 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 准确率高不一定好。类别不平衡时要看召回率和精确率。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Binary Classification 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Binary Classification 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于风控、医学筛查、检索过滤和异常检测。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Classifier

### 关联
- Logistic Regression
- Binary Cross Entropy

### 延伸
- Logistic Regression
- Binary Cross Entropy

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
