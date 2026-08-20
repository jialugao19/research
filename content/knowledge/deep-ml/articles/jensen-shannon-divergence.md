---
id: article-jensen-shannon-divergence
slug: jensen-shannon-divergence
title: Jensen-Shannon Divergence：概念、直觉与边界
concepts:
- jensen-shannon-divergence
learning_units:
- jensen-shannon-divergence-overview
domain: information_theory
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Jensen-Shannon Divergence
- Jensen Shannon
- JS divergence
- information theory
- intermediate
- kl divergence
- entropy
- bhattacharyya distance
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
  id: article-plan-jensen-shannon-divergence
  covered_concepts: 1
  primary_concept: jensen-shannon-divergence
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Jensen-Shannon Divergence：概念、直觉与边界

用对称且有界的方式衡量两个概率分布差异的指标。

关键词：Jensen-Shannon Divergence
- Jensen Shannon
- JS divergence
- information theory
- intermediate
- kl divergence
- entropy
- bhattacharyya distance

## 为什么需要它

KL 散度不对称，有时不便比较两个分布。JSD 更稳定。

## 核心直觉

- 输入：Jensen-Shannon Divergence 所处理的数据、状态或评价对象。
- 操作：JSD 是两个 KL 散度的平均，参考分布是两者的混合分布。
- 观察结果：KL 散度不对称，有时不便比较两个分布。JSD 更稳定。

它像先取两个分布的中间分布，再比较双方离中间有多远。

例子：比较两个文本模型的词分布差异时，可以用 JSD。

## 数学定义

### 表达方式

$$
D_{\mathrm{JS}}(P,Q)=\frac12D_{\mathrm{KL}}(P\Vert M)+\frac12D_{\mathrm{KL}}(Q\Vert M),\qquad M=\frac12(P+Q)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Jensen-Shannon Divergence 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Jensen-Shannon Divergence 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Jensen-Shannon Divergence 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- JSD 小只说明分布相似，不保证样本语义相同。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Jensen-Shannon Divergence 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Jensen-Shannon Divergence 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分布比较、聚类、生成模型评估和漂移监控。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- KL Divergence

### 关联
- Entropy
- Bhattacharyya Distance

### 延伸
- Entropy
- Bhattacharyya Distance

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
