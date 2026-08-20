---
id: article-temporal-difference-learning
slug: temporal-difference-learning
title: 时序差分学习：Bellman、SARSA 与 Q-Learning
concepts:
- temporal-difference-learning
- bellman-equation
- bellman-expectation-equation
- q-learning
- sarsa
- deep-q-network
- replay-buffer
- exploration-exploitation
learning_units:
- temporal-difference-learning-overview
- bellman-equation-overview
- bellman-expectation-equation-overview
- q-learning-overview
- sarsa-overview
- deep-q-network-overview
- replay-buffer-overview
- exploration-exploitation-overview
domain: reinforcement_learning
level: advanced
content_type: algorithm
depth_level: level_3_deep_dive
target_chars:
  minimum: 3000
  maximum: 5000
keywords:
- Temporal Difference Learning
- TD learning
- TD prediction
- reinforcement learning
- intermediate
- bellman equation
- exploration exploitation
- sarsa
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
  id: article-plan-temporal-difference-learning
  covered_concepts: 8
  primary_concept: temporal-difference-learning
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
  - high_impact_or_deep_article
  - multi_concept_article
  - advanced_or_expert_topic
  claim: Automated editorial checks passed; no human or factual certification is implied.
references:
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: Deep Learning Book
  url: https://www.deeplearningbook.org/
  type: textbook
---
# 时序差分学习：Bellman、SARSA 与 Q-Learning

用当前奖励和下一状态估计来更新价值函数的强化学习方法。 本文把 以 Temporal Difference Learning 为主线的 8 个概念 放在同一条学习线上，重点比较它们的输入、操作和边界。

关键词：Temporal Difference Learning
- TD learning
- TD prediction
- reinforcement learning
- intermediate
- bellman equation
- exploration exploitation
- sarsa

## 背景与变体

Temporal Difference Learning 的背景来自这个问题：完整回合结束后再学习可能太慢。TD 学习可以边交互边更新。

深入到这一层时，要把 TD 目标由即时奖励和下一状态价值组成。它结合了 Monte Carlo 和动态规划思想。 和实际应用边界一起看。

常见相邻方向先看 sarsa、q-learning。其它方向放到关系图里处理。

### 问题边界与知识位置

Temporal Difference Learning 处理的核心问题是：完整回合结束后再学习可能太慢。TD 学习可以边交互边更新。 它在完整系统中通常连接数据表示、优化过程与评价结果，不能只按一个孤立算子理解。阅读时先固定输入和输出，再追踪中间状态。文章同时覆盖 Bellman Equation、Bellman Expectation Equation 时，应比较它们分别改变了哪一个环节。

### 数学关系与可检验假设

核心关系可以概括为：TD 目标由即时奖励和下一状态价值组成。它结合了 Monte Carlo 和动态规划思想。 深入阅读的重点不是增加符号数量，而是说明定义、推导和假设如何互相约束。可以从“智能体每走一步，都可以用新状态修正上一个状态的价值”构造最小案例：先手算一轮，再用代码复现，并核对变量形状、随机性来源与数值范围。

### 变体、复杂度与工程观测

Temporal Difference Learning 的相邻变体包括 Bellman Equation、Bellman Expectation Equation。比较时应同时记录训练成本、推理成本和存储成本。不同瓶颈可能给出相反的工程选择，因此不能只用参数量或单次运行时间下结论。部署或大规模实验还应记录输入分布、关键中间量、输出质量与资源使用，保证失败能够定位。

### 失败证据与迁移规则

需要重点排除的误解是：TD 目标本身也含估计。它不是完全无偏的真实回报。 失败样本应按数据、方法假设、实现与评价口径分组，而不是只看平均分。迁移到 它用于 SARSA、Q-learning 和 actor-critic。函数近似时稳定性很重要。 等新场景时，可以复用概念定义，但必须重新确认输入、输出、指标和约束；旧任务中的经验不能直接视为新任务证据。

## 为什么需要它

完整回合结束后再学习可能太慢。TD 学习可以边交互边更新。

这些概念放在一起看，是因为它们共享 Temporal Difference Learning 这条主线。

先看主线，再看 以 Bellman Equation 为主线的 7 个概念 的分工，能减少概念之间的跳跃感。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 Temporal Difference Learning 来说，TD 目标由即时奖励和下一状态价值组成。它结合了 Monte Carlo 和动态规划思想。

在 Temporal Difference Learning 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

一个可操作的掌握标准是：围绕“智能体每走一步，都可以用新状态修正上一个状态的价值”构造小例子。先手动跟踪前两步，再解释每一步为什么改变当前结果。

## 核心直觉

- 输入：Temporal Difference Learning 所处理的数据、状态或评价对象。
- 操作：TD 目标由即时奖励和下一状态价值组成。它结合了 Monte Carlo 和动态规划思想。
- 观察结果：完整回合结束后再学习可能太慢。TD 学习可以边交互边更新。

它像走路时不断修正预计到达时间，而不是等走完再总结。

例子：智能体每走一步，都可以用新状态修正上一个状态的价值。

Temporal Difference Learning 的子概念分工：
- **Bellman Equation**：把当前价值和下一步价值递归联系起来的方程。
- **Bellman Expectation Equation**：描述给定策略下价值函数如何由一步奖励和后续价值递归组成的方程。
- **Q-Learning**：通过学习状态-动作价值函数来寻找优策略的无模型强化学习方法。
- **SARSA**：根据实际执行的下一动作更新动作价值的 on-policy 强化学习方法。

## 数学定义

### 表达方式

$$
\delta_t=R_{t+1}+\gamma V(S_{t+1})-V(S_t),\qquad V(S_t)\leftarrow V(S_t)+\alpha\delta_t
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Temporal Difference Learning 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Temporal Difference Learning 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

### 使用读法

读 Temporal Difference Learning 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

把 Temporal Difference Learning 写成输入、状态更新和输出，推导时只保留影响目标的量。

## 算法流程

Input: Temporal Difference Learning
- Temporal Difference Learning 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: Temporal Difference Learning
- 完整回合结束后再学习可能太慢。TD 学习可以边交互边更新。

Steps: Temporal Difference Learning
1. 明确输入数据和目标统计量或目标函数。
2. 执行核心操作：TD 目标由即时奖励和下一状态价值组成。它结合了 Monte Carlo 和动态规划思想。
3. 记录每次更新或重采样后的结果。
4. 重复直到达到预算、收敛或评估稳定。
5. 用输出结果判断方法是否解决原问题。

## 实现要点

- 明确输入、输出和停止条件。
- 记录随机种子、超参数和数据版本。
- 用小规模样例验证每一步计算是否符合预期。

最小验证可以从这个例子开始：智能体每走一步，都可以用新状态修正上一个状态的价值。先让小样例输出可解释，再把同样检查迁移到真实数据。

```python
q_sa = 0.4
reward = 1.0
next_best = 0.8
alpha = 0.1
gamma = 0.99
q_sa += alpha * (reward + gamma * next_best - q_sa)
print(round(q_sa, 4))
```

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Temporal Difference Learning 时要单独估计训练成本和推理成本。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。
- 应用到真实数据前，要检查这个前提是否和 `reinforcement_learning` 领域的数据来源一致。
- 如果输入形态明显不同于“智能体每走一步，都可以用新状态修正上一个状态的价值”，需要重新确认输出解释。

## 常见误区

### 概念误解
- TD 目标本身也含估计。它不是完全无偏的真实回报。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Temporal Difference Learning 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Temporal Difference Learning 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于 SARSA、Q-learning 和 actor-critic。函数近似时稳定性很重要。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Bellman Equation
- Exploration and Exploitation
- Markov Decision Process
- Policy Evaluation
- Temporal Difference Learning
- Q-Learning
- Neural Network
- Deep Q-Network

### 关联
- Bellman Equation
- Bellman Expectation Equation
- Q-Learning
- SARSA
- Deep Q-Network
- Replay Buffer
- Exploration and Exploitation

### 延伸
- SARSA
- Q-Learning
- Actor-Critic
- Value Iteration
- Policy Gradient
- Exploration and Exploitation
- Replay Buffer
- Temporal Difference Learning

## 延伸阅读

- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **Deep Learning Book**：https://www.deeplearningbook.org/。用途：作为交叉核对材料，确认术语、公式和使用场景。
