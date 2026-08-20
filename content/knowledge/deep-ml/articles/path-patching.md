---
id: article-path-patching
slug: path-patching
title: Path Patching：概念、直觉与边界
concepts:
- path-patching
learning_units:
- path-patching-overview
domain: deep_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Path Patching
- indirect effect isolation
- deep learning
- advanced
- computational graph
- attention mechanism
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
  id: article-plan-path-patching
  covered_concepts: 1
  primary_concept: path-patching
confidence:
  concept: 0.94
  prerequisite: 0.9
  prerequisite_path_eligible: true
generated_version:
  model: curated-catalog-v3
  prompt_version: chapter-profile-v3
review:
  state: automated_editorial
  last_review: null
  reviewer: null
  triggers:
  - advanced_or_expert_topic
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Path Patching：概念、直觉与边界

在神经网络内部替换特定激活路径，以估计信息流因果影响的分析方法。

关键词：Path Patching
- indirect effect isolation
- deep learning
- advanced
- computational graph
- attention mechanism
- theory

## 为什么需要它

只看最终输出很难知道模型内部哪条路径真正起作用。

## 核心直觉

- 输入：Path Patching 所处理的数据、状态或评价对象。
- 操作：方法通常在干净样本和干预样本之间替换中间激活，并比较输出变化。
- 观察结果：只看最终输出很难知道模型内部哪条路径真正起作用。

它像临时换掉一段电路，观察整机行为如何变化。

例子：分析 Transformer 时，可替换某层注意力头输出估计间接影响。

## 数学定义

### 表达方式

$$
\Delta y=y\!\left(h_j\leftarrow h_j^{\mathrm{source}}\right)-y\!\left(h_j^{\mathrm{baseline}}\right)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Path Patching 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Path Patching 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Path Patching 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- Path patching 给的是干预证据，不等于完整机制解释。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Path Patching 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Path Patching 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于可解释性、机制分析和模型调试。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Computational Graph
- Attention Mechanism

### 关联
- Computational Graph
- Attention Mechanism

### 延伸
- Computational Graph
- Attention Mechanism

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
