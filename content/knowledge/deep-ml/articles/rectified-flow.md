---
id: article-rectified-flow
slug: rectified-flow
title: Rectified Flow：概念、直觉与边界
concepts:
- rectified-flow
learning_units:
- rectified-flow-overview
domain: deep_learning
level: advanced
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Rectified Flow
- flow models
- deep learning
- advanced
- diffusion model
- euler sampling
- unipc sampling
- denoising process
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
  id: article-plan-rectified-flow
  covered_concepts: 1
  primary_concept: rectified-flow
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
- title: Denoising Diffusion Probabilistic Models
  url: https://arxiv.org/abs/2006.11239
  type: paper
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# Rectified Flow：概念、直觉与边界

学习从噪声到数据的连续速度场，并用 ODE 方式生成样本的方法。

关键词：Rectified Flow
- flow models
- deep learning
- advanced
- diffusion model
- euler sampling
- unipc sampling
- denoising process

## 为什么需要它

生成模型希望用更直、更少步的路径从噪声到数据。

## 核心直觉

- 输入：Rectified Flow 所处理的数据、状态或评价对象。
- 操作：模型学习连接噪声分布和数据分布的流场。
- 观察结果：生成模型希望用更直、更少步的路径从噪声到数据。

它像把弯曲路线拉直，让采样更直接。

例子：图像生成可用 rectified flow 做少步采样。

## 数学定义

### 表达方式

$$
dx/dt = v_theta(x,t)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Rectified Flow 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Rectified Flow 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Rectified Flow 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 路径更直不代表训练更简单，数据和时间参数化仍关键。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Rectified Flow 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Rectified Flow 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于图像生成、采样加速和连续生成建模。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Diffusion Model
- Euler Sampling

### 关联
- UniPC Sampling
- Denoising Process

### 延伸
- UniPC Sampling
- Denoising Process

## 延伸阅读

- **Denoising Diffusion Probabilistic Models**：https://arxiv.org/abs/2006.11239。用途：追溯原始方法、关键假设和实验设定。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
