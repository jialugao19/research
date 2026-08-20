---
id: article-r-squared
slug: r-squared
title: R-Squared：概念、直觉与边界
concepts:
- r-squared
learning_units:
- r-squared-overview
domain: statistics
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- R-Squared
- R2
- statistics
- beginner
- linear regression
- variance
- model evaluation metrics
- mean squared error
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
  id: article-plan-r-squared
  covered_concepts: 1
  primary_concept: r-squared
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
# R-Squared：概念、直觉与边界

衡量回归模型解释目标变量方差比例的指标。

关键词：R-Squared
- R2
- statistics
- beginner
- linear regression
- variance
- model evaluation metrics
- mean squared error

## 为什么需要它

MSE 给出误差大小，但不直接说明模型解释了多少变化。

## 核心直觉

- 输入：R-Squared 所处理的数据、状态或评价对象。
- 操作：R-squared 接近 1 通常表示解释比例高，但也要看任务和样本。
- 观察结果：MSE 给出误差大小，但不直接说明模型解释了多少变化。

它像看模型把数据波动解释掉了多少。

例子：线性回归报告中常同时给出 MSE 和 R2。

## 数学定义

### 表达方式

$$
R^2=1-\frac{\sum_{i=1}^{n}(y_i-\hat y_i)^2}{\sum_{i=1}^{n}(y_i-\bar y)^2}
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- R-Squared 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 R-Squared 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 R-Squared 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- R2 高不代表因果正确，也不代表泛化一定好。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 R-Squared 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 R-Squared 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于回归评估、报表分析和模型比较。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Regression
- Variance

### 关联
- Model Evaluation Metrics
- Mean Squared Error

### 延伸
- Model Evaluation Metrics
- Mean Squared Error

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
