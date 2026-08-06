# pandas：merge / join / concat

## 核心概念

pandas 里常见的表合并有三类：

- `merge`：按一列或多列 key 合并，类似 SQL join。
- `join`：主要按 index 合并。
- `concat`：沿某个轴把多个对象拼起来，常用于纵向追加或横向并排。

经验规则：

- 有明确键列，例如 `date`、`asset`、`industry`：优先用 `merge`。
- 两张表已经用同样的 index 对齐：可以用 `join`。
- 同结构表按行追加，或多个 Series/DataFrame 按列拼接：用 `concat`。

## 准备数据

下面有一张收益表和一张行业分类表。

```python
import pandas as pd

returns = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"]),
    "asset": ["AAA", "BBB", "AAA", "BBB"],
    "return": [0.01, -0.02, 0.03, 0.00],
})

industry = pd.DataFrame({
    "asset": ["AAA", "BBB", "CCC"],
    "industry": ["tech", "finance", "energy"],
})

print(returns)
print(industry)
```

`returns` 是按 `date-asset` 组织的长表，`industry` 是按 `asset` 组织的静态映射表。

## merge：按 key 合并

把行业信息合并到收益表：

```python
merged = returns.merge(industry, on="asset", how="left")

print(merged)
```

`on="asset"` 表示用 `asset` 列作为连接键。`how="left"` 表示保留左表 `returns` 的所有行。

结果中，每条收益记录都带上了对应资产的行业。

## how：inner / left / right / outer

`how` 决定保留哪些 key。

```python
left = pd.DataFrame({
    "asset": ["AAA", "BBB"],
    "x": [1, 2],
})

right = pd.DataFrame({
    "asset": ["BBB", "CCC"],
    "y": [20, 30],
})

print(left.merge(right, on="asset", how="inner"))
print(left.merge(right, on="asset", how="left"))
print(left.merge(right, on="asset", how="outer"))
```

含义：

- `inner`：只保留两边都有的 key。
- `left`：保留左表所有 key。
- `right`：保留右表所有 key。
- `outer`：保留两边所有 key。

量化研究里，`left` 很常用，因为你通常希望保留主样本表，再把分类、因子或特征补上去。

## 多列 key

如果两张表都按 `date-asset` 标识观测，合并时应使用两个 key。

```python
factor = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"]),
    "asset": ["AAA", "BBB", "AAA", "BBB"],
    "value_factor": [1.2, 0.5, 1.0, 0.7],
})

data = returns.merge(factor, on=["date", "asset"], how="left")

print(data)
```

如果只用 `asset` 合并，会把不同日期的数据错配成多对多结果。这是金融数据里很常见的严重错误。

## validate：检查合并关系

`validate` 可以检查 key 的关系，提前发现重复键或意外多对多合并。

```python
merged = returns.merge(
    industry,
    on="asset",
    how="left",
    validate="many_to_one",
)

print(merged)
```

这里 `returns` 中同一资产会出现多次，`industry` 中每个资产应该只出现一次，所以关系是 `many_to_one`。

常见取值：

- `"one_to_one"`：两边 key 都唯一。
- `"one_to_many"`：左边唯一，右边可重复。
- `"many_to_one"`：左边可重复，右边唯一。
- `"many_to_many"`：两边都可重复。

除非你明确需要多对多，否则应尽量用 `validate` 保护合并逻辑。

## indicator：检查匹配情况

`indicator=True` 会增加 `_merge` 列，显示每行来自哪里。

```python
checked = returns.merge(
    industry,
    on="asset",
    how="outer",
    indicator=True,
)

print(checked)
print(checked["_merge"].value_counts())
```

`_merge` 的可能值：

- `left_only`：只在左表。
- `right_only`：只在右表。
- `both`：两边都有。

这对数据质量检查很有用。例如你可以检查收益表里是否有股票找不到行业，或者行业表里是否有股票不在样本中。

## suffixes：处理重名列

如果两张表有同名非 key 列，pandas 会自动加后缀。

```python
left = pd.DataFrame({
    "asset": ["AAA", "BBB"],
    "score": [1.0, 2.0],
})

right = pd.DataFrame({
    "asset": ["AAA", "BBB"],
    "score": [10.0, 20.0],
})

merged = left.merge(right, on="asset", suffixes=("_model", "_vendor"))

print(merged)
```

不要忽略自动生成的 `_x`、`_y`。列重名通常意味着你需要明确区分字段来源。

## join：按 index 合并

如果两张表已经有相同 index，可以使用 `join`。

```python
price = pd.DataFrame(
    {"close": [100.0, 102.0, 101.0]},
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
)

volume = pd.DataFrame(
    {"volume": [1000, 1200, 900]},
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
)

joined = price.join(volume, how="left")

print(joined)
```

`join` 本质上依赖 index 对齐。使用前要确认 index 的含义一致。

如果 index 不唯一，join 可能产生重复行或多对多效果。不要只看代码能运行，要检查输出行数。

## concat：纵向拼接

`concat` 常用于把同结构表按行追加。

```python
jan = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-02", "2024-01-03"]),
    "asset": ["AAA", "AAA"],
    "return": [0.01, 0.03],
})

feb = pd.DataFrame({
    "date": pd.to_datetime(["2024-02-01", "2024-02-02"]),
    "asset": ["AAA", "AAA"],
    "return": [-0.01, 0.02],
})

all_returns = pd.concat([jan, feb], axis=0, ignore_index=True)

print(all_returns)
```

`axis=0` 表示纵向拼接。`ignore_index=True` 会重新生成 0 到 n-1 的整数 index。

如果原 index 有业务含义，例如日期，不要随便 `ignore_index=True`。

## concat：横向拼接

`concat(axis=1)` 会按 index 横向拼接。

```python
close = pd.Series(
    [100.0, 102.0, 101.0],
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
    name="close",
)

volume = pd.Series(
    [1000, 1200, 900],
    index=pd.to_datetime(["2024-01-02", "2024-01-03", "2024-01-04"]),
    name="volume",
)

table = pd.concat([close, volume], axis=1)

print(table)
```

这和 `join` 类似，都是按 index 对齐。区别是 `concat` 更适合一次拼接多个对象。

## keys：拼接时保留来源

`concat` 可以用 `keys` 保留来源标签。

```python
aaa = pd.Series([0.01, 0.03], index=pd.to_datetime(["2024-01-02", "2024-01-03"]))
bbb = pd.Series([-0.02, 0.00], index=pd.to_datetime(["2024-01-02", "2024-01-03"]))

wide = pd.concat({"AAA": aaa, "BBB": bbb}, axis=1)

print(wide)
```

这里得到宽表，列是资产代码，行是日期。这个模式常用于把多个资产的时间序列拼成矩阵。

## 实战例子：合并收益、因子和行业

典型因子研究长表会把多个来源合并到 `date-asset` 粒度。

```python
returns = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"]),
    "asset": ["AAA", "BBB", "AAA", "BBB"],
    "return": [0.01, -0.02, 0.03, 0.00],
})

factor = pd.DataFrame({
    "date": pd.to_datetime(["2024-01-02", "2024-01-02", "2024-01-03", "2024-01-03"]),
    "asset": ["AAA", "BBB", "AAA", "BBB"],
    "value_factor": [1.2, 0.5, 1.0, 0.7],
})

industry = pd.DataFrame({
    "asset": ["AAA", "BBB"],
    "industry": ["tech", "finance"],
})

data = (
    returns
    .merge(factor, on=["date", "asset"], how="left", validate="one_to_one")
    .merge(industry, on="asset", how="left", validate="many_to_one")
)

print(data)
```

这里两个关系不同：

- `returns` 和 `factor` 都是 `date-asset` 唯一，所以是 `one_to_one`。
- `industry` 每个资产一行，而 `returns` 每个资产多天，所以是 `many_to_one`。

## 实战例子：检查合并是否丢样本

合并后应检查行数和匹配情况。

```python
checked = returns.merge(
    factor,
    on=["date", "asset"],
    how="left",
    indicator=True,
)

print(len(returns), len(checked))
print(checked["_merge"].value_counts())
```

如果 `len(checked) > len(returns)`，可能发生了意外多对多合并。如果 `_merge` 里有 `left_only`，说明左表有记录没找到右表匹配。

## 常见坑

### 1. 忘记多列 key

```python
# 错误风险：只按 asset 合并
# returns.merge(factor, on="asset")
```

如果因子是按 `date-asset` 变化的，只按 `asset` 合并会把不同日期交叉匹配，产生行数膨胀和错配。

### 2. 重复 key 导致多对多

```python
left = pd.DataFrame({"asset": ["AAA", "AAA"], "x": [1, 2]})
right = pd.DataFrame({"asset": ["AAA", "AAA"], "y": [10, 20]})

print(left.merge(right, on="asset"))
```

结果会有 4 行，因为每个左表 AAA 都匹配两个右表 AAA。除非你明确需要笛卡尔式匹配，否则这通常是数据错误。

### 3. join 前没有检查 index

`join` 按 index 对齐。如果两个表 index 看起来都是日期，但一个是交易日、一个是自然日，或者时区/时间戳粒度不同，合并结果可能出现大量缺失。

### 4. concat 后重复 index

```python
combined = pd.concat([jan, feb])
```

如果原表 index 都从 0 开始，拼接后 index 会重复。后续按 index 选择或 join 时可能出问题。是否使用 `ignore_index=True` 要看 index 是否有业务含义。

### 5. 合并时不检查行数

合并前后至少检查：

```python
print(len(left), len(right), len(merged))
```

行数突然变多，常常说明 key 不唯一或合并粒度错了。

## 实战提示

做表合并时，建议固定写检查：

```python
assert returns[["date", "asset"]].duplicated().sum() == 0
assert factor[["date", "asset"]].duplicated().sum() == 0

data = returns.merge(
    factor,
    on=["date", "asset"],
    how="left",
    validate="one_to_one",
)

assert len(data) == len(returns)
```

如果是静态映射表：

```python
assert industry["asset"].duplicated().sum() == 0

data = data.merge(
    industry,
    on="asset",
    how="left",
    validate="many_to_one",
)
```

合并的核心不是“把列拼上去”，而是确认两张表的粒度一致、key 唯一性符合预期、缺失匹配可解释。

## 自检问题

1. `merge`、`join`、`concat` 分别适合什么场景？
2. `how="left"` 和 `how="inner"` 的区别是什么？
3. 为什么 `date-asset` 粒度的数据通常要用两个 key 合并？
4. `validate="many_to_one"` 能检查什么问题？
5. `concat(axis=0)` 后为什么可能出现重复 index？

