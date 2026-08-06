---
id: article-learning-curve
slug: learning-curve
title: Learning Curve：概念、直觉与边界
concepts:
- learning-curve
learning_units:
- learning-curve-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Learning Curve
- machine learning
- beginner
- bias variance tradeoff
- model evaluation metrics
- early stopping
- experiment tracking
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
  id: article-plan-learning-curve
  covered_concepts: 1
  primary_concept: learning-curve
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
# Learning Curve：概念、直觉与边界

展示模型表现随训练样本量或训练过程变化的曲线。

关键词：Learning Curve
- machine learning
- beginner
- bias variance tradeoff
- model evaluation metrics
- early stopping
- experiment tracking
- theory

## 为什么需要它

模型效果不好时，需要判断是数据不够、模型太弱还是过拟合。

## 核心直觉

- 输入：Learning Curve 所处理的数据、状态或评价对象。
- 操作：训练曲线和验证曲线的间距能提示偏差和方差问题。
- 观察结果：模型效果不好时，需要判断是数据不够、模型太弱还是过拟合。

它像观察学习成绩随练习量如何变化。

例子：验证分数随数据量增加仍上升，说明继续收集数据可能有价值。

## 数学定义

### 表达方式

$$
plot(score versus training_size or step)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Learning Curve 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Learning Curve 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Learning Curve 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 单条曲线不足以诊断全部问题。要结合误差分析和数据质量。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Learning Curve 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Learning Curve 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于模型诊断、数据规划和训练监控。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Bias-Variance Tradeoff
- Model Evaluation Metrics

### 关联
- Early Stopping
- Experiment Tracking

### 延伸
- Early Stopping
- Experiment Tracking

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
