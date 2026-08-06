# 计算机基础：列表、字典、集合的底层实现、操作代价和使用取舍

## 核心概念

Python 里最常用的基础容器是：

```text
list: 有序数组
dict: 哈希表映射
set: 哈希集合
```

它们看起来都能“装东西”，但操作代价完全不同。

写策略代码时，选错数据结构会导致：

```text
查找很慢
去重很慢
内存过大
代码复杂
回测速度失控
```

本篇重点是理解什么时候用 list、dict、set。

## list 的底层直觉

Python list 可以理解为动态数组。

它保存的是一段连续位置上的对象引用。

所以按下标访问很快：

```python
values = [10, 20, 30]

print(values[1])
```

结果：

```text
20
```

按下标访问是 O(1)。

因为 Python 可以直接根据位置找到对应元素。

## list append

在列表末尾追加通常是摊销 O(1)。

```python
values = [10, 20, 30]

values.append(40)

print(values)
```

结果：

```text
[10, 20, 30, 40]
```

“摊销”表示：

```text
大多数 append 很快
偶尔 list 扩容，需要复制底层数组
平均下来仍然接近 O(1)
```

这就是为什么构造列表时，通常推荐 append。

## list 头部插入

在列表头部插入很贵。

```python
values = [10, 20, 30]

values.insert(0, 5)

print(values)
```

结果：

```text
[5, 10, 20, 30]
```

这个操作需要把原来的元素整体往后移动。

复杂度是 O(n)。

如果经常从头部插入或弹出，应考虑 `collections.deque`。

## list 查找

list 判断某个值是否存在，通常需要从前往后扫描。

```python
values = [10, 20, 30, 40]
steps = 0
found = False

for value in values:
    steps += 1
    if value == 30:
        found = True
        break

print(found)
print(steps)
```

结果：

```text
True
3
```

查找 `30` 扫描了 `3` 个元素。

最坏情况下要扫描整个列表。

所以 list membership 是 O(n)。

如果你频繁判断某个股票是否在资产池里，list 不是最合适的结构。

## dict 的底层直觉

dict 是哈希表。

它保存 key 到 value 的映射。

例如用股票代码查价格：

```python
prices = {
    "AAPL": 190.0,
    "MSFT": 420.0,
}

print(prices["MSFT"])
```

结果：

```text
420.0
```

平均情况下，dict 查找是 O(1)。

原因是 Python 会对 key 计算 hash，并快速定位到对应位置。

## dict 适合查表

策略代码里，dict 很适合做映射：

```text
symbol -> price
symbol -> position
order_id -> order_state
date -> trading_calendar_info
factor_name -> factor_config
```

例如统计符号出现次数：

```python
counts = {}

for symbol in ["A", "B", "A", "C", "B", "A"]:
    counts[symbol] = counts.get(symbol, 0) + 1

print(counts)
```

结果：

```text
{'A': 3, 'B': 2, 'C': 1}
```

每次更新都通过 key 找到当前计数。

平均复杂度接近 O(1)。

## set 的底层直觉

set 也是哈希表思想。

但它只保存 key，不保存对应 value。

set 适合：

```text
去重
快速判断是否存在
集合交并差
```

小例子：

```python
symbols = ["A", "B", "A", "C"]

unique = set(symbols)

print(sorted(unique))
print("B" in unique)
```

结果：

```text
['A', 'B', 'C']
True
```

去重后只剩 `A`、`B`、`C`。

membership 平均是 O(1)。

## list 和 set 的 membership

list 和 set 都能写 `in`。

但代价不同。

```python
list_symbols = ["A", "B", "C"]
set_symbols = {"A", "B", "C"}

print("D" in list_symbols)
print("D" in set_symbols)
```

结果：

```text
False
False
```

输出一样。

但 list 要顺序扫描。

set 通过 hash 查找。

如果资产池有几千只股票，并且每天要检查很多次 membership，set 会更合适。

## zip 到 dict

如果有两个列表，一个是资产，一个是收益，可以转成 dict 方便查表。

```python
assets = ["A", "B", "C"]
returns = [0.01, -0.02, 0.03]

lookup = dict(zip(assets, returns))

print(lookup)
```

结果：

```text
{'A': 0.01, 'B': -0.02, 'C': 0.03}
```

转成 dict 后，可以用 `lookup["B"]` 直接查收益。

如果保持两个列表，就需要先找资产位置，再找对应收益。

## set 集合运算

set 可以高效做交集、差集、并集。

例如当前持仓和可交易资产：

```python
positions = {"A", "B", "C"}
tradable = {"B", "C", "D"}

print(sorted(positions & tradable))
print(sorted(positions - tradable))
```

结果：

```text
['B', 'C']
['A']
```

含义是：

```text
B、C 既持仓又可交易
A 有持仓但当前不可交易
```

这类集合操作在处理资产池、停牌、可交易标记时很常用。

## append 构造结果

循环中构造结果时，list append 是常见写法。

```python
rows = []

for i in range(3):
    rows.append(i * i)

print(rows)
```

结果：

```text
[0, 1, 4]
```

这比反复做列表拼接更好。

例如：

```text
rows = rows + [new_item]
```

这种写法会反复创建新列表，成本更高。

## hashable 限制

dict 的 key 和 set 的元素必须可哈希。

列表是可变对象，不能放进 set。

```python
bad_keys = [["A"], ["B"]]

try:
    set(bad_keys)
except TypeError as exc:
    print(type(exc).__name__)
```

结果：

```text
TypeError
```

如果需要把组合键放进 dict 或 set，常用 tuple。

例如：

```text
(date, symbol)
(account_id, order_id)
(exchange, ticker)
```

tuple 不可变，所以可以作为 key。

## 常见操作代价

可以粗略记成：

```text
list[index]: O(1)
list append: 摊销 O(1)
list insert/delete at front/middle: O(n)
list membership: O(n)

dict get/set/delete by key: 平均 O(1)
dict iteration: O(n)

set add/remove/membership: 平均 O(1)
set union/intersection/difference: 与集合大小相关
```

这里的 O(1) 是平均情况。

哈希冲突、扩容、对象 hash 成本都会影响实际性能。

## 策略代码中的使用取舍

常见选择：

```text
保留顺序、按位置访问 -> list
通过 key 快速查值 -> dict
快速判断是否存在、去重、集合运算 -> set
频繁头部插入或弹出 -> deque
大量数值向量运算 -> numpy / pandas
```

例如：

```text
日内 tick 序列：list 或数组
订单状态表：dict
当前可交易资产池：set
因子名到配置：dict
已处理文件名集合：set
```

## 常见误区

常见错误包括：

```text
用 list 反复做 membership 检查
用 list 头部 insert 模拟队列
用两个平行 list 做查表
不需要顺序却保留大量 list
把可变对象当 dict key
为了去重手写 O(n^2) 循环
```

这些错误小数据看不出来，大数据会很慢。

## 小结

list、dict、set 是 Python 策略代码的基础。

核心记忆：

```text
list: 顺序和位置
dict: key -> value 映射
set: 唯一元素和快速 membership
```

写代码前先问：

```text
我需要保持顺序吗？
我需要按 key 查值吗？
我只是判断存在或去重吗？
我是否频繁在中间插入删除？
```

选对数据结构，通常比事后微优化更有效。

下一篇讨论 SQL 的多表 JOIN 和聚合查询。
