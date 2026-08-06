---
id: article-feed-forward-network
slug: feed-forward-network
title: Feed-Forward Network：模型结构与训练要点
concepts:
- feed-forward-network
learning_units:
- feed-forward-network-overview
domain: llm
level: intermediate
content_type: model
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Feed-Forward Network
- MLP block
- FFN
- llm
- intermediate
- transformer architecture
- gelu activation
- residual stream
profile:
  required_sections:
  - 为什么需要它
  - 结构直觉
  - 数学定义
  - 推导
  - 训练与推理
  - 假设与限制
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-feed-forward-network
  covered_concepts: 1
  primary_concept: feed-forward-network
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
- title: Attention Is All You Need
  url: https://arxiv.org/abs/1706.03762
  type: paper
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Feed-Forward Network：模型结构与训练要点

Transformer 块中对每个位置独立应用的两层或多层前馈子网络。

关键词：Feed-Forward Network
- MLP block
- FFN
- llm
- intermediate
- transformer architecture
- gelu activation
- residual stream

## 为什么需要它

注意力负责混合位置，模型还需要对每个位置做非线性特征变换。

选择这个模型时，要同时看表达能力、训练数据规模和 它用于 Transformer、LLM 和视觉 Transformer。参数量常占模型很大部分。

Feed-Forward Network 的表达能力来自模型结构，但泛化能力还取决于数据覆盖、正则化和训练目标。

在“Transformer 中的 MLP 层就是典型 FFN”这样的场景里，要区分模型真的学到结构，还是只利用了数据中的捷径特征。

## 结构直觉

- 输入：Feed-Forward Network 所处理的数据、状态或评价对象。
- 操作：FFN 通常先升维，再经过激活函数，再降维回隐藏维度。
- 观察结果：注意力负责混合位置，模型还需要对每个位置做非线性特征变换。

它像每个 token 自己经过一个小型加工站。

例子：Transformer 中的 MLP 层就是典型 FFN。

## 数学定义

### 表达方式

$$
FFN(x) = W2 activation(W1 x + b1) + b2
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Feed-Forward Network 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Feed-Forward Network 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

### 使用读法

读 Feed-Forward Network 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

先写出 Feed-Forward Network 的打分或表示，再把它连接到损失函数。

## 训练与推理

- 记录输入特征、目标变量、损失函数和评价指标。
- 分别检查训练误差、验证误差和线上分布漂移。
- 关注初始化、正则化和学习率对稳定性的影响。

最小验证可以从这个例子开始：Transformer 中的 MLP 层就是典型 FFN。先让小样例输出可解释，再把同样检查迁移到真实数据。

## 假设与限制

- 训练分布需要尽量接近部署分布。
- 模型容量、数据量和正则化强度需要匹配。
- 评价集不能泄漏到训练或调参流程中。
- 应用到真实数据前，要检查这个前提是否和 `llm` 领域的数据来源一致。
- 如果输入形态明显不同于“Transformer 中的 MLP 层就是典型 FFN”，需要重新确认输出解释。

## 常见误区

### 概念误解
- FFN 不混合不同 token。位置之间的信息混合主要由注意力完成。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Feed-Forward Network 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Feed-Forward Network 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 Transformer、LLM 和视觉 Transformer。参数量常占模型很大部分。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Transformer Architecture
- GELU Activation

### 关联
- Residual Stream
- Multi-Head Attention

### 延伸
- Residual Stream
- Multi-Head Attention

## 延伸阅读

- **Attention Is All You Need**：https://arxiv.org/abs/1706.03762。用途：追溯原始方法、关键假设和实验设定。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
