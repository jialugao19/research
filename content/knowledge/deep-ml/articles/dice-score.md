---
id: article-dice-score
slug: dice-score
title: Dice Score：指标含义与使用边界
concepts:
- dice-score
learning_units:
- dice-score-overview
domain: machine_learning
level: intermediate
content_type: metric
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Dice Score
- dice coefficient
- machine learning
- intermediate
- confusion matrix
- semantic segmentation
- f1 score
- metric
profile:
  required_sections:
  - 衡量什么
  - 数学定义
  - 指标解释
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-dice-score
  covered_concepts: 1
  primary_concept: dice-score
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Dice Score：指标含义与使用边界

衡量两个集合或二值预测重叠程度的指标。

关键词：Dice Score
- dice coefficient
- machine learning
- intermediate
- confusion matrix
- semantic segmentation
- f1 score
- metric

## 衡量什么

分割和稀疏分类常更关心正类区域重叠。

## 数学定义

### 表达方式

$$
Dice = 2TP / (2TP + FP + FN)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Dice Score 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Dice Score 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 指标解释

- Dice Score 的数值只回答一个特定评价问题。
- 高分不一定代表模型整体更好，必须结合数据分布和错误代价。
- 指标变化要和阈值、样本量、类别比例一起解释。

## 常见误区

### 概念误解
- Dice 高不代表边界全部准确，还要结合任务需求看。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Dice Score 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Dice Score 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分类、分割、检索和集合相似度评估。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Confusion Matrix

### 关联
- Semantic Segmentation
- F1 Score

### 延伸
- Semantic Segmentation
- F1 Score

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
