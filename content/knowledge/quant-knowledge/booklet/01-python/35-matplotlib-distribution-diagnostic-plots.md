# 35. matplotlib：直方图、箱线图、散点矩阵与诊断图

## 核心概念

前几节已经讲了 line、scatter、bar 和多子图布局。本节关注另一类常用图：用图形检查数据分布、离群点和模型误差。

常见问题：

- 单个变量大致长什么样？是否偏态？是否有厚尾？
- 两组收益或误差的分布是否不同？
- 哪些样本可能是离群点？
- 多个特征之间是否明显相关？
- 模型残差是否有系统结构？

常用工具：

- `ax.hist`：直方图。
- `ax.boxplot`：箱线图。
- `ax.scatter`：诊断散点图。
- `pandas.plotting.scatter_matrix`：散点矩阵，底层仍然使用 matplotlib。
- `ax.axhline` / `ax.axvline`：添加参考线。
- 多子图布局：把多个诊断视角放在同一张 Figure 中。

这些图通常不是最终结论，而是发现问题的第一步。

## 准备环境

```python
import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from pandas.plotting import scatter_matrix
```

准备一组可复现数据：

```python
rng = np.random.default_rng(42)

returns = pd.DataFrame({
    "strategy": rng.normal(0.0010, 0.018, size=250),
    "benchmark": rng.normal(0.0006, 0.014, size=250),
})

returns.loc[[20, 120], "strategy"] = [-0.090, 0.075]
returns.loc[[80], "benchmark"] = [-0.065]

features = pd.DataFrame({
    "momentum": rng.normal(0.0, 1.0, size=120),
    "value": rng.normal(0.0, 1.0, size=120),
    "volatility": rng.lognormal(mean=-2.0, sigma=0.35, size=120),
})
features["future_return"] = (
    0.015 * features["momentum"]
    - 0.010 * features["volatility"]
    + rng.normal(0.0, 0.020, size=120)
)

prediction = pd.DataFrame({
    "actual": rng.normal(0.0, 0.030, size=160),
})
prediction["predicted"] = 0.45 * prediction["actual"] + rng.normal(0.0, 0.018, size=160)
prediction["residual"] = prediction["actual"] - prediction["predicted"]
```

## 直方图：hist

直方图用来观察一个连续变量的分布。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.hist(returns["strategy"], bins=30)

ax.set_title("Strategy Return Distribution")
ax.set_xlabel("Daily return")
ax.set_ylabel("Count")

fig.tight_layout()
plt.close(fig)
```

`bins` 控制分箱数量。分箱太少会掩盖细节，分箱太多会让图形看起来噪声很大。

## 多组直方图

比较两组分布时，可以在同一个 Axes 上画多个直方图。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.hist(
    returns["strategy"],
    bins=30,
    alpha=0.55,
    label="strategy",
)
ax.hist(
    returns["benchmark"],
    bins=30,
    alpha=0.55,
    label="benchmark",
)

ax.axvline(0.0, color="black", linewidth=1)
ax.set_title("Return Distribution Comparison")
ax.set_xlabel("Daily return")
ax.set_ylabel("Count")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

`alpha` 控制透明度。多组直方图重叠时，如果不设置透明度，后画的分布会遮住先画的分布。

## density=True：比较形状而不是样本量

如果两组样本数量不同，直接比较 count 可能误导。这时可以把直方图归一化为密度。

```python
short_sample = returns["strategy"].iloc[:120]
long_sample = returns["benchmark"]

fig, ax = plt.subplots(figsize=(6, 4))

ax.hist(short_sample, bins=25, density=True, alpha=0.55, label="short sample")
ax.hist(long_sample, bins=25, density=True, alpha=0.55, label="long sample")

ax.set_title("Density Histogram")
ax.set_xlabel("Daily return")
ax.set_ylabel("Density")
ax.legend()

fig.tight_layout()
plt.close(fig)
```

`density=True` 后，柱子的面积总和约等于 1。它适合比较分布形状，不适合表达样本数量。

## 箱线图：boxplot

箱线图适合快速检查中位数、四分位范围和离群点。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.boxplot(
    [returns["strategy"], returns["benchmark"]],
    tick_labels=["strategy", "benchmark"],
    showmeans=True,
)

ax.axhline(0.0, color="black", linewidth=1)
ax.set_title("Return Boxplot")
ax.set_ylabel("Daily return")

fig.tight_layout()
plt.close(fig)
```

箱体表示四分位范围，箱体中间的线通常是中位数。须外的点常被标为离群点，但“离群”不等于“错误数据”。

## 水平箱线图

当类别名称较长，或者想把数值轴放在 x 方向时，可以使用水平箱线图。

```python
grouped_returns = [
    rng.normal(0.001, 0.012, size=80),
    rng.normal(0.000, 0.018, size=80),
    rng.normal(0.002, 0.022, size=80),
]

fig, ax = plt.subplots(figsize=(7, 4))

ax.boxplot(
    grouped_returns,
    tick_labels=["low volatility", "mid volatility", "high volatility"],
    vert=False,
    showmeans=True,
)

ax.axvline(0.0, color="black", linewidth=1)
ax.set_title("Return by Volatility Bucket")
ax.set_xlabel("Daily return")

fig.tight_layout()
plt.close(fig)
```

`vert=False` 表示水平显示。组名较长时，水平箱线图通常比旋转 x 轴标签更清楚。

## 散点矩阵

散点矩阵用于一次查看多个数值变量之间的两两关系。

```python
axes = scatter_matrix(
    features[["momentum", "value", "volatility", "future_return"]],
    figsize=(8, 8),
    diagonal="hist",
    alpha=0.65,
)

fig = axes[0, 0].figure
fig.suptitle("Feature Scatter Matrix")
fig.tight_layout()

plt.close(fig)
```

对角线显示单变量分布，非对角线显示两个变量的点云关系。散点矩阵很适合初筛相关性、非线性关系和异常样本。

注意：变量太多时，散点矩阵会迅速变得难读。通常只放 3 到 6 个关键变量。

## 相关矩阵热力图

matplotlib 没有强制要求使用 seaborn。简单热力图可以直接用 `imshow`。

```python
corr = features[["momentum", "value", "volatility", "future_return"]].corr()

fig, ax = plt.subplots(figsize=(5, 4))

image = ax.imshow(corr, vmin=-1, vmax=1, cmap="coolwarm")

ax.set_xticks(range(len(corr.columns)))
ax.set_xticklabels(corr.columns, rotation=30, ha="right")
ax.set_yticks(range(len(corr.index)))
ax.set_yticklabels(corr.index)

fig.colorbar(image, ax=ax, label="Correlation")
ax.set_title("Feature Correlation")

fig.tight_layout()
plt.close(fig)
```

相关矩阵只能展示线性相关。点云图仍然重要，因为它能暴露非线性、分段关系和离群点。

## 预测值 vs 实际值

回归模型最常见的诊断图之一，是预测值和实际值的散点图。

```python
fig, ax = plt.subplots(figsize=(5, 5))

ax.scatter(prediction["actual"], prediction["predicted"], alpha=0.7)

limits = [
    min(prediction["actual"].min(), prediction["predicted"].min()),
    max(prediction["actual"].max(), prediction["predicted"].max()),
]
ax.plot(limits, limits, color="black", linewidth=1, linestyle="--")

ax.set_title("Predicted vs Actual")
ax.set_xlabel("Actual")
ax.set_ylabel("Predicted")

fig.tight_layout()
plt.close(fig)
```

虚线是理想情况 `predicted = actual`。点离虚线越远，预测误差越大。

## 残差 vs 预测值

残差诊断图用来检查模型是否有系统性错误。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.scatter(prediction["predicted"], prediction["residual"], alpha=0.7)
ax.axhline(0.0, color="black", linewidth=1, linestyle="--")

ax.set_title("Residual vs Predicted")
ax.set_xlabel("Predicted")
ax.set_ylabel("Residual")

fig.tight_layout()
plt.close(fig)
```

理想情况下，残差应该围绕 0 随机散开。如果出现漏斗形、弯曲形或明显分层，说明模型可能遗漏了结构。

## 残差分布

残差直方图可以检查误差是否偏斜、厚尾或有极端值。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.hist(prediction["residual"], bins=30, alpha=0.8)
ax.axvline(0.0, color="black", linewidth=1, linestyle="--")

ax.set_title("Residual Distribution")
ax.set_xlabel("Residual")
ax.set_ylabel("Count")

fig.tight_layout()
plt.close(fig)
```

如果残差长期偏正或偏负，模型可能存在系统性低估或高估。

## 多图诊断面板

实际工作中，常把几个诊断图放在同一张 Figure 中。

```python
fig, axes = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)

axes[0, 0].hist(returns["strategy"], bins=30)
axes[0, 0].set_title("Strategy Return")
axes[0, 0].set_xlabel("Daily return")

axes[0, 1].boxplot(
    [returns["strategy"], returns["benchmark"]],
    tick_labels=["strategy", "benchmark"],
    showmeans=True,
)
axes[0, 1].set_title("Return Boxplot")

axes[1, 0].scatter(prediction["actual"], prediction["predicted"], alpha=0.7)
limits = [
    min(prediction["actual"].min(), prediction["predicted"].min()),
    max(prediction["actual"].max(), prediction["predicted"].max()),
]
axes[1, 0].plot(limits, limits, color="black", linewidth=1, linestyle="--")
axes[1, 0].set_title("Predicted vs Actual")

axes[1, 1].scatter(prediction["predicted"], prediction["residual"], alpha=0.7)
axes[1, 1].axhline(0.0, color="black", linewidth=1, linestyle="--")
axes[1, 1].set_title("Residual vs Predicted")

fig.suptitle("Distribution and Model Diagnostics")

plt.close(fig)
```

这种面板适合训练后检查，也适合把数据质量问题快速汇总给别人。

## 常见坑

第一，把直方图当成精确概率密度。

直方图受 `bins` 影响很大。换一个分箱数量，视觉形态可能变化。结论不要只依赖一个分箱设置。

第二，样本量不同却比较 count。

两组样本量差异很大时，count 直方图会让样本量更大的组看起来更“高”。比较形状时用 `density=True`。

第三，把箱线图离群点直接删除。

箱线图上的点只是统计规则标记的极端值。它们可能是错误数据，也可能是最重要的风险事件。

第四，散点矩阵变量太多。

变量太多会导致每个面板很小，读者看不出关系。先选关键变量，再分批画。

第五，残差图只看“像不像正态”。

对模型诊断来说，残差是否围绕 0 随机分布、是否随预测值变化、是否有结构性模式，通常比单纯正态性更重要。

## 实战提示

做分布和诊断图时，可以按这个顺序检查：

1. 单变量分布：直方图看偏态、厚尾和极端值。
2. 组间对比：箱线图看中位数、离散程度和异常点。
3. 特征关系：散点矩阵看相关性、非线性和异常组合。
4. 模型误差：预测值 vs 实际值、残差 vs 预测值、残差分布。
5. 结论复核：改变 `bins`、样本区间或分组方式，看结论是否稳定。

一个诊断图模板：

```python
def plot_regression_diagnostics(actual, predicted):
    actual = pd.Series(actual, name="actual")
    predicted = pd.Series(predicted, name="predicted")
    residual = actual - predicted

    fig, axes = plt.subplots(1, 3, figsize=(12, 4), constrained_layout=True)

    axes[0].scatter(actual, predicted, alpha=0.7)
    limits = [min(actual.min(), predicted.min()), max(actual.max(), predicted.max())]
    axes[0].plot(limits, limits, color="black", linewidth=1, linestyle="--")
    axes[0].set_title("Predicted vs Actual")

    axes[1].scatter(predicted, residual, alpha=0.7)
    axes[1].axhline(0.0, color="black", linewidth=1, linestyle="--")
    axes[1].set_title("Residual vs Predicted")

    axes[2].hist(residual, bins=30)
    axes[2].axvline(0.0, color="black", linewidth=1, linestyle="--")
    axes[2].set_title("Residual Distribution")

    return fig, axes


fig, axes = plot_regression_diagnostics(
    prediction["actual"],
    prediction["predicted"],
)
plt.close(fig)
```

这个函数返回 `fig, axes`，方便调用者继续设置标题、保存图片或加更多标注。

## 小结

本节的重点：

- `ax.hist` 用于观察连续变量分布。
- `density=True` 适合样本量不同但要比较分布形状的场景。
- `ax.boxplot` 用于比较中位数、离散程度和离群点。
- `scatter_matrix` 适合快速查看多个变量的两两关系。
- `imshow` 可以画简单相关矩阵热力图。
- 预测值 vs 实际值、残差 vs 预测值、残差分布是常用模型诊断组合。
- 诊断图的目标是发现问题，不是单独证明结论。

## 自检问题

1. `bins` 过大或过小会怎样影响直方图？
2. 两组样本量不同但要比较分布形状时，为什么要考虑 `density=True`？
3. 箱线图上出现离群点，为什么不能直接删除？
4. 散点矩阵适合什么场景？为什么变量太多时不适合使用？
5. 残差 vs 预测值图中，如果点云呈漏斗形，可能说明什么？
