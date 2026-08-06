---
id: article-multiclass-classification
slug: multiclass-classification
title: Multiclass Classification：概念、直觉与边界
concepts:
- multiclass-classification
learning_units:
- multiclass-classification-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Multiclass Classification
- multi-class classification
- machine learning
- beginner
- softmax function
- cross entropy
- multilabel classification
- confusion matrix
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
  id: article-plan-multiclass-classification
  covered_concepts: 1
  primary_concept: multiclass-classification
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Multiclass Classification：概念、直觉与边界

从三个或更多互斥类别中选择一个类别的监督学习任务。

关键词：Multiclass Classification
- multi-class classification
- machine learning
- beginner
- softmax function
- cross entropy
- multilabel classification
- confusion matrix

## 为什么需要它

很多分类任务不只是二选一。多分类提供了统一建模方式。

## 核心直觉

- 输入：Multiclass Classification 所处理的数据、状态或评价对象。
- 操作：常见输出是每个类别的 logits。训练常用 softmax 和交叉熵。
- 观察结果：很多分类任务不只是二选一。多分类提供了统一建模方式。

它像在多个候选答案中选一个最合适的。

例子：手写数字识别要在 0 到 9 之间选择一个类别。

## 数学定义

### 表达方式

$$
predicted_class = argmax logits
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Multiclass Classification 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Multiclass Classification 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Multiclass Classification 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 多分类和多标签不同。多分类通常只有一个真类别。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Multiclass Classification 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Multiclass Classification 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于图像分类、文本分类和意图识别。类别不均衡时要看分类别指标。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Softmax Function
- Cross Entropy

### 关联
- Multilabel Classification
- Confusion Matrix

### 延伸
- Multilabel Classification
- Confusion Matrix

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
