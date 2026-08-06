# 时间序列：时间窗口划分、防止未来信息泄露与非平稳性处理

## 核心概念

时间序列建模最容易出错的地方不是模型本身，而是时间对齐。

一个可交易预测必须满足：

```text
在预测时点 t，只使用 t 当时及之前可见的信息，预测 t 之后的结果。
```

因此需要同时处理三个问题：

- 怎么划分 train / validation / test 时间窗口。
- 怎么构造特征和标签，避免未来信息泄露。
- 怎么处理非平稳性，避免用过期关系做预测。

如果时间窗口和数据对齐错了，模型再复杂也只是在学习未来。

## 什么是未来信息泄露

未来信息泄露 lookahead leakage 指训练或回测中使用了当时不可见的信息。

常见形式：

- 用 `return[t]` 预测 `return[t]`，但交易只能在 `t` 之前决策。
- rolling 特征没有 `.shift(1)`。
- 使用全样本标准化、全样本分位数、全样本缺失值填充。
- 用完整样本选特征、选参数、选股票池。
- 用未来成分股、未来财务数据、未来停牌退市信息。
- 重叠标签没有 embargo，导致训练标签和测试标签共享未来收益。

防泄露的核心原则：

```text
每一步数据处理都必须问：这个数在当时能不能知道？
```

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一条日收益序列，并在后半段加入轻微 regime 变化：

```python
rng = np.random.default_rng(72)

n_obs = 260
dates = pd.bdate_range("2024-01-02", periods=n_obs)

returns = pd.Series(
    rng.normal(loc=0.0003, scale=0.01, size=n_obs),
    index=dates,
    name="return",
)

returns.iloc[140:] = returns.iloc[140:] + 0.0007

price = (100 * (1 + returns).cumprod()).rename("price")

print(price.head())
print(price.tail())
```

这里后半段均值略有变化，用来模拟非平稳环境。

真实市场中的 regime 变化通常更复杂，可能体现在均值、波动、相关性、流动性和交易成本上。

## 正确构造滞后特征

假设用过去 20 日平均收益预测未来 5 日收益。

特征必须只使用当前日期之前的数据：

```python
lookback = 20
horizon = 5

feature = returns.rolling(lookback).mean().shift(1).rename("feature")
```

这里的 `.shift(1)` 很关键。

如果今天收盘后生成信号，过去 20 日收益可以包括今天还是不包括今天，取决于交易假设：

- 如果用今天收盘价生成明天开盘交易信号，可以包括今天收益。
- 如果在今天收盘前交易，不能包括今天收盘收益。

本例采用更保守的写法：`feature[t]` 只使用 `t-1` 及以前的收益。

## 正确构造未来标签

未来 5 日收益：

```python
forward_return_5d = sum(
    returns.shift(-step)
    for step in range(1, horizon + 1)
).rename("forward_return_5d")

panel = pd.concat([feature, forward_return_5d], axis=1).dropna()

print(panel.head())
print(panel.tail())
```

对齐含义：

```text
panel.loc[t, "feature"] 使用 t 之前的信息
panel.loc[t, "forward_return_5d"] 使用 t+1 到 t+5 的收益
```

最后几天没有完整未来收益，会被 `dropna()` 去掉。

## 错误示例：居中 rolling

`center=True` 会把窗口放在当前日期两边，因此使用未来数据。

```python
bad_feature = returns.rolling(
    lookback,
    center=True,
).mean().rename("bad_feature")

bad_panel = pd.concat([bad_feature, forward_return_5d], axis=1).dropna()

good_corr = panel["feature"].corr(panel["forward_return_5d"])
bad_corr = bad_panel["bad_feature"].corr(bad_panel["forward_return_5d"])

print(good_corr)
print(bad_corr)
```

如果 `bad_corr` 明显更高，不代表模型更好，而是因为特征直接看到了未来。

这种错误在 rolling、expanding、标准化、行业中性化、横截面排名中都可能出现。

## 时间顺序 train / test

时间序列不能随机打乱切分。

简单切分：

```python
train = panel.loc[: "2024-08-30"]
test = panel.loc["2024-09-02" :]

print(train.index.min(), train.index.max())
print(test.index.min(), test.index.max())
```

时间顺序切分保证：

```text
train 的日期早于 test
```

随机切分会把未来样本放进训练集，导致模型间接看到未来 regime 和分布。

## walk-forward 切分

更接近实盘的方式是 walk-forward。

例如：

- 训练 80 个样本。
- 跳过 5 天 embargo。
- 测试 20 个样本。
- 每次向前滚动 20 个样本。

```python
def make_walk_forward_splits(index, train_size, test_size, embargo):
    splits = []
    start = 0

    while True:
        train_start = start
        train_end = train_start + train_size
        test_start = train_end + embargo
        test_end = test_start + test_size

        if test_end > len(index):
            break

        splits.append({
            "train_start": index[train_start],
            "train_end": index[train_end - 1],
            "test_start": index[test_start],
            "test_end": index[test_end - 1],
        })

        start += test_size

    return pd.DataFrame(splits)


splits = make_walk_forward_splits(
    panel.index,
    train_size=80,
    test_size=20,
    embargo=horizon,
)

print(splits)
```

walk-forward 的优点：

- 每次只用过去训练。
- 可以观察模型随时间衰减。
- 更接近真实上线后的反复更新。

## embargo 的作用

如果标签是未来 5 日收益，训练样本靠近测试样本时，标签区间可能重叠。

例如训练样本 `t` 的标签用到 `t+1` 到 `t+5`，而测试样本从 `t+3` 开始，就会共享未来收益。

`embargo=horizon` 的作用是：

```text
训练窗口结束后，空出一段时间，再开始测试窗口。
```

检查：

```python
assert (splits["train_end"] < splits["test_start"]).all()

print(splits[["train_end", "test_start"]].head())
```

在高频或重叠标签场景中，还可能需要 purged cross-validation，把和测试标签区间重叠的训练样本剔除。

## 标准化也要只用训练集

错误做法：

```text
用全样本 mean/std 标准化，然后再切 train/test
```

正确做法：每个窗口只用训练集估计标准化参数。

```python
scaled_rows = []

for _, split in splits.iterrows():
    train_window = panel.loc[split["train_start"] : split["train_end"]]
    test_window = panel.loc[split["test_start"] : split["test_end"]]

    mean_train = train_window["feature"].mean()
    std_train = train_window["feature"].std(ddof=1)

    test_z = (test_window["feature"] - mean_train) / std_train

    scaled_rows.append({
        "train_start": split["train_start"],
        "train_end": split["train_end"],
        "test_start": split["test_start"],
        "test_end": split["test_end"],
        "train_mean": mean_train,
        "test_z_mean": test_z.mean(),
    })

scaled_summary = pd.DataFrame(scaled_rows)

print(scaled_summary.head())
```

这同样适用于：

- winsorize 阈值。
- 缺失值填充值。
- PCA。
- 特征选择。
- 行业或市值中性化参数。
- 模型超参数选择。

## 非平稳性处理

非平稳性不是只靠一个检验解决。实际策略要处理的是关系随时间变化。

常见做法：

1. 使用滚动窗口训练，而不是无限扩张。
2. 对特征做去趋势、差分、收益率化或标准化。
3. 分 regime 训练或加入 regime 特征。
4. 对模型参数做衰减加权，近期样本权重更高。
5. 设置样本外监控，发现 performance decay 后降权。
6. 分年份、分波动环境、分市场状态评估。

示例：比较前后半段收益均值。

```python
first_half_mean = returns.iloc[:140].mean()
second_half_mean = returns.iloc[140:].mean()

print(first_half_mean)
print(second_half_mean)
```

如果分布已经变化，全样本训练出来的参数可能过时。

## expanding window 和 rolling window

两种常见训练窗口：

```text
expanding window: 训练集从起点不断扩大
rolling window: 只保留最近固定长度样本
```

选择取决于问题：

- 如果关系稳定，expanding 使用更多数据，估计更稳。
- 如果关系变化快，rolling 更能适应近期状态。
- 如果样本太短，rolling 估计可能很 noisy。

伪代码：

```text
for each rebalance date:
    if expanding:
        train = data[start : t]
    if rolling:
        train = data[t - lookback : t]

    fit preprocessing on train
    fit model on train
    predict next period
```

关键点：无论 expanding 还是 rolling，窗口右端都不能超过预测时点。

## 常见坑

第一，rolling 后忘记 shift。

如果 rolling 特征包含当前或未来标签期的信息，回测会被抬高。

第二，全样本预处理。

全样本标准化、PCA、特征选择、缺失值填充都会泄露未来分布。

第三，随机切分时间序列。

随机切分破坏时间顺序，让训练集看到未来 regime。

第四，重叠标签不做 embargo。

训练和测试标签共享未来收益，会低估误差。

第五，用样本外结果反复调参。

如果一直根据 test 表现改模型，test 会变成新的训练集。

第六，只在全样本报告一个指标。

非平稳市场中，全样本 Sharpe 可能掩盖策略只在某一段有效。

## 实战提示

构建时间序列研究流程时可以按下面检查：

1. 明确预测时点和交易时点。
2. 明确特征可见时间，所有 rolling / expanding 必要时 shift。
3. 明确标签区间，尤其是多日 forward return。
4. 按时间顺序划分 train / validation / test。
5. 对重叠标签使用 embargo 或 purging。
6. 所有预处理只在训练窗口 fit，再 transform 测试窗口。
7. 用 walk-forward 评估模型稳定性。
8. 分 regime、年份、波动环境检查非平稳性。
9. 把最后一次真正未碰过的 holdout 留到最终确认。

## 小结

本节的重点：

- 时间序列预测必须只使用预测时点可见的信息。
- rolling、标准化、特征选择、标签构造都可能泄露未来。
- forward return 标签要和特征日期严格对齐。
- 时间序列应按时间顺序切分，不能随机打乱。
- 重叠标签需要 embargo 或 purging。
- 非平稳性需要 rolling、expanding、regime 分析和样本外监控。
- 防泄露是量化研究的基础工程要求。

## 自检问题

1. 为什么时间序列不能随机 train / test split？
2. rolling 特征为什么经常需要 `.shift(1)`？
3. forward return 标签和特征日期应该如何对齐？
4. embargo 解决什么问题？
5. 为什么全样本标准化会泄露未来？
6. rolling window 和 expanding window 分别适合什么场景？
