---
id: article-label-smoothing
slug: label-smoothing
title: Label Smoothing：概念、直觉与边界
concepts:
- label-smoothing
learning_units:
- label-smoothing-overview
domain: deep_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Label Smoothing
- deep learning
- intermediate
- cross entropy
- one hot encoding
- model calibration
- regularization
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
  id: article-plan-label-smoothing
  covered_concepts: 1
  primary_concept: label-smoothing
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Label Smoothing：概念、直觉与边界

把硬标签稍微软化的分类训练正则化方法。

关键词：Label Smoothing
- deep learning
- intermediate
- cross entropy
- one hot encoding
- model calibration
- regularization
- theory

## 为什么需要它

模型过度相信硬标签时，可能变得过于自信。label smoothing 缓解这种问题。

## 核心直觉

- 输入：Label Smoothing 所处理的数据、状态或评价对象。
- 操作：真实类别概率会从 1 降到略小值。其它类别分到少量概率。
- 观察结果：模型过度相信硬标签时，可能变得过于自信。label smoothing 缓解这种问题。

它像告诉模型答案很明确，但不要自信到极端。

例子：图像分类训练中，label smoothing 可减少过度自信预测。

## 数学定义

### 表达方式

$$
\tilde y_k=(1-\varepsilon)y_k+\frac{\varepsilon}{K},\qquad \varepsilon\in[0,1]
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Label Smoothing 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Label Smoothing 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Label Smoothing 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 它不是修正错误标签的万能方法。噪声标签仍需要单独处理。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Label Smoothing 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Label Smoothing 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分类、Transformer 训练和模型校准。过强会降低可分性。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Cross Entropy
- One-Hot Encoding

### 关联
- Model Calibration
- Regularization

### 延伸
- Model Calibration
- Regularization

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
