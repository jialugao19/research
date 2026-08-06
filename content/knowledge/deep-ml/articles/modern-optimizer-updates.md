---
id: article-modern-optimizer-updates
slug: modern-optimizer-updates
title: 现代优化器更新：AdamW 与 Muon
concepts:
- adamw-optimizer
- muon-optimizer
learning_units:
- adamw-optimizer-overview
- muon-optimizer-overview
domain: optimization
level: advanced
content_type: algorithm
depth_level: level_3_deep_dive
target_chars:
  minimum: 3000
  maximum: 5000
keywords:
- AdamW Optimizer
- decoupled weight decay
- optimization
- intermediate
- adam optimizer
- weight decay
- regularization
- learning rate schedule
profile:
  required_sections:
  - 背景与变体
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
  id: article-plan-modern-optimizer-updates
  covered_concepts: 2
  primary_concept: adamw-optimizer
confidence:
  concept: 0.92
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
  - high_impact_or_deep_article
  - multi_concept_article
  - advanced_or_expert_topic
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
- title: Decoupled Weight Decay Regularization
  url: https://arxiv.org/abs/1711.05101
  type: paper
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: 'Muon: An Optimizer for Hidden Layers in Neural Networks'
  url: https://kellerjordan.github.io/posts/muon/
  type: technical_note
---
# 现代优化器更新：AdamW 与 Muon

把权重衰减与 Adam 的自适应梯度更新解耦，使参数收缩不再被逐坐标预条件缩放的优化器。 本文把 AdamW Optimizer、Muon Optimizer 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：AdamW Optimizer
- decoupled weight decay
- optimization
- intermediate
- adam optimizer
- weight decay
- regularization
- learning rate schedule

## 背景与变体

优化器设计同时处理方向、尺度、噪声和正则化。AdamW 与 Muon 位于不同层面，不能只按名称并列比较。

AdamW 延续 Adam 的逐坐标自适应更新，但把 weight decay 从梯度预条件中解耦。它让参数收缩拥有独立超参数和更清楚的解释。

Muon 面向二维隐藏层权重。它先积累矩阵动量，再近似正交化更新方向。非二维参数与特殊矩阵通常继续使用 AdamW。

实验时应保留纯 AdamW 基线，并固定数据顺序、训练预算和调参预算。结论要同时报告验证质量、吞吐、状态内存和稳定性。

## 为什么需要它

把 L2 惩罚直接混入 Adam 梯度后，衰减项也会经过自适应缩放，不能形成统一的参数收缩。

这些概念放在一起看，是因为它们共享 AdamW Optimizer 这条主线。

先看主线，再看 Muon Optimizer 的分工，能减少概念之间的跳跃感。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 AdamW Optimizer 来说，更新由自适应梯度步和 decoupled weight decay 两部分组成；bias 与归一化参数通常需要单独决定是否衰减。

在 AdamW Optimizer 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

一个可操作的掌握标准是：围绕“训练 Transformer 时，矩阵权重使用 weight decay，bias 与 norm 参数不衰减”构造小例子。先手动跟踪前两步，再解释每一步为什么改变当前结果。

## 核心直觉

- 输入：AdamW Optimizer 所处理的数据、状态或评价对象。
- 操作：更新由自适应梯度步和 decoupled weight decay 两部分组成；bias 与归一化参数通常需要单独决定是否衰减。
- 观察结果：把 L2 惩罚直接混入 Adam 梯度后，衰减项也会经过自适应缩放，不能形成统一的参数收缩。

AdamW 先按 Adam 处理任务梯度，再单独把参数按比例缩小，让优化方向和参数规模控制各司其职。

例子：训练 Transformer 时，矩阵权重使用 weight decay，bias 与 norm 参数不衰减。

AdamW Optimizer 的子概念分工：
- **Muon Optimizer**：对二维隐藏层权重的动量更新做矩阵正交化，并把其它参数交给常规优化器处理的混合优化策略。

## 数学定义

### AdamW：把衰减从梯度预条件中拿出来

$$
\theta_{t+1}=(1-\eta_t\lambda)\theta_t-\eta_t\frac{\hat m_t}{\sqrt{\hat v_t}+\epsilon}
$$

### 变量解释

- (\eta_t) 是学习率。
- (\lambda) 是解耦权重衰减系数。
- (\hat m_t,\hat v_t) 是偏差修正后的一阶与二阶矩。

衰减直接作用于参数，不进入 Adam 的逐坐标缩放。

### Muon：把二维更新看成矩阵

$$
M_t=\beta M_{t-1}+(1-\beta)G_t,\qquad U_t\approx\operatorname{orth}(M_t)
$$

### 含义

Muon 对二维隐藏层权重的动量矩阵做近似正交化；bias、norm、embedding 等非二维或特殊参数通常交给 AdamW。正交化可用 Newton--Schulz 迭代近似，避免每步完整 SVD。

## 推导

普通 L2 正则把 lambda×theta 加到梯度中。对 SGD，这与按比例缩小参数可对应；对 Adam，正则项也会被每个坐标的二阶矩缩放，因此不同坐标的有效衰减不同。AdamW 把收缩项移到预条件之后，使 weight decay 有独立、统一的含义。

Muon 的出发点不同：隐藏层参数天然是矩阵，逐元素缩放没有直接控制更新矩阵的奇异值结构。先形成动量，再近似把更新映射到较均衡的正交方向，目标是改善矩阵参数的更新几何。两者解决的问题并不相同，所以常以参数分组共同使用。

## 算法流程

Input: 参数、梯度、参数类型标签、学习率、动量与衰减配置。

Output: 更新后的参数与可恢复的优化器状态。

Steps:
1. 把二维隐藏层权重与 bias、norm、embedding 等其它参数显式分组。
2. 对 AdamW 组更新一阶、二阶矩，再执行解耦权重衰减。
3. 对 Muon 组更新动量矩阵，规范化其尺度并执行有限次 Newton--Schulz 迭代。
4. 按实现约定缩放正交化方向，再更新二维参数。
5. 记录两组的学习率、范数、状态内存和实际更新量，和纯 AdamW 基线比较。

## 实现要点

- AdamW 通常不对 bias 与归一化缩放参数做 weight decay，但必须把规则写成可检查的参数组。
- Muon 参数筛选不能只写“二维就用”；共享 embedding、输出头和特殊矩阵可能需要排除。
- Newton--Schulz 前先按实现约定缩放矩阵，迭代次数与低精度误差需要作为超参数记录。
- 比较优化器时固定模型、数据顺序、训练 token 数、学习率搜索预算和评估口径。
- checkpoint 必须保存两个优化器或联合优化器的完整状态与参数组映射。

## 复杂度

AdamW 为每个参数维护一阶与二阶矩，状态内存通常约为参数量的两份同精度张量。Muon 至少维护动量矩阵，并为正交化增加若干矩阵乘法；计算增量取决于矩阵形状和迭代次数。

评估时要分别报告 optimizer step 时间、峰值显存、端到端吞吐和达到同等验证损失的总训练成本。单步更慢的更新可能减少所需步数，也可能没有收益，不能只看一个维度。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。
- 应用到真实数据前，要检查这个前提是否和 `optimization` 领域的数据来源一致。
- 如果输入形态明显不同于“训练 Transformer 时，矩阵权重使用 weight decay，bias 与 norm 参数不衰减”，需要重新确认输出解释。

## 常见误区

### 概念误解
- AdamW 不是把 Adam 的 loss 多加一项 L2 就结束；解耦位置决定了它与普通 L2 正则的差异。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 AdamW Optimizer 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 AdamW Optimizer 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它常用于 Transformer、视觉模型和其它使用 Adam 系优化器的深度网络训练。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Adam Optimizer
- Weight Decay
- Momentum Optimizer
- Matrix Multiplication
- Newton-Schulz Iteration

### 关联
- Muon Optimizer

### 延伸
- Regularization
- Learning Rate Schedule
- AdamW Optimizer
- Singular Value Decomposition

## 延伸阅读

- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
- **Decoupled Weight Decay Regularization**：https://arxiv.org/abs/1711.05101。用途：追溯原始方法、关键假设和实验设定。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Muon: An Optimizer for Hidden Layers in Neural Networks**：https://kellerjordan.github.io/posts/muon/。用途：作为交叉核对材料，确认术语、公式和使用场景。
