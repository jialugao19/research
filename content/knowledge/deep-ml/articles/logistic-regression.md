---
id: article-logistic-regression
slug: logistic-regression
title: Logistic Regression：模型结构与训练要点
concepts:
- logistic-regression
learning_units:
- logistic-regression-overview
domain: machine_learning
level: beginner
content_type: model
depth_level: level_2_standard
target_chars:
  minimum: 1500
  maximum: 2500
keywords:
- sigmoid
- log-odds
- binary classification
- cross entropy
- Logistic Regression
- logit model
- machine learning
- beginner
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
  id: article-plan-logistic-regression
  covered_concepts: 1
  primary_concept: logistic-regression
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
- title: CS229 Machine Learning Notes
  url: https://cs229.stanford.edu/main_notes.pdf
  type: course_notes
- title: scikit-learn User Guide
  url: https://scikit-learn.org/stable/user_guide.html
  type: official_docs
---
# Logistic Regression：模型结构与训练要点

Logistic Regression 是用线性打分和 sigmoid 函数建模二分类条件概率的监督学习模型。

关键词：sigmoid
- log-odds
- binary classification
- cross entropy
- Logistic Regression
- logit model
- machine learning
- beginner

## 为什么需要它

许多任务要判断是或否。逻辑回归把线性分数转成类别概率。

选择这个模型时，要同时看表达能力、训练数据规模和 它用于风控、医学筛查和可解释分类。复杂边界需要非线性特征或其它模型。

Logistic Regression 的表达能力来自模型结构，但泛化能力还取决于数据覆盖、正则化和训练目标。

在“判断邮件是否为垃圾邮件，可以用词频特征训练逻辑回归”这样的场景里，要区分模型真的学到结构，还是只利用了数据中的捷径特征。

## 结构直觉

- 输入：特征向量 x 和二分类标签。
- 操作：先用线性函数打分，再用 sigmoid 转成概率。
- 观察结果：观察预测概率和真实标签之间的交叉熵是否降低。

它像先算一个倾向分，再把分数压到 0 到 1 之间。

例子：判断邮件是否为垃圾邮件，可以用词频特征训练逻辑回归。

## 数学定义

### 表达方式

$$
\Pr(y=1\mid x)=\sigma(w^{\top}x+b),\qquad \sigma(z)=\frac{1}{1+e^{-z}}
$$

### 变量解释

- x 是特征
- w 和 b 是参数
- sigma 是 sigmoid 函数
- 输出是正类概率

### 含义

线性打分先产生 log-odds，sigmoid 再把它压到 0 到 1 之间。

### 使用读法

读 Logistic Regression 的公式时，先确认输入对象，再确认输出量。不要只看符号是否熟悉，还要能说出每个变量来自哪一步数据或模型计算。

## 推导

推导先假设 log-odds 是线性的，再用 sigmoid 把线性打分变成概率。

$$
\log\frac{\Pr(y=1\mid x)}{\Pr(y=0\mid x)}=w^{\top}x+b
$$

log-odds 的线性假设让模型可解释，sigmoid 负责把分数映射为概率。

## 训练与推理

- 输入特征最好标准化，尤其是在使用正则化时。
- 输出是概率估计，不是天然校准过的业务决策。
- 类别不均衡时不要只看 accuracy，要检查 precision、recall 或 AUC。
- 完全线性可分数据可能导致参数继续增大，需要正则化。

最小验证可以从这个例子开始：判断邮件是否为垃圾邮件，可以用词频特征训练逻辑回归。先让小样例输出可解释，再把同样检查迁移到真实数据。

## 假设与限制

- 训练分布需要尽量接近部署分布。
- 模型容量、数据量和正则化强度需要匹配。
- 评价集不能泄漏到训练或调参流程中。
- 应用到真实数据前，要检查这个前提是否和 `machine_learning` 领域的数据来源一致。
- 如果输入形态明显不同于“判断邮件是否为垃圾邮件，可以用词频特征训练逻辑回归”，需要重新确认输出解释。

## 常见误区

### 概念误解
- 名字里有 regression，但它常用于分类。不要被术语误导。
### 数学误解
- 公式给出的是条件关系，不会自动保证数据满足这些条件。
- 对 Logistic Regression 来说，符号相同不代表变量口径相同。
### 使用误区
- 在 Logistic Regression 上得到更高分，也可能只是换了阈值、样本分布或评估口径。
- 如果只看 它用于风控、医学筛查和可解释分类。复杂边界需要非线性特征或其它模型。 的平均表现，很容易高估方法的稳定性。

## 相关概念

### 前置
- Linear Regression
- Cross Entropy

### 关联
- Model Evaluation Metrics
- Regularization

### 延伸
- Model Evaluation Metrics
- Regularization

## 延伸阅读

- **CS229 Machine Learning Notes**：https://cs229.stanford.edu/main_notes.pdf。用途：补足理论背景、标准符号和课堂推导。
- **scikit-learn User Guide**：https://scikit-learn.org/stable/user_guide.html。用途：查看 API 行为、参数约定和工程实现边界。
