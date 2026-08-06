---
id: article-gradient-descent
slug: gradient-descent
title: 梯度下降与优化器家族
concepts:
- gradient-descent
- stochastic-gradient-descent
- mini-batch-training
- momentum-optimizer
- rmsprop-optimizer
- adam-optimizer
- adagrad-optimizer
- adadelta-optimizer
- adamax-optimizer
learning_units:
- gradient-descent-overview
- stochastic-gradient-descent-overview
- mini-batch-training-overview
- momentum-optimizer-overview
- rmsprop-optimizer-overview
- adam-optimizer-overview
- adagrad-optimizer-overview
- adadelta-optimizer-overview
- adamax-optimizer-overview
domain: deep_learning
level: intermediate
content_type: algorithm
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- objective function
- gradient
- learning rate
- convergence
- Gradient Descent
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
  formula_required: true
  formula_mode: display
  algorithm_flow_required: true
  complexity_required: true
status: published
article_plan:
  id: article-plan-gradient-descent
  covered_concepts: 9
  primary_concept: gradient-descent
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: 'Adam: A Method for Stochastic Optimization'
  url: https://arxiv.org/abs/1412.6980
  type: paper
---
# 梯度下降与优化器家族

Gradient Descent 是一种沿目标函数负梯度方向迭代更新参数的优化方法。 本文把 以 Gradient Descent 为主线的 9 个概念 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：objective function
- gradient
- learning rate
- convergence
- Gradient Descent

## 为什么需要它

模型需要从错误中调整参数。梯度下降给出了一个简单的调整方向。

这些概念放在一起看，是因为它们共享 Gradient Descent 这条主线。

先看主线，再看 以 Stochastic Gradient Descent 为主线的 8 个概念 的分工，能减少概念之间的跳跃感。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 Gradient Descent 来说，每一步先计算梯度，再用学习率控制步长。学习率过大容易震荡，过小会很慢。

在 Gradient Descent 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

## 核心直觉

- 输入：参数向量和一个可微目标函数。
- 操作：计算当前位置的梯度，沿负梯度方向走一小步。
- 观察结果：观察损失是否下降，以及更新是否收敛或震荡。

如果损失像山坡高度，梯度指向上坡最快方向。沿负梯度走，通常会下山。

Gradient Descent 的子概念分工：
- **Stochastic Gradient Descent**：用单个样本或小批量样本估计梯度，并反复更新参数的训练方法。
- **Mini-Batch Training**：每次用一小批样本估计梯度并更新模型参数的训练方式。

## 数学定义

### 表达方式

$$
\theta_{t+1}=\theta_t-\eta\nabla J(\theta_t)
$$

### 变量解释

- \theta 是参数
- \eta 是学习率

### 含义

梯度给出局部上升最快方向，负梯度更新让目标函数在局部线性近似下下降。

## 推导

推导依赖一阶泰勒近似：在当前位置附近，用梯度描述目标函数的局部变化。

$$
J(\theta+\Delta)\approx J(\theta)+\nabla J(\theta)^\top\Delta,\quad \Delta=-\eta\nabla J(\theta)
$$

如果学习率足够小，负梯度方向会在局部线性近似下让目标下降。

## 算法流程

Input: Gradient Descent
- 参数向量和一个可微目标函数。
- 必要的超参数或停止条件。

Output: Gradient Descent
- 观察损失是否下降，以及更新是否收敛或震荡。

Steps: Gradient Descent
1. 固定输入、目标与停止条件。
2. 执行核心操作：计算当前位置的梯度，沿负梯度方向走一小步。
3. 检查输出，并在达到预算或稳定条件时停止。

## 实现要点

- 学习率过大容易震荡，过小会让收敛非常慢。
- 梯度尺度受特征标准化影响；未标准化特征会放大调参难度。
- 监控 loss 曲线和梯度范数，区分未收敛、发散和数值溢出。
- 批量、小批量和随机梯度的噪声不同，不能直接比较单步更新。

```python
theta = 1.0
lr = 0.1
for _ in range(5):
    grad = 2 * theta
    theta -= lr * grad
print(round(theta, 4))
```

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Gradient Descent 时要单独估计训练成本和推理成本。

## 假设与限制

- 目标函数需要在局部可微或至少有可用的梯度估计。
- 学习率和梯度尺度需要匹配。
- 非凸目标下收敛点不一定是全局最优。

## 常见误区

### 概念误解
- 梯度下降不保证找到全局最优。它也不是越快越好，稳定性很重要。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Gradient Descent 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Gradient Descent 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它是神经网络训练的基础。复杂优化器大多是在它上面加入动量、缩放或自适应学习率。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Algebra
- Gradient Descent
- Mini-Batch Training
- Stochastic Gradient Descent

### 关联
- Stochastic Gradient Descent
- Mini-Batch Training
- Momentum Optimizer
- RMSprop Optimizer

### 延伸
- Stochastic Gradient Descent
- Adam Optimizer
- Backpropagation
- Batch Normalization

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Adam: A Method for Stochastic Optimization**：https://arxiv.org/abs/1412.6980。用途：追溯原始方法、关键假设和实验设定。
