---
id: article-k-means-clustering
slug: k-means-clustering
title: 聚类方法与评估：K-Means 到 DBSCAN
concepts:
- k-means-clustering
- mini-batch-kmeans
- kmeans-plus-plus
- elbow-method
- hierarchical-clustering
- dbscan-clustering
- clustering-evaluation
- silhouette-score
- calinski-harabasz-index
- davies-bouldin-index
- adjusted-rand-index
- normalized-mutual-information
learning_units:
- k-means-clustering-overview
- mini-batch-kmeans-overview
- kmeans-plus-plus-overview
- elbow-method-overview
- hierarchical-clustering-overview
- dbscan-clustering-overview
- clustering-evaluation-overview
- silhouette-score-overview
- calinski-harabasz-index-overview
- davies-bouldin-index-overview
- adjusted-rand-index-overview
- normalized-mutual-information-overview
domain: machine_learning
level: intermediate
content_type: algorithm
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- k-Means Clustering
- kmeans
- k-means fit
- machine learning
- beginner
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 算法流程
  - 实现要点
  - 复杂度
  - 假设与限制
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: true
  complexity_required: true
status: published
article_plan:
  id: article-plan-k-means-clustering
  covered_concepts: 12
  primary_concept: k-means-clustering
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
  - multi_concept_article
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# 聚类方法与评估：K-Means 到 DBSCAN

把样本分成 k 个簇，并让每个样本靠近所属簇中心的无监督方法。 本文把 以 k-Means Clustering 为主线的 12 个概念 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：k-Means Clustering
- kmeans
- k-means fit
- machine learning
- beginner

## 为什么需要它

没有标签时，仍然可能想发现数据中的群组结构。k-means 是常用起点。

这些概念放在一起看，是因为它们共享 k-Means Clustering 这条主线。

先看主线，再看 以 Mini-Batch k-Means 为主线的 11 个概念 的分工，能减少概念之间的跳跃感。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 k-Means Clustering 来说，算法在分配样本和更新中心之间交替。初始化会影响结果。

在 k-Means Clustering 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

## 核心直觉

- 输入：k-Means Clustering 所处理的数据、状态或评价对象。
- 操作：算法在分配样本和更新中心之间交替。初始化会影响结果。
- 观察结果：没有标签时，仍然可能想发现数据中的群组结构。k-means 是常用起点。

它像反复调整几个集合中心。样本归最近中心，中心再移动到样本平均位置。

k-Means Clustering 的子概念分工：
- **Mini-Batch k-Means**：用小批量样本近似更新聚类中心的 k-means 变体。
- **K-Means++ Initialization**：为 K-Means 选择初始中心的一种概率初始化方法。

## 数学定义

### 表达方式

`目标是最小化样本到所属中心的平方距离之和`

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策

### 含义

这里保留的是 k-Means Clustering 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

把 k-Means Clustering 写成输入、状态更新和输出，推导时只保留影响目标的量。

## 算法流程

Input: k-Means Clustering
- k-Means Clustering 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: k-Means Clustering
- 没有标签时，仍然可能想发现数据中的群组结构。k-means 是常用起点。

Steps: k-Means Clustering
1. 固定输入、目标与停止条件。
2. 执行核心操作：算法在分配样本和更新中心之间交替。初始化会影响结果。
3. 检查输出，并在达到预算或稳定条件时停止。

## 实现要点

- 明确输入、输出和停止条件。
- 记录随机种子、超参数和数据版本。
- 用小规模样例验证每一步计算是否符合预期。

```python
points = [0.0, 1.0, 9.0, 10.0]
centers = [0.0, 10.0]
for _ in range(3):
    groups = [[p for p in points if abs(p - c) <= abs(p - centers[1 - i])]
              for i, c in enumerate(centers)]
    centers = [sum(group) / len(group) for group in groups]
print(centers)
```

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 k-Means Clustering 时要单独估计训练成本和推理成本。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。

## 常见误区

### 概念误解
- k-means 会强行分成 k 类。数据没有簇结构时，结果也可能看似合理。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 k-Means Clustering 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 k-Means Clustering 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于聚类、压缩和探索分析。非球形簇或尺度差异大时效果会变差。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Normalization
- Linear Algebra
- k-Means Clustering
- Mini-Batch Training

### 关联
- Mini-Batch k-Means
- K-Means++ Initialization
- Elbow Method
- Hierarchical Clustering

### 延伸
- k-Nearest Neighbors
- Principal Component Analysis
- K-Means++ Initialization
- Clustering Evaluation

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
