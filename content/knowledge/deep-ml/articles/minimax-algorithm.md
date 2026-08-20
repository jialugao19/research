---
id: article-minimax-algorithm
slug: minimax-algorithm
title: Minimax Algorithm：算法直觉与实现要点
concepts:
- minimax-algorithm
learning_units:
- minimax-algorithm-overview
domain: game_theory
level: intermediate
content_type: algorithm
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Minimax Algorithm
- minimax
- tic tac toe minimax
- game theory
- intermediate
- recursion
- graph traversal
- dynamic programming
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
  id: article-plan-minimax-algorithm
  covered_concepts: 1
  primary_concept: minimax-algorithm
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
- title: Introduction to Algorithms
  url: https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/
  type: textbook
- title: 'Reinforcement Learning: An Introduction'
  url: http://incompleteideas.net/book/RLbook2020.pdf
  type: textbook
---
# Minimax Algorithm：算法直觉与实现要点

在零和博弈中假设双方都理性，选择最优行动的搜索算法。

关键词：Minimax Algorithm
- minimax
- tic tac toe minimax
- game theory
- intermediate
- recursion
- graph traversal
- dynamic programming

## 为什么需要它

对抗游戏中，自己的好决策取决于对手会如何回应。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 Minimax Algorithm 来说，最大化玩家选择最大收益，最小化玩家选择最小收益。

在 Minimax Algorithm 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

一个可操作的掌握标准是：围绕“井字棋可以用 minimax 搜索必胜、必平或必败状态”构造小例子。先手动跟踪前两步，再解释每一步为什么改变当前结果。

## 核心直觉

- 输入：Minimax Algorithm 所处理的数据、状态或评价对象。
- 操作：最大化玩家选择最大收益，最小化玩家选择最小收益。
- 观察结果：对抗游戏中，自己的好决策取决于对手会如何回应。

它像下棋时先假设对手会走最让你难受的一步。

例子：井字棋可以用 minimax 搜索必胜、必平或必败状态。

## 数学定义

### 表达方式

$$
V(s)=\max_{a\in\mathcal A(s)}\min_{b\in\mathcal B(s,a)}V(T(s,a,b))
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Minimax Algorithm 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Minimax Algorithm 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

### 使用读法

读 Minimax Algorithm 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

把 Minimax Algorithm 写成输入、状态更新和输出，推导时只保留影响目标的量。

## 算法流程

Input: Minimax Algorithm
- Minimax Algorithm 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: Minimax Algorithm
- 对抗游戏中，自己的好决策取决于对手会如何回应。

Steps: Minimax Algorithm
1. 明确输入数据和目标统计量或目标函数。
2. 执行核心操作：最大化玩家选择最大收益，最小化玩家选择最小收益。
3. 记录每次更新或重采样后的结果。
4. 重复直到达到预算、收敛或评估稳定。
5. 用输出结果判断方法是否解决原问题。

## 实现要点

- 明确输入、输出和停止条件。
- 记录随机种子、超参数和数据版本。
- 用小规模样例验证每一步计算是否符合预期。

最小验证可以从这个例子开始：井字棋可以用 minimax 搜索必胜、必平或必败状态。先让小样例输出可解释，再把同样检查迁移到真实数据。

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Minimax Algorithm 时要单独估计训练成本和推理成本。

## 假设与限制

- 输入数据需要满足方法默认的数据条件。
- 输出解释必须绑定具体任务和评价目标。
- 边界样本和异常值可能改变结论。
- 应用到真实数据前，要检查这个前提是否和 `game_theory` 领域的数据来源一致。
- 如果输入形态明显不同于“井字棋可以用 minimax 搜索必胜、必平或必败状态”，需要重新确认输出解释。

## 常见误区

### 概念误解
- minimax 依赖状态搜索。复杂游戏通常还要剪枝或近似评估。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Minimax Algorithm 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Minimax Algorithm 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于棋类 AI、博弈搜索、策略评估和对抗推理。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Recursion
- Graph Traversal

### 关联
- Dynamic Programming
- Q-Learning

### 延伸
- Dynamic Programming
- Q-Learning

## 延伸阅读

- **Introduction to Algorithms**：https://mitpress.mit.edu/9780262046305/introduction-to-algorithms/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **Reinforcement Learning: An Introduction**：http://incompleteideas.net/book/RLbook2020.pdf。用途：作为交叉核对材料，确认术语、公式和使用场景。
