---
id: article-sql-null-handling
slug: sql-null-handling
title: SQL NULL Handling：工程用法与常见坑
concepts:
- sql-null-handling
learning_units:
- sql-null-handling-overview
domain: sql
level: beginner
content_type: engineering
depth_level: level_1_card
target_chars:
  minimum: 700
  maximum: 1400
keywords:
- SQL NULL Handling
- 'null'
- sql
- beginner
- sql where filtering
- pandas dataframe
- data leakage
- engineering
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
  id: article-plan-sql-null-handling
  covered_concepts: 1
  primary_concept: sql-null-handling
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
- title: PostgreSQL Documentation
  url: https://www.postgresql.org/docs/current/
  type: official_docs
- title: SQLite Documentation
  url: https://www.sqlite.org/docs.html
  type: official_docs
---
# SQL NULL Handling：工程用法与常见坑

处理数据库中未知或缺失值 NULL 的规则和方法。

关键词：SQL NULL Handling
- null
- sql
- beginner
- sql where filtering
- pandas dataframe
- data leakage
- engineering

## 问题场景

缺失值会改变比较、聚合和连接结果。NULL 需要显式处理。

## 核心机制

- 输入：SQL NULL Handling 所处理的数据、状态或评价对象。
- 操作：判断 NULL 通常用 IS NULL，而不是等号比较。
- 观察结果：缺失值会改变比较、聚合和连接结果。NULL 需要显式处理。

NULL 不是 0，也不是空字符串。它表示未知或缺失。

例子：统计用户年龄均值时，NULL 年龄通常不会参与 AVG。

## 实现要点

- 先固定输入输出契约，包括数据形状、类型、单位和空值策略。
- 把性能指标和正确性指标分开记录，避免只优化速度。
- 为边界输入、极端规模和失败重试写最小测试。

## 常见故障

### 配置错误
- 参数、数据形状或运行环境和 SQL NULL Handling 的预期不一致。
### 运行错误
- 资源、并发或数值范围异常会让结果不稳定。
### 解释错误
- NULL = NULL 的结果并不是真。SQL 使用三值逻辑。

## 相关概念

### 前置
- SQL WHERE Filtering

### 关联
- pandas DataFrame
- Data Leakage

### 延伸
- pandas DataFrame
- Data Leakage

## 延伸阅读

- **PostgreSQL Documentation**：https://www.postgresql.org/docs/current/。用途：作为交叉核对材料，确认术语、公式和使用场景。
- **SQLite Documentation**：https://www.sqlite.org/docs.html。用途：作为交叉核对材料，确认术语、公式和使用场景。
