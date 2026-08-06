# NumPy：随机数与可复现性

## 核心概念

随机数在模拟、抽样、bootstrap、模型初始化、交叉验证和压力测试里都很常见。可复现性的核心要求是：同一段代码、同一个随机种子、同一套关键依赖版本，应能产生同样的随机序列或同样的实验结果。

现代 NumPy 推荐使用 `np.random.default_rng` 创建随机数生成器：

```python
import numpy as np

rng = np.random.default_rng(seed=42)

x = rng.normal(size=5)
print(x)
```

`rng` 是一个独立的随机数生成器。只要 seed 相同，并且调用顺序相同，它就会产生相同的随机序列。

## 同一个 seed 产生同样结果

```python
import numpy as np

rng1 = np.random.default_rng(123)
rng2 = np.random.default_rng(123)

x1 = rng1.normal(size=4)
x2 = rng2.normal(size=4)

print(x1)
print(x2)
print(np.allclose(x1, x2))  # True
```

如果 seed 不同，结果通常不同：

```python
rng1 = np.random.default_rng(123)
rng2 = np.random.default_rng(456)

x1 = rng1.normal(size=4)
x2 = rng2.normal(size=4)

print(np.allclose(x1, x2))  # False
```

可复现不是“不随机”，而是“随机序列可以被重新生成”。

## 不推荐依赖全局随机状态

旧写法经常使用：

```python
np.random.seed(42)
x = np.random.normal(size=5)
```

这种写法会修改 NumPy 的全局随机状态。项目变大后，任何地方调用 `np.random` 都可能影响后续结果，调试会变难。

更推荐把 `rng` 显式传入函数：

```python
def simulate_returns(rng, n_days):
    return rng.normal(loc=0.0005, scale=0.02, size=n_days)

rng = np.random.default_rng(42)
returns = simulate_returns(rng, n_days=5)

print(returns)
```

这样函数的随机性来源是明确的，测试和复现也更容易。

## 常用随机分布

`Generator` 提供很多常用分布：

```python
rng = np.random.default_rng(42)

normal = rng.normal(loc=0.0, scale=1.0, size=5)
uniform = rng.uniform(low=0.0, high=1.0, size=5)
integers = rng.integers(low=0, high=10, size=5)

print(normal)
print(uniform)
print(integers)
```

常见含义：

- `normal(loc, scale, size)`：正态分布，`loc` 是均值，`scale` 是标准差。
- `uniform(low, high, size)`：均匀分布，取值在 `[low, high)`。
- `integers(low, high, size)`：离散整数，取值在 `[low, high)`。

在量化研究中，正态随机数常用于简单收益模拟，但真实收益通常有厚尾、偏度、波动聚集等特征。模拟例子能帮助理解方法，不应直接替代真实建模。

## 实战例子：模拟组合收益

假设你想快速模拟 252 天、3 个资产的日收益，并用固定权重计算组合收益：

```python
import numpy as np

rng = np.random.default_rng(7)

returns = rng.normal(loc=0.0005, scale=0.02, size=(252, 3))
weights = np.array([0.5, 0.3, 0.2])

portfolio_returns = returns @ weights

print(returns.shape)            # (252, 3)
print(portfolio_returns.shape)  # (252,)
print(portfolio_returns.mean())
print(portfolio_returns.std())
```

这个例子里，随机性只来自 `rng`。如果你重新创建 `np.random.default_rng(7)` 并按同样顺序调用，结果会相同。

## 随机抽样：choice

`choice` 可以从给定集合里抽样。

```python
rng = np.random.default_rng(42)

assets = np.array(["A", "B", "C", "D", "E"])
sample = rng.choice(assets, size=3, replace=False)

print(sample)
```

参数 `replace=False` 表示不放回抽样，同一个元素不会被抽到多次。`replace=True` 表示放回抽样，常用于 bootstrap。

```python
rng = np.random.default_rng(42)

returns = np.array([0.01, -0.02, 0.03, 0.00, 0.02])
bootstrap_sample = rng.choice(returns, size=5, replace=True)

print(bootstrap_sample)
```

bootstrap 的核心思想是：从已有样本中有放回抽样，构造许多“类似样本”，用来估计统计量的不确定性。完整 bootstrap 会在概率统计章节继续展开。

## 随机打乱：permutation 与 shuffle

`permutation` 返回打乱后的新数组：

```python
rng = np.random.default_rng(42)

x = np.array([1, 2, 3, 4, 5])
y = rng.permutation(x)

print(x)  # [1 2 3 4 5]
print(y)
```

`shuffle` 会原地修改数组：

```python
rng = np.random.default_rng(42)

x = np.array([1, 2, 3, 4, 5])
rng.shuffle(x)

print(x)
```

如果你不想改变原始数据，用 `permutation`；如果你明确希望原地打乱，用 `shuffle`。

## 时间序列里不要随意打乱

随机打乱在很多机器学习任务里有用，但时间序列任务要非常谨慎。

```python
rng = np.random.default_rng(42)

dates = np.arange(10)
shuffled_dates = rng.permutation(dates)

print(shuffled_dates)
```

如果你把时间序列样本随机打乱后再切分训练集和测试集，可能让未来样本进入训练过程，从而产生未来信息泄露。对于预测未来收益、波动率或成交量这类任务，通常应按时间顺序切分：

```python
n = 10
train_idx = np.arange(0, 7)
test_idx = np.arange(7, 10)

print(train_idx)  # [0 1 2 3 4 5 6]
print(test_idx)   # [7 8 9]
```

随机性不是问题本身，问题是随机操作是否破坏了时间因果关系。

## 实战例子：随机但可复现的横截面抽样

有时你想从某一天可交易股票池里随机抽一批股票做 sanity check。

```python
rng = np.random.default_rng(2024)

tradable = np.array(["AAA", "BBB", "CCC", "DDD", "EEE", "FFF"])
selected = rng.choice(tradable, size=3, replace=False)

print(selected)
```

如果这段抽样被用于报告或测试，应记录 seed：

```python
seed = 2024
rng = np.random.default_rng(seed)
selected = rng.choice(tradable, size=3, replace=False)

print(seed)
print(selected)
```

这样别人可以复现你抽到的是哪几只股票。

## 调用顺序也会影响结果

同一个 seed 下，如果调用顺序不同，后续结果也会不同。

```python
rng1 = np.random.default_rng(42)
a1 = rng1.normal(size=3)
b1 = rng1.normal(size=3)

rng2 = np.random.default_rng(42)
b2 = rng2.normal(size=3)
a2 = rng2.normal(size=3)

print(np.allclose(a1, a2))  # False
print(np.allclose(b1, b2))  # False
```

`rng` 像一个会不断前进的序列读取器。每调用一次随机函数，内部状态都会前进。

如果两个模块需要互不影响的随机序列，可以给它们创建独立的 generator：

```python
rng_data = np.random.default_rng(100)
rng_model = np.random.default_rng(200)

sample = rng_data.normal(size=3)
init = rng_model.normal(size=3)
```

## 不要在循环里反复设置同一个 seed

错误写法：

```python
samples = []

for i in range(3):
    rng = np.random.default_rng(42)
    samples.append(rng.normal())

print(samples)
```

这会得到三个完全相同的随机数，因为每次循环都从同一个初始状态重新开始。

更合理的写法是只创建一次 generator：

```python
rng = np.random.default_rng(42)
samples = []

for i in range(3):
    samples.append(rng.normal())

print(samples)
```

## 实验记录应该包含什么

如果实验依赖随机性，至少记录：

- seed。
- NumPy 版本。
- 关键库版本，例如 scikit-learn、PyTorch、LightGBM。
- 随机抽样方法，例如是否放回抽样。
- 数据切分方法，尤其是时间序列是否按时间切分。
- 并行设置，因为并行任务中的随机性更容易变复杂。

可以在脚本开头输出：

```python
import numpy as np

seed = 42
rng = np.random.default_rng(seed)

print("seed:", seed)
print("numpy:", np.__version__)
```

严格复现通常不仅需要 seed，还需要固定依赖版本和运行环境。

## 常见坑

### 1. 以为 seed 相同就能保证所有环境完全一致

seed 是必要条件，不一定是充分条件。不同 NumPy 版本、不同底层算法、不同并行库，可能导致结果有差异。严肃实验应记录依赖版本。

### 2. 在函数内部偷偷创建随机数生成器

```python
def bad_sample(x):
    rng = np.random.default_rng(42)
    return rng.choice(x, size=2, replace=False)
```

这个函数每次调用都会返回同样的抽样结果，而且调用者无法控制随机性。更好的方式是传入 `rng`：

```python
def good_sample(x, rng):
    return rng.choice(x, size=2, replace=False)
```

### 3. 用随机打乱处理时间序列切分

时间序列预测里，随机打乱后再切分训练/测试通常有泄露风险。应优先按时间切分，并确保特征只使用预测时点之前能看到的信息。

### 4. 把随机模拟当作真实市场

正态随机收益可以用于教学或 sanity check，但真实市场收益有厚尾、相关性、波动聚集和制度切换。模拟假设必须写清楚。

### 5. 用 NumPy 随机数做安全用途

NumPy 随机数适合科学计算和模拟，不适合密码、密钥、token 等安全场景。安全随机数应使用专门的安全随机库。

## 实战提示

建议养成这个习惯：

```python
def run_experiment(seed=42):
    rng = np.random.default_rng(seed)

    # 所有随机操作都从 rng 来
    x = rng.normal(size=100)
    idx = rng.choice(np.arange(100), size=20, replace=False)

    return x[idx].mean()

print(run_experiment(seed=42))
print(run_experiment(seed=42))  # 同样结果
```

这种写法有几个好处：

1. seed 集中在入口处。
2. 随机性来源清楚。
3. 函数容易测试。
4. 实验日志容易记录。

## 自检问题

1. 为什么现代 NumPy 更推荐 `np.random.default_rng`？
2. 同一个 seed 下，为什么调用顺序不同会导致后续结果不同？
3. `choice(..., replace=True)` 和 `replace=False` 有什么区别？
4. 为什么时间序列任务里随机打乱样本可能导致未来信息泄露？
5. 一个依赖随机性的实验，除了 seed，还应该记录哪些信息？

