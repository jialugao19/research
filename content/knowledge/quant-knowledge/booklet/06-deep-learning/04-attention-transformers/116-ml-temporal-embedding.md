# Temporal Embedding

## 核心概念

temporal embedding 是时间嵌入。

它的作用是把时间相关信息变成模型可使用的向量。

普通特征告诉模型：

```text
这个时点发生了什么？
```

temporal embedding 额外告诉模型：

```text
这个时点在序列里的哪里？
它属于什么日历环境？
它距离目标时点有多远？
```

在时间序列里，这很重要。

因为同样的收益率、成交量、价差，在不同位置和不同日历环境下，含义可能不一样。

例如：

```text
开盘后的成交量放大
收盘前的成交量放大
财报日前的波动放大
长假后的跳空
```

这些都不是单靠数值特征一定能稳定表达的。

## 和 attention 的区别

attention 负责回答：

```text
当前 token 应该从其他 token 读取多少信息？
```

temporal embedding 负责回答：

```text
每个 token 的时间身份是什么？
```

如果没有 temporal embedding，Transformer 这类模型只看到一组 token，很难天然知道先后顺序。

小例子：

```python
sequence_length = 5
positions = list(range(sequence_length))

print(positions)
```

结果：

```text
[0, 1, 2, 3, 4]
```

这组位置编号本身很简单。

但它给了模型区分 `t-4`、`t-3`、`t-2`、`t-1`、`t` 的入口。

## 绝对位置 embedding

最直接的做法是给每个位置一个可学习向量。

例如窗口长度是 `252`，每个位置用 `16` 维向量表示：

```python
num_positions = 252
d_model = 16

num_params = num_positions * d_model

print(num_params)
```

结果：

```text
4032
```

这表示模型有 `4032` 个位置 embedding 参数。

绝对位置 embedding 的含义是：

```text
第 0 个位置有自己的向量
第 1 个位置有自己的向量
...
第 251 个位置有自己的向量
```

优点是灵活。

缺点是对训练时没见过的更长窗口不自然。

例如只训练过 `252` 日窗口，直接推到 `500` 日窗口时，后面的新位置没有已学习的 embedding。

## sinusoidal 位置编码

另一种做法是不用学习参数，而是用正弦和余弦生成位置编码。

它的好处是可以为任意位置计算编码。

小例子：

```python
import math

position = 3
d_model = 4

encoding = []
for i in range(d_model):
    denominator = 10000 ** (2 * (i // 2) / d_model)
    value = position / denominator
    encoding.append(math.sin(value) if i % 2 == 0 else math.cos(value))

print(encoding)
```

结果：

```text
[0.1411200080598672, -0.9899924966004454, 0.02999550020249566, 0.9995500337489875]
```

不同维度使用不同频率。

低频维度变化慢，高频维度变化快。

这让模型既能感知短距离变化，也能感知长距离位置差异。

## 相对时间 embedding

绝对位置关心：

```text
这个 token 在窗口中的第几个位置？
```

相对时间关心：

```text
这个 token 距离预测时点有多远？
```

在金融时间序列中，相对距离经常更有意义。

例如：

```text
t-1 的信息通常比 t-60 的信息更接近预测目标
```

可以把距离分桶：

```python
distances = [0, 1, 2, 5, 20]

def bucket(distance):
    if distance <= 1:
        return "near"
    if distance <= 5:
        return "mid"
    return "far"

buckets = [bucket(distance) for distance in distances]

print(buckets)
```

结果：

```text
['near', 'near', 'mid', 'mid', 'far']
```

分桶后，可以给 `near`、`mid`、`far` 各自一个 embedding。

这比直接让模型记住每个具体距离更稳健。

## 日历 embedding

日历 embedding 用来表示交易日和自然时间属性。

常见变量包括：

```text
星期几
月份
季末、月末、周末前
开盘后第几分钟
距离收盘还有多久
是否节假日前后
是否指数调仓日
是否财报窗口
```

最简单的类别表示是 one-hot。

例如只考虑一周 5 个交易日，星期三记作 `2`：

```python
day_of_week = 2

one_hot = [
    1 if i == day_of_week else 0
    for i in range(5)
]

print(one_hot)
```

结果：

```text
[0, 0, 1, 0, 0]
```

深度学习模型里，也可以把星期几映射成一个低维可学习向量。

这样模型不必把星期几当成互相完全独立的五个变量。

## 周期变量的 sin/cos 编码

有些时间变量是周期性的。

例如星期一和星期五在编号上相隔 `4`，但在下一个交易周里又相邻。

直接使用整数编号可能误导模型。

可以用正弦和余弦编码周期位置：

```python
import math

day = 3
period = 5

sin_value = math.sin(2 * math.pi * day / period)
cos_value = math.cos(2 * math.pi * day / period)

print(sin_value)
print(cos_value)
```

结果：

```text
-0.587785252292473
-0.8090169943749476
```

`sin` 和 `cos` 一起使用，可以表达周期中的角度位置。

这种编码常用于：

```text
星期几
月份
日内分钟
一年中的第几个交易日
```

## 日内时间 embedding

日内数据中，时间位置尤其重要。

开盘、午间、收盘的流动性和波动率通常不同。

例如距离收盘还有 `30` 分钟，一个交易日有 `390` 分钟：

```python
minutes_to_close = 30
session_minutes = 390

value = minutes_to_close / session_minutes

print(value)
```

结果：

```text
0.07692307692307693
```

这个归一化变量表示：

```text
当前距离收盘很近
```

对于分钟级预测，它可能比简单的分钟编号更直接。

## add 和 concatenate

temporal embedding 通常要和原始特征 embedding 合并。

常见有两种方式。

第一种是相加。

要求两个向量维度相同：

```python
feature_embedding = [0.2, -0.1, 0.4]
position_embedding = [0.01, 0.02, -0.03]

combined = [
    feature_value + position_value
    for feature_value, position_value in zip(feature_embedding, position_embedding)
]

print(combined)
```

结果：

```text
[0.21000000000000002, -0.08, 0.37]
```

相加常见于 Transformer：

```text
token embedding + position embedding
```

第二种是拼接。

拼接不要求维度相同：

```python
feature_embedding = [0.2, -0.1, 0.4]
calendar_embedding = [0.5, 0.1]

combined = feature_embedding + calendar_embedding

print(combined)
```

结果：

```text
[0.2, -0.1, 0.4, 0.5, 0.1]
```

拼接后通常再接一层线性变换，把维度投影回模型需要的宽度。

## 不规则交易日

金融时间序列和自然语言序列不同。

文本中的 token 通常按连续位置排列。

市场数据有很多不规则性：

```text
周末没有交易
节假日没有交易
不同市场交易日不同
不同资产停牌情况不同
日内交易时段可能不连续
期货有夜盘
跨市场资产有时区差异
```

所以位置编号 `0, 1, 2, 3` 不一定等于自然时间间隔相同。

例如：

```text
周五到下周一：相邻两个交易日，但相隔三个自然日
节前到节后：相邻两个交易日，但信息断层更大
```

因此，实际建模时常同时使用：

```text
交易序号位置
自然日间隔
日历标签
市场 session 标签
距离事件的天数
```

## 事件 embedding

事件也可以作为 temporal embedding 的一部分。

例如：

```text
距离财报日还有几天
是否 FOMC 日
是否 CPI 发布日
是否期权到期日
是否指数调仓日
```

关键问题不是能不能编码，而是预测时是否已知。

例如：

```python
known_at_prediction = {
    "market_holiday": True,
    "future_earnings_surprise": False,
}

safe_features = [
    name
    for name, safe in known_at_prediction.items()
    if safe
]

print(safe_features)
```

结果：

```text
['market_holiday']
```

交易所假期通常提前知道。

未来财报超预期幅度在预测时不知道。

后者不能作为特征。

## 防止时间泄露

temporal embedding 看起来像辅助信息，但一样会泄露未来。

常见风险包括：

```text
使用预测时还不知道的事件结果
用全样本统计值标准化时间特征
用未来样本扩展类别词表
把标签窗口里的信息编码进当前特征
跨资产对齐时混入未来时区的数据
```

如果使用可学习类别 embedding，应只在训练集确定类别映射。

验证集或测试集出现未知类别时，应该落到 unknown 类别。

小例子：

```python
known_categories = {
    "Mon": 0,
    "Tue": 1,
    "Wed": 2,
}

category = "Fri"
index = known_categories.get(category, -1)

print(index)
```

结果：

```text
-1
```

这里 `-1` 表示未知类别。

实际模型里通常会给 unknown 单独一个 embedding。

## 在时间序列模型中的位置

temporal embedding 可以放在输入端。

典型流程是：

```text
原始数值特征
-> 特征投影成 token embedding
-> 加上或拼接 temporal embedding
-> 输入 LSTM、GRU、Transformer 或其他序列模型
```

对 Transformer 来说，它尤其关键。

因为 self-attention 本身不自带顺序感。

对 LSTM 和 GRU 来说，它不是必需条件，但仍可能有帮助。

因为循环结构知道输入顺序，却不一定知道：

```text
当前是周几
是否接近收盘
距离节假日有多远
```

## 小结

temporal embedding 的重点不是把时间变量越做越多。

重点是把预测时真实可用的时间信息，用稳定、可泛化的方式交给模型。

实践中要优先检查四件事：

```text
位置编码是否符合窗口定义
日历和事件信息在预测时是否已知
训练、验证、测试的类别映射是否隔离
不同市场和资产的时间戳是否正确对齐
```

下一篇讨论 sequence modeling。

它会进一步说明如何把单点样本组织成输入窗口、预测标签和 many-to-one / many-to-many 结构。
