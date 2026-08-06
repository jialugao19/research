# 34. matplotlib：subplots、多图布局与共享坐标轴

## 核心概念

当你想在一张图里比较多个视角时，就需要多子图布局。

常见场景：

- 同时展示策略净值、回撤、成交量。
- 比较多个模型的指标。
- 分行业、分资产、分参数画多张小图。
- 左边画主图，右边画分布或解释图。

matplotlib 里常用工具：

- `plt.subplots(nrows, ncols)`：创建规则网格。
- `sharex` / `sharey`：共享坐标轴。
- `fig.suptitle`：整张 Figure 的标题。
- `fig.legend`：整张 Figure 的图例。
- `constrained_layout=True`：自动布局。
- `fig.delaxes`：删除多余空白子图。
- `GridSpec`：更灵活的非均匀布局。
- `subplot_mosaic`：用字符串布局描述子图。

## 准备环境

```python
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
```

准备数据：

```python
dates = pd.date_range("2024-01-01", periods=10, freq="D")

nav = pd.DataFrame({
    "strategy": [1.00, 1.01, 1.03, 1.02, 1.05, 1.06, 1.08, 1.07, 1.10, 1.12],
    "benchmark": [1.00, 1.005, 1.015, 1.020, 1.030, 1.035, 1.045, 1.050, 1.055, 1.060],
}, index=dates)

returns = nav.pct_change(fill_method=None).fillna(0.0)
drawdown = nav / nav.cummax() - 1.0

metrics = pd.Series({
    "accuracy": 0.72,
    "precision": 0.68,
    "recall": 0.75,
    "auc": 0.79,
})
```

## 一行多图

最简单的多图布局是一行多个 Axes。

```python
fig, axes = plt.subplots(1, 2, figsize=(10, 4), constrained_layout=True)

axes[0].plot(nav.index, nav["strategy"], label="strategy")
axes[0].plot(nav.index, nav["benchmark"], label="benchmark")
axes[0].set_title("NAV")
axes[0].set_ylabel("NAV")

axes[1].bar(metrics.index, metrics.values)
axes[1].set_title("Metrics")
axes[1].set_ylim(0, 1)

fig.suptitle("Strategy Overview")

plt.close(fig)
```

当 `nrows=1` 或 `ncols=1` 时，`axes` 默认是一维数组。可以用下标 `axes[0]`、`axes[1]` 访问。

## 二维 Axes 网格

创建 2x2 图：

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 7), constrained_layout=True)

axes[0, 0].plot(nav.index, nav["strategy"])
axes[0, 0].set_title("Strategy NAV")

axes[0, 1].plot(nav.index, nav["benchmark"], color="tab:orange")
axes[0, 1].set_title("Benchmark NAV")

axes[1, 0].bar(metrics.index, metrics.values)
axes[1, 0].set_title("Classification Metrics")

axes[1, 1].scatter(returns["benchmark"], returns["strategy"])
axes[1, 1].set_title("Return Scatter")
axes[1, 1].set_xlabel("Benchmark return")
axes[1, 1].set_ylabel("Strategy return")

fig.suptitle("2x2 Layout")

plt.close(fig)
```

二维网格中，`axes[row, col]` 表示第几行第几列。

## flatten：循环填充子图

当要画很多类似小图时，常用 `axes.ravel()` 或 `axes.flatten()`。

```python
feature_data = pd.DataFrame({
    "momentum": [-1.2, -0.8, -0.4, 0.1, 0.5, 0.9],
    "volatility": [0.40, 0.35, 0.32, 0.28, 0.24, 0.21],
    "liquidity": [8, 9, 11, 13, 15, 18],
    "size": [100, 120, 150, 170, 210, 260],
})

fig, axes = plt.subplots(2, 2, figsize=(9, 6), constrained_layout=True)

for ax, column in zip(axes.ravel(), feature_data.columns):
    ax.plot(feature_data.index, feature_data[column], marker="o")
    ax.set_title(column)

fig.suptitle("Feature Paths")

plt.close(fig)
```

这种写法避免手动写 `axes[0, 0]`、`axes[0, 1]` 等重复代码。

## 删除多余子图

如果子图数量多于数据列，可以删除空白 Axes。

```python
three_features = feature_data[["momentum", "volatility", "liquidity"]]

fig, axes = plt.subplots(2, 2, figsize=(9, 6), constrained_layout=True)
flat_axes = axes.ravel()

for ax, column in zip(flat_axes, three_features.columns):
    ax.plot(three_features.index, three_features[column], marker="o")
    ax.set_title(column)

for ax in flat_axes[len(three_features.columns):]:
    fig.delaxes(ax)

fig.suptitle("Three Features")

plt.close(fig)
```

`fig.delaxes(ax)` 会从 Figure 中移除空白子图。

## squeeze=False：保持 axes 二维

当 `nrows=1` 或 `ncols=1` 时，`axes` 默认可能是一维数组或单个 Axes。为了统一代码，可以设置 `squeeze=False`。

```python
fig, axes = plt.subplots(1, 3, figsize=(10, 3), squeeze=False, constrained_layout=True)

print(axes.shape)

for ax, column in zip(axes.ravel(), three_features.columns):
    ax.plot(three_features.index, three_features[column])
    ax.set_title(column)

plt.close(fig)
```

使用 `squeeze=False` 后，`axes` 总是二维数组，循环代码更稳定。

## sharex：共享 x 轴

多个时间序列子图通常应该共享 x 轴。

```python
fig, axes = plt.subplots(
    2,
    1,
    figsize=(8, 6),
    sharex=True,
    constrained_layout=True,
)

axes[0].plot(nav.index, nav["strategy"], label="strategy")
axes[0].plot(nav.index, nav["benchmark"], label="benchmark")
axes[0].set_title("NAV")
axes[0].set_ylabel("NAV")

axes[1].plot(drawdown.index, drawdown["strategy"], color="tab:red")
axes[1].set_title("Strategy Drawdown")
axes[1].set_ylabel("Drawdown")
axes[1].set_xlabel("Date")

fig.suptitle("NAV and Drawdown")

plt.close(fig)
```

`sharex=True` 表示两个子图使用同一个 x 轴范围。缩放或设置 x 范围时会一起变化。

## sharey：共享 y 轴

对比同尺度指标时，使用共享 y 轴更公平。

```python
model_scores = pd.DataFrame({
    "model_a": [0.70, 0.68, 0.74],
    "model_b": [0.76, 0.71, 0.78],
}, index=["accuracy", "precision", "recall"])

fig, axes = plt.subplots(1, 2, figsize=(9, 4), sharey=True, constrained_layout=True)

axes[0].bar(model_scores.index, model_scores["model_a"])
axes[0].set_title("Model A")
axes[0].set_ylim(0, 1)

axes[1].bar(model_scores.index, model_scores["model_b"], color="tab:orange")
axes[1].set_title("Model B")

fig.suptitle("Model Comparison")

plt.close(fig)
```

如果两个子图 y 轴范围不同，视觉比较很容易误导。

## 整张图的标题：suptitle

每个 Axes 可以有自己的 `set_title`，整张 Figure 可以有 `suptitle`。

```python
fig, axes = plt.subplots(1, 2, figsize=(9, 4), constrained_layout=True)

axes[0].plot(nav.index, nav["strategy"])
axes[0].set_title("Strategy")

axes[1].plot(nav.index, nav["benchmark"])
axes[1].set_title("Benchmark")

fig.suptitle("NAV Comparison")

plt.close(fig)
```

`suptitle` 说明整张图的主题，子图标题说明各自面板内容。

## 整张图的图例：fig.legend

如果多张子图使用同一套线条，可以使用整张 Figure 的图例。

```python
fig, axes = plt.subplots(2, 1, figsize=(8, 6), sharex=True, constrained_layout=True)

line1, = axes[0].plot(nav.index, nav["strategy"], label="strategy", color="tab:blue")
line2, = axes[0].plot(nav.index, nav["benchmark"], label="benchmark", color="tab:orange")

axes[1].plot(returns.index, returns["strategy"], color="tab:blue")
axes[1].plot(returns.index, returns["benchmark"], color="tab:orange")

axes[0].set_title("NAV")
axes[1].set_title("Daily Return")

fig.legend(
    handles=[line1, line2],
    loc="upper center",
    ncol=2,
    frameon=False,
)

plt.close(fig)
```

全局图例能避免每个子图重复放图例。

## constrained_layout 和 tight_layout

常用自动布局方式有两个：

- `constrained_layout=True`：创建 Figure 时启用，更适合复杂布局。
- `fig.tight_layout()`：绘图后调用，适合简单布局。

```python
fig, axes = plt.subplots(2, 2, figsize=(9, 6), constrained_layout=True)

for ax in axes.ravel():
    ax.plot(nav.index, nav["strategy"])
    ax.set_title("Panel")

fig.suptitle("Constrained Layout")

plt.close(fig)
```

不要在复杂图里盲目同时使用两者。如果布局很复杂，优先尝试 `constrained_layout=True`。

## width_ratios 和 height_ratios

有时不同子图需要不同宽度或高度。

```python
fig, axes = plt.subplots(
    1,
    2,
    figsize=(10, 4),
    gridspec_kw={"width_ratios": [2, 1]},
    constrained_layout=True,
)

axes[0].plot(nav.index, nav["strategy"])
axes[0].set_title("Main Chart")

axes[1].bar(metrics.index, metrics.values)
axes[1].set_title("Metrics")

plt.close(fig)
```

左图宽度是右图的两倍。类似地，`height_ratios` 控制行高比例。

## GridSpec：更灵活的布局

`GridSpec` 可以让某个子图跨多行或多列。

```python
fig = plt.figure(figsize=(10, 6), constrained_layout=True)
gs = fig.add_gridspec(2, 2)

ax_main = fig.add_subplot(gs[0, :])
ax_left = fig.add_subplot(gs[1, 0])
ax_right = fig.add_subplot(gs[1, 1])

ax_main.plot(nav.index, nav["strategy"])
ax_main.set_title("Main NAV")

ax_left.bar(metrics.index, metrics.values)
ax_left.set_title("Metrics")

ax_right.scatter(returns["benchmark"], returns["strategy"])
ax_right.set_title("Return Scatter")

plt.close(fig)
```

`gs[0, :]` 表示第一行跨所有列。

## subplot_mosaic：用名字描述布局

`subplot_mosaic` 可以用字符串或列表描述布局，并返回字典。

```python
fig, axd = plt.subplot_mosaic(
    [
        ["nav", "nav"],
        ["drawdown", "metrics"],
    ],
    figsize=(10, 6),
    constrained_layout=True,
)

axd["nav"].plot(nav.index, nav["strategy"])
axd["nav"].set_title("NAV")

axd["drawdown"].plot(drawdown.index, drawdown["strategy"], color="tab:red")
axd["drawdown"].set_title("Drawdown")

axd["metrics"].bar(metrics.index, metrics.values)
axd["metrics"].set_title("Metrics")

plt.close(fig)
```

这种写法在复杂图里可读性很好，因为可以用名字访问 Axes。

## 常见坑

第一，axes 维度不稳定。

`plt.subplots(1, 3)` 返回一维 axes，`plt.subplots(2, 3)` 返回二维 axes，`plt.subplots()` 返回单个 Axes。循环代码里可以用 `squeeze=False` 或 `np.ravel(axes)` 统一处理。

第二，子图太多。

一张图里塞太多面板会让读者无法聚焦。可以分多张图，或只展示 top N。

第三，不共享坐标轴导致视觉误导。

比较同类指标时，尽量共享 y 轴或手动统一范围。

第四，全局图例和 suptitle 被裁切。

使用 `constrained_layout=True`，或调整图例位置和画布大小。

第五，空白子图没有删除。

如果网格比数据多，使用 `fig.delaxes(ax)` 删除空白面板。

## 实战提示

循环绘制多个特征的模板：

```python
columns = ["momentum", "volatility", "liquidity"]

fig, axes = plt.subplots(2, 2, figsize=(9, 6), squeeze=False, constrained_layout=True)
flat_axes = axes.ravel()

for ax, column in zip(flat_axes, columns):
    ax.plot(feature_data.index, feature_data[column])
    ax.set_title(column)

for ax in flat_axes[len(columns):]:
    fig.delaxes(ax)

fig.suptitle("Feature Diagnostics")
plt.close(fig)
```

多图布局前先决定：

1. 每个子图是否是同类指标？
2. 是否应该共享 x 轴或 y 轴？
3. 是否需要整张图的标题？
4. 图例应该放在每个子图里，还是整张图上？
5. 子图数量是否太多？

## 小结

matplotlib 多图布局的基本工具：

- `plt.subplots(nrows, ncols)` 创建规则子图网格。
- `axes.ravel()` 适合循环填充。
- `squeeze=False` 让 axes 维度稳定。
- `sharex` / `sharey` 让坐标轴共享。
- `fig.suptitle` 添加整张图标题。
- `fig.legend` 添加整张图图例。
- `constrained_layout=True` 自动管理布局。
- `fig.delaxes` 删除空白子图。
- `GridSpec` 和 `subplot_mosaic` 处理复杂布局。

多图的重点不是塞更多图，而是让读者能在统一尺度下比较不同视角。

## 自检问题

1. `plt.subplots(1, 3)` 和 `plt.subplots(2, 3)` 返回的 axes 形状有什么不同？
2. 为什么循环画多子图时常用 `axes.ravel()`？
3. `sharex=True` 和 `sharey=True` 分别解决什么问题？
4. `fig.suptitle` 和 `ax.set_title` 有什么区别？
5. 什么时候应该使用 `GridSpec` 或 `subplot_mosaic`？
