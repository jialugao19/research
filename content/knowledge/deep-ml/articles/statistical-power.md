---
id: article-statistical-power
slug: statistical-power
title: Statistical Power：概念、直觉与边界
concepts:
- statistical-power
learning_units:
- statistical-power-overview
domain: statistics
level: intermediate
content_type: theory
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Statistical Power
- power experiment
- statistics
- intermediate
- hypothesis testing
- experiment design
- confidence interval
- theory
profile:
  required_sections:
  - 为什么需要它
  - 核心直觉
  - 数学定义
  - 推导
  - 常见误区
  - 相关概念
  - 延伸阅读
  formula_required: true
  formula_mode: display
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-statistical-power
  covered_concepts: 1
  primary_concept: statistical-power
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
# Statistical Power：概念、直觉与边界

当真实效果存在时，统计检验正确拒绝原假设的概率。

关键词：Statistical Power
- power experiment
- statistics
- intermediate
- hypothesis testing
- experiment design
- confidence interval
- theory

## 为什么需要它

样本太少时，真实效果也可能检不出来。统计功效衡量这种检出能力。

## 核心直觉

- 输入：Statistical Power 所处理的数据、状态或评价对象。
- 操作：功效受样本量、效应大小、显著性水平和噪声影响。
- 观察结果：样本太少时，真实效果也可能检不出来。统计功效衡量这种检出能力。

它像实验有多大把握发现真实差异。

例子：A/B 测试前可估算需要多少用户才能检测到目标提升。

## 数学定义

### 表达方式

$$
\operatorname{Power}(\theta)=\Pr_{\theta}(\text{reject }H_0)=1-\beta(\theta),\qquad \theta\in H_1
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Statistical Power 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Statistical Power 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

## 推导

从 Statistical Power 的定义出发，先写清事件、变量或对象，再代入条件关系。

## 常见误区

### 概念误解
- 未显著不代表没有效果。功效不足时结论很弱。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Statistical Power 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Statistical Power 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于实验设计、A/B 测试、医学研究和模型比较。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Hypothesis Testing

### 关联
- Experiment Design
- Confidence Interval

### 延伸
- Experiment Design
- Confidence Interval

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
