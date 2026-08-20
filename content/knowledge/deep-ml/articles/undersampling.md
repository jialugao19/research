---
id: article-undersampling
slug: undersampling
title: Undersampling：算法直觉与实现要点
concepts:
- undersampling
learning_units:
- undersampling-overview
domain: machine_learning
level: beginner
content_type: algorithm
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Undersampling
- dataset undersampling
- machine learning
- beginner
- dataset balancing
- class imbalance
- precision recall
- algorithm
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 算法流程
  - 复杂度
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: true
  complexity_required: true
status: published
article_plan:
  id: article-plan-undersampling
  covered_concepts: 1
  primary_concept: undersampling
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Undersampling：算法直觉与实现要点

减少多数类样本数量以缓解类别不平衡的方法。

关键词：Undersampling
- dataset undersampling
- machine learning
- beginner
- dataset balancing
- class imbalance
- precision recall
- algorithm

## 为什么需要它

多数类太多会让模型忽视少数类。欠采样降低这种主导效应。

## 核心直觉

- 输入：Undersampling 所处理的数据、状态或评价对象。
- 操作：欠采样简单但会丢失信息。通常要和验证指标一起评估。
- 观察结果：多数类太多会让模型忽视少数类。欠采样降低这种主导效应。

它像从人数过多的一组里抽掉一部分样本。

例子：二分类中，保留全部正样本，只抽取一部分负样本训练。

## 数学定义

### 表达方式

$$
D^{\prime}=D_{\mathrm{minority}}\cup S,\qquad S\subset D_{\mathrm{majority}},\quad |S|=\rho|D_{\mathrm{minority}}|
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Undersampling 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Undersampling 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 算法流程

Input: Undersampling
- Undersampling 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: Undersampling
- 多数类太多会让模型忽视少数类。欠采样降低这种主导效应。

Steps: Undersampling
1. 明确输入数据和目标统计量或目标函数。
2. 执行核心操作：欠采样简单但会丢失信息。通常要和验证指标一起评估。
3. 记录每次更新或重采样后的结果。
4. 重复直到达到预算、收敛或评估稳定。
5. 用输出结果判断方法是否解决原问题。

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Undersampling 时要单独估计训练成本和推理成本。

## 常见误区

### 概念误解
- 欠采样不是免费提升。丢失的多数类信息可能有价值。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Undersampling 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Undersampling 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于风控、异常检测、医疗筛查和快速基线训练。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Dataset Balancing

### 关联
- Class Imbalance
- Precision and Recall

### 延伸
- Class Imbalance
- Precision and Recall

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
