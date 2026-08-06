# matplotlib：时间序列图、双轴图与 pandas 绘图互操作

## 核心概念

金融、实验监控和业务指标里，大量图都是时间序列图。时间序列绘图的关键不只是把线画出来，还要处理：

- x 轴是否是真正的日期时间索引。
- 日期刻度是否可读。
- 多个面板是否共享同一个时间轴。
- 是否需要标注事件区间。
- 不同量纲是否应该放在同一张图里。
- pandas 的 `.plot(...)` 如何和 matplotlib 的 `Figure` / `Axes` 配合。

本节聚焦四类常见任务：

- 用 `DatetimeIndex` 画 line 图。
- 用共享 x 轴画净值和回撤。
- 用 `ax.twinx()` 画双 y 轴图。
- 用 pandas `.plot(ax=...)` 复用 matplotlib 的布局和样式。

## 准备环境

```python
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.dates as mdates
import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
```

准备一组时间序列数据：

```python
rng = np.random.default_rng(7)

dates = pd.bdate_range("2024-01-02", periods=80)

returns = pd.DataFrame(
    rng.normal(
        loc=[0.0008, 0.0005],
        scale=[0.012, 0.010],
        size=(len(dates), 2),
    ),
    index=dates,
    columns=["strategy", "benchmark"],
)

nav = (1.0 + returns).cumprod()
drawdown = nav / nav.cummax() - 1.0

volume = pd.Series(
    rng.integers(80_000, 180_000, size=len(dates)),
    index=dates,
    name="volume",
)

turnover = pd.Series(
    rng.uniform(0.05, 0.35, size=len(dates)),
    index=dates,
    name="turnover",
)

events = pd.DataFrame(
    {
        "start": [pd.Timestamp("2024-02-12"), pd.Timestamp("2024-03-18")],
        "end": [pd.Timestamp("2024-02-20"), pd.Timestamp("2024-03-25")],
        "label": ["rebalance", "risk review"],
    }
)
```

`pd.bdate_range` 生成工作日索引，更接近交易日数据。真实交易日还要考虑节假日，本节先聚焦绘图。

## DatetimeIndex 基础折线图

只要 x 轴传入日期，matplotlib 就能识别并绘制时间序列。

```python
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(nav.index, nav["strategy"], label="strategy")
ax.plot(nav.index, nav["benchmark"], label="benchmark")

ax.set_title("Strategy vs Benchmark NAV")
ax.set_xlabel("Date")
ax.set_ylabel("NAV")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

这里的重点是：`nav.index` 是 `DatetimeIndex`，y 轴是数值列。不要把日期先转成字符串再画，否则日期排序、间隔和刻度格式都会变差。

## 日期刻度格式

默认日期刻度有时太密或太长。可以使用 `matplotlib.dates` 控制刻度定位和显示格式。

```python
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(nav.index, nav["strategy"], label="strategy")

locator = mdates.AutoDateLocator()
formatter = mdates.ConciseDateFormatter(locator)

ax.xaxis.set_major_locator(locator)
ax.xaxis.set_major_formatter(formatter)

ax.set_title("NAV with Concise Date Ticks")
ax.set_ylabel("NAV")

fig.tight_layout()
plt.close(fig)
```

`AutoDateLocator` 会根据时间跨度自动选择合适的刻度间隔，`ConciseDateFormatter` 会压缩重复的年月信息。

## 旋转日期标签

如果日期标签仍然拥挤，可以旋转 x 轴标签。

```python
fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(nav.index, nav["strategy"])
ax.set_title("Rotated Date Labels")
ax.set_ylabel("NAV")

ax.tick_params(axis="x", rotation=30)

fig.tight_layout()
plt.close(fig)
```

日期图通常优先使用合适的 locator 和 formatter；旋转标签是补充手段，不是唯一手段。

## 移动平均线

时间序列图常叠加滚动均值，用来观察趋势。

```python
rolling_mean = nav["strategy"].rolling(window=10, min_periods=1).mean()

fig, ax = plt.subplots(figsize=(8, 4))

ax.plot(nav.index, nav["strategy"], label="strategy", alpha=0.65)
ax.plot(rolling_mean.index, rolling_mean, label="10-day mean", linewidth=2)

ax.set_title("NAV and Rolling Mean")
ax.set_ylabel("NAV")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

滚动均值只适合辅助观察。建模时要注意窗口方向，不能用未来数据平滑过去。

## 净值和回撤：共享 x 轴

净值和回撤通常是同一个时间轴上的两个视角，适合上下排列并共享 x 轴。

```python
fig, axes = plt.subplots(
    2,
    1,
    figsize=(9, 6),
    sharex=True,
    constrained_layout=True,
)

axes[0].plot(nav.index, nav["strategy"], label="strategy")
axes[0].plot(nav.index, nav["benchmark"], label="benchmark")
axes[0].set_title("NAV")
axes[0].set_ylabel("NAV")
axes[0].legend()

axes[1].plot(drawdown.index, drawdown["strategy"], color="tab:red")
axes[1].fill_between(
    drawdown.index,
    drawdown["strategy"],
    0.0,
    color="tab:red",
    alpha=0.25,
)
axes[1].set_title("Strategy Drawdown")
axes[1].set_ylabel("Drawdown")
axes[1].yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

fig.suptitle("Strategy Diagnostics")

plt.close(fig)
```

`sharex=True` 能保证两个面板的时间范围一致。读者可以直接对齐某一天的净值和回撤。

## 事件线和事件区间

时间序列常需要标注调仓、上线、风控或异常事件。

```python
fig, ax = plt.subplots(figsize=(9, 4))

ax.plot(nav.index, nav["strategy"], label="strategy")

for _, event in events.iterrows():
    ax.axvspan(event["start"], event["end"], color="tab:orange", alpha=0.18)
    ax.axvline(event["start"], color="tab:orange", linewidth=1, linestyle="--")

ax.set_title("NAV with Event Windows")
ax.set_ylabel("NAV")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

`axvline` 标注某个时间点，`axvspan` 标注一段时间。事件标注要克制，太多会压过数据本身。

## 双 y 轴：twinx

当两个序列共享同一个 x 轴，但量纲完全不同时，可以使用双 y 轴。

```python
fig, ax_left = plt.subplots(figsize=(9, 4))

line_nav, = ax_left.plot(
    nav.index,
    nav["strategy"],
    color="tab:blue",
    label="NAV",
)
ax_left.set_ylabel("NAV", color="tab:blue")
ax_left.tick_params(axis="y", labelcolor="tab:blue")

ax_right = ax_left.twinx()
line_volume, = ax_right.plot(
    volume.index,
    volume,
    color="tab:green",
    alpha=0.65,
    label="volume",
)
ax_right.set_ylabel("Volume", color="tab:green")
ax_right.tick_params(axis="y", labelcolor="tab:green")

ax_left.set_title("NAV and Volume")
ax_left.legend(handles=[line_nav, line_volume], loc="upper left")

fig.tight_layout()
plt.close(fig)
```

`twinx()` 会创建一个共享 x 轴的新 Axes。双轴图容易误导，所以要让左右 y 轴颜色与线条颜色一致，并清楚标注单位。

## 双轴图的替代方案

如果双轴图让关系看起来过于强，可以改用上下两个共享 x 轴的面板。

```python
fig, axes = plt.subplots(
    2,
    1,
    figsize=(9, 5),
    sharex=True,
    constrained_layout=True,
)

axes[0].plot(nav.index, nav["strategy"], color="tab:blue")
axes[0].set_title("NAV")
axes[0].set_ylabel("NAV")

axes[1].bar(volume.index, volume, color="tab:green", alpha=0.65)
axes[1].set_title("Volume")
axes[1].set_ylabel("Shares")

plt.close(fig)
```

报告里如果重点是比较两个序列的时间位置，上下共享 x 轴通常比双 y 轴更稳妥。

## pandas Series.plot

pandas 的 `.plot(...)` 是 matplotlib 的封装。它会返回一个 Axes，可以继续用 matplotlib 设置标题、坐标轴和格式。

```python
fig, ax = plt.subplots(figsize=(8, 4))

nav["strategy"].plot(ax=ax, label="strategy")
nav["benchmark"].plot(ax=ax, label="benchmark")

ax.set_title("Pandas Series.plot on Matplotlib Axes")
ax.set_ylabel("NAV")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

这适合快速画 pandas 对象，同时保留 matplotlib 的精细控制。

## pandas DataFrame.plot

DataFrame 的 `.plot(...)` 默认会把多个数值列画在同一个 Axes 上。

```python
fig, ax = plt.subplots(figsize=(8, 4))

nav.plot(ax=ax)

ax.set_title("DataFrame.plot")
ax.set_ylabel("NAV")

fig.tight_layout()
plt.close(fig)
```

如果不传 `ax`，pandas 会自己创建 Figure。为了统一布局、标题和导出，建议显式传入已有 Axes。

## pandas subplots=True

pandas 也可以一次画多个子图。

```python
axes = nav.plot(
    subplots=True,
    figsize=(8, 5),
    sharex=True,
    legend=False,
)

fig = axes[0].figure
axes[0].set_title("Strategy NAV")
axes[1].set_title("Benchmark NAV")

fig.tight_layout()
plt.close(fig)
```

`subplots=True` 返回 Axes 数组。后续仍然可以用 `axes[0]`、`axes[1]` 修改每个面板。

## pandas secondary_y

pandas 也支持通过 `secondary_y` 创建右侧 y 轴。

```python
plot_data = pd.DataFrame({
    "nav": nav["strategy"],
    "turnover": turnover,
})

fig, ax = plt.subplots(figsize=(9, 4))

plot_data.plot(
    ax=ax,
    secondary_y=["turnover"],
    mark_right=False,
)

ax.set_title("NAV and Turnover")
ax.set_ylabel("NAV")
ax.right_ax.set_ylabel("Turnover")
ax.right_ax.yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

fig.tight_layout()
plt.close(fig)
```

`secondary_y` 的底层也是创建第二个 Axes。它适合快速探索；正式报告里仍然要检查左右轴标签、颜色和图例是否清楚。

## 常见坑

第一，把日期转成字符串再画。

字符串日期看起来像日期，但 matplotlib 不知道它们是真正的时间。优先保留 `DatetimeIndex` 或 `Timestamp`。

第二，时间索引没有排序。

line 图会按数据顺序连线，不会自动按日期排序。绘图前可以使用 `sort_index()`。

第三，双 y 轴暗示不存在的关系。

左右 y 轴缩放方式不同，线条形状可能看起来“同步”，但这不代表统计关系。双轴图必须清楚标注单位，并尽量只用于辅助展示。

第四，pandas 自动创建 Figure 后难以统一排版。

如果要放进报告或多图布局，先用 `plt.subplots(...)` 创建 Figure 和 Axes，再把 `ax=ax` 传给 pandas。

第五，滚动均线被误用为建模特征。

画图时的滚动均线可以辅助观察趋势；建模时必须确认窗口只使用当前和过去数据，不能混入未来。

## 实战提示

时间序列图可以按这个顺序检查：

1. 索引是否是 `DatetimeIndex`。
2. 索引是否单调递增。
3. 是否有缺失日期或不规则间隔。
4. 多个面板是否应该 `sharex=True`。
5. y 轴是否是百分比、净值、价格、数量等明确单位。
6. 双 y 轴是否真的必要。
7. pandas `.plot(...)` 是否传入了明确的 `ax`。

一个实用模板：

```python
def plot_nav_drawdown(nav_data):
    nav_data = nav_data.sort_index()
    dd = nav_data / nav_data.cummax() - 1.0

    fig, axes = plt.subplots(
        2,
        1,
        figsize=(9, 6),
        sharex=True,
        constrained_layout=True,
    )

    nav_data.plot(ax=axes[0])
    axes[0].set_title("NAV")
    axes[0].set_ylabel("NAV")

    dd.plot(ax=axes[1], legend=False)
    axes[1].set_title("Drawdown")
    axes[1].set_ylabel("Drawdown")
    axes[1].yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

    return fig, axes


fig, axes = plot_nav_drawdown(nav)
plt.close(fig)
```

这个模板把数据排序、回撤计算、共享 x 轴和百分比刻度放在一起，适合作为策略诊断图的起点。

## 小结

本节的重点：

- 时间序列图应保留 `DatetimeIndex`，不要把日期转成字符串。
- `AutoDateLocator` 和 `ConciseDateFormatter` 可以改善日期刻度。
- 净值和回撤适合上下排列并 `sharex=True`。
- `axvline` 和 `axvspan` 可以标注事件点和事件区间。
- `ax.twinx()` 可以创建双 y 轴，但要谨慎使用。
- pandas `.plot(ax=...)` 可以复用 matplotlib 的 Figure / Axes。
- pandas 的 `secondary_y` 是快速双轴图工具，正式使用时要检查标签和图例。

## 自检问题

1. 为什么不建议把日期先转成字符串再画时间序列图？
2. `sharex=True` 对净值和回撤图有什么好处？
3. 双 y 轴图为什么容易误导？怎样降低误导？
4. pandas `.plot(ax=ax)` 相比不传 `ax` 有什么优势？
5. `axvline` 和 `axvspan` 分别适合标注什么？
