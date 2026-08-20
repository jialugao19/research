---
id: article-experiment-design
slug: experiment-design
title: Experiment Design：概念、直觉与边界
concepts:
- experiment-design
learning_units:
- experiment-design-overview
domain: statistics
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Experiment Design
- statistics
- intermediate
- hypothesis testing
- statistical power
- model evaluation metrics
- rollout analysis
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
  id: article-plan-experiment-design
  covered_concepts: 1
  primary_concept: experiment-design
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
---
# Experiment Design：概念、直觉与边界

在收集数据前规划处理组、样本量、指标和比较方式的过程。

关键词：Experiment Design
- statistics
- intermediate
- hypothesis testing
- statistical power
- model evaluation metrics
- rollout analysis
- theory

## 为什么需要它

实验设计不好，后续分析很难补救。设计决定证据质量。

## 核心直觉

- 输入：Experiment Design 所处理的数据、状态或评价对象。
- 操作：关键要素包括随机化、对照组、样本量、主要指标和停止规则。
- 观察结果：实验设计不好，后续分析很难补救。设计决定证据质量。

它像开工前先画实验蓝图。

例子：上线新模型前，先设计 A/B 实验和护栏指标。

## 数学定义

### 表达方式

$$
\hat\tau=\bar Y_{T}-\bar Y_{C},\qquad \bar Y_T=\frac1{n_T}\sum_{i:T_i=1}Y_i,\quad \bar Y_C=\frac1{n_C}\sum_{i:T_i=0}Y_i
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Experiment Design 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Experiment Design 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Experiment Design 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 事后挑指标会增加假阳性风险。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Experiment Design 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Experiment Design 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 A/B 测试、模型比较、产品实验和科学研究。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Hypothesis Testing
- Statistical Power

### 关联
- Model Evaluation Metrics
- Rollout Analysis

### 延伸
- Model Evaluation Metrics
- Rollout Analysis

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
