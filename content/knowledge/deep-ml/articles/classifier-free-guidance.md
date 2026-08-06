---
id: article-classifier-free-guidance
slug: classifier-free-guidance
title: Classifier-Free Guidance：模型结构与训练要点
concepts:
- classifier-free-guidance
learning_units:
- classifier-free-guidance-overview
domain: deep_learning
level: advanced
content_type: model
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Classifier-Free Guidance
- CFG
- guidance scale
- deep learning
- advanced
- denoising process
- diffusion model
- model
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
  id: article-plan-classifier-free-guidance
  covered_concepts: 1
  primary_concept: classifier-free-guidance
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
- title: Hugging Face Transformers Documentation
  url: https://huggingface.co/docs/transformers/index
  type: official_docs
---
# Classifier-Free Guidance：模型结构与训练要点

扩散模型中用条件和无条件预测差值增强生成条件一致性的方法。

关键词：Classifier-Free Guidance
- CFG
- guidance scale
- deep learning
- advanced
- denoising process
- diffusion model
- model

## 为什么需要它

生成结果可能不够贴合提示。CFG 用引导强度拉近条件目标。

选择这个模型时，要同时看表达能力、训练数据规模和 它用于文本到图像、图像编辑和可控生成。

Classifier-Free Guidance 的表达能力来自模型结构，但泛化能力还取决于数据覆盖、正则化和训练目标。

在“文生图模型常通过 CFG 提升提示词跟随度”这样的场景里，要区分模型真的学到结构，还是只利用了数据中的捷径特征。

## 结构直觉

- 输入：Classifier-Free Guidance 所处理的数据、状态或评价对象。
- 操作：模型混合条件预测和无条件预测。guidance scale 控制强度。
- 观察结果：生成结果可能不够贴合提示。CFG 用引导强度拉近条件目标。

它像同时看普通版本和按提示版本，再把提示方向放大。

例子：文生图模型常通过 CFG 提升提示词跟随度。

## 数学定义

### 表达方式

$$
pred = uncond + s \cdot  (cond - uncond)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Classifier-Free Guidance 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Classifier-Free Guidance 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

### 使用读法

读 Classifier-Free Guidance 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

先写出 Classifier-Free Guidance 的打分或表示，再把它连接到损失函数。

## 训练与推理

- 记录输入特征、目标变量、损失函数和评价指标。
- 分别检查训练误差、验证误差和线上分布漂移。
- 关注初始化、正则化和学习率对稳定性的影响。

最小验证可以从这个例子开始：文生图模型常通过 CFG 提升提示词跟随度。先让小样例输出可解释，再把同样检查迁移到真实数据。

## 假设与限制

- 训练分布需要尽量接近部署分布。
- 模型容量、数据量和正则化强度需要匹配。
- 评价集不能泄漏到训练或调参流程中。
- 应用到真实数据前，要检查这个前提是否和 `deep_learning` 领域的数据来源一致。
- 如果输入形态明显不同于“文生图模型常通过 CFG 提升提示词跟随度”，需要重新确认输出解释。

## 常见误区

### 概念误解
- 引导强度过高会带来失真或多样性下降。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Classifier-Free Guidance 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Classifier-Free Guidance 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于文本到图像、图像编辑和可控生成。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Denoising Process

### 关联
- Diffusion Model

### 延伸
- Diffusion Model

## 延伸阅读

- **Denoising Diffusion Probabilistic Models**：https://arxiv.org/abs/2006.11239。用途：追溯原始方法、关键假设和实验设定。
- **Hugging Face Transformers Documentation**：https://huggingface.co/docs/transformers/index。用途：作为交叉核对材料，确认术语、公式和使用场景。
