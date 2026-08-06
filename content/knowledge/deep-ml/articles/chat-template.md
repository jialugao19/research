---
id: article-chat-template
slug: chat-template
title: Chat Template：概念、直觉与边界
concepts:
- chat-template
learning_units:
- chat-template-overview
domain: llm
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Chat Template
- template encoding
- llm
- beginner
- prompt template
- tokenization
- instruction tuning
- instruction loss masking
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
  id: article-plan-chat-template
  covered_concepts: 1
  primary_concept: chat-template
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# Chat Template：概念、直觉与边界

把多轮对话角色和内容转换成模型输入文本的格式规则。

关键词：Chat Template
- template encoding
- llm
- beginner
- prompt template
- tokenization
- instruction tuning
- instruction loss masking

## 为什么需要它

聊天模型需要知道谁在说话。chat template 把系统、用户和助手消息编码成统一格式。

## 核心直觉

- 输入：Chat Template 所处理的数据、状态或评价对象。
- 操作：模板通常定义角色标记、分隔符、结束符和是否加入生成提示。
- 观察结果：聊天模型需要知道谁在说话。chat template 把系统、用户和助手消息编码成统一格式。

它像给对话加上固定剧本格式。

例子：同一段对话在不同模型中可能需要不同 chat template。

## 数学定义

### 表达方式

$$
tokens = tokenizer.apply_chat_template(messages)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Chat Template 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Chat Template 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Chat Template 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 模板错了会显著影响回答行为，即使模型权重相同。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Chat Template 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Chat Template 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于聊天推理、指令微调、评测和数据整理。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Prompt Template
- Tokenization

### 关联
- Instruction Tuning
- Instruction Loss Masking

### 延伸
- Instruction Tuning
- Instruction Loss Masking

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
