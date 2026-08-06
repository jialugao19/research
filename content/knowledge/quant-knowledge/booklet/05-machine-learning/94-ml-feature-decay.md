# 94. 机器学习：feature decay 的信号衰减、半衰期、滞后评估和再训练节奏

## 核心概念

feature decay 是特征衰减。

在机器学习和量化研究里，它问的是：

```text
一个特征在产生之后，预测能力会维持多久？
```

很多金融特征不是永久有效的。

例如：

- 订单流冲击可能几分钟内衰减。
- 日频 momentum 可能持续数周到数月。
- 财报 surprise 可能在公告后一段时间逐渐被市场消化。
- 高频 spread、depth、imbalance 特征可能很快失效。
- 宏观变量的影响可能慢，但更新频率也低。

feature decay 的核心不是问：

```text
这个特征有没有用？
```

而是问：

```text
这个特征在多长预测期限内有用？
```

如果不知道衰减速度，就很容易把短效特征用于长周期预测，或者把长效特征过度频繁交易。

## 为什么要看 feature decay

feature decay 直接影响：

- 预测 horizon。
- 持仓周期。
- 特征刷新频率。
- 模型再训练频率。
- 交易成本假设。
- 特征是否应该进入模型。
- 标签构造是否匹配信号周期。

例子：

```text
一个特征对未来 1 天收益有效，但对未来 20 天收益无效
```

这不说明它没用。

它说明：

```text
这个特征更适合短周期模型
```

相反，如果一个特征只在未来 60 天有解释力，用它做日内交易就可能只是噪声。

## lag bucket

最常见的 decay 检查，是把未来收益按滞后期拆开。

例如今天的信号 `signal_t`，分别预测：

```text
r_{t+1}
r_{t+2}
r_{t+3}
r_{t+4}
...
```

如果相关性随 lag 逐渐下降，就说明信号在衰减。

简化例子：

```python
signal = [0.9, 0.7, 0.4, 0.2]
future_return_lag1 = [0.08, 0.06, 0.03, 0.01]
future_return_lag3 = [0.04, 0.03, 0.02, 0.00]
future_return_lag5 = [0.01, 0.01, 0.00, -0.01]

def dot(a, b):
    return sum(x * y for x, y in zip(a, b))

score_by_lag = {
    1: dot(signal, future_return_lag1),
    3: dot(signal, future_return_lag3),
    5: dot(signal, future_return_lag5),
}

print(score_by_lag)
```

结果：

```text
{1: 0.128, 3: 0.065, 5: 0.014}
```

这里 lag 越长，信号和未来收益的关系越弱。

这就是一个简化的 feature decay 曲线。

真实项目里通常不会直接用点积，而是看：

- Pearson correlation。
- Spearman rank correlation。
- IC / RankIC。
- 分组收益。
- long-short return。
- 命中率。
- 回归系数。

## decay curve

decay curve 是把不同 lag 下的预测能力画成曲线。

简化成表：

```python
ic_by_lag = {
    1: 0.060,
    2: 0.045,
    3: 0.032,
    5: 0.018,
    10: 0.004,
}

for lag, ic in ic_by_lag.items():
    print(lag, ic)
```

结果：

```text
1 0.06
2 0.045
3 0.032
5 0.018
10 0.004
```

解释：

```text
lag=1 时 IC 最强
lag=10 时 IC 接近 0
```

这说明特征可能适合 1 到 5 天的预测，不适合 10 天以上。

如果 decay curve 很不平滑，要检查：

- 样本是否太少。
- 是否有极端日期。
- 是否跨了不同 regime。
- 是否有数据对齐错误。
- 标签是否重叠过多。

## 半衰期

半衰期是信号强度衰减到初始值一半所需的时间。

如果初始 IC 是 `0.06`，一半是 `0.03`。

```python
ic_by_lag = {
    1: 0.060,
    2: 0.045,
    3: 0.032,
    5: 0.018,
    10: 0.004,
}

initial_ic = ic_by_lag[1]
half_level = initial_ic / 2

half_life = None
for lag, ic in ic_by_lag.items():
    if ic <= half_level:
        half_life = lag
        break

print(half_level)
print(half_life)
```

结果：

```text
0.03
5
```

这里第一个低于 `0.03` 的点是 lag 5。

所以粗略半衰期是 5 天。

注意这只是离散估计。

如果要更精细，可以对 decay curve 做指数衰减拟合。

## 指数衰减直觉

很多衰减可以用指数形式近似：

```text
strength(lag) = initial_strength * exp(-decay_rate * lag)
```

简化例子：

```python
import math

initial_strength = 0.08
decay_rate = 0.25

strength_by_lag = {}
for lag in [1, 2, 3, 5, 10]:
    strength_by_lag[lag] = initial_strength * math.exp(-decay_rate * lag)

print(strength_by_lag)
```

结果：

```text
{1: 0.062304062645712394, 2: 0.04852245277701067, 3: 0.037789324219281176, 5: 0.022920383748815207, 10: 0.0065667998899119045}
```

`decay_rate` 越大，信号衰减越快。

指数衰减常用于：

- 特征加权。
- 事件影响建模。
- 最近样本加权。
- turnover 控制。
- 预测 horizon 选择。

## half-life 和 decay rate

指数衰减下，半衰期和 decay rate 的关系是：

```text
half_life = log(2) / decay_rate
```

```python
import math

decay_rate = 0.25
half_life = math.log(2) / decay_rate

print(half_life)
```

结果：

```text
2.772588722239781
```

如果单位是天，半衰期约为 `2.77` 天。

这表示信号强度大约每 2.77 天减半。

## horizon mismatch

feature decay 最常见的问题是 horizon mismatch。

也就是：

```text
特征的有效周期和标签周期不匹配
```

例子：

```text
用分钟级 order imbalance 预测未来 60 天收益
用季度财报特征预测下一分钟收益
```

这两种都很可能不合适。

简化判断：

```python
feature_half_life_days = 3
label_horizon_days = 20

is_mismatch = label_horizon_days > 3 * feature_half_life_days

print(is_mismatch)
```

结果：

```text
True
```

这里标签 horizon 是半衰期的 6.67 倍。

特征可能已经衰减得很弱。

这个规则不是定理，只是一个风险提示。

## 信息更新频率

特征衰减还要和信息更新频率一起看。

例如：

```text
日频价格特征每天更新
财报特征每季度更新
宏观数据每月更新
order book 特征每秒甚至更快更新
```

如果一个特征更新很慢，就不要假设它每天都有新信息。

```python
feature_update_days = {
    "order_imbalance": 1 / 390,
    "daily_momentum": 1,
    "earnings_surprise": 63,
}

for name, days in feature_update_days.items():
    print(name, days)
```

结果：

```text
order_imbalance 0.002564102564102564
daily_momentum 1
earnings_surprise 63
```

`order_imbalance` 的信息刷新非常快。

`earnings_surprise` 可能很久才有一次真正的新信息。

## 避免未来信息泄露

计算 feature decay 时，最容易泄露的是标签对齐。

错误做法：

```python
signal_t = compute_signal(data_until_t)
future_return = return_from_t_minus_5_to_t_plus_5
```

这个 `future_return` 混入了 `t` 之后的信息，也混入了 `t` 之前的一部分。

更清晰的做法：

```text
signal_t 使用 t 时刻可见信息
label_t_lag_k 使用 t 到 t+k 的未来收益
```

伪代码：

```python
for t in dates:
    x_t = features_available_at(t)
    y_t_1d = return_between(t, t + 1)
    y_t_5d = return_between(t, t + 5)
```

注意：

```text
features_available_at(t) 不能包含 t+1 之后才知道的数据
```

对于财报、公告、成分股、复权价格，都要使用实际可得时间。

## 重叠标签问题

如果用未来 5 天收益作为标签：

```text
y_t     = r_{t+1} + ... + r_{t+5}
y_{t+1} = r_{t+2} + ... + r_{t+6}
```

两个标签高度重叠。

这会让统计显得样本很多，但实际独立信息较少。

简化例子：

```python
returns = [0.01, 0.02, -0.01, 0.00, 0.03, 0.01]
horizon = 3

labels = []
for start in range(len(returns) - horizon + 1):
    labels.append(sum(returns[start:start + horizon]))

print(labels)
```

结果：

```text
[0.019999999999999997, 0.01, 0.019999999999999997, 0.04]
```

相邻标签共享大部分收益。

做 decay 评估时要考虑：

- 使用 non-overlapping label。
- 使用 Newey-West 或 block bootstrap。
- 按日期聚合后再检验。
- 不要把重叠标签当作完全独立样本。

## 特征淘汰

feature decay 可以帮助淘汰特征。

假设一个特征在不同 lag 的 IC：

```python
ic_by_lag = [0.005, -0.002, 0.001, 0.000]

max_abs_ic = max(abs(x) for x in ic_by_lag)
keep_feature = max_abs_ic >= 0.01

print(max_abs_ic)
print(keep_feature)
```

结果：

```text
0.005
False
```

这个特征在所有 horizon 下都很弱。

可以考虑：

- 删除。
- 降低优先级。
- 只作为交互项候选。
- 检查是否在某些 regime 下有效。

不要只因为总体弱就立刻删除。

有些特征可能：

- 只在高波动状态有效。
- 只对小盘股有效。
- 只在特定事件后有效。
- 只在成本较低的交易场景有效。

## 再训练节奏

feature decay 也会影响模型再训练。

两种 decay 要区分：

```text
feature signal decay: 一个信号对未来收益的影响衰减
model decay: 模型参数随市场变化逐渐失效
```

如果信号本身半衰期很短，模型通常需要更频繁地更新特征和仓位。

如果模型表现随时间下降，就需要评估再训练频率。

简化规则：

```python
validation_ic_by_month = [0.04, 0.035, 0.028, 0.015, 0.005]

initial_ic = validation_ic_by_month[0]
current_ic = validation_ic_by_month[-1]

needs_retrain = current_ic < initial_ic / 2

print(needs_retrain)
```

结果：

```text
True
```

这表示当前验证 IC 已经低于初始 IC 的一半。

可以考虑重新训练、重新选择特征或调整 regime。

## decay 和交易成本

短半衰期特征通常带来更高换手。

如果一个特征很快衰减，就需要更快交易才能捕捉收益。

但更快交易意味着：

- 更高手续费。
- 更高滑点。
- 更高 market impact。
- 更强容量约束。

所以要问：

```text
信号衰减之前，扣除成本后还能赚到钱吗？
```

简化例子：

```python
gross_alpha = 0.0012
trading_cost = 0.0008
net_alpha = gross_alpha - trading_cost

print(net_alpha)
print(net_alpha > 0)
```

结果：

```text
0.00039999999999999996
True
```

短周期特征不能只看预测能力。

必须同时看交易成本和可执行性。

## 实战检查清单

分析 feature decay 时，至少检查：

- 不同 lag 的 IC / RankIC。
- 不同 horizon 的 long-short 收益。
- decay curve 是否平滑。
- 半衰期大约是多少。
- 特征更新频率是否匹配。
- 标签 horizon 是否匹配。
- 是否有未来信息泄露。
- 是否有重叠标签导致的显著性夸大。
- 分 regime、行业、市值后的 decay 是否一致。
- 扣除交易成本后是否仍然有效。

## 常见误区

第一，只看一个 horizon。

```text
只看未来 5 天收益有效，不知道 1 天、10 天、20 天怎样
```

第二，把短效特征用于长周期预测。

第三，把长效低频特征用于高频交易。

第四，用未来波动率、未来收益或事后事件分类来计算 decay。

第五，忽略重叠标签，把显著性估得太乐观。

第六，只看总体 decay，不看不同 regime 下是否不同。

第七，只看 gross alpha，不看交易成本。

## 小结

feature decay 研究的是特征预测能力随时间如何变弱。

它帮助你回答：

```text
这个特征适合预测多远？
持仓周期应该多长？
模型或特征需要多频繁更新？
这个信号扣除交易成本后是否还有意义？
```

一个好的特征研究，不应该只报告总体 IC。

更应该报告：

```text
IC by lag
decay curve
half-life
matched horizon
cost-adjusted performance
```

在金融机器学习里，特征有没有用只是第一步。

特征能用多久，往往同样重要。
