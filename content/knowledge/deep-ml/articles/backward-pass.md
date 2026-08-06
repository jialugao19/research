---
id: article-backward-pass
slug: backward-pass
title: Backward Pass：概念、直觉与边界
concepts:
- backward-pass
learning_units:
- backward-pass-overview
domain: deep_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Backward Pass
- loss backward
- deep learning
- beginner
- forward pass
- backpropagation
- optimizer step
- zero grad
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
  id: article-plan-backward-pass
  covered_concepts: 1
  primary_concept: backward-pass
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Backward Pass：概念、直觉与边界

根据损失从后往前计算各参数梯度的过程。

关键词：Backward Pass
- loss backward
- deep learning
- beginner
- forward pass
- backpropagation
- optimizer step
- zero grad

## 为什么需要它

模型需要知道哪些参数该怎么改。backward pass 负责给出梯度。

## 核心直觉

- 输入：Backward Pass 所处理的数据、状态或评价对象。
- 操作：反向传播沿计算图使用链式法则。框架通常自动完成这一步。
- 观察结果：模型需要知道哪些参数该怎么改。backward pass 负责给出梯度。

它像从最终错误倒推每个旋钮的责任。

例子：调用 loss.backward 会为参数累积梯度。

## 数学定义

### 表达方式

$$
grad = d loss / d parameter
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Backward Pass 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Backward Pass 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Backward Pass 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- backward 只算梯度，不自动改变参数。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Backward Pass 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Backward Pass 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于训练循环、自定义算子和梯度调试。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Forward Pass
- Backpropagation

### 关联
- Optimizer Step
- Zero Grad

### 延伸
- Optimizer Step
- Zero Grad

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
