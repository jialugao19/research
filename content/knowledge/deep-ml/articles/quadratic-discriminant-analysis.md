---
id: article-quadratic-discriminant-analysis
slug: quadratic-discriminant-analysis
title: Quadratic Discriminant Analysis：概念、直觉与边界
concepts:
- quadratic-discriminant-analysis
learning_units:
- quadratic-discriminant-analysis-overview
domain: machine_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Quadratic Discriminant Analysis
- QDA
- machine learning
- intermediate
- linear discriminant analysis
- gaussian distribution
- classifier
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
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-quadratic-discriminant-analysis
  covered_concepts: 1
  primary_concept: quadratic-discriminant-analysis
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
# Quadratic Discriminant Analysis：概念、直觉与边界

允许不同类别拥有不同协方差矩阵的高斯判别分类模型。

关键词：Quadratic Discriminant Analysis
- QDA
- machine learning
- intermediate
- linear discriminant analysis
- gaussian distribution
- classifier
- theory

## 为什么需要它

类别分布形状不同时，线性边界可能不足。QDA 提供二次边界。

## 核心直觉

- 输入：Quadratic Discriminant Analysis 所处理的数据、状态或评价对象。
- 操作：QDA 比 LDA 更灵活，但参数更多。小样本时可能不稳定。
- 观察结果：类别分布形状不同时，线性边界可能不足。QDA 提供二次边界。

它像允许每个类别有自己的椭圆形范围。

例子：两类数据方差结构差异大时，QDA 可能优于 LDA。

## 数学定义

### 表达方式

$$
\delta_k(x)=-\frac12\log|\Sigma_k|-\frac12(x-\mu_k)^{\top}\Sigma_k^{-1}(x-\mu_k)+\log\pi_k
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Quadratic Discriminant Analysis 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Quadratic Discriminant Analysis 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Quadratic Discriminant Analysis 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 更灵活不等于更好。数据少时容易过拟合。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Quadratic Discriminant Analysis 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Quadratic Discriminant Analysis 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于统计分类、低维数据和可解释基线。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Discriminant Analysis

### 关联
- Gaussian Distribution
- Classifier

### 延伸
- Gaussian Distribution
- Classifier

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
