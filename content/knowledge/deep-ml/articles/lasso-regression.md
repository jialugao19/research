---
id: article-lasso-regression
slug: lasso-regression
title: Lasso Regression：模型结构与训练要点
concepts:
- lasso-regression
learning_units:
- lasso-regression-overview
domain: machine_learning
level: intermediate
content_type: model
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- Lasso Regression
- L1 regression
- machine learning
- intermediate
- linear regression
- regularization
- ridge regression
- model
profile:
  required_sections:
  - 为什么需要它
  - 结构直觉
  - 数学定义
  - 推导
  - 训练与推理
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
  id: article-plan-lasso-regression
  covered_concepts: 1
  primary_concept: lasso-regression
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
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
---
# Lasso Regression：模型结构与训练要点

在线性回归中加入 L1 正则化的回归方法。

关键词：Lasso Regression
- L1 regression
- machine learning
- intermediate
- linear regression
- regularization
- ridge regression
- model

## 为什么需要它

高维数据中，可能只有少数特征真正有用。Lasso 倾向产生稀疏解。

选择这个模型时，要同时看表达能力、训练数据规模和 它用于特征选择、可解释回归和高维建模。正则强度很关键。

Lasso Regression 的表达能力来自模型结构，但泛化能力还取决于数据覆盖、正则化和训练目标。

在“基因表达特征很多时，Lasso 可以筛出一部分重要变量”这样的场景里，要区分模型真的学到结构，还是只利用了数据中的捷径特征。

## 结构直觉

- 输入：Lasso Regression 所处理的数据、状态或评价对象。
- 操作：L1 惩罚会把部分权重压到零。这样模型更稀疏。
- 观察结果：高维数据中，可能只有少数特征真正有用。Lasso 倾向产生稀疏解。

它像鼓励模型只保留少数关键旋钮。

例子：基因表达特征很多时，Lasso 可以筛出一部分重要变量。

## 数学定义

### 表达方式

$$
\hat w=\underset{w}{\operatorname{arg\,min}}\left\{\frac1n\lVert y-Xw\rVert_2^2+\lambda\lVert w\rVert_1\right\},\qquad \lambda\ge0
$$

### 变量解释

- 符号的输入项表示方法接收的数据、状态或中间表示
- 等号或箭头右侧表示计算得到的统计量、预测、表示或决策
- Lasso Regression 的变量口径必须结合数据形状、单位和任务目标解释

### 含义

该表达式记录 Lasso Regression 的核心变量关系。解释结果时，需要把每个符号重新绑定到具体任务的输入、状态或评价口径。

### 使用读法

读 Lasso Regression 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

先写出 Lasso Regression 的打分或表示，再把它连接到损失函数。

## 训练与推理

- 记录输入特征、目标变量、损失函数和评价指标。
- 分别检查训练误差、验证误差和线上分布漂移。
- 关注初始化、正则化和学习率对稳定性的影响。

最小验证可以从这个例子开始：基因表达特征很多时，Lasso 可以筛出一部分重要变量。先让小样例输出可解释，再把同样检查迁移到真实数据。

## 假设与限制

- 训练分布需要尽量接近部署分布。
- 模型容量、数据量和正则化强度需要匹配。
- 评价集不能泄漏到训练或调参流程中。
- 应用到真实数据前，要检查这个前提是否和 `machine_learning` 领域的数据来源一致。
- 如果输入形态明显不同于“基因表达特征很多时，Lasso 可以筛出一部分重要变量”，需要重新确认输出解释。

## 常见误区

### 概念误解
- 稀疏不等于一定正确。强相关特征中选择结果可能不稳定。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Lasso Regression 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Lasso Regression 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于特征选择、可解释回归和高维建模。正则强度很关键。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Regression
- Regularization

### 关联
- Ridge Regression

### 延伸
- Ridge Regression

## 延伸阅读

- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
