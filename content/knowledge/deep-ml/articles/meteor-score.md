---
id: article-meteor-score
slug: meteor-score
title: METEOR Score：指标含义与使用边界
concepts:
- meteor-score
learning_units:
- meteor-score-overview
domain: nlp
level: intermediate
content_type: metric
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- METEOR Score
- METEOR
- nlp
- intermediate
- translation evaluation
- text generation evaluation
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
  id: article-plan-meteor-score
  covered_concepts: 1
  primary_concept: meteor-score
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# METEOR Score：指标含义与使用边界

一种用于机器翻译评估的自动指标，考虑词形、同义和词序等因素。

关键词：METEOR Score
- METEOR
- nlp
- intermediate
- translation evaluation
- text generation evaluation
- metric

## 衡量什么

简单词重叠指标可能过于粗糙。METEOR 尝试更贴近人类判断。

## 数学定义

### 表达方式

$$
F_{\mathrm{mean}}=\frac{PR}{\alpha P+(1-\alpha)R},\qquad \operatorname{METEOR}=F_{\mathrm{mean}}\left(1-\gamma\left(\frac{c}{m}\right)^\beta\right)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- METEOR Score 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 METEOR Score 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 指标解释

- METEOR Score 的数值只回答一个特定评价问题。
- 高分不一定代表模型整体更好，必须结合数据分布和错误代价。
- 指标变化要和阈值、样本量、类别比例一起解释。

## 常见误区

### 概念误解
- METEOR 仍是自动指标。不能替代人工质量审查。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 METEOR Score 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 METEOR Score 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于翻译、摘要和文本生成评估。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Translation Evaluation

### 关联
- Text Generation Evaluation

### 延伸
- Text Generation Evaluation

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
