---
id: article-random-search
slug: random-search
title: Random Search：算法直觉与实现要点
concepts:
- random-search
learning_units:
- random-search-overview
domain: machine_learning
level: beginner
content_type: algorithm
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Random Search
- machine learning
- beginner
- hyperparameter tuning
- grid search
- algorithm
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 算法流程
  - 复杂度
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: true
  complexity_required: true
status: published
article_plan:
  id: article-plan-random-search
  covered_concepts: 1
  primary_concept: random-search
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Random Search：算法直觉与实现要点

从超参数空间中随机采样配置并比较验证表现的调参方法。

关键词：Random Search
- machine learning
- beginner
- hyperparameter tuning
- grid search
- algorithm

## 为什么需要它

网格搜索在高维空间中成本很高。随机搜索能更快探索重要维度。

## 核心直觉

- 输入：Random Search 所处理的数据、状态或评价对象。
- 操作：随机搜索适合部分参数更重要的场景。预算可直接控制采样次数。
- 观察结果：网格搜索在高维空间中成本很高。随机搜索能更快探索重要维度。

它像不按棋盘逐格试，而是在空间里随机撒点。

例子：随机采样 50 组学习率和正则强度来训练模型。

## 数学定义

### 表达方式

$$
\lambda_1,\ldots,\lambda_T\overset{\mathrm{iid}}{\sim}p(\lambda),\qquad \lambda^{\star}=\operatorname{arg\,min}_{t\le T}\widehat R_{\mathrm{val}}(\lambda_t)
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Random Search 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Random Search 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 算法流程

Input: Random Search
- Random Search 所处理的数据、状态或评价对象。
- 必要的超参数或停止条件。

Output: Random Search
- 网格搜索在高维空间中成本很高。随机搜索能更快探索重要维度。

Steps: Random Search
1. 明确输入数据和目标统计量或目标函数。
2. 执行核心操作：随机搜索适合部分参数更重要的场景。预算可直接控制采样次数。
3. 记录每次更新或重采样后的结果。
4. 重复直到达到预算、收敛或评估稳定。
5. 用输出结果判断方法是否解决原问题。

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Random Search 时要单独估计训练成本和推理成本。

## 常见误区

### 概念误解
- 随机不代表粗糙。足够预算下常比稀疏网格更有效。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Random Search 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Random Search 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于超参搜索、模型选择和实验探索。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Hyperparameter Tuning

### 关联
- Grid Search

### 延伸
- Grid Search

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
