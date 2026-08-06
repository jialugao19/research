# 知识点

## A. Python

### 熟练

- numpy
- pandas
- scipy
- sklearn
- matplotlib
- statsmodels

### 理解

- vectorization
- memory layout
- multiprocessing
- profiling
- 数据对齐
- rolling window
- feature pipeline
- backtest leakage
- lookahead bias

## B. 概率统计 + 时间序列

### 概率统计

- OLS
- regularization
- PCA
- covariance shrinkage
- bootstrap
- Bayesian basics
- cross-sectional regression
- factor model
- IC / RankIC
- turnover
- Sharpe
- drawdown
- capacity

### 时间序列

- **基础随机微积分与期权定价思想**（布朗运动、伊藤引理等基本性质）
- ARIMA
- GARCH，平稳性、自相关、协整
- Kalman filter
- regime switch
- cointegration
- stationarity
- autocorrelation
- 怎么划分时间窗口防止未来信息泄露，如何处理非平稳性

## C. 数据结构与算法

- hashmap
- heap
- binary search
- deque
- sorting
- graph basics
- rolling median
- top-k
- stream processing
- order book simulation
- interval merge

## D. Brain Teaser / Green Book

- 条件概率
- 贝叶斯
- 期望
- combinatorics
- optimal stopping
- game theory
- 快速心算与估算

## E. 机器学习

- robustness
- stability
- regime
- feature decay
- transaction cost

### 基础模型

- 决策树/随机森林/XGBoost/LightGBM
    - 解释分裂准则、过拟合控制、特征重要性。
- linear model baseline
    - 线性回归、逻辑回归，正则化（L1/L2），从损失函数到参数估计推导
- SVM、K-Means
- feature importance
- overfitting diagnosis
- hyperparameter tuning
- ensemble

## F. 深度学习

### Part 1 · 基础与训练正确性

- NN：神经元、层、激活、前向传播、损失与反向传播
- 梯度检查与完整 checkpoint 恢复

### Part 2 · 训练与优化

- AdamW、Muon 与参数分组
- Batch、Layer、Instance、Group 归一化的统计维度

### Part 3 · 序列模型

- LSTM
- GRU
- sequence modeling：窗口、标签对齐与防泄露评估

### Part 4 · Attention 与 Transformer

- attention 的 query/key/value、mask 与多头机制
- temporal embedding
- Transformer for TS

### Part 5 · 高效系统

- Attention IO 瓶颈、online softmax 与 FlashAttention

## G. Market Microstructure

- bid-ask spread
- order imbalance
- queue position
- adverse selection
- inventory risk
- market impact
- VPIN
- opening/closing auction
- 因子模型：Fama-French、Barra 风险因子，理解因子构造、中性化、行业与市值控制。
- 投资组合理论：均值-方差优化、协方差收缩、风险平价。
- 市场微观结构：bid-ask bounce、成交量加权平均价（VWAP）、tick数据特性
- 回测框架：事件驱动回测与向量化回测的区别，幸存者偏差、前视偏差、交易成本（手续费、滑点）如何纳入。

## H. 计算机基础

- 算法复杂度（大O表示法），能分析自己策略代码的效率。
- 基本数据结构：列表、字典、集合的底层实现与操作代价。
- SQL：能从数据库提取行情、财务数据，会写多表JOIN和聚合查询。
- Linux命令行基本操作。
- Git版本控制，能展示自己的代码仓库。
- 了解Docker或分布式计算框架（如Spark）的基本概念
