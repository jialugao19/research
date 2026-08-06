# Mental Math & Estimation

## 核心概念

快速心算与估算不是追求精确到小数点后很多位。

它追求：

```text
数量级正确
推理过程清楚
误差范围可接受
能快速发现荒谬答案
```

面试中常见问题：

- 市场规模有多大？
- 某策略容量大概多少？
- 年化收益和日收益怎么换算？
- 某个延迟、成交量、内存、吞吐是否合理？
- 复杂概率或组合数大约是多少？

好估算通常包含：

```text
拆分问题
给出假设
用简单数字近似
算数量级
做 sanity check
```

## 数量级

数量级是 `10` 的幂。

例如：

```text
1,000        = 10^3
1,000,000    = 10^6
1,000,000,000 = 10^9
```

快速估算时，先判断结果大概是：

```text
几千？
几百万？
几十亿？
```

很多错误一眼就能通过数量级发现。

例子：

```text
如果全市场每天成交额约 5000 亿人民币，
一个策略说自己每天能稳定吃掉 1 万亿成交额，
数量级上就需要非常强的解释。
```

## 常用单位

金融和系统题里常见单位：

```text
K = thousand = 10^3
M = million = 10^6
B = billion = 10^9
T = trillion = 10^12
```

存储单位粗略记：

```text
1 KB ~ 10^3 bytes
1 MB ~ 10^6 bytes
1 GB ~ 10^9 bytes
1 TB ~ 10^12 bytes
```

时间：

```text
1 day = 24 * 3600 = 86400 seconds ~ 1e5 seconds
1 year ~ 252 trading days
1 trading day ~ 6.5 hours for US equities
```

近似时，把 `86400` 看成 `1e5` 很常见。

但最后要知道这是约 `16%` 的误差。

## 拆分乘法

心算大数乘法时，先拆分。

例子：

```text
48 * 25
```

因为：

```text
25 = 100 / 4
```

所以：

```text
48 * 25 = 48 * 100 / 4 = 1200
```

代码验证：

```python
print(48 * 25)
```

结果：

```text
1200
```

另一个例子：

```text
97 * 103
```

看成：

```text
(100 - 3)(100 + 3) = 10000 - 9 = 9991
```

```python
print(97 * 103)
```

结果：

```text
9991
```

## 百分比心算

百分比可以互换：

```text
a% of b = b% of a
```

例如：

```text
8% of 25 = 25% of 8 = 2
```

代码：

```python
print(0.08 * 25)
print(0.25 * 8)
```

结果：

```text
2.0
2.0
```

常用百分比：

```text
1% = 除以 100
10% = 除以 10
25% = 四分之一
50% = 一半
75% = 四分之三
```

## 增长率近似

小百分比变化可以近似相加。

例如：

```text
先涨 2%，再涨 3%
```

精确：

```text
1.02 * 1.03 - 1 = 5.06%
```

近似：

```text
2% + 3% = 5%
```

误差：

```text
0.06%
```

代码：

```python
exact = 1.02 * 1.03 - 1
approx = 0.02 + 0.03

print(exact)
print(approx)
print(exact - approx)
```

结果：

```text
0.050600000000000006
0.05
0.0006000000000000033
```

小变化相乘时，交叉项通常很小。

但如果变化很大，例如 `30%` 和 `40%`，就不能简单相加。

## 复利近似：72 法则

72 法则：

```text
翻倍时间约等于 72 / 年化收益率百分数
```

例如年化 8%：

```text
72 / 8 = 9 年
```

精确翻倍时间：

```python
import math

exact_years = math.log(2) / math.log(1.08)
rule_72 = 72 / 8

print(exact_years)
print(rule_72)
```

结果：

```text
9.006468342000588
9.0
```

这在心算中很方便。

## 日收益和年化收益

粗略换算：

```text
年化收益 ~ 日收益 * 252
```

如果日均收益是 `5 bps`：

```text
5 bps = 0.05% = 0.0005
年化约 0.0005 * 252 = 0.126 = 12.6%
```

代码：

```python
daily_return = 0.0005
annual_approx = daily_return * 252

print(annual_approx)
```

结果：

```text
0.126
```

如果要复利精确值：

```python
annual_exact = (1 + daily_return) ** 252 - 1

print(annual_exact)
```

结果约为：

```text
0.13424645086258704
```

小日收益下，线性近似通常够快。

## 年化波动换日波动

常用近似：

```text
annual vol = daily vol * sqrt(252)
```

所以：

```text
daily vol = annual vol / sqrt(252)
```

因为：

```text
sqrt(252) ~ 16
```

年化波动 16% 对应日波动约：

```text
16% / 16 = 1%
```

代码：

```python
import math

daily_vol = 0.16 / math.sqrt(252)

print(daily_vol)
```

结果：

```text
0.010079052613579392
```

所以心算 `sqrt(252) ~ 16` 很实用。

## bps 心算

bps 是 basis point，基点。

```text
1 bp = 0.01% = 0.0001
10 bps = 0.10% = 0.001
100 bps = 1% = 0.01
```

如果成交额是 2000 万，成本是 5 bps：

```text
20,000,000 * 0.0005 = 10,000
```

代码：

```python
notional = 20_000_000
cost_bps = 5
cost = notional * cost_bps / 10_000

print(cost)
```

结果：

```text
10000.0
```

记住：

```text
bps / 10000 = 小数形式
```

## Sharpe 近似

如果日均收益 `mu_daily`，日波动 `sigma_daily`：

```text
Sharpe ~ mu_daily / sigma_daily * sqrt(252)
```

例子：

```text
日均收益 5 bps = 0.0005
日波动 1% = 0.01
sqrt(252) ~ 16
Sharpe ~ 0.0005 / 0.01 * 16 = 0.8
```

代码：

```python
import math

sharpe = 0.0005 / 0.01 * math.sqrt(252)

print(sharpe)
```

结果：

```text
0.7937253933193773
```

心算 `0.8` 足够接近。

## 容量估算

容量题常见思路：

```text
策略成交额不能超过市场成交额的某个比例
```

例如：

```text
可交易股票日均成交额合计 100 亿
策略最多占 5%
```

则每日可成交：

```text
100 亿 * 5% = 5 亿
```

如果换手率是每天 20%，组合规模容量约：

```text
组合规模 * 20% = 5 亿
组合规模 = 25 亿
```

代码：

```python
market_adv = 10_000_000_000
participation = 0.05
daily_tradable = market_adv * participation
turnover = 0.20
capacity = daily_tradable / turnover

print(daily_tradable)
print(capacity)
```

结果：

```text
500000000.0
2500000000.0
```

这只是粗估。

真实容量还要看冲击成本、持仓集中度、成交曲线和风险限制。

## 市场规模 Fermi 估算

Fermi estimation 是把复杂问题拆成可估数量。

例子：

```text
一个城市每天咖啡销售额大概多少？
```

假设：

```text
人口 1000 万
每天买咖啡的人占 10%
每人每天 1 杯
每杯 25 元
```

销售额：

```text
10,000,000 * 10% * 1 * 25 = 25,000,000 元
```

也就是每天约 2500 万。

代码：

```python
population = 10_000_000
buyer_ratio = 0.10
cups_per_buyer = 1
price = 25

revenue = population * buyer_ratio * cups_per_buyer * price

print(revenue)
```

结果：

```text
25000000.0
```

重点不是答案唯一正确，而是：

```text
假设清楚
量级合理
能解释误差来源
```

## 延迟和吞吐估算

系统题常问：

```text
每秒能处理多少条消息？
```

如果单条消息处理耗时 `50 microseconds`：

```text
50 us = 50 * 10^-6 seconds
每秒处理量 ~ 1 / 50e-6 = 20,000
```

代码：

```python
latency_seconds = 50e-6
throughput = 1 / latency_seconds

print(throughput)
```

结果：

```text
20000.0
```

如果有 8 个并行 worker，理想吞吐：

```text
160,000 / second
```

但实际要扣除锁、IO、序列化、网络和负载不均。

## 内存估算

假设要保存：

```text
1000 只股票
每只股票 1,000,000 个 tick
每个 tick 记录 5 个 float64
```

一个 float64 是 8 bytes。

内存：

```text
1000 * 1,000,000 * 5 * 8
= 40,000,000,000 bytes
~ 40 GB
```

代码：

```python
symbols = 1000
ticks = 1_000_000
fields = 5
bytes_per_float = 8

memory_bytes = symbols * ticks * fields * bytes_per_float
memory_gb = memory_bytes / 1e9

print(memory_gb)
```

结果：

```text
40.0
```

这能帮助你判断：

```text
是否能放内存？
是否需要压缩？
是否需要分块处理？
```

## 概率近似

小概率事件的至少一次发生概率：

```text
1 - (1-p)^n
```

当 `p` 小、`np` 不太大时：

```text
1 - (1-p)^n ~ np
```

例如：

```text
每天 0.1% 概率出故障，30 天至少一次故障
```

近似：

```text
30 * 0.1% = 3%
```

精确：

```python
p = 0.001
n = 30

exact = 1 - (1 - p) ** n
approx = n * p

print(exact)
print(approx)
```

结果：

```text
0.02956903273635825
0.03
```

近似很好。

如果 `np` 很大，这个近似会失效。

## 对数近似

常用近似：

```text
ln(1+x) ~ x
```

当 `x` 很小时成立。

例如：

```text
ln(1.01) ~ 0.01
```

代码：

```python
import math

print(math.log(1.01))
print(0.01)
```

结果：

```text
0.009950330853168092
0.01
```

这和复利、连续收益、增长率估算都有关。

## 面试表达模板

估算题回答时可以这样组织：

```text
1. 我先做几个假设。
2. 把问题拆成 A * B * C。
3. 用容易心算的数字估。
4. 得到数量级。
5. 说明误差可能来自哪里。
6. 做一个 sanity check。
```

例如市场容量题：

```text
假设可交易 ADV 是 100 亿。
策略最多参与 5%，所以每天最多成交 5 亿。
如果日换手 20%，容量约 25 亿。
如果冲击成本更敏感，容量可能低于这个数。
```

这样的回答比直接报一个数字更可靠。

## 常见错误

### 错误 1：过早追求精确

估算题首先要数量级正确。

如果第一步假设错了 10 倍，小数点后再精确也没意义。

### 错误 2：单位混乱

常见混乱：

- bps 和 percent。
- million 和 billion。
- bytes 和 bits。
- 日收益和年化收益。
- 秒、毫秒、微秒。

先统一单位再计算。

### 错误 3：忘记 sanity check

算出结果后问：

```text
这个数和常识一致吗？
有没有超过总市场规模？
有没有超过机器内存？
有没有超过一天总秒数？
```

### 错误 4：把近似当精确

`sqrt(252) ~ 16`、`ln(1+x) ~ x`、`1-(1-p)^n ~ np` 都有适用范围。

需要知道什么时候误差会变大。

### 错误 5：假设不说清

估算没有唯一答案。

面试官更看重你如何拆解问题。

不说假设，别人无法判断你的答案是否合理。

## 解题步骤

快速心算与估算可以按这个流程：

1. 先判断目标单位。
2. 写出拆分公式。
3. 把复杂数字换成容易算的近似。
4. 保留 1 到 2 位有效数字。
5. 算完做数量级检查。
6. 说明误差来源和敏感假设。

## 记忆要点

- 估算先看数量级，再看细节。
- 单位统一比小数精度更重要。
- 百分比可以互换：`a% of b = b% of a`。
- 小增长率可以近似相加。
- 72 法则可估复利翻倍时间。
- `sqrt(252) ~ 16` 常用于年化和日频转换。
- `1 bp = 0.0001`。
- 小概率至少一次可近似为 `np`。
- Fermi 题要拆假设、算数量级、做 sanity check。

## 自测题

1. 为什么估算题要先看数量级？
2. 5 bps 成本对应的小数是多少？
3. 年化波动 16% 大约对应多少日波动？
4. 日均收益 5 bps 粗略年化是多少？
5. Fermi 估算题回答时为什么要明确假设？
