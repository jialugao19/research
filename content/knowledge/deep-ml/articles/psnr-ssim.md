---
id: article-psnr-ssim
slug: psnr-ssim
title: PSNR and SSIM：概念、直觉与边界
concepts:
- psnr-ssim
learning_units:
- psnr-ssim-overview
domain: computer_vision
level: beginner
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- PSNR and SSIM
- PSNR
- SSIM
- computer vision
- beginner
- mean squared error
- image reconstruction
- video quality metrics
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
  id: article-plan-psnr-ssim
  covered_concepts: 1
  primary_concept: psnr-ssim
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
---
# PSNR and SSIM：概念、直觉与边界

评估图像重建质量的两个常用指标。

关键词：PSNR and SSIM
- PSNR
- SSIM
- computer vision
- beginner
- mean squared error
- image reconstruction
- video quality metrics

## 为什么需要它

重建任务需要衡量输出和参考图像的差异。PSNR 和 SSIM 提供基线指标。

## 核心直觉

- 输入：PSNR and SSIM 所处理的数据、状态或评价对象。
- 操作：PSNR 基于均方误差。SSIM 比较亮度、对比度和结构。
- 观察结果：重建任务需要衡量输出和参考图像的差异。PSNR 和 SSIM 提供基线指标。

PSNR 看像素误差。SSIM 更关注结构相似度。

例子：图像压缩和超分辨率任务常报告 PSNR 与 SSIM。

## 数学定义

### 表达方式

$$
PSNR = 10 log10(MAX^2 / MSE)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- PSNR and SSIM 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 PSNR and SSIM 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 PSNR and SSIM 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 指标高不一定视觉最好。过平滑结果也可能分数不错。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 PSNR and SSIM 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 PSNR and SSIM 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于重建、压缩、去噪和超分辨率。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Mean Squared Error

### 关联
- Image Reconstruction
- Video Quality Metrics

### 延伸
- Image Reconstruction
- Video Quality Metrics

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
