---
id: article-kv-cache
slug: kv-cache
title: KV Cache：概念、直觉与边界
concepts:
- kv-cache
learning_units:
- kv-cache-overview
domain: llm
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- KV Cache
- key value cache
- llm
- advanced
- causal mask
- multi head attention
- streaming inference
- grouped query attention
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
  id: article-plan-kv-cache
  covered_concepts: 1
  primary_concept: kv-cache
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
- title: Attention Is All You Need
  url: https://arxiv.org/abs/1706.03762
  type: paper
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
---
# KV Cache：概念、直觉与边界

自回归解码时按层保存历史 token 的 key/value 投影、只处理新增 token 的推理机制。

关键词：KV Cache
- key value cache
- llm
- advanced
- causal mask
- multi head attention
- streaming inference
- grouped query attention

## 为什么需要它

生成每个新 token 时，重复计算所有历史注意力很浪费。KV cache 复用历史结果。

## 核心直觉

自回归生成的第 `t` 步只需要产生最新位置的输出。历史 token 的各层 K/V 会被当前和未来 query 反复读取，因此值得缓存；历史 Q 已完成对应位置的输出，通常不再复用。

有 cache 后，每步只处理新增 token，再让当前 query 读取历史 K/V。Attention 仍要扫描上下文，并非常数成本。

每层 K/V 不同，缓存随 batch、KV head、序列长度和 head dimension 线性增长。这是用显存换前缀重算。

## 数学定义

### 表达方式

$$
K_{1:t}=\operatorname{concat}(K_{1:t-1},k_t),\quad V_{1:t}=\operatorname{concat}(V_{1:t-1},v_t),\quad o_t=\operatorname{Attention}(q_t,K_{1:t},V_{1:t})
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- KV Cache 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 KV Cache 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 KV Cache 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- KV cache 不会消除当前 token 对全部历史 K/V 的注意力计算，也主要不是普通并行训练的优化；它用持续增长的显存换取少算历史层。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 KV Cache 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 KV Cache 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于聊天模型、代码补全和流式推理。批处理时缓存管理更复杂。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Causal Mask
- Multi-Head Attention

### 关联
- Streaming Inference
- Grouped-Query Attention

### 延伸
- Streaming Inference
- Grouped-Query Attention

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Attention Is All You Need**：https://arxiv.org/abs/1706.03762。用途：追溯原始方法、关键假设和实验设定。
- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
