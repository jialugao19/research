---
id: article-linear-probing
slug: linear-probing
title: Linear Probing：概念、直觉与边界
concepts:
- linear-probing
learning_units:
- linear-probing-overview
domain: machine_learning
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Linear Probing
- linear probe
- machine learning
- intermediate
- transfer learning
- linear layer
- feature space
- model evaluation metrics
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
  id: article-plan-linear-probing
  covered_concepts: 1
  primary_concept: linear-probing
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Linear Probing：概念、直觉与边界

冻结预训练表示，只训练线性分类器来评估表示质量的方法。

关键词：Linear Probing
- linear probe
- machine learning
- intermediate
- transfer learning
- linear layer
- feature space
- model evaluation metrics

## 为什么需要它

我们需要判断表示本身是否有用，而不是只看完整微调结果。

## 核心直觉

- 输入：Linear Probing 所处理的数据、状态或评价对象。
- 操作：线性探针通常固定 backbone，只训练最后的线性层。
- 观察结果：我们需要判断表示本身是否有用，而不是只看完整微调结果。

它像不改学生的笔记，只用一个简单测试看笔记是否包含答案线索。

例子：视觉自监督模型常用 linear probing 评估特征。

## 数学定义

### 表达方式

$$
features = frozen_encoder(x), y = linear_probe(features)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Linear Probing 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Linear Probing 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Linear Probing 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 线性探针低分不一定表示模型没用，可能任务需要非线性读出。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Linear Probing 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Linear Probing 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于表示学习评估、自监督学习和迁移学习诊断。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Transfer Learning
- Linear Layer

### 关联
- Feature Space
- Model Evaluation Metrics

### 延伸
- Feature Space
- Model Evaluation Metrics

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
