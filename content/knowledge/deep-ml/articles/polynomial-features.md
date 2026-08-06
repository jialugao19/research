---
id: article-polynomial-features
slug: polynomial-features
title: Polynomial Features：概念、直觉与边界
concepts:
- polynomial-features
learning_units:
- polynomial-features-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Polynomial Features
- polynomial
- polynomial feature
- machine learning
- beginner
- linear regression
- feature scaling
- kernel method
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
  id: article-plan-polynomial-features
  covered_concepts: 1
  primary_concept: polynomial-features
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
# Polynomial Features：概念、直觉与边界

把原始特征扩展为多项式项和交互项的特征工程方法。

关键词：Polynomial Features
- polynomial
- polynomial feature
- machine learning
- beginner
- linear regression
- feature scaling
- kernel method

## 为什么需要它

线性模型只能表达线性关系。多项式特征让简单模型拟合弯曲关系。

## 核心直觉

- 输入：Polynomial Features 所处理的数据、状态或评价对象。
- 操作：常见扩展包括 x^2、x^3 和 x1*x2。维度会随阶数快速增加。
- 观察结果：线性模型只能表达线性关系。多项式特征让简单模型拟合弯曲关系。

它像给模型加入平方项和交叉项，让直尺可以近似曲线。

例子：用线性回归拟合 U 形曲线时，可以加入二次项。

## 数学定义

### 表达方式

$$
features = [x, x^2, x1\cdot x2]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Polynomial Features 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Polynomial Features 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Polynomial Features 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 阶数越高越容易过拟合。验证集必须参与选择。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Polynomial Features 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Polynomial Features 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于表格建模、线性模型增强和非线性基线。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Regression
- Feature Scaling

### 关联
- Kernel Method
- Feature Selection

### 延伸
- Kernel Method
- Feature Selection

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
