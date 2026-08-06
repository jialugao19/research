---
id: article-hypergeometric-distribution
slug: hypergeometric-distribution
title: Hypergeometric Distribution：指标含义与使用边界
concepts:
- hypergeometric-distribution
learning_units:
- hypergeometric-distribution-overview
domain: probability
level: intermediate
content_type: metric
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Hypergeometric Distribution
- hypergeometric
- hypergeometric pmf
- probability
- intermediate
- binomial distribution
- expected value
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
  id: article-plan-hypergeometric-distribution
  covered_concepts: 1
  primary_concept: hypergeometric-distribution
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: NumPy Documentation
  url: https://numpy.org/doc/stable/
  type: official_docs
---
# Hypergeometric Distribution：指标含义与使用边界

描述不放回抽样中成功次数分布的离散概率模型。

关键词：Hypergeometric Distribution
- hypergeometric
- hypergeometric pmf
- probability
- intermediate
- binomial distribution
- expected value
- metric

## 衡量什么

抽样不放回时，每次抽取会改变剩余组成。二项分布不再合适。

## 数学定义

### 表达方式

$$
P(X=k)=C(K,k)C(N-K,n-k)/C(N,n)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Hypergeometric Distribution 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Hypergeometric Distribution 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 指标解释

- Hypergeometric Distribution 的数值只回答一个特定评价问题。
- 高分不一定代表模型整体更好，必须结合数据分布和错误代价。
- 指标变化要和阈值、样本量、类别比例一起解释。

## 常见误区

### 概念误解
- 有放回抽样通常用二项分布，不应混用。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Hypergeometric Distribution 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Hypergeometric Distribution 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于抽检、富集分析、牌类概率和小样本抽样。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability

### 关联
- Binomial Distribution
- Expected Value

### 延伸
- Binomial Distribution
- Expected Value

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **NumPy Documentation**：https://numpy.org/doc/stable/。用途：作为交叉核对材料，确认术语、公式和使用场景。
