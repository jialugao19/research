---
id: article-distance-metrics
slug: distance-metrics
title: Distance Metrics：指标含义与使用边界
concepts:
- distance-metrics
learning_units:
- distance-metrics-overview
domain: machine_learning
level: beginner
content_type: metric
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Distance Metrics
- distance metric
- distance
- machine learning
- beginner
- vector norm
- cosine similarity
- dbscan clustering
profile:
  required_sections:
  - 衡量什么
  - 数学定义
  - 指标解释
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-distance-metrics
  covered_concepts: 1
  primary_concept: distance-metrics
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
# Distance Metrics：指标含义与使用边界

衡量两个样本在特征空间中相距多远的方法集合。

关键词：Distance Metrics
- distance metric
- distance
- machine learning
- beginner
- vector norm
- cosine similarity
- dbscan clustering

## 衡量什么

邻近、聚类和检索都依赖距离定义。距离选错会改变模型行为。

## 数学定义

### 表达方式

`d(x,y) depends on metric choice`

此处保留 Distance Metrics 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Distance Metrics 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Distance Metrics 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 指标解释

- Distance Metrics 的数值只回答一个特定评价问题。
- 高分不一定代表模型整体更好，必须结合数据分布和错误代价。
- 指标变化要和阈值、样本量、类别比例一起解释。

## 常见误区

### 概念误解
- 没有通用最优距离。特征尺度和任务目标很关键。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Distance Metrics 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Distance Metrics 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 KNN、聚类、检索、异常检测和推荐。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Vector Norm
- Cosine Similarity

### 关联
- DBSCAN Clustering
- k-Nearest Neighbors

### 延伸
- DBSCAN Clustering
- k-Nearest Neighbors

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
