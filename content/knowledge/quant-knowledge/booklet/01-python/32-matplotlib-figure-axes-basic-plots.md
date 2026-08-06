# matplotlib：Figure / Axes 与基础 line、scatter、bar 图

## 核心概念

matplotlib 的核心对象是：

- `Figure`：整张画布。
- `Axes`：画布上的一个坐标系，也就是通常说的一张子图。

推荐使用面向对象写法：

```python
fig, ax = plt.subplots()
ax.plot(...)
```

而不是到处使用全局状态式写法：

```python
plt.plot(...)
```

面向对象写法更适合复杂图、多子图、报告导出和可复现绘图。

## 准备环境

```python
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")  # 无图形界面环境中也能保存图片

import matplotlib.pyplot as plt
```

`Agg` 是非交互式后端，适合脚本、服务器和自动化测试。平时在 notebook 或本地桌面环境中，不一定需要手动设置后端。

## Figure 和 Axes

创建一张图：

```python
fig, ax = plt.subplots(figsize=(6, 4))

print(type(fig))
print(type(ax))
print(fig.axes)

plt.close(fig)
```

`figsize=(6, 4)` 表示画布宽 6 英寸、高 4 英寸。

一个 `Figure` 可以包含多个 `Axes`。本节先只讲单个 Axes。

## line 图：plot

line 图适合展示有顺序的变量，例如时间序列、训练损失、累计收益。

```python
dates = pd.date_range("2024-01-01", periods=6, freq="D")
nav = pd.Series([1.00, 1.01, 1.03, 1.02, 1.05, 1.07], index=dates, name="nav")

fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav.values)

ax.set_title("Net Asset Value")
ax.set_xlabel("Date")
ax.set_ylabel("NAV")

fig.tight_layout()

plt.close(fig)
```

最重要的是看清楚：

- x 轴传日期。
- y 轴传数值。
- `ax.plot(...)` 在当前 Axes 上添加一条线。

## 多条 line

同一个 Axes 上可以画多条线。

```python
portfolio = pd.DataFrame({
    "strategy": [1.00, 1.01, 1.03, 1.02, 1.05, 1.07],
    "benchmark": [1.00, 1.005, 1.015, 1.020, 1.030, 1.040],
}, index=dates)

fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(portfolio.index, portfolio["strategy"], label="strategy")
ax.plot(portfolio.index, portfolio["benchmark"], label="benchmark")

ax.set_title("Strategy vs Benchmark")
ax.set_xlabel("Date")
ax.set_ylabel("NAV")
ax.legend()

fig.tight_layout()

plt.close(fig)
```

`label` 配合 `ax.legend()` 显示图例。图例和样式细节会在下一节展开。

## scatter 图：scatter

scatter 图适合展示两个数值变量之间的关系。

```python
factor = pd.DataFrame({
    "value_score": [-1.2, -0.7, -0.3, 0.2, 0.5, 0.9, 1.3, 1.8],
    "future_return": [-0.030, -0.015, -0.010, 0.004, 0.009, 0.018, 0.025, 0.036],
})

fig, ax = plt.subplots(figsize=(5, 4))

ax.scatter(factor["value_score"], factor["future_return"])

ax.set_title("Factor vs Future Return")
ax.set_xlabel("Value score")
ax.set_ylabel("Future return")

fig.tight_layout()

plt.close(fig)
```

scatter 图不要求 x 轴有顺序。它更关注点云形态、离群点和相关关系。

## scatter 的颜色和大小

可以用颜色或点大小编码第三个变量。

```python
factor["volatility"] = [0.35, 0.32, 0.30, 0.26, 0.24, 0.21, 0.18, 0.16]

fig, ax = plt.subplots(figsize=(5, 4))

points = ax.scatter(
    factor["value_score"],
    factor["future_return"],
    c=factor["volatility"],
    s=80,
)

fig.colorbar(points, ax=ax, label="Volatility")

ax.set_title("Factor, Return and Volatility")
ax.set_xlabel("Value score")
ax.set_ylabel("Future return")

fig.tight_layout()

plt.close(fig)
```

`c=` 控制颜色，`s=` 控制点大小。颜色条由 `fig.colorbar(...)` 添加。

## bar 图：bar

bar 图适合比较离散类别的数值，例如行业收益、模型指标、分组均值。

```python
industry_return = pd.Series(
    {
        "tech": 0.035,
        "finance": 0.012,
        "energy": -0.008,
        "health": 0.021,
    },
    name="return",
)

fig, ax = plt.subplots(figsize=(6, 4))

ax.bar(industry_return.index, industry_return.values)

ax.set_title("Industry Return")
ax.set_xlabel("Industry")
ax.set_ylabel("Return")

fig.tight_layout()

plt.close(fig)
```

bar 图的 x 轴通常是类别，y 轴是数值。

## 水平 bar：barh

当类别名称较长，或想按数值排序时，水平 bar 更清楚。

```python
sorted_return = industry_return.sort_values()

fig, ax = plt.subplots(figsize=(6, 4))

ax.barh(sorted_return.index, sorted_return.values)

ax.set_title("Industry Return Sorted")
ax.set_xlabel("Return")
ax.set_ylabel("Industry")

fig.tight_layout()

plt.close(fig)
```

`barh` 的第一个参数是 y 轴类别，第二个参数是 x 轴数值。

## pandas 数据和 matplotlib

pandas 的 index 和列名可以直接提供给 matplotlib。

```python
returns = pd.DataFrame({
    "strategy": [0.010, 0.020, -0.010, 0.030, 0.015],
    "benchmark": [0.006, 0.012, -0.004, 0.018, 0.010],
}, index=pd.date_range("2024-01-01", periods=5, freq="D"))

cum = (1.0 + returns).cumprod()

fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(cum.index, cum["strategy"])
ax.plot(cum.index, cum["benchmark"])

ax.set_title("Cumulative Return")
ax.set_xlabel("Date")
ax.set_ylabel("Cumulative NAV")

fig.tight_layout()

plt.close(fig)
```

matplotlib 不会替你理解数据语义。你仍然要决定 index、columns 和单位应该如何映射到 x 轴、y 轴、颜色、大小或分面。

## 保存图片

本节只讲最小保存方式，导出规范后续单独展开。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav.values)
ax.set_title("Net Asset Value")

fig.tight_layout()
fig.savefig("nav_example.png", dpi=150)

plt.close(fig)
```

脚本里建议保存后关闭 figure，避免批量画图时占用内存。

```python
plt.close(fig)
```

## 为什么要 close figure

如果循环生成很多图，不关闭 figure 会不断占用内存。

```python
for i in range(3):
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [i, i + 1, i + 2])
    plt.close(fig)
```

在 notebook 中问题不明显，在脚本或服务中会更明显。养成 `plt.close(fig)` 的习惯更稳。

## 常见坑

第一，混用 `plt.plot` 和 `ax.plot` 导致画到错误的图上。

推荐在同一段代码里统一使用面向对象写法：

```python
fig, ax = plt.subplots()
ax.plot([1, 2, 3], [1, 4, 9])
plt.close(fig)
```

第二，忘记 `fig.tight_layout()`，导致标题、坐标轴文字被挤出画布。

```python
fig.tight_layout()
```

第三，bar 图类别太多。

类别太多时，bar 图会变得难读。可以排序后只画 top N，或者使用水平 bar。

第四，scatter 点太多重叠。

点很多时可以降低透明度、抽样、使用 hexbin 或密度图。后续诊断图小节会再展开。

第五，画完大量图不关闭。

批量生成图时应 `plt.close(fig)`。

## 实战提示

一个最小但清楚的绘图模板：

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav.values)

ax.set_title("Net Asset Value")
ax.set_xlabel("Date")
ax.set_ylabel("NAV")

fig.tight_layout()
fig.savefig("nav.png", dpi=150)

plt.close(fig)
```

画图前先问：

1. x 轴是什么？
2. y 轴是什么？
3. 数据是有序序列、点云关系，还是类别比较？
4. 图要展示给谁看？
5. 是否需要保存为文件？

根据答案选择：

- 有序序列：line。
- 两个连续变量关系：scatter。
- 类别数值比较：bar 或 barh。

## 小结

matplotlib 的基础绘图可以先掌握：

- `fig, ax = plt.subplots()` 创建 Figure 和 Axes。
- `ax.plot` 画 line。
- `ax.scatter` 画 scatter。
- `ax.bar` / `ax.barh` 画 bar。
- `ax.set_title`、`ax.set_xlabel`、`ax.set_ylabel` 添加基础文字。
- `fig.tight_layout()` 调整布局。
- `fig.savefig(...)` 保存图片。
- `plt.close(fig)` 释放 figure。

后续小节会继续展开标题、坐标轴、图例、颜色、样式和多子图布局。

## 自检问题

1. `Figure` 和 `Axes` 分别代表什么？
2. 为什么推荐使用 `fig, ax = plt.subplots()` 和 `ax.plot(...)`？
3. line、scatter、bar 分别适合什么类型的数据关系？
4. 为什么脚本里批量画图后要 `plt.close(fig)`？
5. `fig.tight_layout()` 主要解决什么问题？
