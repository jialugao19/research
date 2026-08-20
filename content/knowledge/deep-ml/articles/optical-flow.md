---
id: article-optical-flow
slug: optical-flow
title: Optical Flow：概念、直觉与边界
concepts:
- optical-flow
learning_units:
- optical-flow-overview
domain: computer_vision
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Optical Flow
- EPE
- computer vision
- intermediate
- convolutional neural network
- video quality metrics
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
  id: article-plan-optical-flow
  covered_concepts: 1
  primary_concept: optical-flow
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
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Optical Flow：概念、直觉与边界

估计视频相邻帧中像素或局部区域运动方向和速度的任务。

关键词：Optical Flow
- EPE
- computer vision
- intermediate
- convolutional neural network
- video quality metrics
- theory

## 为什么需要它

视频理解需要知道画面如何移动。光流提供密集运动信息。

## 核心直觉

- 输入：Optical Flow 所处理的数据、状态或评价对象。
- 操作：光流假设短时间内亮度变化可追踪。遮挡和快速运动会增加难度。
- 观察结果：视频理解需要知道画面如何移动。光流提供密集运动信息。

它像给每个像素画一根运动箭头。

例子：自动驾驶视频中，光流可辅助理解车辆和行人运动。

## 数学定义

### 表达方式

$$
I_xu+I_yv+I_t=0,\qquad (u,v)=\left(\frac{dx}{dt},\frac{dy}{dt}\right)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Optical Flow 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Optical Flow 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Optical Flow 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 光流不是目标检测。它关注运动场，而不是类别标签。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Optical Flow 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Optical Flow 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于视频理解、稳定、防抖、跟踪和动作分析。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Convolutional Neural Network

### 关联
- Video Quality Metrics

### 延伸
- Video Quality Metrics

## 延伸阅读

- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
