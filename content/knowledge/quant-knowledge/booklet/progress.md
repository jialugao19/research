# 小册子生成进度

来源大纲：`knowledge/outline.md`

## A. Python

### numpy

- [x] ndarray、dtype 与 shape
- [x] 索引、切片、视图与拷贝
- [x] broadcasting
- [x] axis 语义与聚合
- [x] 向量化计算与性能
- [x] 缺失值、nan 与 inf
- [x] 随机数与可复现性
- [x] 线性代数基础

### pandas

- [x] Series、DataFrame 与 Index
- [x] 选择、过滤、赋值与链式赋值
- [x] 缺失值处理
- [x] groupby / agg / transform
- [x] merge / join / concat
- [x] 时间序列索引与重采样
- [x] rolling / expanding / ewm
- [x] 数据对齐与广播
- [x] 向量化、apply 与性能
- [x] 因子数据面板的长表/宽表组织
- [x] 常见泄露：shift、rolling、未来函数

### 其余 Python 熟练项

- [x] scipy
  - [x] scipy 与 numpy 的关系、常用子模块、ndarray 互操作
  - [x] scipy.stats：分布、概率密度、分位数与随机变量
  - [x] scipy.optimize：最小化、约束优化与根查找
  - [x] scipy.linalg：矩阵分解与线性方程
  - [x] scipy.sparse：稀疏矩阵格式与基本运算
- [x] sklearn
  - [x] estimator API：fit / predict / transform 与 Pipeline 基础
  - [x] train / test split、交叉验证与时间序列切分
  - [x] preprocessing：StandardScaler、OneHotEncoder 与 ColumnTransformer
  - [x] 监督学习基础：线性模型、树模型、分类与回归指标
  - [x] model selection：GridSearchCV、RandomizedSearchCV 与泄露风险
  - [x] feature importance、permutation importance 与模型解释
  - [x] sklearn 与 pandas / numpy 数据形态互操作
- [x] matplotlib
  - [x] Figure / Axes 与基础 line、scatter、bar 图
  - [x] 标题、坐标轴、图例、颜色和样式
  - [x] subplots、多图布局与共享坐标轴
  - [x] 直方图、箱线图、散点矩阵与诊断图
  - [x] 时间序列图、双轴图与 pandas 绘图互操作
  - [x] savefig、分辨率、导出格式与报告图片规范
- [x] statsmodels
  - [x] statsmodels 与 sklearn 的区别、数据接口与结果对象
  - [x] OLS：矩阵接口、公式接口与 summary 解读
  - [x] 回归诊断：残差、异方差、稳健标准误与影响点
  - [x] 时间序列模型接口：ARIMA / SARIMAX 基础与预测结果

### Python 理解项

- [x] vectorization
- [x] memory layout
- [x] multiprocessing
- [x] profiling
- [x] 数据对齐
- [x] rolling window
- [x] feature pipeline
- [x] backtest leakage
- [x] lookahead bias

## B. 概率统计 + 时间序列

### 概率统计

- [x] OLS
- [x] regularization
- [x] PCA
- [x] covariance shrinkage
- [x] bootstrap
- [x] Bayesian basics
- [x] cross-sectional regression
- [x] factor model
- [x] IC / RankIC
- [x] turnover
- [x] Sharpe
- [x] drawdown
- [x] capacity

### 时间序列

- [x] 基础随机微积分与期权定价思想
- [x] ARIMA
- [x] GARCH，平稳性、自相关、协整
- [x] Kalman filter
- [x] regime switch
- [x] cointegration
- [x] stationarity
- [x] autocorrelation
- [x] 怎么划分时间窗口防止未来信息泄露，如何处理非平稳性

## C. 数据结构与算法

- [x] hashmap
- [x] heap
- [x] binary search
- [x] deque
- [x] sorting
- [x] graph basics
- [x] rolling median
- [x] top-k
- [x] stream processing
- [x] order book simulation
- [x] interval merge

## D. Brain Teaser / Green Book

- [x] 条件概率
- [x] 贝叶斯
- [x] 期望
- [x] combinatorics
- [x] optimal stopping
- [x] game theory
- [x] 快速心算与估算

## E. 机器学习

- [x] robustness
- [x] stability
- [x] regime
- [x] feature decay
- [x] transaction cost
- [x] 决策树 / 随机森林 / XGBoost / LightGBM
  - [x] 决策树：分裂准则
  - [x] 决策树：过拟合控制
  - [x] 随机森林
  - [x] XGBoost / LightGBM
  - [x] 树模型特征重要性
- [x] linear model baseline
- [x] SVM、K-Means
  - [x] SVM
  - [x] K-Means
- [x] feature importance
- [x] overfitting diagnosis
- [x] hyperparameter tuning
- [x] ensemble

## F. 深度学习

### Part 1 · 基础与训练正确性

- [x] NN
- [x] 梯度检查与完整 checkpoint 恢复

### Part 2 · 训练与优化

- [x] AdamW、Muon 与参数分组
- [x] 归一化方法的统计维度

### Part 3 · 序列模型

- [x] LSTM
- [x] GRU
- [x] sequence modeling

### Part 4 · Attention 与 Transformer

- [x] attention
- [x] temporal embedding
- [x] Transformer for TS

### Part 5 · 高效系统

- [x] Attention IO 瓶颈、online softmax 与 FlashAttention

## G. Market Microstructure

- [x] bid-ask spread
- [x] order imbalance
- [x] queue position
- [x] adverse selection
- [x] inventory risk
- [x] market impact
- [x] VPIN
- [x] opening/closing auction
- [x] 因子模型：Fama-French、Barra 风险因子，理解因子构造、中性化、行业与市值控制
- [x] 投资组合理论：均值-方差优化、协方差收缩、风险平价
- [x] 市场微观结构：bid-ask bounce、VWAP、tick 数据特性
- [x] 回测框架：事件驱动回测与向量化回测、幸存者偏差、前视偏差、交易成本

## H. 计算机基础

- [x] 算法复杂度：大 O 表示法
- [x] 基本数据结构：列表、字典、集合的底层实现与操作代价
- [x] SQL：多表 JOIN 和聚合查询
- [x] Linux 命令行基本操作
- [x] Git 版本控制
- [x] Docker 或分布式计算框架基本概念

## 下一篇

全部完成：`knowledge/outline.md` 中的知识点均已覆盖到 `knowledge/booklet/` 小册子。
