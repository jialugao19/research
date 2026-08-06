# 33. matplotlib：标题、坐标轴、图例、颜色和样式

## 核心概念

图形不是只把线画出来就结束。可读的图至少要回答：

- 这张图讲什么？
- x 轴和 y 轴分别是什么？
- 单位是什么？
- 多条线或多组点分别代表什么？
- 颜色、线型、marker 的含义是什么？
- 坐标轴范围和刻度是否容易读？

本节聚焦 matplotlib 中最常用的可读性组件：

- 标题：`ax.set_title`
- 坐标轴标签：`ax.set_xlabel`、`ax.set_ylabel`
- 坐标轴范围：`ax.set_xlim`、`ax.set_ylim`
- 刻度和刻度标签：`set_xticks`、`set_xticklabels`、formatter
- 图例：`label` + `ax.legend`
- 颜色、线型、marker、透明度
- 网格和样式上下文

## 准备环境

```python
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import FuncFormatter, PercentFormatter
```

准备一组净值和收益数据：

```python
dates = pd.date_range("2024-01-01", periods=8, freq="D")

nav = pd.DataFrame({
    "strategy": [1.00, 1.01, 1.03, 1.02, 1.05, 1.06, 1.08, 1.10],
    "benchmark": [1.00, 1.005, 1.015, 1.020, 1.030, 1.035, 1.045, 1.055],
}, index=dates)

industry_return = pd.Series({
    "tech": 0.035,
    "finance": 0.012,
    "energy": -0.008,
    "health": 0.021,
})
```

## 标题和坐标轴标签

标题和坐标轴标签是最基本的信息。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"])

ax.set_title("Strategy Net Asset Value")
ax.set_xlabel("Date")
ax.set_ylabel("NAV")

fig.tight_layout()
plt.close(fig)
```

标题应该说明图在展示什么；坐标轴标签应该说明变量和单位。

如果 y 轴是百分比，不要只写 `Return`，最好写清楚：

```python
ax.set_ylabel("Return")
```

后面会配合百分比刻度格式化。

## 标题位置和字体大小

`set_title` 可以设置字体大小、粗细和位置。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"])

ax.set_title(
    "Strategy NAV",
    fontsize=13,
    fontweight="bold",
    loc="left",
)

fig.tight_layout()
plt.close(fig)
```

`loc="left"` 常用于报告图，让标题与绘图区左边对齐。

不要在一张小图里使用过大的标题字号。图是为了展示数据，不是展示标题。

## 坐标轴范围

可以用 `set_xlim` 和 `set_ylim` 控制范围。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"])

ax.set_ylim(0.98, 1.12)
ax.set_title("Strategy NAV with Fixed Y Range")
ax.set_ylabel("NAV")

fig.tight_layout()
plt.close(fig)
```

坐标轴范围会影响读者感知。过窄会夸大波动，过宽会掩盖变化。报告中比较多张图时，统一 y 轴范围通常更公平。

## 百分比刻度

收益率经常需要显示为百分比。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.bar(industry_return.index, industry_return.values)

ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))

ax.set_title("Industry Return")
ax.set_ylabel("Return")

fig.tight_layout()
plt.close(fig)
```

`PercentFormatter(xmax=1.0, decimals=1)` 表示数据 `0.035` 显示为 `3.5%`。

如果你的数据已经是 `3.5` 表示 3.5%，就应该使用 `xmax=100`。

## 自定义刻度格式

也可以用 `FuncFormatter` 自定义格式。

```python
fig, ax = plt.subplots(figsize=(6, 4))

market_cap = pd.Series({
    "AAA": 12_000_000_000,
    "BBB": 8_500_000_000,
    "CCC": 3_200_000_000,
})

ax.bar(market_cap.index, market_cap.values)

def billions(x, pos):
    return f"{x / 1e9:.1f}B"

ax.yaxis.set_major_formatter(FuncFormatter(billions))

ax.set_title("Market Cap")
ax.set_ylabel("USD")

fig.tight_layout()
plt.close(fig)
```

formatter 的作用是改变显示方式，不改变原始数据。

## 类别刻度旋转

类别名较长时，可以旋转 x 轴刻度标签。

```python
long_names = pd.Series({
    "information technology": 0.035,
    "financial services": 0.012,
    "consumer discretionary": 0.018,
    "health care": 0.021,
})

fig, ax = plt.subplots(figsize=(7, 4))

ax.bar(long_names.index, long_names.values)

ax.tick_params(axis="x", rotation=30)
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))

ax.set_title("Sector Return")
ax.set_ylabel("Return")

fig.tight_layout()
plt.close(fig)
```

如果旋转后仍然拥挤，水平 bar 通常更好。

## 图例：legend

图例来自每个图元的 `label`。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"], label="Strategy")
ax.plot(nav.index, nav["benchmark"], label="Benchmark")

ax.set_title("Strategy vs Benchmark")
ax.set_ylabel("NAV")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

如果没有设置 `label`，`legend` 不知道应该显示什么。

## 图例位置和标题

图例可以设置位置、列数、标题和边框。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"], label="Strategy")
ax.plot(nav.index, nav["benchmark"], label="Benchmark")

legend = ax.legend(
    loc="upper left",
    title="Series",
    frameon=False,
)

ax.set_title("Strategy vs Benchmark")
ax.set_ylabel("NAV")

fig.tight_layout()
plt.close(fig)
```

图例不要遮挡关键数据。如果图内放不下，可以放到图外，但多图布局会在下一节展开。

## 颜色

matplotlib 支持多种颜色写法：

- 命名颜色：`"black"`、`"red"`。
- tab 调色板：`"tab:blue"`、`"tab:orange"`。
- 十六进制：`"#1f77b4"`。
- 灰度字符串：`"0.3"`。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"], color="tab:blue", label="Strategy")
ax.plot(nav.index, nav["benchmark"], color="tab:orange", label="Benchmark")

ax.legend()
ax.set_title("Color Example")

fig.tight_layout()
plt.close(fig)
```

颜色应该服务于区分信息，不要使用太多颜色。报告图里通常 2-5 种主色就够。

## 线型和 marker

同一张图里，除了颜色，也可以用线型和 marker 区分系列。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(
    nav.index,
    nav["strategy"],
    color="tab:blue",
    linestyle="-",
    marker="o",
    label="Strategy",
)
ax.plot(
    nav.index,
    nav["benchmark"],
    color="tab:orange",
    linestyle="--",
    marker="s",
    label="Benchmark",
)

ax.legend()
ax.set_title("Line Style and Marker")

fig.tight_layout()
plt.close(fig)
```

常见线型：

- `"-"`：实线。
- `"--"`：虚线。
- `":"`：点线。
- `"-."`：点划线。

marker 适合样本点不太多的序列。点太多时 marker 会让图变脏。

## 透明度 alpha

`alpha` 控制透明度，范围从 0 到 1。

```python
rng = np.random.default_rng(42)

x = rng.normal(size=100)
y = 0.5 * x + rng.normal(scale=0.5, size=100)

fig, ax = plt.subplots(figsize=(5, 4))

ax.scatter(x, y, alpha=0.5, color="tab:blue")

ax.set_title("Scatter with Alpha")
ax.set_xlabel("x")
ax.set_ylabel("y")

fig.tight_layout()
plt.close(fig)
```

点很多时，透明度可以缓解重叠问题。

## 网格

网格可以帮助读数，但不要太重。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"], color="tab:blue")

ax.grid(True, axis="y", linestyle="--", alpha=0.3)

ax.set_title("NAV with Grid")
ax.set_ylabel("NAV")

fig.tight_layout()
plt.close(fig)
```

常见做法是只开 y 轴网格，让读者更容易比较数值，同时不干扰 x 轴。

## 参考线

参考线可以突出基准值，例如 0 收益。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.bar(industry_return.index, industry_return.values, color="tab:blue")
ax.axhline(0.0, color="black", linewidth=1)

ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
ax.set_title("Industry Return with Zero Line")
ax.set_ylabel("Return")

fig.tight_layout()
plt.close(fig)
```

`axhline` 画水平线，`axvline` 画垂直线。

## 注释 annotation

可以用 `annotate` 标注重点。

```python
best_date = nav["strategy"].idxmax()
best_value = nav["strategy"].max()

fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"], color="tab:blue")

ax.annotate(
    "High",
    xy=(best_date, best_value),
    xytext=(best_date, best_value + 0.02),
    arrowprops={"arrowstyle": "->", "color": "0.3"},
)

ax.set_title("Strategy NAV with Annotation")
ax.set_ylabel("NAV")

fig.tight_layout()
plt.close(fig)
```

注释应该少而准。过多注释会让图变得难读。

## 样式上下文

matplotlib 有内置样式，可以用 `plt.style.context` 临时启用。

```python
with plt.style.context("ggplot"):
    fig, ax = plt.subplots(figsize=(6, 4))
    ax.plot(nav.index, nav["strategy"], label="Strategy")
    ax.plot(nav.index, nav["benchmark"], label="Benchmark")
    ax.legend()
    ax.set_title("Temporary Style")
    fig.tight_layout()
    plt.close(fig)
```

`style.context` 只在 `with` 代码块内生效，适合局部改变风格。不要在共享代码里随意全局修改样式，容易影响其他图。

## rcParams：全局默认值

`plt.rcParams` 可以修改全局默认样式。

```python
old_title_size = plt.rcParams["axes.titlesize"]

plt.rcParams["axes.titlesize"] = 12

fig, ax = plt.subplots()
ax.plot([0, 1], [0, 1])
ax.set_title("rcParams Example")
plt.close(fig)

plt.rcParams["axes.titlesize"] = old_title_size
```

如果修改全局参数，最好保存旧值并恢复，避免影响后续图。

## 常见坑

第一，没有坐标轴单位。

`Return`、`NAV`、`Market cap` 这类标签应尽量说明单位或比例含义。

第二，图例遮挡数据。

可以调整 `loc`，或让图例放到图外。多图布局会在后续小节展开。

第三，颜色太多或含义不一致。

同一份报告里，颜色含义最好保持一致。例如策略始终蓝色、基准始终橙色。

第四，百分比刻度和数据单位不匹配。

如果数据是 `0.05`，使用 `PercentFormatter(xmax=1.0)`；如果数据是 `5`，使用 `xmax=100`。需要固定小数位时，显式设置 `decimals`。

第五，全局 rcParams 修改后不恢复。

这会让后面的图出现难以追踪的样式变化。局部样式优先使用 `plt.style.context`。

## 实战提示

报告图的最小可读性清单：

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav["strategy"], color="tab:blue", label="Strategy")
ax.plot(nav.index, nav["benchmark"], color="tab:orange", label="Benchmark")

ax.set_title("Strategy vs Benchmark", loc="left")
ax.set_xlabel("Date")
ax.set_ylabel("NAV")
ax.legend(frameon=False)
ax.grid(True, axis="y", linestyle="--", alpha=0.3)

fig.tight_layout()
plt.close(fig)
```

如果是收益率图：

```python
ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0, decimals=1))
ax.axhline(0.0, color="black", linewidth=1)
```

写图形代码时，建议把“数据映射到视觉元素”的关系写清楚：

- x 轴映射什么。
- y 轴映射什么。
- 颜色代表什么。
- 线型或 marker 代表什么。
- 图例是否解释了所有视觉编码。

## 小结

图形可读性主要靠这些组件：

- 标题说明主题。
- 坐标轴标签说明变量和单位。
- 刻度格式让数值容易读。
- 图例解释颜色、线型和 marker。
- 颜色和样式保持克制且一致。
- 网格和参考线辅助读数。
- 注释突出少数关键点。
- 样式上下文避免全局副作用。

这些细节不会改变数据，但会显著影响读者是否能正确理解图。

## 自检问题

1. 为什么坐标轴标签最好包含单位或比例含义？
2. `PercentFormatter(xmax=1.0)` 适合什么样的数据？
3. `label` 和 `ax.legend()` 之间是什么关系？
4. 什么时候应该用透明度 `alpha`？
5. 为什么不建议随意长期修改全局 `rcParams`？
