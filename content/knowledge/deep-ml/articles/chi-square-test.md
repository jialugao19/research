---
id: article-chi-square-test
slug: chi-square-test
title: Chi-Square Test：概念、直觉与边界
concepts:
- chi-square-test
learning_units:
- chi-square-test-overview
domain: statistics
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Chi-Square Test
- chi square
- chi-square
- statistics
- intermediate
- hypothesis testing
- phi coefficient
- confidence interval
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
  id: article-plan-chi-square-test
  covered_concepts: 1
  primary_concept: chi-square-test
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
# Chi-Square Test：概念、直觉与边界

用于检验类别频数是否偏离期望频数的统计检验方法。

关键词：Chi-Square Test
- chi square
- chi-square
- statistics
- intermediate
- hypothesis testing
- phi coefficient
- confidence interval

## 为什么需要它

面对类别计数时，我们常要判断差异是否可能只是随机波动。

## 核心直觉

- 输入：Chi-Square Test 所处理的数据、状态或评价对象。
- 操作：统计量累计每个格子的平方偏差，并按期望频数缩放。
- 观察结果：面对类别计数时，我们常要判断差异是否可能只是随机波动。

它像比较观察到的格子计数和理论上该有的计数。

例子：检验两个二元标签是否独立时，可使用二乘二列联表。

## 数学定义

### 表达方式

$$
\chi^2=\sum_{j=1}^{m}\frac{(O_j-E_j)^2}{E_j},\qquad E_j>0
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Chi-Square Test 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Chi-Square Test 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Chi-Square Test 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 样本量太小或期望频数太低时，卡方近似可能不可靠。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Chi-Square Test 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Chi-Square Test 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于列联表、特征筛选、A/B 测试和类别分布检查。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Hypothesis Testing

### 关联
- Phi Coefficient
- Confidence Interval

### 延伸
- Phi Coefficient
- Confidence Interval

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **NumPy Documentation**：https://numpy.org/doc/stable/。用途：作为交叉核对材料，确认术语、公式和使用场景。
