---
id: article-dummy-regressor
slug: dummy-regressor
title: Dummy Regressor：概念、直觉与边界
concepts:
- dummy-regressor
learning_units:
- dummy-regressor-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Dummy Regressor
- regressor baseline
- machine learning
- beginner
- linear regression
- model evaluation metrics
- bias variance tradeoff
- r squared
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
  id: article-plan-dummy-regressor
  covered_concepts: 1
  primary_concept: dummy-regressor
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
# Dummy Regressor：概念、直觉与边界

不学习复杂关系，只输出简单统计量的回归基线模型。

关键词：Dummy Regressor
- regressor baseline
- machine learning
- beginner
- linear regression
- model evaluation metrics
- bias variance tradeoff
- r squared

## 为什么需要它

复杂模型必须先超过朴素基线，结果才有解释价值。

## 核心直觉

- 输入：Dummy Regressor 所处理的数据、状态或评价对象。
- 操作：常见策略包括输出均值、中位数或固定分位数。
- 观察结果：复杂模型必须先超过朴素基线，结果才有解释价值。

它像先问只猜平均值能拿多少分。

例子：房价回归模型应明显优于总是预测训练集均价的基线。

## 数学定义

### 表达方式

$$
\hat y(x)=\bar y_{\mathrm{train}}=\frac1n\sum_{i=1}^{n}y_i
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Dummy Regressor 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Dummy Regressor 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Dummy Regressor 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 基线简单不等于没用，它能暴露任务或指标问题。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Dummy Regressor 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Dummy Regressor 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于回归评估、实验审计和模型上线门槛。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Regression
- Model Evaluation Metrics

### 关联
- Bias-Variance Tradeoff
- R-Squared

### 延伸
- Bias-Variance Tradeoff
- R-Squared

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
