---
id: article-training-resume-and-gradient-checking
slug: training-resume-and-gradient-checking
title: 训练正确性：梯度检查与断点续训
concepts:
- gradient-checking
- checkpoint-resume-training
learning_units:
- gradient-checking-overview
- checkpoint-resume-training-overview
domain: deep_learning
level: intermediate
content_type: engineering
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Gradient Checking
- gradcheck
- finite-difference gradient check
- deep learning
- intermediate
- backpropagation
- automatic differentiation
- custom autograd function
profile:
  required_sections:
  - 问题场景
  - 核心机制
  - 实现要点
  - 检查清单
  - 假设与限制
  - 常见故障
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-training-resume-and-gradient-checking
  covered_concepts: 2
  primary_concept: gradient-checking
confidence:
  concept: 0.97
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
- title: Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)
  url: https://datawhalechina.github.io/deep-learning-notes/zh/index.html
  type: course_notes
- title: PyTorch Documentation
  url: https://pytorch.org/docs/stable/index.html
  type: official_docs
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# 训练正确性：梯度检查与断点续训

用有限差分近似数值梯度，并与反向传播给出的解析梯度比较的正确性检查方法。 本文把 Gradient Checking、Checkpoint Resume Training 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：Gradient Checking
- gradcheck
- finite-difference gradient check
- deep learning
- intermediate
- backpropagation
- automatic differentiation
- custom autograd function

## 问题场景

手写 backward 或自定义算子可能输出形状正确但数值错误，只看损失下降无法可靠定位局部导数问题。

这些概念放在一起看，是因为它们共享 Gradient Checking 这条主线。

先看主线，再看 Checkpoint Resume Training 的分工，能减少概念之间的跳跃感。

工程上要先固定运行约束，因为 手写 backward 或自定义算子可能输出形状正确但数值错误，只看损失下降无法可靠定位局部导数问题。

Gradient Checking 的难点通常不是单个 API，而是上游数据、资源预算和运行时约束同时变化。

落地时先把“为自定义激活函数实现 backward 后，逐个扰动少量参数并检查相对误差是否落在预设容差内”这类最小例子跑通，再逐步扩大规模。

## 核心机制

这两个检查分别守住训练流程的两个边界。

梯度检查守住“局部导数是否正确”。对第 (i) 个参数使用中心差分：

$$
g_i^{\mathrm{num}}=\frac{L(\theta+h e_i)-L(\theta-h e_i)}{2h}
$$

再与 backward 得到的 (g_i^{\mathrm{ana}}) 比较相对误差。检查时应使用小张量、双精度、固定随机性，并避开 ReLU 折点等不可微位置。

断点续训守住“下一步更新所需状态是否完整”。模型参数只决定当前前向结果；Adam 的一阶与二阶矩、学习率计划、AMP scaler、global step、随机数状态和数据顺序都会影响下一步。恢复顺序应是先按同一配置重建对象，再加载各自 state_dict，最后从记录的下一步继续。

## 实现要点

- 梯度检查只抽取少量参数或使用框架 gradcheck；全模型有限差分成本过高。
- 用相对误差而非只看绝对误差，并同时记录容差、dtype 与差分步长。
- checkpoint 至少包含 model、optimizer、epoch 或 global step；按需增加 scheduler、scaler、随机状态和采样器状态。
- 保存时先写临时文件再原子替换，避免进程中断留下半个 checkpoint。
- 加载外部 checkpoint 时限制反序列化对象，并显式选择 map_location。
- 恢复后先跑一个短区间，对比学习率、loss、参数更新量和数据位置，再启动长任务。

## 检查清单

- 数值梯度与解析梯度是否在同一参数、同一 loss reduction 和同一 batch 上比较？
- dropout、数据增强与随机采样是否关闭或固定？
- 模型结构、优化器参数组和 scheduler 配置是否与保存时一致？
- optimizer state 是否已经迁移到目标设备，global step 是否没有重复执行？
- 数据迭代器恢复后是否跳过或重复样本？分布式 world size 改变时是否明确降级策略？
- 恢复前后是否保存了配置、代码版本和 checkpoint 摘要，便于审计差异？

## 假设与限制

梯度检查验证的是给定小样例上的局部导数，不证明整个训练目标正确，也不覆盖数据泄漏和标签口径。差分步长过大有截断误差，过小会受浮点消减误差影响。

完全复现续训还依赖硬件、并行拓扑、确定性算子和数据加载顺序。若 world size、batch size 或梯度累积发生变化，应把它视为新训练轨迹，并记录为显式变更，而不是宣称无缝恢复。

## 常见故障

### 梯度检查失败
- 在不可微点比较，或忘记关闭 dropout 等随机操作。
- 使用 float32 和过小差分步长，数值消减淹没真实变化。
- backward 的 broadcast、reduction 或 batch averaging 与前向定义不一致。

### 断点恢复漂移
- 只加载 model state，没有加载 optimizer 与 scheduler state。
- 保存的是“已完成步”却从同一步重新执行，导致样本或更新重复。
- 参数组顺序改变，优化器状态被加载到错误参数。
- checkpoint 文件写入不完整，或来自不可信来源却直接反序列化。

## 相关概念

### 前置
- Backpropagation
- Automatic Differentiation
- Checkpointing
- PyTorch State Dict
- Experiment Tracking

### 关联
- Checkpoint Resume Training

### 延伸
- Custom Autograd Function
- Partial Derivative
- Resumable Processing
- Learning Rate Schedule

## 延伸阅读

- **Datawhale / jshn9515 Deep Learning Notes (CC BY-NC 4.0)**：https://datawhalechina.github.io/deep-learning-notes/zh/index.html。用途：补足理论背景、标准符号和课堂推导。
- **PyTorch Documentation**：https://pytorch.org/docs/stable/index.html。用途：查看 API 行为、参数约定和工程实现边界。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
