# 73. 数据结构与算法：hashmap 的接口、哈希冲突、复杂度和量化数据应用

## 核心概念

hashmap 哈希表是一种 key-value 数据结构。

在 Python 中最常用的 hashmap 是：

```python
dict
```

它支持：

- 按 key 插入 value。
- 按 key 查询 value。
- 按 key 更新 value。
- 判断 key 是否存在。
- 删除 key。

平均情况下，这些操作的时间复杂度接近：

```text
O(1)
```

这就是 hashmap 的核心价值：用空间换时间，把很多查找问题从线性扫描变成近似常数时间查询。

## hashmap 回答的问题

hashmap 适合处理：

- 计数。
- 去重。
- 快速查找。
- 建索引。
- 缓存中间结果。
- 按 symbol / date / id 做映射。
- 判断某个元素是否已经出现过。

量化和数据处理中很常见：

```text
(symbol, date) -> price record
order_id -> order state
symbol -> latest quote
factor_name -> factor values
user_id -> portfolio
```

如果你发现自己在循环里反复扫描列表找某个 key，通常应该考虑 hashmap。

## 基础接口

```python
price_by_symbol = {
    "AAPL": 185.6,
    "MSFT": 370.2,
}

price_by_symbol["NVDA"] = 490.1
price_by_symbol["AAPL"] = 184.1

print(price_by_symbol["AAPL"])
print("MSFT" in price_by_symbol)
print(price_by_symbol.get("TSLA", None))
```

常见接口：

```python
price_by_symbol[key]          # 查询；key 不存在会报错
price_by_symbol.get(key)      # 查询；key 不存在返回 None
price_by_symbol.get(key, 0)   # 查询；key 不存在返回默认值
key in price_by_symbol        # 判断是否存在
del price_by_symbol[key]      # 删除
```

## 计数例子

统计 symbol 出现次数：

```python
symbols = ["AAPL", "MSFT", "AAPL", "NVDA", "MSFT", "AAPL"]

counts = {}

for symbol in symbols:
    counts[symbol] = counts.get(symbol, 0) + 1

print(counts)
```

输出应类似：

```text
{"AAPL": 3, "MSFT": 2, "NVDA": 1}
```

Python 标准库也提供 `Counter`：

```python
from collections import Counter

counts_fast = Counter(symbols)

print(counts_fast)
```

`Counter` 本质上也是基于 dict 的计数工具。

## 去重和重复检测

找出重复出现的价格位置：

```python
prices = [101, 99, 105, 101, 103, 99]

last_seen = {}
duplicates = []

for i, price in enumerate(prices):
    if price in last_seen:
        duplicates.append((last_seen[price], i, price))

    last_seen[price] = i

print(duplicates)
```

结果：

```text
[(0, 3, 101), (1, 5, 99)]
```

如果不用 hashmap，每次都向前扫描历史价格，复杂度会接近 `O(n^2)`。

用 hashmap 记录“上一次见到的位置”，整体可以做到 `O(n)`。

## 经典例子：two sum

给定数组和目标值，找两个数相加等于目标。

```python
nums = [7, 3, 11, 2, 8]
target = 10

seen = {}
answer = None

for i, x in enumerate(nums):
    need = target - x

    if need in seen:
        answer = (seen[need], i)
        break

    seen[x] = i

print(answer)
```

解释：

- 遍历到 `x` 时，想知道之前是否出现过 `target - x`。
- `seen` 把历史数字映射到下标。
- 查询历史数字是否出现过是 `O(1)` 平均复杂度。

这类模式在面试里很常见：

```text
遍历当前元素 + hashmap 记录过去信息
```

## 量化例子：按 symbol 和 date 建索引

假设有一些行情记录：

```python
records = [
    {"symbol": "AAPL", "date": "2024-01-02", "close": 185.6},
    {"symbol": "MSFT", "date": "2024-01-02", "close": 370.2},
    {"symbol": "AAPL", "date": "2024-01-03", "close": 184.1},
]
```

把 `(symbol, date)` 映射到整条记录：

```python
record_index = {
    (row["symbol"], row["date"]): row
    for row in records
}

print(record_index[("AAPL", "2024-01-03")]["close"])
```

这里的 key 是 tuple。

Python dict 的 key 必须是 hashable 的。常见可 hash key：

- `str`
- `int`
- `float`
- `tuple`，前提是 tuple 内部元素也可 hash

常见不可 hash key：

- `list`
- `dict`
- `set`

因为它们可变，不能稳定作为哈希键。

## 一对多映射

如果一个 symbol 对应多条记录，可以用 `defaultdict(list)`：

```python
from collections import defaultdict

by_symbol = defaultdict(list)

for row in records:
    by_symbol[row["symbol"]].append(row)

print(by_symbol["AAPL"])
```

这类结构常用于：

- `symbol -> all trades`
- `date -> all records`
- `sector -> symbols`
- `order_id -> fills`

如果不用 `defaultdict`，也可以写：

```python
by_symbol = {}

for row in records:
    if row["symbol"] not in by_symbol:
        by_symbol[row["symbol"]] = []

    by_symbol[row["symbol"]].append(row)
```

`defaultdict` 只是把初始化列表这件事封装掉。

## 哈希冲突

hashmap 的内部会先对 key 计算 hash 值，再把 key 放到某个位置。

不同 key 可能得到相同位置，这叫哈希冲突。

Python dict 会处理冲突，所以使用者通常不用自己处理。

用一个人为的坏 hash 类演示：

```python
class BadHash:
    def __init__(self, value):
        self.value = value

    def __hash__(self):
        return 1

    def __eq__(self, other):
        return isinstance(other, BadHash) and self.value == other.value


collision_map = {
    BadHash(i): i
    for i in range(5)
}

print(collision_map[BadHash(3)])
print(len(collision_map))
```

所有 key 的 hash 都是 `1`，但因为 `__eq__` 能区分真实值，dict 仍然能正确查询。

不过大量冲突会降低性能。

平均复杂度是 `O(1)`，但最坏情况可能退化。

## dict 的复杂度

常见操作平均复杂度：

```text
get / set / delete / in: O(1)
遍历所有 key/value: O(n)
```

需要注意：

- 平均 `O(1)` 不等于每次都一样快。
- hash 冲突、扩容、key 的 hash 计算成本都会影响实际性能。
- dict 会占用额外内存。
- Python 3.7+ 的普通 dict 保留插入顺序，但算法题里通常不要把 dict 当排序结构。

如果需要按 key 有序查询，hashmap 不是合适结构；可能需要排序数组、平衡树或 heap。

## 常见模式

模式一：计数。

```text
key -> count
```

模式二：记录首次或最近出现位置。

```text
value -> index
```

模式三：分组。

```text
group_key -> list of items
```

模式四：缓存。

```text
input_args -> computed_result
```

模式五：反向索引。

```text
id -> object
symbol/date -> row
```

这些模式是很多算法题和数据管道的基础。

## 常见坑

第一，用可变对象做 key。

`list` 不能直接做 key。可以把它转成 tuple。

第二，忘记 key 不存在的情况。

直接 `d[key]` 会报 `KeyError`。不确定存在时，用 `get`、`in` 或 `defaultdict`。

第三，在遍历 dict 时修改大小。

遍历 `dict.keys()` 时新增或删除 key 可能报错。需要先复制 key 列表。

第四，把平均 `O(1)` 理解成免费。

dict 很快，但内存开销不小。海量数据时要注意内存。

第五，忽略 key 的唯一性。

如果用 `(symbol, date)` 做 key，同一个 key 重复出现会覆盖旧记录。需要确认这是你想要的行为。

## 实战提示

使用 hashmap 时可以按下面判断：

1. 是否需要按 key 快速查找？
2. 是否需要记录某个元素是否出现过？
3. 是否要把数据按某个字段分组？
4. 是否能用 tuple 组成复合 key？
5. key 重复时应该覆盖、累加还是追加到列表？
6. 数据规模是否大到需要关注内存？

在量化代码里，hashmap 经常用于把慢速扫描变成快速查表。

但如果数据已经在 pandas DataFrame 中，很多场景更适合用：

```text
set_index
merge
groupby
join
```

hashmap 是底层思维，pandas 是批量数据接口。两者不冲突。

## 小结

本节的重点：

- hashmap 存储 key-value 映射。
- Python 的 `dict` 是最常用 hashmap。
- 查询、插入、删除平均复杂度接近 `O(1)`。
- 常见用途包括计数、去重、分组、缓存和索引映射。
- key 必须 hashable。
- 哈希冲突由 dict 内部处理，但大量冲突会影响性能。
- 在量化数据处理中，hashmap 常用于 `(symbol, date) -> record` 这类快速查表。

## 自检问题

1. hashmap 为什么能把很多查找问题从 `O(n)` 降到平均 `O(1)`？
2. Python 中哪些对象可以做 dict key，哪些不适合？
3. `dict.get(key, default)` 和 `dict[key]` 有什么区别？
4. 什么是哈希冲突？
5. 为什么 `(symbol, date)` 适合作为行情记录的复合 key？
6. 什么时候应该用 `defaultdict(list)`？
