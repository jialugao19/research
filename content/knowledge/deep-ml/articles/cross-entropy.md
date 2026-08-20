---
id: article-cross-entropy
slug: cross-entropy
title: Cross Entropy：概念、直觉与边界
concepts:
- cross-entropy
learning_units:
- cross-entropy-overview
domain: machine_learning
level: beginner
content_type: theory
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Cross Entropy
- log loss
- machine learning
- beginner
- probability
- softmax function
- neural network
- theory
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
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
  id: article-plan-cross-entropy
  covered_concepts: 1
  primary_concept: cross-entropy
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
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
---
# Cross Entropy：概念、直觉与边界

Cross Entropy 是衡量真实分布与预测分布差异的损失函数，分类任务中常用它惩罚对正确类别分配过低概率的预测。

关键词：Cross Entropy
- log loss
- machine learning
- beginner
- probability
- softmax function
- neural network
- theory

## 为什么需要它

分类训练需要惩罚错误预测。交叉熵能对真实类别概率过低的情况给出强惩罚。

学习这个概念时，先固定样本空间、变量定义和条件，再解释核心关系：单标签分类中，softmax 与交叉熵可在 logits 上合并为 log-sum-exp 计算。这样既更稳定，也得到简洁梯度 p-y。

Cross Entropy 的价值在于给模糊问题划出可推理的边界。定义清楚以后，后续公式、例子和误区才有共同口径。

学习时可以从“真实类别概率是 0.9 时损失很小。概率是 0.01 时，损失会明显变大”开始，再回到定义检查哪些条件被默认使用。

## 核心直觉

单标签分类的交叉熵只读取真实类别对应的预测概率，并取负对数。预测正确且自信时损失接近零；把真实类别概率压到接近零时，惩罚会快速增大。

实际实现通常不先生成概率再取对数，而是在 logits 上把 softmax 与交叉熵融合成稳定的 log-sum-exp 计算。两者合并后的 logit 梯度是 `p - one_hot(y)`：模型分给各类的概率，减去真实标签分布。

因此，交叉熵既关心是否排对类别，也关心置信度。它不等于准确率，低交叉熵也不能单独证明样本外校准或业务收益。

## 数学定义

### 表达方式

$$
H(p,q)=-\sum_{i\in\mathcal X}p_i\log q_i
$$

### 变量解释

- p 是真实分布
- q 是预测分布
- i 是类别索引
- log q_i 是模型给正确概率后的对数惩罚

### 含义

当真实分布 p 固定时，最小化交叉熵等价于让预测分布 q 接近 p。

### 使用读法

读 Cross Entropy 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

推导从 Cross Entropy 的标准定义出发，保留会改变输出解释的变量。

$$
H(p,q)=H(p)+D_{\mathrm{KL}}(p\Vert q)
$$

推导的结果要回到 Cross Entropy 的使用场景中解释，不能只停留在符号变形。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。
- 应用到真实数据前，要检查这个前提是否和 `machine_learning` 领域的数据来源一致。
- 如果输入形态明显不同于“真实类别概率是 0.9 时损失很小。概率是 0.01 时，损失会明显变大”，需要重新确认输出解释。

## 常见误区

### 概念误解
- 交叉熵不是准确率；框架的 CrossEntropyLoss 通常接收原始 logits，而不是已经 softmax 的概率。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Cross Entropy 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Cross Entropy 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于分类、语言建模和策略学习。标签有噪声时，过高置信可能带来问题。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability
- Softmax Function

### 关联
- Neural Network

### 延伸
- Neural Network

## 延伸阅读

- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
