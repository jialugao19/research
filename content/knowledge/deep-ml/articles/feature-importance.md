---
id: article-feature-importance
slug: feature-importance
title: Feature Importance：概念、直觉与边界
concepts:
- feature-importance
learning_units:
- feature-importance-overview
domain: machine_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Feature Importance
- importance
- machine learning
- intermediate
- random forest
- model evaluation metrics
- shap values
- data leakage
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
  id: article-plan-feature-importance
  covered_concepts: 1
  primary_concept: feature-importance
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Feature Importance：概念、直觉与边界

衡量特征对模型预测贡献程度的方法集合。

关键词：Feature Importance
- importance
- machine learning
- intermediate
- random forest
- model evaluation metrics
- shap values
- data leakage

## 为什么需要它

训练模型后，常需要知道哪些特征影响预测。特征重要性提供解释入口。

## 核心直觉

- 输入：Feature Importance 所处理的数据、状态或评价对象。
- 操作：不同方法含义不同。树模型重要性、置换重要性和 SHAP 不能混为一谈。
- 观察结果：训练模型后，常需要知道哪些特征影响预测。特征重要性提供解释入口。

它像看模型主要依赖哪些线索做判断。

例子：风控模型中，收入、负债和历史逾期可能有不同重要性。

## 数学定义

### 表达方式

`permutation importance 比较打乱特征前后的指标变化`

此处保留 Feature Importance 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Feature Importance 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Feature Importance 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

从 Feature Importance 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 重要性不等于因果影响。相关特征会让解释变复杂。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Feature Importance 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Feature Importance 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于模型解释、特征筛选和风险审查。解释要结合业务验证。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Random Forest
- Model Evaluation Metrics

### 关联
- SHAP Values
- Data Leakage

### 延伸
- SHAP Values
- Data Leakage

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
