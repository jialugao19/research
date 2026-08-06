---
id: article-beam-search
slug: beam-search
title: 语言模型解码：Beam Search、温度与 Top-p
concepts:
- beam-search
- beam-search-length-penalty
- temperature-sampling
- top-k-sampling
- nucleus-sampling
- autoregressive-generation
- perplexity
learning_units:
- beam-search-overview
- beam-search-length-penalty-overview
- temperature-sampling-overview
- top-k-sampling-overview
- nucleus-sampling-overview
- autoregressive-generation-overview
- perplexity-overview
domain: llm
level: intermediate
content_type: algorithm
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Beam Search
- llm
- intermediate
- language modeling
- temperature sampling
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 算法流程
  - 实现要点
  - 复杂度
  - 假设与限制
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: true
  complexity_required: true
status: published
article_plan:
  id: article-plan-beam-search
  covered_concepts: 7
  primary_concept: beam-search
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
  - multi_concept_article
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: Attention Is All You Need
  url: https://arxiv.org/abs/1706.03762
  type: paper
---
# 语言模型解码：Beam Search、温度与 Top-p

在序列生成中保留多个高分候选路径的搜索方法。 本文把 以 Beam Search 为主线的 7 个概念 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：Beam Search
- llm
- intermediate
- language modeling
- temperature sampling

## 为什么需要它

每步只选最高概率 token 可能错过更好的整体序列。beam search 保留多个选择。

这些概念放在一起看，是因为它们共享 Beam Search 这条主线。

先看主线，再看 以 Beam Search Length Penalty 为主线的 6 个概念 的分工，能减少概念之间的跳跃感。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 Beam Search 来说，beam width 决定保留候选数。宽度越大，搜索更充分，但成本更高。

在 Beam Search 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

## 核心直觉

- 输入：Beam Search 所处理的数据、状态或评价对象。
- 操作：beam width 决定保留候选数。宽度越大，搜索更充分，但成本更高。
- 观察结果：每步只选最高概率 token 可能错过更好的整体序列。beam search 保留多个选择。

它像同时尝试几条写作路线。每一步只保留目前最有希望的路线。

Beam Search 的子概念分工：
- **Beam Search Length Penalty**：在 beam search 中调整序列长度偏好的打分项。
- **Temperature Sampling**：通过温度参数调整生成分布平滑程度的采样方法。

## 数学定义

### 表达方式

`每步扩展候选，再按累计分数保留 top-k`

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策

### 含义

这里保留的是 Beam Search 的结构化表达，而不是可直接推导的标准公式。它用于说明输入、操作与输出的边界；实际计算应以任务定义和权威资料为准。

## 推导

把 Beam Search 写成输入、状态更新和输出，推导时只保留影响目标的量。

## 算法流程

Input: Beam Search
- Beam Search 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: Beam Search
- 每步只选最高概率 token 可能错过更好的整体序列。beam search 保留多个选择。

Steps: Beam Search
1. 固定输入、目标与停止条件。
2. 执行核心操作：beam width 决定保留候选数。宽度越大，搜索更充分，但成本更高。
3. 检查输出，并在达到预算或稳定条件时停止。

## 实现要点

- 明确输入、输出和停止条件。
- 记录随机种子、超参数和数据版本。
- 用小规模样例验证每一步计算是否符合预期。

```python
beams = [("", 0.0)]
steps = [{"A": -0.1, "B": -0.7}, {"C": -0.2, "D": -0.4}]
for scores in steps:
    beams = [(text + token, score + logp)
             for text, score in beams for token, logp in scores.items()]
    beams = sorted(beams, key=lambda item: item[1], reverse=True)[:2]
print(beams)
```

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Beam Search 时要单独估计训练成本和推理成本。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。

## 常见误区

### 概念误解
- beam 越大不一定越自然。它可能偏向保守或重复文本。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Beam Search 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Beam Search 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于翻译、摘要和结构化生成。开放式聊天常更偏向采样方法。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Language Modeling
- Beam Search
- Softmax Function
- Temperature Sampling

### 关联
- Beam Search Length Penalty
- Temperature Sampling
- Top-k Sampling
- Nucleus Sampling

### 延伸
- Temperature Sampling
- Perplexity
- Nucleus Sampling
- Beam Search

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Attention Is All You Need**：https://arxiv.org/abs/1706.03762。用途：追溯原始方法、关键假设和实验设定。
