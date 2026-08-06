# 市场微观结构：VPIN 的成交量分桶、买卖量不平衡和毒性订单流

## 核心概念

VPIN 是 volume-synchronized probability of informed trading。

直译是：

```text
按成交量同步的知情交易概率
```

实际使用时，可以先把它理解成：

```text
用成交量分桶后的买卖量不平衡，近似衡量订单流毒性。
```

这里的毒性订单流指：

```text
一边的主动成交明显占优，流动性提供者更可能面对有信息交易。
```

VPIN 和前面 adverse selection 相关。

它试图用成交数据识别：当前市场里，被动提供流动性是否更危险。

## 买卖量不平衡

VPIN 的核心是买卖量不平衡。

如果一个成交量桶里，买量是 `700`，卖量是 `300`：

```python
buy_volume = 700
sell_volume = 300

bucket_volume = buy_volume + sell_volume
imbalance = abs(buy_volume - sell_volume) / bucket_volume

print(imbalance)
```

结果：

```text
0.4
```

这个桶的买卖量不平衡是 `0.4`。

如果买卖量完全相等，不平衡是 `0`。

如果几乎全是一边成交，不平衡接近 `1`。

## 为什么用成交量分桶

普通时间分桶是：

```text
每 1 分钟一个桶
```

成交量分桶是：

```text
每累计固定成交量形成一个桶
```

这样做的直觉是：

```text
市场活跃时，时间过得快；
市场冷清时，时间过得慢。
```

VPIN 希望用“成交量时间”而不是自然时间来观察订单流。

例如每个桶目标成交量是 `1000`：

```python
trades = [200, 300, 600, 400, 500]
bucket_size = 1000

buckets = []
current = 0
for trade in trades:
    current += trade
    if current >= bucket_size:
        buckets.append(current)
        current = 0

print(buckets)
print(current)
```

结果：

```text
[1100]
900
```

这里第一个桶累计到 `1100`，剩余未完成桶是 `900`。

真实实现可以把跨桶成交拆开，让每个桶更接近固定大小。

本例只展示核心思想。

## 判断买卖方向

计算 VPIN 需要知道每笔成交是主动买还是主动卖。

如果已有成交方向，可以直接累计。

```python
signed_trades = [
    (200, "buy"),
    (300, "sell"),
    (500, "buy"),
]

buy = sum(
    size
    for size, side in signed_trades
    if side == "buy"
)
sell = sum(
    size
    for size, side in signed_trades
    if side == "sell"
)

print(buy)
print(sell)
```

结果：

```text
700
300
```

但很多数据里没有真实主动方向。

这时只能用规则估计，例如：

```text
成交价靠近 ask -> 估计为主动买
成交价靠近 bid -> 估计为主动卖
tick rule：价格上涨成交估计为买，下跌估计为卖
```

方向估计错误会直接影响 VPIN。

## 单个桶的 imbalance

每个桶计算：

```text
abs(buy_volume - sell_volume) / bucket_volume
```

例如三个桶：

```python
buckets = [
    {"buy": 600, "sell": 400},
    {"buy": 900, "sell": 100},
    {"buy": 450, "sell": 550},
]

imbalances = []
for bucket in buckets:
    total = bucket["buy"] + bucket["sell"]
    imbalances.append(abs(bucket["buy"] - bucket["sell"]) / total)

vpin = sum(imbalances) / len(imbalances)

print(imbalances)
print(round(vpin, 4))
```

结果：

```text
[0.2, 0.8, 0.1]
0.3667
```

这里 VPIN 是最近三个桶 imbalance 的平均值。

第二个桶非常不平衡，对 VPIN 有明显拉升。

## 滚动 VPIN

实际使用时，VPIN 通常是滚动平均。

例如 imbalance 序列是：

```python
imbalances = [0.2, 0.8, 0.1, 0.6]
window = 2

rolling_vpin = []
for i in range(window, len(imbalances) + 1):
    rolling_vpin.append(sum(imbalances[i - window:i]) / window)

print(rolling_vpin)
```

结果：

```text
[0.5, 0.45, 0.35]
```

VPIN 越高，表示最近成交量桶中的买卖不平衡越强。

这可能意味着流动性提供者面对更高 adverse selection 风险。

## VPIN 的交易含义

VPIN 高时，可能代表：

```text
买单或卖单一边倒
市场正在吸收方向性信息
流动性提供者更容易被有信息订单打中
短期波动可能升高
spread 可能变宽
```

一个简单风控规则：

```python
vpin = 0.75
threshold = 0.6

reduce_liquidity = vpin > threshold

print(reduce_liquidity)
```

结果：

```text
True
```

这表示 VPIN 高于阈值时，减少被动挂单或扩大报价。

注意，这不是说 VPIN 高就一定买或卖。

它更像市场状态和执行风险指标。

## 和 order imbalance 的区别

order imbalance 看的是盘口存量。

```text
bid size 和 ask size 谁更厚？
```

VPIN 看的是成交流量。

```text
最近成交里，主动买量和主动卖量是否失衡？
```

两者可以互补：

```text
盘口买盘很厚，但成交持续主动卖出 -> 支撑可能被消耗
盘口看起来平衡，但成交流持续偏买 -> 可能有隐藏买压
```

一个看订单簿静态深度。

一个看已经发生的交易流。

## 成交方向估计误差

VPIN 对成交方向估计很敏感。

假设真实方向和估计方向如下：

```python
true_sides = ["buy", "sell", "buy", "sell"]
estimated_sides = ["buy", "buy", "buy", "sell"]

accuracy = sum(
    actual == estimated
    for actual, estimated in zip(true_sides, estimated_sides)
) / len(true_sides)

print(accuracy)
```

结果：

```text
0.75
```

这里有 `25%` 的方向估计错误。

如果错误集中发生在关键时段，VPIN 可能会严重偏离真实订单流。

所以高频研究里，成交方向标注质量非常重要。

## 成交量权重

VPIN 关注成交量，而不是交易笔数。

三笔成交量分别是 `100`、`200`、`700`：

```python
volumes = [100, 200, 700]

total = sum(volumes)
weights = [
    volume / total
    for volume in volumes
]

print(weights)
```

结果：

```text
[0.1, 0.2, 0.7]
```

最大那笔成交占总量 `70%`。

如果只按笔数看，三笔交易权重相同。

按成交量看，大单影响更大。

这正是 VPIN 使用成交量分桶的原因之一。

## 常见局限

VPIN 不是无条件有效的预测器。

常见局限包括：

```text
成交方向估计可能错误
分桶大小选择会影响结果
滚动窗口长度会影响平滑程度
高 VPIN 可能只是正常再平衡或大单执行
不同资产的成交机制不同，阈值不能直接搬用
成交数据有延迟、合并或修正时，指标会失真
```

另外，VPIN 高不一定说明未来价格一定上涨或下跌。

它更多说明：

```text
当前订单流更不平衡，流动性提供者面对的风险可能更高。
```

## 回测中的常见错误

使用 VPIN 时，常见错误包括：

```text
用未来成交补当前桶
桶尚未完成就使用完整桶信息
用未来才能知道的成交方向修正当前信号
用全样本分位数设阈值
把 VPIN 当方向信号而不是风险状态
忽略交易成本和 market impact
```

正确做法是：

```text
只使用当前时点已经完成或可确认的成交数据
阈值只在训练区间估计
评估时按时间顺序滚动更新
```

## 小结

VPIN 用成交量分桶中的买卖量不平衡，近似衡量订单流毒性。

核心步骤是：

```text
按成交量构造 bucket
估计每笔成交方向
计算每个 bucket 的买卖量不平衡
对最近若干 bucket 做滚动平均
```

它和 adverse selection、spread、market impact 都有关。

实务中更适合把 VPIN 当作：

```text
流动性风险指标
不利选择风险指标
执行策略的状态变量
```

下一篇讨论 opening/closing auction。

它会解释集合竞价里的撮合价格、订单不平衡和开收盘流动性特征。
