---
id: article-binary-cross-entropy
slug: binary-cross-entropy
title: Binary Cross Entropy：概念、直觉与边界
concepts:
- binary-cross-entropy
learning_units:
- binary-cross-entropy-overview
domain: deep_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Binary Cross Entropy
- BCE
- deep learning
- beginner
- cross entropy
- logistic regression
- focal loss
- class imbalance
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
  id: article-plan-binary-cross-entropy
  covered_concepts: 1
  primary_concept: binary-cross-entropy
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Binary Cross Entropy：概念、直觉与边界

二分类或多标签任务中常用的交叉熵损失。

关键词：Binary Cross Entropy
- BCE
- deep learning
- beginner
- cross entropy
- logistic regression
- focal loss
- class imbalance

## 为什么需要它

二分类模型需要惩罚概率预测错误。BCE 对真实标签概率过低的情况很敏感。

## 核心直觉

- 输入：Binary Cross Entropy 所处理的数据、状态或评价对象。
- 操作：BCE 通常接收概率或 logits。框架中 logits 版本更稳定。
- 观察结果：二分类模型需要惩罚概率预测错误。BCE 对真实标签概率过低的情况很敏感。

它像要求模型把概率押在正确答案上。押错越自信，惩罚越大。

例子：多标签图像分类中，每个标签都可以单独计算 BCE。

## 数学定义

### 表达方式

$$
\ell(y,p)=-y\log p-(1-y)\log(1-p),\qquad 0<p<1
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Binary Cross Entropy 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Binary Cross Entropy 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Binary Cross Entropy 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- BCE 和 softmax 多分类交叉熵不同。多标签任务中类别可以同时为真。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Binary Cross Entropy 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Binary Cross Entropy 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于二分类、多标签分类和对比学习部分目标。类别不平衡时要考虑权重。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Cross Entropy
- Logistic Regression

### 关联
- Focal Loss
- Class Imbalance

### 延伸
- Focal Loss
- Class Imbalance

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
