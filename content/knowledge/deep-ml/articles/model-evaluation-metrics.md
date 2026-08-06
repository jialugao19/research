---
id: article-model-evaluation-metrics
slug: model-evaluation-metrics
title: 分类评估指标：从混淆矩阵到 ROC-AUC
concepts:
- model-evaluation-metrics
- confusion-matrix
- accuracy-score
- precision-recall
- f1-score
- roc-auc
- threshold-selection
- model-calibration
learning_units:
- model-evaluation-metrics-overview
- confusion-matrix-overview
- accuracy-score-overview
- precision-recall-overview
- f1-score-overview
- roc-auc-overview
- threshold-selection-overview
- model-calibration-overview
domain: machine_learning
level: intermediate
content_type: metric
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Model Evaluation Metrics
- metrics
- evaluation score
- machine learning
- beginner
- probability
- data drift
- train validation test split
profile:
  required_sections:
  - 衡量什么
  - 数学定义
  - 指标解释
  - 阈值与失败模式
  - 假设与限制
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-model-evaluation-metrics
  covered_concepts: 8
  primary_concept: model-evaluation-metrics
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
---
# 分类评估指标：从混淆矩阵到 ROC-AUC

用数值指标衡量模型预测质量的方法集合。 本文把 以 Model Evaluation Metrics 为主线的 8 个概念 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：Model Evaluation Metrics
- metrics
- evaluation score
- machine learning
- beginner
- probability
- data drift
- train validation test split

## 衡量什么

不同任务关心不同错误。单一准确率常常不够。

这些概念放在一起看，是因为它们共享 Model Evaluation Metrics 这条主线。

先看主线，再看 以 Confusion Matrix 为主线的 7 个概念 的分工，能减少概念之间的跳跃感。

使用这个指标前，先确认它衡量的是 不同任务关心不同错误。单一准确率常常不够。

Model Evaluation Metrics 的数值本身不是结论。它必须和标签定义、阈值选择、样本量和业务成本一起解释。

如果把它用于 它用于模型比较、上线门槛和监控。数据分布变化时，指标也要重新解释。，最好同时看总体分数和关键切片，否则平均值会掩盖局部失败。

## 数学定义

### 表达方式

`precision = TP / (TP + FP)，recall = TP / (TP + FN)`

此处保留 Model Evaluation Metrics 的结构化表达，不作为标准 TeX 公式发布。

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Model Evaluation Metrics 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

这里保留的是 Model Evaluation Metrics 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

### 使用读法

读 Model Evaluation Metrics 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 指标解释

- Model Evaluation Metrics 的数值只回答一个特定评价问题。
- 高分不一定代表模型整体更好，必须结合数据分布和错误代价。
- 指标变化要和阈值、样本量、类别比例一起解释。

## 阈值与失败模式

- 阈值会改变 Model Evaluation Metrics 的 precision、recall 或业务代价。
- 类别极不均衡时，单一分数可能掩盖少数类失败。
- 指标必须和任务目标一起解释，不能脱离误报和漏报成本。

## 假设与限制

- 标签定义和预测输出必须一致。
- 样本量太小时，指标波动可能大于真实模型差异。
- 指标只覆盖它定义的问题，不能替代完整错误分析。
- 应用到真实数据前，要检查这个前提是否和 `machine_learning` 领域的数据来源一致。
- 如果输入形态明显不同于“欺诈检测中，漏掉欺诈和误伤正常用户的代价不同。指标选择要反映这种差异”，需要重新确认输出解释。

## 常见误区

### 概念误解
- 高指标不等于业务成功。指标必须和真实目标对齐。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Model Evaluation Metrics 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Model Evaluation Metrics 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于模型比较、上线门槛和监控。数据分布变化时，指标也要重新解释。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability
- Model Evaluation Metrics
- Confusion Matrix
- Precision and Recall
- Model Calibration

### 关联
- Confusion Matrix
- Accuracy Score
- Precision and Recall
- F1 Score
- ROC AUC
- Threshold Selection
- Model Calibration

### 延伸
- Data Drift
- Train Validation Test Split
- ROC AUC
- Precision and Recall
- F1 Score
- Threshold Selection
- Model Evaluation Metrics
- Class Imbalance

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
