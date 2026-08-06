---
id: article-instruction-complexity-scoring
slug: instruction-complexity-scoring
title: Instruction Complexity Scoring：概念、直觉与边界
concepts:
- instruction-complexity-scoring
learning_units:
- instruction-complexity-scoring-overview
domain: llm
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Instruction Complexity Scoring
- instruction complexity
- complexity scoring
- llm
- intermediate
- instruction following evaluation
- instruction constraint checking
- rubric based evaluation
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
  id: article-plan-instruction-complexity-scoring
  covered_concepts: 1
  primary_concept: instruction-complexity-scoring
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Instruction Complexity Scoring：概念、直觉与边界

按约束数量、意图数量和输出要求评估指令复杂度的方法。

关键词：Instruction Complexity Scoring
- instruction complexity
- complexity scoring
- llm
- intermediate
- instruction following evaluation
- instruction constraint checking
- rubric based evaluation

## 为什么需要它

不同提示难度差异很大。评测集需要区分简单指令和复杂指令。

## 核心直觉

- 输入：Instruction Complexity Scoring 所处理的数据、状态或评价对象。
- 操作：评分可统计约束、格式要求、工具需求、推理步骤和多意图数量。
- 观察结果：不同提示难度差异很大。评测集需要区分简单指令和复杂指令。

它像给任务说明书标注难度。

例子：同时要求格式、引用和多步推理的任务复杂度更高。

## 数学定义

### 表达方式

$$
complexity = weighted_sum(constraints, intents, steps)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Instruction Complexity Scoring 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Instruction Complexity Scoring 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Instruction Complexity Scoring 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 长提示不一定复杂，短提示也可能包含严格约束。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Instruction Complexity Scoring 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Instruction Complexity Scoring 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于指令评测、数据筛选、课程训练和 benchmark 分层。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Instruction Following Evaluation

### 关联
- Instruction Constraint Checking
- Rubric-Based Evaluation

### 延伸
- Instruction Constraint Checking
- Rubric-Based Evaluation

## 延伸阅读

- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
