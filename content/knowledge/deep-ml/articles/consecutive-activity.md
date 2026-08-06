---
id: article-consecutive-activity
slug: consecutive-activity
title: Consecutive Activity：工程用法与常见坑
concepts:
- consecutive-activity
learning_units:
- consecutive-activity-overview
domain: sql
level: intermediate
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- Consecutive Activity
- consecutive days
- consecutive login
- sql
- intermediate
- sql date functions
- sql window functions
- cohort retention
profile:
  required_sections:
  - 问题场景
  - 核心机制
  - 实现要点
  - 常见故障
  - 相关概念
  - 延伸阅读
  formula_required: false
  formula_mode: expression
  algorithm_flow_required: false
  complexity_required: false
status: published
article_plan:
  id: article-plan-consecutive-activity
  covered_concepts: 1
  primary_concept: consecutive-activity
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
- title: PostgreSQL Documentation
  url: https://www.postgresql.org/docs/current/
  type: official_docs
- title: SQLite Documentation
  url: https://www.sqlite.org/docs.html
  type: official_docs
---
# Consecutive Activity：工程用法与常见坑

识别用户或实体连续多天、多周发生行为的分析模式。

关键词：Consecutive Activity
- consecutive days
- consecutive login
- sql
- intermediate
- sql date functions
- sql window functions
- cohort retention

## 问题场景

连续活跃比单次活跃更能说明习惯。SQL 需要处理日期间隔。

## 核心机制

- 输入：Consecutive Activity 所处理的数据、状态或评价对象。
- 操作：常见做法是用窗口函数、日期差和分组技巧识别连续段。
- 观察结果：连续活跃比单次活跃更能说明习惯。SQL 需要处理日期间隔。

它像查一个人是否连续打卡。

例子：找出连续登录三天以上的用户。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 Consecutive Activity 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- 缺失日期和时区会影响连续性判断。

## 相关概念

### 前置
- SQL Date Functions
- SQL Window Functions

### 关联
- Cohort Retention

### 延伸
- Cohort Retention

## 延伸阅读

- **PostgreSQL Documentation**：https://www.postgresql.org/docs/current/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **SQLite Documentation**：https://www.sqlite.org/docs.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
