---
id: article-bootstrap-sampling
slug: bootstrap-sampling
title: Bootstrap Sampling：算法直觉与实现要点
concepts:
- bootstrap-sampling
learning_units:
- bootstrap-sampling-overview
domain: statistics
level: intermediate
content_type: algorithm
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- empirical distribution
- resampling
- sampling distribution
- confidence interval
- Bootstrap Sampling
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
  id: article-plan-bootstrap-sampling
  covered_concepts: 1
  primary_concept: bootstrap-sampling
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
---
# Bootstrap Sampling：算法直觉与实现要点

Bootstrap Sampling 是一种基于经验分布的重采样方法，通过从原始样本中有放回抽取样本，估计统计量的抽样分布。

关键词：empirical distribution
- resampling
- sampling distribution
- confidence interval
- Bootstrap Sampling

## 为什么需要它

很多统计量难以直接写出方差。Bootstrap 用重采样近似不确定性。

判断是否采用这个算法时，重点看输入规模、停止条件和核心动作。对 Bootstrap Sampling 来说，每次有放回抽样生成一个数据集，再计算目标统计量。

在 Bootstrap Sampling 中，输入规模决定计算预算，停止条件决定结果稳定性。只看最终输出，往往看不出误差来自数据、初始化还是迭代过程。

## 核心直觉

- 输入：一组有限样本，例如 100 个观测值。
- 操作：每次从这 100 个值中有放回抽取 100 次，允许同一个样本重复出现，并重复生成 B 个新样本集。
- 观察结果：观察均值、方差或其它统计量在 B 次重采样中的波动范围。

它像用手头样本反复模拟新的小世界。

## 数学定义

### 表达方式

$$
X^*=(x_1^*,\ldots,x_n^*),\quad x_i^*\sim \hat P_n
$$

### 变量解释

- X 是原始样本
- X^* 是一次 bootstrap 样本

### 含义

经验分布把每个观测样本赋予相同概率。重复从经验分布抽样后，统计量的波动近似原统计量的抽样分布。

## 推导

推导从经验分布开始：把每个已观测样本看成概率质量相同的离散点。

$$
\hat P_n(x)=\frac{1}{n}\sum_{i=1}^n \mathbf{1}(x_i=x)
$$

这个推导说明 bootstrap 的随机性来自经验分布，而不是来自新采集的数据。

## 算法流程

Input: Bootstrap Sampling
- 一组有限样本，例如 100 个观测值。
- 必要的超参数或停止条件。

Output: Bootstrap Sampling
- 观察均值、方差或其它统计量在 B 次重采样中的波动范围。

Steps: Bootstrap Sampling
1. 固定输入、目标与停止条件。
2. 执行核心操作：每次从这 100 个值中有放回抽取 100 次，允许同一个样本重复出现，并重复生成 B 个新样本集。
3. 检查输出，并在达到预算或稳定条件时停止。

## 实现要点

- bootstrap size 通常设为原始样本量 n；如果改成其它大小，需要说明估计目标改变了什么。
- 采样必须设置 replacement=True，否则得到的是子采样而不是 bootstrap。
- B 次重采样要足够大；教学演示可以用几百次，报告置信区间通常需要更多重复。
- 固定随机种子便于复现，但不要把单个 seed 下的结果当作稳定结论。

```python
import random

data = [1.2, 0.9, 1.4, 1.1]
B = 1000
means = []
random.seed(7)

for _ in range(B):
    sample = random.choices(data, k=len(data))  # replacement=True
    means.append(sum(sample) / len(sample))

means.sort()
ci = (means[int(0.025 * B)], means[int(0.975 * B)])
print(ci)
```

## 复杂度

- 时间复杂度主要由样本数、迭代次数和每步计算成本决定。
- 空间复杂度主要来自中间状态、缓存和模型参数。
- 分析 Bootstrap Sampling 时要单独估计训练成本和推理成本。

## 假设与限制

- 样本最好近似独立同分布。
- 原始样本需要能够代表总体；有偏样本不会因为重采样而自动变无偏。
- 极小样本下经验分布过于粗糙，置信区间可能不稳定。

## 常见误区

### 概念误解
- Bootstrap 不能修复有偏样本。原始数据质量仍是前提。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Bootstrap Sampling 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Bootstrap Sampling 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于置信区间、模型评估和小样本分析。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Sampling Distribution

### 关联
- Confidence Interval
- Random Forest

### 延伸
- Confidence Interval
- Random Forest

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
