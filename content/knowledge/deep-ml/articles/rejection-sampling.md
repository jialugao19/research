---
id: article-rejection-sampling
slug: rejection-sampling
title: Rejection Sampling：算法直觉与实现要点
concepts:
- rejection-sampling
learning_units:
- rejection-sampling-overview
domain: probability
level: intermediate
content_type: algorithm
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Rejection Sampling
- probability
- intermediate
- sampling distribution
- monte carlo methods
- algorithm
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
  id: article-plan-rejection-sampling
  covered_concepts: 1
  primary_concept: rejection-sampling
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
---
# Rejection Sampling：算法直觉与实现要点

从容易采样的提议分布中抽样，再按概率接受或拒绝的采样方法。

关键词：Rejection Sampling
- probability
- intermediate
- sampling distribution
- monte carlo methods
- algorithm

## 为什么需要它

目标分布可能难以直接采样。拒绝采样用更简单分布间接生成样本。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 Rejection Sampling 来说，提议分布需要覆盖目标分布。包络常数越松，接受率越低。

在 Rejection Sampling 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

一个可操作的掌握标准是：围绕“从复杂一维分布采样时，可用均匀分布作提议分布”构造小例子。先手动跟踪前两步，再解释每一步为什么改变当前结果。

## 核心直觉

- 输入：Rejection Sampling 所处理的数据、状态或评价对象。
- 操作：提议分布需要覆盖目标分布。包络常数越松，接受率越低。
- 观察结果：目标分布可能难以直接采样。拒绝采样用更简单分布间接生成样本。

它像先撒一批候选点，再只留下落在目标形状下方的点。

例子：从复杂一维分布采样时，可用均匀分布作提议分布。

## 数学定义

### 表达方式

$$
X\sim q,\quad U\sim\operatorname{Unif}(0,1),\qquad \text{accept }X\iff U\le\frac{p(X)}{M q(X)},\quad Mq(x)\ge p(x)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Rejection Sampling 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Rejection Sampling 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

### 使用读法

读 Rejection Sampling 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

把 Rejection Sampling 写成输入、状态更新和输出，推导时只保留影响目标的量。

## 算法流程

Input: Rejection Sampling
- Rejection Sampling 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: Rejection Sampling
- 目标分布可能难以直接采样。拒绝采样用更简单分布间接生成样本。

Steps: Rejection Sampling
1. 明确输入数据和目标统计量或目标函数。
2. 执行核心操作：提议分布需要覆盖目标分布。包络常数越松，接受率越低。
3. 记录每次更新或重采样后的结果。
4. 重复直到达到预算、收敛或评估稳定。
5. 用输出结果判断方法是否解决原问题。

## 实现要点

- 明确输入、输出和停止条件。
- 记录随机种子、超参数和数据版本。
- 用小规模样例验证每一步计算是否符合预期。

最小验证可以从这个例子开始：从复杂一维分布采样时，可用均匀分布作提议分布。先让小样例输出可解释，再把同样检查迁移到真实数据。

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Rejection Sampling 时要单独估计训练成本和推理成本。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。
- 应用到真实数据前，要检查这个前提是否和 `probability` 领域的数据来源一致。
- 如果输入形态明显不同于“从复杂一维分布采样时，可用均匀分布作提议分布”，需要重新确认输出解释。

## 常见误区

### 概念误解
- 拒绝采样在高维空间效率可能很差。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Rejection Sampling 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Rejection Sampling 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于概率模拟、贝叶斯计算和采样方法教学。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Probability
- Sampling Distribution

### 关联
- Monte Carlo Methods

### 延伸
- Monte Carlo Methods

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
