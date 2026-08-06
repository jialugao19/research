---
id: article-softmax-function
slug: softmax-function
title: Softmax Function：概念、直觉与边界
concepts:
- softmax-function
learning_units:
- softmax-function-overview
domain: deep_learning
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Softmax Function
- probability distribution
- probabilities sum to one
- deep learning
- beginner
- probability
- activation functions
- cross entropy
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
  id: article-plan-softmax-function
  covered_concepts: 1
  primary_concept: softmax-function
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
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
---
# Softmax Function：概念、直觉与边界

把整组 logits 联合映射到概率单纯形的归一化指数函数。

关键词：Softmax Function
- probability distribution
- probabilities sum to one
- deep learning
- beginner
- probability
- activation functions
- cross entropy

## 为什么需要它

分类模型常输出一组 logits。softmax 把它们转成更容易解释的类别概率形式。

## 核心直觉

Softmax 接收的是一整组相对分数。指数会放大分数差异，归一化再把总量固定为 1，因此提高一个 logit 会同时改变所有类别的概率。

它不是逐元素 sigmoid。数值实现应使用 `z - max(z)`；减去同一个常数不改变概率，却能避免指数溢出。

输出形式像概率分布，但可靠概率还需要校准证据。分类训练若使用融合交叉熵，模型应交付 logits，让损失函数内部完成稳定 softmax。

## 数学定义

### 表达方式

$$
softmax(x_i) = exp(x_i) / sum_j exp(x_j)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Softmax Function 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Softmax Function 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Softmax Function 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- softmax 输出和为 1 不等于概率已校准；使用融合的交叉熵损失时，还不应先在模型外重复做 softmax。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Softmax Function 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Softmax Function 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于多分类、注意力权重和策略分布。类别很多时，计算成本需要关注。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability
- Activation Functions

### 关联
- Cross Entropy
- Scaled Dot-Product Attention

### 延伸
- Cross Entropy
- Scaled Dot-Product Attention

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
