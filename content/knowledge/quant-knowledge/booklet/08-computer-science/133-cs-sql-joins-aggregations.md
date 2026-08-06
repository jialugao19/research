# 133. 计算机基础：SQL 多表 JOIN、聚合查询和行情财务数据提取

## 核心概念

SQL 用来从关系型数据库中查询结构化数据。

量化和数据工程里常见表包括：

```text
行情表 prices
资产信息表 assets
财务表 fundamentals
交易日历表 calendar
行业分类表 industry
组合持仓表 positions
订单成交表 fills
```

SQL 的核心能力包括：

```text
过滤行
选择列
多表 JOIN
分组聚合
排序
窗口函数
```

本篇重点是多表 JOIN 和聚合查询。

## 示例数据

下面用 Python 内置 `sqlite3` 构造一个小数据库。

```python
import sqlite3

conn = sqlite3.connect(":memory:")
cur = conn.cursor()

cur.execute("CREATE TABLE prices (dt TEXT, symbol TEXT, close REAL, volume INTEGER)")
cur.execute("CREATE TABLE assets (symbol TEXT, sector TEXT, listed INTEGER)")
cur.execute("CREATE TABLE fundamentals (symbol TEXT, report_date TEXT, pe REAL)")

cur.executemany("INSERT INTO prices VALUES (?, ?, ?, ?)", [
    ("2026-01-02", "AAA", 10.0, 1000),
    ("2026-01-03", "AAA", 10.5, 1500),
    ("2026-01-02", "BBB", 20.0, 800),
    ("2026-01-03", "BBB", 19.0, 1200),
    ("2026-01-03", "CCC", 5.0, 300),
])
cur.executemany("INSERT INTO assets VALUES (?, ?, ?)", [
    ("AAA", "Tech", 1),
    ("BBB", "Finance", 1),
    ("CCC", "Tech", 0),
])
cur.executemany("INSERT INTO fundamentals VALUES (?, ?, ?)", [
    ("AAA", "2025-12-31", 18.0),
    ("BBB", "2025-12-31", 12.0),
])

rows = cur.execute(
    "SELECT symbol, close FROM prices WHERE dt = '2026-01-03' ORDER BY symbol"
).fetchall()

print(rows)
```

结果：

```text
[('AAA', 10.5), ('BBB', 19.0), ('CCC', 5.0)]
```

后面的例子都基于这三张表。

## SELECT 和 WHERE

最基础的查询是：

```sql
SELECT symbol, close
FROM prices
WHERE dt = '2026-01-03'
ORDER BY symbol;
```

含义是：

```text
从 prices 表中取 2026-01-03 的 symbol 和 close
按 symbol 排序
```

`WHERE` 过滤行。

`SELECT` 选择列。

`ORDER BY` 控制输出顺序。

如果没有 `ORDER BY`，数据库不保证返回顺序。

## INNER JOIN

JOIN 用来把多张表按 key 合并。

例如把行情表和资产信息表按 `symbol` 合并：

```python
rows = cur.execute("""
SELECT p.symbol, p.close, a.sector
FROM prices AS p
JOIN assets AS a
  ON p.symbol = a.symbol
WHERE p.dt = '2026-01-03'
ORDER BY p.symbol
""").fetchall()

print(rows)
```

结果：

```text
[('AAA', 10.5, 'Tech'), ('BBB', 19.0, 'Finance'), ('CCC', 5.0, 'Tech')]
```

这里：

```text
p 是 prices 的别名
a 是 assets 的别名
ON p.symbol = a.symbol 是 JOIN 条件
```

INNER JOIN 只保留两边都匹配到的行。

## LEFT JOIN

LEFT JOIN 保留左表所有行。

右表匹配不到时，用 `NULL`。

例如把行情表和财务表合并：

```python
rows = cur.execute("""
SELECT p.symbol, p.close, f.pe
FROM prices AS p
LEFT JOIN fundamentals AS f
  ON p.symbol = f.symbol
WHERE p.dt = '2026-01-03'
ORDER BY p.symbol
""").fetchall()

print(rows)
```

结果：

```text
[('AAA', 10.5, 18.0), ('BBB', 19.0, 12.0), ('CCC', 5.0, None)]
```

`CCC` 没有财务数据。

LEFT JOIN 仍然保留了 `CCC` 的行情行。

这在金融数据里很重要。

因为缺失财务数据本身可能有含义，不能随便被 INNER JOIN 删除。

## GROUP BY 聚合

GROUP BY 用来按组聚合。

例如按行业计算平均收盘价和总成交量：

```python
rows = cur.execute("""
SELECT a.sector, AVG(p.close) AS avg_close, SUM(p.volume) AS total_volume
FROM prices AS p
JOIN assets AS a
  ON p.symbol = a.symbol
WHERE p.dt = '2026-01-03'
GROUP BY a.sector
ORDER BY a.sector
""").fetchall()

print(rows)
```

结果：

```text
[('Finance', 19.0, 1200), ('Tech', 7.75, 1800)]
```

`AVG` 是平均值。

`SUM` 是求和。

`AS` 给结果列起别名。

## HAVING

`WHERE` 过滤原始行。

`HAVING` 过滤聚合后的组。

例如保留平均收盘价大于 `10` 的股票：

```python
rows = cur.execute("""
SELECT symbol, AVG(close) AS avg_close
FROM prices
GROUP BY symbol
HAVING AVG(close) > 10
ORDER BY symbol
""").fetchall()

print(rows)
```

结果：

```text
[('AAA', 10.25), ('BBB', 19.5)]
```

注意顺序：

```text
先 GROUP BY
再 HAVING
```

如果是过滤日期或股票池，通常用 `WHERE`。

如果是过滤聚合统计量，用 `HAVING`。

## 多表 JOIN

实际查询经常要合并三张以上表。

例如取某日上市股票的收盘价、行业和 PE：

```python
rows = cur.execute("""
SELECT p.dt, p.symbol, p.close, a.sector, f.pe
FROM prices AS p
JOIN assets AS a
  ON p.symbol = a.symbol
LEFT JOIN fundamentals AS f
  ON p.symbol = f.symbol
WHERE p.dt = '2026-01-03'
  AND a.listed = 1
ORDER BY p.symbol
""").fetchall()

print(rows)
```

结果：

```text
[('2026-01-03', 'AAA', 10.5, 'Tech', 18.0), ('2026-01-03', 'BBB', 19.0, 'Finance', 12.0)]
```

`CCC` 被过滤掉，因为 `listed = 0`。

这个查询非常接近真实工作：

```text
取行情
合并资产信息
合并财务数据
过滤可交易资产
```

## 日期范围和资产池

取行情数据时，经常需要日期范围和资产池过滤：

```python
rows = cur.execute("""
SELECT p.symbol, p.dt, p.close
FROM prices AS p
WHERE p.dt BETWEEN '2026-01-02' AND '2026-01-03'
  AND p.symbol IN ('AAA', 'BBB')
ORDER BY p.symbol, p.dt
""").fetchall()

print(rows)
```

结果：

```text
[('AAA', '2026-01-02', 10.0), ('AAA', '2026-01-03', 10.5), ('BBB', '2026-01-02', 20.0), ('BBB', '2026-01-03', 19.0)]
```

常用过滤条件：

```text
BETWEEN: 日期区间
IN: 资产池
=, >, <, >=, <=: 数值过滤
IS NULL / IS NOT NULL: 缺失过滤
```

## 窗口函数

窗口函数可以在不压缩行数的情况下做分组计算。

例如按股票取上一日收盘价：

```python
rows = cur.execute("""
SELECT symbol, dt, close,
       LAG(close) OVER (PARTITION BY symbol ORDER BY dt) AS prev_close
FROM prices
WHERE symbol IN ('AAA', 'BBB')
ORDER BY symbol, dt
""").fetchall()

print(rows)
```

结果：

```text
[('AAA', '2026-01-02', 10.0, None), ('AAA', '2026-01-03', 10.5, 10.0), ('BBB', '2026-01-02', 20.0, None), ('BBB', '2026-01-03', 19.0, 20.0)]
```

`PARTITION BY symbol` 表示每只股票内部计算。

`ORDER BY dt` 表示按日期排序。

`LAG(close)` 表示上一行的 close。

这类写法常用于计算收益、滞后特征和环比变化。

## COUNT 检查数据完整性

查询前后要检查行数。

例如每只股票有几行行情：

```python
rows = cur.execute("""
SELECT symbol, COUNT(*) AS n_rows
FROM prices
GROUP BY symbol
ORDER BY n_rows DESC, symbol
""").fetchall()

print(rows)
```

结果：

```text
[('AAA', 2), ('BBB', 2), ('CCC', 1)]
```

行数检查可以发现：

```text
缺日期
重复行
JOIN 后行数膨胀
资产池过滤错误
```

多表 JOIN 后尤其要检查行数。

如果右表同一个 key 有多行，JOIN 可能把左表行数放大。

## JOIN 常见坑

JOIN 常见错误包括：

```text
忘记 ON 条件，产生笛卡尔积
JOIN key 不唯一，导致行数膨胀
INNER JOIN 不小心删掉缺失数据
日期 key 类型不一致
财务数据没有按公告日对齐
行业分类使用了未来版本
```

金融数据尤其要注意时间。

例如财务表里有 `report_date`，但真正可用日期应该是公告日或数据供应商发布时间。

不能只按报表期末日期 JOIN。

## 性能和索引

真实数据库里，查询速度取决于表大小、过滤条件和索引。

常用索引包括：

```text
(symbol, dt)
(dt, symbol)
report_date
industry_code
```

对于行情表，常见访问模式是：

```text
按日期取全市场
按股票取一段历史
按日期和股票池取子集
```

索引应该服务这些访问模式。

否则大表查询会退化成全表扫描。

## 回测中的防泄露

SQL 查询也会制造前视偏差。

常见风险：

```text
用未来成分股列表过滤历史资产池
用最新行业分类 JOIN 历史数据
用全历史财务表直接 JOIN 到过去日期
用未来复权因子修正过去价格但没有说明口径
把退市资产从历史样本中删掉
```

正确做法是：

```text
所有表都带有效日期或可用日期
查询时按回测时点过滤可见数据
JOIN 后检查行数和缺失
```

## 小结

SQL 是从数据库提取行情、财务和资产信息的基础工具。

需要掌握：

```text
SELECT / WHERE / ORDER BY
INNER JOIN / LEFT JOIN
GROUP BY / HAVING
SUM / AVG / COUNT
日期范围和资产池过滤
窗口函数 LAG
JOIN 后行数检查
索引和查询性能
时间对齐与防泄露
```

下一篇讨论 Linux 命令行基本操作。
