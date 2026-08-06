---
id: article-checkpointing
slug: checkpointing
title: Checkpointing：工程用法与常见坑
concepts:
- checkpointing
learning_units:
- checkpointing-overview
domain: mlops
level: beginner
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Checkpointing
- model checkpoint
- recomputation
- mlops
- beginner
- experiment tracking
- pytorch module
- early stopping
profile:
  required_sections:
  - 问题场景
  - 核心机制
  - 实现要点
  - 常见故障
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-checkpointing
  covered_concepts: 1
  primary_concept: checkpointing
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: MLflow Documentation
  url: https://mlflow.org/docs/latest/index.html
  type: official_docs
---
# Checkpointing：工程用法与常见坑

在训练过程中保存模型和训练状态的工程机制。

关键词：Checkpointing
- model checkpoint
- recomputation
- mlops
- beginner
- experiment tracking
- pytorch module
- early stopping

## 问题场景

训练可能中断，也可能需要回到最好版本。checkpoint 保存恢复所需证据。

## 核心机制

- 输入：Checkpointing 所处理的数据、状态或评价对象。
- 操作：完整 checkpoint 通常包含模型权重、优化器状态、epoch、随机种子和配置。
- 观察结果：训练可能中断，也可能需要回到最好版本。checkpoint 保存恢复所需证据。

它像游戏存档。出错后不用从第一步重新开始。

例子：长时间训练大模型时，每隔一定步数保存一次 checkpoint。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Checkpointing 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- 只保存权重不一定能恢复训练。优化器状态也会影响后续结果。

## 相关概念

### 前置
- Experiment Tracking
- PyTorch Module

### 关联
- Early Stopping
- Model Serving

### 延伸
- Early Stopping
- Model Serving

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **MLflow Documentation**：https://mlflow.org/docs/latest/index.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
