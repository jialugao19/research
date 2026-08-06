# 48. Python 理解项：feature pipeline 特征流水线的组织、复现与防错

## 核心概念

feature pipeline 指的是从原始数据到模型特征表的一整条可复现流程。

它不只是 sklearn 的 `Pipeline` API，而是更宽的工程约定：

- 输入数据需要什么列、什么键、什么时间粒度。
- 每一步生成哪些中间列和最终特征列。
- 哪些步骤是纯转换，哪些步骤需要在训练集上 `fit` 状态。
- 时间序列特征是否只使用过去信息。
- 训练、验证、测试和线上预测是否使用同一套列顺序和变换状态。
- 结果是否可以被检查、保存、复跑和对账。

一个好的 feature pipeline 应该让这些问题有明确答案：

```text
同一份原始数据，重复运行是否得到同一张特征表？
测试集是否复用训练集学到的预处理状态？
每个特征列是否能说清楚使用了哪些原始字段和哪些历史窗口？
如果原始数据缺列、重复键、列顺序变化，代码会静默出错还是明确报错？
```

## 准备环境

```python
from dataclasses import dataclass

import numpy as np
import pandas as pd
```

准备一张小型资产长表。每一行是一只资产在某一天的观测。

```python
raw = pd.DataFrame({
    "date": pd.to_datetime([
        "2024-01-02", "2024-01-03", "2024-01-04",
        "2024-01-05", "2024-01-08", "2024-01-09",
        "2024-01-02", "2024-01-03", "2024-01-04",
        "2024-01-05", "2024-01-08", "2024-01-09",
    ]),
    "asset": ["AAA"] * 6 + ["BBB"] * 6,
    "close": [100.0, 102.0, 101.0, 103.0, 104.0, 106.0,
              50.0, 49.0, 51.0, 52.0, 51.0, 53.0],
    "volume": [1000, 1200, 1100, 1300, 1250, 1400,
               800, 820, 900, 880, 870, 930],
    "sector": ["tech"] * 6 + ["finance"] * 6,
})

print(raw)
```

本节目标是把这张原始表变成模型可用的特征表。

## 先定义输入契约

pipeline 的第一步通常不是算特征，而是检查输入是否符合契约。

```python
REQUIRED_COLUMNS = ["date", "asset", "close", "volume", "sector"]


def validate_raw_frame(frame):
    missing = sorted(set(REQUIRED_COLUMNS) - set(frame.columns))
    if missing:
        raise ValueError(f"missing columns: {missing}")

    key = ["date", "asset"]
    if frame[key].isna().any().any():
        raise ValueError("date and asset cannot be missing")

    duplicated = frame.duplicated(key)
    if duplicated.any():
        examples = frame.loc[duplicated, key].head().to_dict("records")
        raise ValueError(f"duplicated date-asset keys: {examples}")


validate_raw_frame(raw)
```

这一步看起来普通，但能提前拦住很多难查的问题：

- 原始文件少列。
- 同一个 `date, asset` 有重复行。
- 键列有缺失。
- 上游字段名改了但下游还在旧列名上计算。

## 纯特征生成函数

第一类步骤是纯转换：不从训练集学习参数，只根据每行及其历史数据生成特征。

```python
def add_market_features(raw_frame):
    validate_raw_frame(raw_frame)

    frame = raw_frame.copy()
    frame["date"] = pd.to_datetime(frame["date"])
    frame = frame.sort_values(["asset", "date"]).reset_index(drop=True)

    grouped = frame.groupby("asset", group_keys=False)

    frame["return_1d"] = grouped["close"].pct_change(fill_method=None)

    grouped = frame.groupby("asset", group_keys=False)
    frame["return_lag_1d"] = grouped["return_1d"].shift(1)
    frame["volume_lag_1d"] = grouped["volume"].shift(1)

    frame["return_mean_2d"] = grouped["return_1d"].transform(
        lambda s: s.shift(1).rolling(2, min_periods=2).mean()
    )
    frame["return_vol_2d"] = grouped["return_1d"].transform(
        lambda s: s.shift(1).rolling(2, min_periods=2).std()
    )

    frame["target_return_fwd_1d"] = grouped["close"].shift(-1) / frame["close"] - 1.0

    return frame


market_features = add_market_features(raw)

print(market_features)
```

这里有几个关键约定：

- 先 `copy()`，避免在外部原始表上原地修改。
- 先排序，再按资产分组。
- 滞后和 rolling 都在资产内部计算。
- 特征列用 `shift(1)`，只使用过去数据。
- `target_return_fwd_1d` 使用未来收益，但它是标签，不是特征。

## 横截面特征

有些特征是在同一天的资产之间比较出来的，例如横截面 z-score 和排名。

```python
def cross_sectional_zscore(values):
    std = values.std(ddof=0)
    if pd.isna(std) or np.isclose(std, 0.0):
        return values * 0.0
    return (values - values.mean()) / std


def add_cross_sectional_features(feature_frame):
    frame = feature_frame.copy()

    frame["return_lag_1d_z"] = (
        frame
        .groupby("date")["return_lag_1d"]
        .transform(cross_sectional_zscore)
    )

    frame["volume_lag_1d_rank"] = (
        frame
        .groupby("date")["volume_lag_1d"]
        .rank(pct=True)
    )

    return frame


all_features = add_cross_sectional_features(market_features)

print(all_features[[
    "date",
    "asset",
    "return_lag_1d",
    "return_lag_1d_z",
    "volume_lag_1d_rank",
]])
```

横截面处理通常按 `date` 分组。前提是同一日期的这些原始观测在决策时点已经可见。

如果某些资产的数据会延迟发布，就不能简单认为同日横截面全都可见。

## 固定最终特征列

pipeline 应该显式定义最终特征列，而不是用“除了标签以外的所有列”。

```python
FEATURE_COLUMNS = [
    "return_lag_1d",
    "return_mean_2d",
    "return_vol_2d",
    "return_lag_1d_z",
    "volume_lag_1d_rank",
]

TARGET_COLUMN = "target_return_fwd_1d"


def make_model_table(raw_frame):
    market = add_market_features(raw_frame)
    features = add_cross_sectional_features(market)

    output_columns = ["date", "asset"] + FEATURE_COLUMNS + [TARGET_COLUMN]

    table = (
        features
        .loc[:, output_columns]
        .dropna(subset=FEATURE_COLUMNS + [TARGET_COLUMN])
        .sort_values(["date", "asset"])
        .reset_index(drop=True)
    )

    return table


model_table = make_model_table(raw)

print(model_table)
```

显式列清单有几个好处：

- 新增调试列不会自动进入模型。
- 特征顺序稳定，便于保存模型和线上对齐。
- 代码审查时能直接看到模型使用了哪些变量。
- 训练和预测可以检查列是否一致。

## 训练期 fit，测试期 transform

第二类步骤是有状态转换，例如缺失值填充、标准化、winsorize、类别编码、PCA。

这些步骤只能在训练集上 `fit`，再复用同一个状态转换训练集、测试集和未来数据。

下面写一个简单的状态对象：用训练集学习每列的中位数、均值和标准差。

```python
@dataclass(frozen=True)
class FeatureState:
    columns: tuple
    medians: pd.Series
    means: pd.Series
    scales: pd.Series


def fit_feature_state(table, feature_columns):
    X = table.loc[:, feature_columns]

    medians = X.median()
    filled = X.fillna(medians)
    means = filled.mean()
    scales = filled.std(ddof=0).replace(0.0, 1.0)

    return FeatureState(
        columns=tuple(feature_columns),
        medians=medians,
        means=means,
        scales=scales,
    )
```

转换函数只使用 `state`，不能重新计算测试集的均值和标准差。

```python
def transform_features(table, state):
    expected = list(state.columns)
    missing = sorted(set(expected) - set(table.columns))
    if missing:
        raise ValueError(f"missing feature columns: {missing}")

    X = table.loc[:, expected].copy()
    X = X.fillna(state.medians)
    X = (X - state.means) / state.scales
    X.columns = [f"{name}_std" for name in expected]

    return pd.concat(
        [table[["date", "asset"]].reset_index(drop=True), X.reset_index(drop=True)],
        axis=1,
    )
```

把数据按日期切成训练和测试：

```python
split_date = pd.Timestamp("2024-01-05")

train_table = model_table[model_table["date"].le(split_date)].reset_index(drop=True)
test_table = model_table[model_table["date"].gt(split_date)].reset_index(drop=True)

state = fit_feature_state(train_table, FEATURE_COLUMNS)

X_train = transform_features(train_table, state)
X_test = transform_features(test_table, state)

y_train = train_table[TARGET_COLUMN]
y_test = test_table[TARGET_COLUMN]

print(X_train)
print(X_test)
print(y_train)
print(y_test)
```

`X_test` 的标准化参数来自 `train_table`，不是测试集自己。

这是 feature pipeline 和普通脚本的关键区别：状态在哪里学习、在哪里复用，都要明确写出来。

## 流水线入口函数

可以把前面的步骤组合成一个入口函数，返回训练、测试、标签和状态。

```python
def build_training_bundle(raw_frame, split_date):
    table = make_model_table(raw_frame)

    split_date = pd.Timestamp(split_date)
    train = table[table["date"].le(split_date)].reset_index(drop=True)
    test = table[table["date"].gt(split_date)].reset_index(drop=True)

    if train.empty:
        raise ValueError("train table is empty")
    if test.empty:
        raise ValueError("test table is empty")

    state = fit_feature_state(train, FEATURE_COLUMNS)

    bundle = {
        "X_train": transform_features(train, state),
        "y_train": train[TARGET_COLUMN].reset_index(drop=True),
        "X_test": transform_features(test, state),
        "y_test": test[TARGET_COLUMN].reset_index(drop=True),
        "state": state,
        "feature_columns": FEATURE_COLUMNS,
    }

    return bundle


bundle = build_training_bundle(raw, split_date="2024-01-05")

print(bundle["X_train"])
print(bundle["X_test"])
```

这种入口函数方便测试，也方便在 notebook、训练脚本和回测脚本之间复用同一套逻辑。

## 历史窗口需要上下文

时间序列特征还有一个容易忽略的问题：测试期的 rolling 特征需要测试期之前的历史数据。

如果只把测试期原始数据喂给 pipeline，窗口开头会丢失历史上下文。

```python
test_raw_only = raw[raw["date"].gt(split_date)]
test_table_without_history = make_model_table(test_raw_only)

print(test_table_without_history)
```

在这个例子里，`test_table_without_history` 是空的，因为 2 日 rolling 特征需要测试期之前的收益历史。

离线训练时，常见做法是：

1. 用完整原始时间段生成特征，但每个特征必须只向过去看。
2. 再按日期切分训练、验证和测试。
3. 有状态预处理只在训练部分 `fit`。

线上预测时，则需要保留足够长的历史缓存，不能只传当天一行数据。

## 输出检查

feature pipeline 应该在输出处做基本检查。

```python
def validate_model_table(table):
    key = ["date", "asset"]
    if table.duplicated(key).any():
        raise ValueError("model table has duplicated keys")

    missing = sorted(set(FEATURE_COLUMNS + [TARGET_COLUMN]) - set(table.columns))
    if missing:
        raise ValueError(f"model table missing columns: {missing}")

    values = table.loc[:, FEATURE_COLUMNS + [TARGET_COLUMN]]
    if not np.isfinite(values.to_numpy()).all():
        raise ValueError("model table contains non-finite values")


validate_model_table(model_table)
```

这些检查不会证明策略没有泄露，但能拦住结构性错误：

- 重复样本。
- 关键列缺失。
- 特征里出现 `inf`。
- 上游变化导致输出 schema 不一致。

## 记录 manifest

训练时最好记录一个轻量 manifest，说明当前 pipeline 用了哪些列和训练区间。

```python
manifest = {
    "feature_columns": list(state.columns),
    "target_column": TARGET_COLUMN,
    "train_start": str(train_table["date"].min().date()),
    "train_end": str(train_table["date"].max().date()),
    "test_start": str(test_table["date"].min().date()),
    "test_end": str(test_table["date"].max().date()),
    "n_train_rows": int(len(train_table)),
    "n_test_rows": int(len(test_table)),
}

print(manifest)
```

真实项目中，manifest 还可以包括：

- 原始数据版本。
- pipeline 代码版本。
- 参数配置。
- 特征列 hash。
- 模型文件路径。
- 训练脚本命令。

这样做的目的不是形式化，而是让几周后还能回答“这次模型到底用什么数据和什么特征训练出来”。

## 常见坑

第一，把全流程写成一个长 notebook 单元。

这样很难复用、测试和定位问题。更好的方式是拆成小函数：输入校验、特征生成、状态拟合、状态转换、输出校验。

第二，在测试集上重新 `fit` 预处理。

例如对测试集重新计算标准化均值、填充值或类别字典，会改变评估口径，严重时构成信息泄露。

第三，依赖隐式列顺序。

模型输入应该由 `FEATURE_COLUMNS` 这类显式清单控制。不要依赖 DataFrame 当前列顺序，也不要把所有数值列自动塞进模型。

第四，忘记历史上下文。

rolling、lag、expanding 特征在预测期需要历史缓存。只给当天或测试期切片，往往会得到大量缺失或错误窗口。

第五，原地修改共享 DataFrame。

多个函数共用同一个对象并原地加列，容易产生顺序依赖。默认使用 `.copy()`，让函数输入输出更清楚。

## 实战提示

写 feature pipeline 时，可以按这个顺序组织：

1. 定义原始输入契约：必需列、唯一键、时间粒度。
2. 定义最终输出契约：主键列、特征列、标签列。
3. 把纯特征生成写成函数，并保证排序、分组和 shift 语义明确。
4. 把有状态预处理拆成 `fit_state` 和 `transform_with_state`。
5. 先生成时间安全的特征表，再切分训练、验证和测试。
6. 只在训练集上拟合状态。
7. 保存 manifest，记录特征列、训练区间、数据版本和参数。
8. 给关键函数写小样本测试。

## 小结

本节的重点：

- feature pipeline 是从原始数据到模型输入的可复现流程。
- 输入契约和输出契约要显式定义。
- 纯特征生成和有状态预处理要分开。
- 时间序列特征必须先排序、分组，并明确是否使用 `shift(1)`。
- 测试集和线上数据必须复用训练集拟合出的状态。
- rolling 特征在测试期需要历史上下文。
- 显式 `FEATURE_COLUMNS` 和 manifest 能显著降低复现和上线风险。

## 自检问题

1. feature pipeline 和 sklearn `Pipeline` 有什么区别？
2. 为什么最终特征列应该用显式清单，而不是自动选择所有数值列？
3. 哪些步骤需要在训练集上 `fit` 状态？
4. 为什么测试期 rolling 特征需要历史上下文？
5. manifest 至少应该记录哪些信息？
