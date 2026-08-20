---
id: article-mixture-of-experts
slug: mixture-of-experts
title: Mixture of Experts：概念、直觉与边界
concepts:
- mixture-of-experts
learning_units:
- mixture-of-experts-overview
domain: llm
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Mixture of Experts
- MoE
- mixture experts
- llm
- advanced
- feed forward network
- transformer architecture
- dynamic batching
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
  id: article-plan-mixture-of-experts
  covered_concepts: 1
  primary_concept: mixture-of-experts
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Mixture of Experts：概念、直觉与边界

用路由器为每个输入选择少量专家网络参与计算的模型结构。

关键词：Mixture of Experts
- MoE
- mixture experts
- llm
- advanced
- feed forward network
- transformer architecture
- dynamic batching

## 为什么需要它

模型想增加参数容量，但不想每个 token 都计算全部参数。MoE 提供稀疏计算。

## 核心直觉

- 输入：Mixture of Experts 所处理的数据、状态或评价对象。
- 操作：路由器选择专家。训练要处理负载均衡和专家塌缩问题。
- 观察结果：模型想增加参数容量，但不想每个 token 都计算全部参数。MoE 提供稀疏计算。

它像把问题分给少数合适专家处理。

例子：稀疏专家语言模型常只激活部分 FFN 专家。

## 数学定义

### 表达方式

$$
y=\sum_{k\in\operatorname{TopK}(g(x))}\tilde g_k(x)E_k(x),\qquad \sum_k\tilde g_k(x)=1
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Mixture of Experts 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Mixture of Experts 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Mixture of Experts 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- MoE 参数多，不代表推理一定慢。关键看激活专家数量。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Mixture of Experts 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Mixture of Experts 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于大模型扩容、多任务建模和高吞吐推理。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Feed-Forward Network
- Transformer Architecture

### 关联
- Dynamic Batching
- Model Serving

### 延伸
- Dynamic Batching
- Model Serving

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
