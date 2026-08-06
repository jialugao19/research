# Transaction Costs

## 核心概念

transaction cost 是交易成本。

在量化机器学习里，它不是一个回测结束后才扣掉的数字。

它会影响：

- 标签是否有意义。
- 预测阈值怎么设。
- 模型目标函数怎么选。
- 样本权重怎么设。
- 换手和仓位怎么控制。
- 策略从 gross alpha 到 net alpha 是否仍然成立。

很多模型看起来预测能力不错，但扣除交易成本后没有收益。

所以机器学习策略要关心的问题不是：

```text
模型能不能预测一点点收益？
```

而是：

```text
模型预测的收益是否足够覆盖交易成本？
```

## 常见成本组成

交易成本通常包括：

- commission：手续费。
- tax / fee：税费和交易所费用。
- bid-ask spread：买卖价差。
- slippage：滑点。
- market impact：自己的交易推动价格。
- borrow fee：融券或借券成本。
- funding cost：资金成本。
- delay cost：信号到成交之间的价格变化。

简化写法：

```text
net_return = gross_return - transaction_cost
```

真实项目里，成本不一定是固定比例。

它通常和以下因素有关：

- 股票流动性。
- 订单大小。
- 成交量占比。
- 波动率。
- spread。
- 交易方向。
- 市场状态。
- 执行算法。

## 固定成本

最简单的成本模型是假设每次交易固定扣一个比例。

```python
gross_returns = [0.003, 0.001, -0.002, 0.004]
cost_per_trade = 0.001

net_returns = [
    gross - cost_per_trade
    for gross in gross_returns
]

print(net_returns)
print(sum(gross_returns))
print(sum(net_returns))
```

结果：

```text
[0.002, 0.0, -0.003, 0.003]
0.006
0.002
```

gross 总收益是 `0.006`。

扣成本后只剩 `0.002`。

这说明小 alpha 很容易被成本吃掉。

## 买卖价差成本

如果用中间价 `mid` 估计收益，但真实成交需要跨过 bid-ask spread。

假设买入时付半个 spread，卖出时再付半个 spread。

一次完整买卖大约付一个 spread。

```python
gross_return = 0.0020
spread = 0.0012

net_return = gross_return - spread

print(net_return)
```

结果：

```text
0.0008
```

如果 `gross_return` 小于 spread，策略可能无法赚钱。

这对高频和短周期特征尤其重要。

## 换手成本

组合策略里，成本常按换手计算。

```text
cost = turnover * cost_rate
```

其中 turnover 表示组合权重变化的绝对值之和。

简化例子：

```python
old_weights = {"A": 0.50, "B": 0.30, "C": 0.20}
new_weights = {"A": 0.40, "B": 0.40, "C": 0.20}
cost_rate = 0.002

turnover = sum(
    abs(new_weights[name] - old_weights[name])
    for name in old_weights
)
cost = turnover * cost_rate

print(turnover)
print(cost)
```

结果：

```text
0.19999999999999996
0.0003999999999999999
```

这里换手约 `20%`，成本约 `0.04%`。

如果每天都这样换仓，成本会非常高。

## 双边换手

有些系统把买入和卖出都计入 turnover。

有些系统把组合一买一卖的 `20%` 调仓记成 `20%`，有些记成 `10%`。

所以要先确认定义。

```python
old_weights = {"A": 0.50, "B": 0.30, "C": 0.20}
new_weights = {"A": 0.40, "B": 0.40, "C": 0.20}

one_way_turnover = sum(
    abs(new_weights[name] - old_weights[name])
    for name in old_weights
) / 2

two_way_turnover = sum(
    abs(new_weights[name] - old_weights[name])
    for name in old_weights
)

print(one_way_turnover)
print(two_way_turnover)
```

结果：

```text
0.09999999999999998
0.19999999999999996
```

两种定义都有人用。

报告结果时必须写清楚。

## 滑点

slippage 是预期成交价和实际成交价的差。

例如模型用信号产生时的价格做回测，但真实成交晚了一点。

```python
signal_price = 100.00
execution_price = 100.08
shares = 100

slippage_cost = (execution_price - signal_price) * shares

print(slippage_cost)
```

结果：

```text
7.9999999999998295
```

买入时实际成交价更高，所以成本约 `8` 元。

卖出时方向相反。

滑点常来自：

- 下单延迟。
- 市场波动。
- 订单簿深度不足。
- 信号拥挤。
- 回测用 close，实盘只能 next open 或 VWAP。

## market impact

market impact 是自己的交易影响价格。

交易量越大、市场越不流动，冲击越大。

一个简化模型：

```text
impact_cost = impact_coefficient * (order_value / daily_volume_value) ** 2
```

```python
impact_coefficient = 0.10
order_value = 2_000_000
daily_volume_value = 100_000_000

participation = order_value / daily_volume_value
impact_cost = impact_coefficient * participation ** 2

print(participation)
print(impact_cost)
```

结果：

```text
0.02
4e-05
```

这里订单占日成交额 `2%`。

冲击成本是 `0.004%`。

这只是教学模型，真实冲击成本通常更复杂。

## gross label 和 net label

机器学习中，成本可以进入标签。

gross label：

```text
y = future_return
```

net label：

```text
y = future_return - cost_to_trade
```

简化例子：

```python
future_returns = [0.003, 0.001, -0.001, 0.004]
costs = [0.001, 0.001, 0.001, 0.002]

net_labels = [
    ret - cost
    for ret, cost in zip(future_returns, costs)
]

print(net_labels)
```

结果：

```text
[0.002, 0.0, -0.002, 0.002]
```

如果模型目标是交易盈利，net label 往往比 gross label 更接近真实目标。

但要注意：

```text
成本本身也必须是决策时可估计的，不能使用事后成交信息泄露未来。
```

## 分类标签的成本阈值

如果做分类，不应该简单把 `future_return > 0` 当作买入标签。

应该考虑成本阈值。

```python
future_returns = [0.0005, 0.0015, -0.0002, 0.0030]
cost_threshold = 0.0010

labels = [
    1 if ret > cost_threshold else 0
    for ret in future_returns
]

print(labels)
```

结果：

```text
[0, 1, 0, 1]
```

`0.0005` 是正收益，但不足以覆盖成本。

所以不应该标成可交易机会。

## no-trade zone

有成本时，很多小预测不值得交易。

可以设置 no-trade zone。

```python
predicted_returns = [0.0003, 0.0012, -0.0015, 0.0000]
cost_threshold = 0.0010

actions = []
for pred in predicted_returns:
    if pred > cost_threshold:
        actions.append("buy")
    elif pred < -cost_threshold:
        actions.append("sell")
    else:
        actions.append("hold")

print(actions)
```

结果：

```text
['hold', 'buy', 'sell', 'hold']
```

no-trade zone 可以降低换手。

它把模型从：

```text
只要预测为正就买
```

改成：

```text
预测收益明显超过成本才交易
```

## 成本敏感的样本权重

不同股票的成本不同。

同样的预测误差，在低成本股票上更有交易价值。

可以给低成本、可交易样本更高权重。

```python
costs = [0.0005, 0.0010, 0.0030, 0.0008]

weights = [
    1 / cost
    for cost in costs
]

total = sum(weights)
normalized_weights = [
    weight / total
    for weight in weights
]

print(normalized_weights)
```

结果：

```text
[0.4363636363636363, 0.21818181818181814, 0.07272727272727271, 0.2727272727272727]
```

成本越低，权重越高。

真实建模时要避免权重过大，可以加上下限和上限。

## 交易成本和模型选择

同样的预测指标，换手可能完全不同。

```python
models = {
    "fast_model": {"gross_alpha": 0.020, "cost": 0.018},
    "slow_model": {"gross_alpha": 0.014, "cost": 0.006},
}

net_alpha = {
    name: values["gross_alpha"] - values["cost"]
    for name, values in models.items()
}

best_model = max(net_alpha, key=net_alpha.get)

print(net_alpha)
print(best_model)
```

结果：

```text
{'fast_model': 0.0020000000000000018, 'slow_model': 0.008}
slow_model
```

`fast_model` 的 gross alpha 更高。

但扣成本后，`slow_model` 更好。

所以模型选择不能只看：

- AUC。
- accuracy。
- MSE。
- gross IC。
- gross return。

还要看：

- net return。
- net Sharpe。
- turnover。
- capacity。
- drawdown after cost。

## 成本进入目标函数

训练时可以把成本写进目标函数。

伪代码：

```python
prediction = model(features)
expected_return = prediction * realized_return
trade_cost = cost_model(old_position, new_position)

loss = -expected_return + trade_cost
model.optimize(loss)
```

这类方法更接近真实交易目标。

但也更难：

- 成本模型本身可能估错。
- 仓位变化可能不可微。
- 交易约束会让优化更复杂。
- 回测和实盘执行之间仍可能有差距。

基础阶段可以先做到：

```text
训练看 gross label，评估必须看 net performance
```

然后再逐步把成本加入标签、阈值和目标函数。

## 换手惩罚

为了降低交易成本，可以惩罚仓位变化。

```python
old_position = 0.40
target_position = 0.75
turnover_penalty = 0.10

score = 0.03
adjusted_score = score - turnover_penalty * abs(target_position - old_position)

print(adjusted_score)
```

结果：

```text
-0.0049999999999999975
```

原始分数是正的。

但如果调仓幅度太大，扣掉换手惩罚后就不值得交易。

这说明成本约束可以改变最终决策。

## 成本和容量

capacity 是策略能承载的资金规模。

资金越大，交易越多，impact 通常越高。

```python
base_alpha = 0.030
base_cost = 0.005
scale = 3

scaled_cost = base_cost * scale ** 2
net_alpha = base_alpha - scaled_cost

print(scaled_cost)
print(net_alpha)
```

结果：

```text
0.045
-0.015
```

如果 impact 随规模平方增长，资金扩大 3 倍后，策略可能从盈利变成亏损。

所以评估模型时要问：

```text
这个 alpha 在多大资金规模下还成立？
```

## 回测中的成本位置

成本必须在每次交易发生时扣除。

不要只在最后用一个总比例随便扣。

简化回测：

```python
positions = [0, 1, 1, -1, 0]
returns = [0.00, 0.01, -0.02, 0.03, 0.01]
cost_rate = 0.001

net_pnl = []
for t in range(1, len(positions)):
    gross = positions[t - 1] * returns[t]
    turnover = abs(positions[t] - positions[t - 1])
    cost = turnover * cost_rate
    net_pnl.append(gross - cost)

print(net_pnl)
print(sum(net_pnl))
```

结果：

```text
[-0.001, -0.02, 0.027999999999999997, -0.011]
-0.0040000000000000036
```

这里每次仓位变化都扣成本。

如果忽略成本，总收益会被高估。

## 常见泄露和错误

第一，用事后成交价估计成本。

```text
训练时使用了真实成交后才知道的 slippage
```

这会泄露未来执行结果。

第二，用幸存股票池估计成本。

```text
只保留现在还活跃且流动性好的股票
```

会低估历史成本。

第三，所有股票使用同一个成本。

```text
大盘高流动性股票和小盘低流动性股票成本完全不同
```

第四，调参时只看扣成本前指标。

第五，把日频信号假设成可以在收盘价无成本成交。

第六，忽略卖空、借券、涨跌停、停牌和容量约束。

## 实战检查清单

做机器学习策略时，至少检查：

- gross performance 和 net performance。
- 成本模型假设是否清楚。
- cost rate 是否按股票、日期、流动性变化。
- 换手率是否过高。
- 预测阈值是否覆盖成本。
- 标签是否考虑成本。
- 是否有 no-trade zone。
- 模型选择是否按 net 指标。
- 成本是否在每次调仓时扣。
- 成本参数提高后策略是否仍稳健。
- 策略容量是否会被 market impact 限制。

## 小结

transaction cost 是机器学习策略从预测走向交易的关键约束。

它会把很多看似有效的弱信号变成不可交易信号。

在建模时，要把成本放在三个位置考虑：

```text
标签：预测目标是否覆盖成本
决策：预测值是否超过交易阈值
评估：回测指标是否扣除成本
```

一个模型的 gross 指标好，只说明它可能有预测能力。

只有扣除手续费、价差、滑点、冲击成本和换手之后仍然有效，才说明它有交易价值。
