---
id: article-cumulative-distribution-function
slug: cumulative-distribution-function
title: Cumulative Distribution Function：概念、直觉与边界
concepts:
- cumulative-distribution-function
learning_units:
- cumulative-distribution-function-overview
domain: probability
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Cumulative Distribution Function
- CDF
- distribution cdf
- probability
- beginner
- probability density function
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
  id: article-plan-cumulative-distribution-function
  covered_concepts: 1
  primary_concept: cumulative-distribution-function
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
# Cumulative Distribution Function：概念、直觉与边界

给出随机变量小于等于某个值概率的函数。

关键词：Cumulative Distribution Function
- CDF
- distribution cdf
- probability
- beginner
- probability density function
- theory

## 为什么需要它

概率密度只描述局部形状。CDF 直接回答落在阈值以下的概率。

## 核心直觉

- 输入：Cumulative Distribution Function 所处理的数据、状态或评价对象。
- 操作：CDF 单调不降，最终趋近 1。连续分布的 PDF 是 CDF 的导数。
- 观察结果：概率密度只描述局部形状。CDF 直接回答落在阈值以下的概率。

它像从左到右累计概率。

例子：用 CDF 可以计算延迟不超过 200ms 的概率。

## 数学定义

### 表达方式

$$
F_X(x)=\Pr(X\le x),\qquad F_X(x)=\int_{-\infty}^{x}f_X(t)\,dt\ \text{for continuous }X
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Cumulative Distribution Function 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Cumulative Distribution Function 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Cumulative Distribution Function 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- PDF 值本身不是概率。区间概率来自积分或 CDF 差。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Cumulative Distribution Function 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Cumulative Distribution Function 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于概率计算、分位数、统计检验和风险分析。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability

### 关联
- Probability Density Function

### 延伸
- Probability Density Function

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
