---
id: article-shap-values
slug: shap-values
title: SHAP Values：概念、直觉与边界
concepts:
- shap-values
learning_units:
- shap-values-overview
domain: machine_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- SHAP Values
- SHAP
- machine learning
- advanced
- feature importance
- model calibration
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
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-shap-values
  covered_concepts: 1
  primary_concept: shap-values
confidence:
  concept: 0.94
  prerequisite: 0.9
  prerequisite_path_eligible: true
generated_version:
  model: curated-catalog-v3
  prompt_version: chapter-profile-v3
review:
  state: automated_editorial
  last_review: null
  reviewer: null
  triggers:
  - advanced_or_expert_topic
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# SHAP Values：概念、直觉与边界

基于博弈论思想解释单个预测中特征贡献的方法。

关键词：SHAP Values
- SHAP
- machine learning
- advanced
- feature importance
- model calibration
- theory

## 为什么需要它

全局重要性不说明单个样本为什么被这样预测。SHAP 提供局部解释。

## 核心直觉

- 输入：SHAP Values 所处理的数据、状态或评价对象。
- 操作：SHAP 估计每个特征加入模型后带来的边际贡献。
- 观察结果：全局重要性不说明单个样本为什么被这样预测。SHAP 提供局部解释。

它像把一次预测的分数，分摊给各个参与特征。

例子：贷款拒绝样本中，SHAP 可以显示负债率贡献了多少风险分。

## 数学定义

### 表达方式

`预测值可分解为基线值加各特征贡献`

此处保留 SHAP Values 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- SHAP Values 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 SHAP Values 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 SHAP Values 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- SHAP 解释仍基于模型和背景数据。它不是因果证明。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 SHAP Values 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 SHAP Values 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于模型审查、风控解释和特征诊断。高维模型计算成本较高。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Feature Importance

### 关联
- Model Calibration

### 延伸
- Model Calibration

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
