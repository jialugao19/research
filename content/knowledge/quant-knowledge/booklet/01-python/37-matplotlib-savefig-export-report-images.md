# matplotlib：savefig、分辨率、导出格式与报告图片规范

## 核心概念

画图的最后一步通常不是 `plt.show()`，而是把图片稳定导出到文件，供报告、论文、网页、实验记录或自动化流水线使用。

导出图片时要关注：

- 输出格式：PNG、PDF、SVG、JPEG。
- 画布尺寸：`figsize`，单位是英寸。
- 分辨率：`dpi`，主要影响位图格式。
- 像素尺寸：`figsize * dpi`。
- 边距裁切：`bbox_inches`、`pad_inches`。
- 背景：白底、透明背景或指定颜色。
- 文件命名：是否能追溯数据、模型、日期和版本。
- 资源释放：批量画图后是否 `plt.close(fig)`。

matplotlib 的核心导出方法是：

```python
fig.savefig(path, dpi=..., bbox_inches=...)
```

## 准备环境

```python
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd

import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt
from matplotlib.ticker import PercentFormatter
```

准备数据和输出目录：

```python
rng = np.random.default_rng(11)

dates = pd.bdate_range("2024-01-02", periods=60)
returns = pd.Series(
    rng.normal(0.0008, 0.012, size=len(dates)),
    index=dates,
    name="return",
)
nav = (1.0 + returns).cumprod()
drawdown = nav / nav.cummax() - 1.0

figure_dir = Path("outputs/figures")
figure_dir.mkdir(parents=True, exist_ok=True)
```

实际项目里，不要把图片随手保存到当前目录。使用固定的输出目录，更容易清理和追踪。

## 最基本的 savefig

先创建 `Figure` 和 `Axes`，再调用 `fig.savefig(...)`。

```python
fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(nav.index, nav.values)
ax.set_title("Strategy NAV")
ax.set_ylabel("NAV")

output_path = figure_dir / "strategy_nav.png"
fig.savefig(output_path)

plt.close(fig)
```

`savefig` 应该在 `plt.close(fig)` 之前调用。关闭后再保存，图像对象可能已经不再适合继续使用。

## figsize、dpi 和像素尺寸

`figsize` 的单位是英寸，`dpi` 是每英寸像素数。PNG 这类位图的像素尺寸大约是：

```text
width_pixels = figsize_width * dpi
height_pixels = figsize_height * dpi
```

例子：

```python
fig, ax = plt.subplots(figsize=(6, 4), dpi=100)

ax.plot(nav.index, nav.values)
ax.set_title("6x4 inches at 150 dpi")

output_path = figure_dir / "nav_6x4_150dpi.png"
fig.savefig(output_path, dpi=150)

plt.close(fig)
```

这里导出的 PNG 大约是 `900 x 600` 像素。注意：创建 Figure 时的 `dpi=100` 影响交互显示和默认渲染，`savefig(dpi=150)` 会覆盖保存时的分辨率。

## 使用 bbox_inches="tight"

有些图的标题、图例或旋转标签可能被裁切。可以使用 `bbox_inches="tight"` 自动收紧边界。

```python
fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(nav.index, nav.values, label="strategy")
ax.set_title("NAV with Legend Outside")
ax.set_ylabel("NAV")
ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))

output_path = figure_dir / "nav_tight_bbox.png"
fig.savefig(output_path, dpi=150, bbox_inches="tight", pad_inches=0.1)

plt.close(fig)
```

`bbox_inches="tight"` 很实用，但它可能改变最终图片的精确像素尺寸。如果报告模板要求固定尺寸，需要提前测试。

## PNG、PDF 和 SVG

常见格式有不同用途：

- PNG：位图，适合网页、Markdown、PPT 和快速报告。
- PDF：矢量格式，适合论文、LaTeX 和打印。
- SVG：矢量格式，适合网页和可编辑图形。
- JPEG：有损压缩，不适合线图和文字密集图。

同一张图可以导出多种格式：

```python
fig, ax = plt.subplots(figsize=(7, 4))

ax.plot(nav.index, nav.values)
ax.set_title("NAV Exported in Multiple Formats")
ax.set_ylabel("NAV")

for suffix in ["png", "pdf", "svg"]:
    fig.savefig(
        figure_dir / f"nav_export.{suffix}",
        dpi=150,
        bbox_inches="tight",
    )

plt.close(fig)
```

矢量格式不会因为放大而变糊，但如果图里有大量散点、热力图或栅格图，文件可能很大。

## 透明背景和白色背景

默认导出通常是白底。需要叠加到深色背景或网页上时，可以使用透明背景。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav.values, color="tab:blue")
ax.set_title("Transparent Background")
ax.set_ylabel("NAV")

fig.savefig(
    figure_dir / "nav_transparent.png",
    dpi=150,
    transparent=True,
    bbox_inches="tight",
)

plt.close(fig)
```

如果报告要求稳定的白色背景，可以显式指定：

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav.values)
ax.set_title("White Background")

fig.savefig(
    figure_dir / "nav_white_background.png",
    dpi=150,
    facecolor="white",
    bbox_inches="tight",
)

plt.close(fig)
```

透明背景适合网页叠加，但对阅读性有要求的报告图通常更推荐白底。

## constrained_layout 与 tight_layout 后保存

保存前要先处理布局，避免标题、坐标轴标签或图例被挤掉。

```python
fig, axes = plt.subplots(
    2,
    1,
    figsize=(8, 6),
    sharex=True,
    constrained_layout=True,
)

axes[0].plot(nav.index, nav.values)
axes[0].set_title("NAV")
axes[0].set_ylabel("NAV")

axes[1].plot(drawdown.index, drawdown.values, color="tab:red")
axes[1].fill_between(drawdown.index, drawdown.values, 0.0, color="tab:red", alpha=0.25)
axes[1].set_title("Drawdown")
axes[1].set_ylabel("Drawdown")
axes[1].yaxis.set_major_formatter(PercentFormatter(xmax=1.0))

fig.suptitle("Strategy Report Figure")
fig.savefig(figure_dir / "nav_drawdown_report.png", dpi=150)

plt.close(fig)
```

如果没有使用 `constrained_layout=True`，可以在保存前调用 `fig.tight_layout()`。复杂多图一般优先使用 `constrained_layout=True`。

## 保存到内存：BytesIO

有时不需要落盘，而是把图片发送到 Web API、邮件、数据库或测试代码里。可以保存到 `BytesIO`。

```python
fig, ax = plt.subplots(figsize=(6, 4))

ax.plot(nav.index, nav.values)
ax.set_title("In-memory PNG")

buffer = BytesIO()
fig.savefig(buffer, format="png", dpi=120, bbox_inches="tight")
buffer.seek(0)

png_bytes = buffer.getvalue()

plt.close(fig)
```

`png_bytes` 是二进制内容，可以传给网络接口或写入其他存储系统。

## 批量导出多张图

批量生成报告图片时，要给每张 Figure 及时 `close`。

```python
series_by_name = {
    "nav": nav,
    "drawdown": drawdown,
    "return": returns,
}

for name, series in series_by_name.items():
    fig, ax = plt.subplots(figsize=(7, 4))

    ax.plot(series.index, series.values)
    ax.set_title(name)
    ax.set_ylabel(name)

    fig.savefig(
        figure_dir / f"{name}.png",
        dpi=150,
        bbox_inches="tight",
    )
    plt.close(fig)
```

如果循环里不关闭 Figure，长时间运行的脚本会占用越来越多内存，并可能触发 matplotlib 的打开 Figure 数量警告。

## 文件命名规范

报告图片的命名应该稳定、可追溯、可排序。

较差的命名：

```text
plot.png
new_plot.png
final2.png
```

更好的命名：

```text
2024q1_strategy_nav_daily.png
2024q1_strategy_drawdown_daily.png
model_v3_residual_diagnostics.png
```

建议包含：

- 数据范围或批次。
- 主题或指标。
- 频率或粒度。
- 模型或实验版本。
- 必要时包含日期。

不要在文件名里放空格、中文标点或过长的自然语言描述。报告系统、命令行工具和云存储对简单文件名更友好。

## 报告图片规范

一组报告图最好保持一致：

- 相同类型的图使用相同 `figsize`。
- 同一指标使用相同 y 轴范围或明确说明范围不同。
- 百分比统一显示为百分比刻度。
- 图片使用稳定的白色背景，除非有明确透明需求。
- 标题、坐标轴标签、图例命名保持一致。
- 导出目录和文件名可由脚本重复生成。
- 每张图都能独立说明变量含义和单位。

一个简单的报告导出函数：

```python
def save_report_figure(fig, path, dpi=150):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        path,
        dpi=dpi,
        bbox_inches="tight",
        pad_inches=0.1,
        facecolor="white",
    )
    plt.close(fig)


fig, ax = plt.subplots(figsize=(7, 4))
ax.plot(nav.index, nav.values)
ax.set_title("Strategy NAV")
ax.set_ylabel("NAV")

save_report_figure(fig, figure_dir / "report_strategy_nav.png")
```

函数里统一保存参数，可以避免同一份报告里每张图尺寸和边距都不一样。

## 常见坑

第一，保存的是空白图。

常见原因是保存了错误的 Figure，或在保存前已经关闭。推荐使用面向对象写法，始终调用 `fig.savefig(...)`。

第二，图片在报告里太糊。

位图分辨率太低时会糊。增加 `figsize` 或 `dpi`，或者导出为 PDF / SVG。

第三，`bbox_inches="tight"` 改变像素尺寸。

它会按内容重新计算边界，适合防裁切，但不适合严格固定像素尺寸的场景。

第四，批量画图不关闭 Figure。

循环里一定要 `plt.close(fig)`，否则内存和 Figure 数量会持续增长。

第五，JPEG 用在线图和文字图上。

JPEG 有损压缩会让线条和文字边缘变脏。线图、柱状图和报告图优先使用 PNG、PDF 或 SVG。

## 实战提示

导出图片前可以问自己：

1. 这张图给谁看？报告、网页、论文还是调试？
2. 要位图还是矢量图？
3. 目标尺寸是多少？是否需要固定像素？
4. 是否会被放到深色背景上？
5. 文件名是否能追溯数据和版本？
6. 这张图是否可以由脚本稳定重跑生成？

常用选择：

- Markdown / GitHub / PPT：PNG，`dpi=150` 或 `dpi=200`。
- 论文 / LaTeX / 打印：PDF。
- 网页可编辑矢量：SVG。
- 大量照片类图像：JPEG，但不适合线图。

## 小结

本节的重点：

- 使用 `fig.savefig(...)` 导出图片，优先使用面向对象写法。
- PNG 的像素尺寸由 `figsize * dpi` 决定。
- `bbox_inches="tight"` 可以防裁切，但会改变最终边界。
- PDF / SVG 是矢量格式，适合论文和可缩放场景。
- `transparent=True` 可导出透明背景，报告图通常显式用白底。
- 批量导出时必须 `plt.close(fig)`。
- 报告图片要有稳定命名、统一尺寸、清晰单位和可重复生成流程。

## 自检问题

1. `figsize=(6, 4)`、`dpi=150` 的 PNG 大约是多少像素？
2. `bbox_inches="tight"` 解决什么问题？它有什么副作用？
3. PNG、PDF、SVG 分别适合什么场景？
4. 为什么批量导出图片时必须关闭 Figure？
5. 一个好的报告图片文件名应该包含哪些信息？
