# Python 理解项：profiling 性能剖析、计时与瓶颈定位

## 核心概念

性能优化的第一步不是改代码，而是定位瓶颈。

常见错误是：

- 看到代码里有 `for` 就立刻改成向量化。
- 看到任务慢就立刻上 multiprocessing。
- 看到内存涨就猜测是某个 DataFrame 太大。
- 只凭一次运行时间判断优化是否有效。

profiling 的目标是把“感觉慢”变成证据：

```text
哪段代码慢？
慢在 CPU、I/O、内存分配，还是数据传递？
优化后结果是否仍然正确？
优化后性能是否稳定变好？
```

本节主要使用标准库工具：

- `time.perf_counter`：粗粒度计时。
- `timeit`：重复计时小函数。
- `cProfile`：函数级性能剖析。
- `pstats`：整理和排序 profiler 结果。
- `tracemalloc`：追踪 Python 层内存分配。

## 准备环境

```python
import cProfile
import io
import pstats
import time
import timeit
import tracemalloc

import numpy as np
import pandas as pd
```

准备一组数据：

```python
rng = np.random.default_rng(45)

prices = pd.Series(
    100.0 * np.cumprod(1.0 + rng.normal(0.0005, 0.015, size=5_000)),
    name="price",
)

df = pd.DataFrame({
    "price": prices,
    "volume": rng.integers(1_000, 50_000, size=len(prices)),
})
```

下面的例子都尽量小，便于快速运行。真实项目中，profiling 应该在接近真实的数据规模上做。

## 先明确目标

性能优化前要明确目标：

- 是降低总耗时？
- 是降低单次请求延迟？
- 是降低峰值内存？
- 是提升吞吐量？
- 是减少 I/O 等待？

不同目标对应不同工具。比如：

- 小函数比较：用 `timeit`。
- 脚本哪里慢：用 `cProfile`。
- Python 对象内存增长：用 `tracemalloc`。
- NumPy 大数组内存峰值：还要结合数组 `nbytes`、系统监控或专门工具。

## 单段计时：perf_counter

`time.perf_counter()` 适合给一段代码做粗粒度计时。

```python
start = time.perf_counter()

returns = prices.pct_change(fill_method=None).fillna(0.0)
volatility = returns.rolling(window=20, min_periods=5).std()

elapsed = time.perf_counter() - start

print(elapsed)
```

这种计时适合回答：

```text
这一整段大概耗时多少？
```

它不适合回答：

```text
里面到底哪一行最慢？
```

## 用上下文管理器封装计时

可以写一个简单计时器，方便给多个阶段打点。

```python
class Timer:
    def __init__(self, label):
        self.label = label
        self.elapsed = None

    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.elapsed = time.perf_counter() - self.start


with Timer("feature_build") as timer:
    returns = prices.pct_change(fill_method=None).fillna(0.0)
    momentum = prices / prices.shift(20) - 1.0

print(timer.label)
print(timer.elapsed)
```

这类阶段计时在数据流水线里很有用，可以记录每一步的耗时。

## timeit：重复计时小函数

`timeit` 适合比较两个小函数。

循环版收益率：

```python
def returns_loop(values):
    out = np.empty(len(values) - 1, dtype=np.float64)

    for i in range(1, len(values)):
        out[i - 1] = values[i] / values[i - 1] - 1.0

    return out
```

向量化版收益率：

```python
def returns_vectorized(values):
    return values[1:] / values[:-1] - 1.0
```

重复计时：

```python
values = prices.to_numpy()

loop_time = min(timeit.repeat(lambda: returns_loop(values), number=20, repeat=5))
vec_time = min(timeit.repeat(lambda: returns_vectorized(values), number=20, repeat=5))

print(loop_time)
print(vec_time)
print(np.allclose(returns_loop(values), returns_vectorized(values)))
```

使用 `min(...)` 是为了减少偶发系统噪声的影响。不要只看一次运行结果。

## timeit 的边界

`timeit` 适合小块代码，不适合完整系统分析。

注意：

- 测试函数必须返回相同结果。
- 数据规模要接近真实任务。
- 不要把初始化成本和计算成本混在一起，除非你确实关心总成本。
- 不要只比较平均值，也要关注波动。

更稳妥的写法是先断言正确性：

```python
expected = returns_loop(values)
actual = returns_vectorized(values)

assert np.allclose(expected, actual)
```

再比较耗时。

## cProfile：函数级剖析

当你不知道脚本哪里慢时，用 `cProfile`。

先构造一个小型数据处理流水线：

```python
def slow_row_score(frame):
    scores = []

    for row in frame.itertuples(index=False):
        score = (
            row.price * 0.001
            + np.log1p(row.volume) * 0.1
        )
        scores.append(score)

    return pd.Series(scores, index=frame.index, name="score")


def build_features_slow(frame):
    out = frame.copy()
    out["return"] = out["price"].pct_change(fill_method=None).fillna(0.0)
    out["volatility"] = out["return"].rolling(window=20, min_periods=5).std()
    out["score"] = slow_row_score(out)
    return out
```

用 `cProfile` 跑：

```python
profiler = cProfile.Profile()
profiler.enable()

features_slow = build_features_slow(df)

profiler.disable()
```

结果对象先保存在 `profiler` 中，下一步用 `pstats` 整理。

## pstats：排序 profiler 结果

```python
stream = io.StringIO()

stats = pstats.Stats(profiler, stream=stream)
stats.strip_dirs()
stats.sort_stats("cumtime")
stats.print_stats(10)

profile_text = stream.getvalue()

print(profile_text)
```

常见字段：

- `ncalls`：函数调用次数。
- `tottime`：函数自身耗时，不包含子函数。
- `percall`：每次调用平均耗时。
- `cumtime`：累计耗时，包含子函数。
- `filename:lineno(function)`：函数位置。

通常先看 `cumtime`，找到高层瓶颈；再看 `tottime`，找到自身开销大的函数。

## 根据 profile 重构

如果 profile 显示 `slow_row_score` 耗时高，可以改成向量化。

```python
def fast_row_score(frame):
    return (
        frame["price"] * 0.001
        + np.log1p(frame["volume"]) * 0.1
    ).rename("score")


def build_features_fast(frame):
    out = frame.copy()
    out["return"] = out["price"].pct_change(fill_method=None).fillna(0.0)
    out["volatility"] = out["return"].rolling(window=20, min_periods=5).std()
    out["score"] = fast_row_score(out)
    return out
```

先验证结果一致：

```python
features_fast = build_features_fast(df)

print(np.allclose(features_slow["score"], features_fast["score"]))
```

再计时：

```python
slow_seconds = min(timeit.repeat(lambda: build_features_slow(df), number=3, repeat=3))
fast_seconds = min(timeit.repeat(lambda: build_features_fast(df), number=3, repeat=3))

print(slow_seconds)
print(fast_seconds)
```

优化流程应该是：

```text
profile -> 找热点 -> 修改热点 -> 验证正确性 -> 重新计时
```

## cProfile 的局限

`cProfile` 是函数级 profiler。它能告诉你哪个函数耗时多，但不能精确到每一行。

局限：

- 对 NumPy / pandas 底层 C 代码，只能看到 Python 调用边界。
- 对 I/O 等待和系统调用，需要结合日志或其他工具。
- 对逐行热点，需要额外工具，例如 `line_profiler`。

即使如此，`cProfile` 仍然是定位 Python 代码瓶颈的首选标准库工具。

## 用 pstats 做结构化摘要

有时不想打印文本，而是抽取 top 函数。

```python
stats = pstats.Stats(profiler)
stats.strip_dirs()
stats.sort_stats("cumtime")

top_functions = []

for func, stat in stats.stats.items():
    cc, nc, tt, ct, callers = stat
    filename, line_no, func_name = func
    top_functions.append({
        "function": func_name,
        "file": filename,
        "line": line_no,
        "calls": nc,
        "total_time": tt,
        "cum_time": ct,
    })

profile_df = (
    pd.DataFrame(top_functions)
    .sort_values("cum_time", ascending=False)
    .head(10)
    .reset_index(drop=True)
)

print(profile_df)
```

结构化表格适合保存到实验日志或性能报告里。

## tracemalloc：追踪 Python 内存分配

`tracemalloc` 可以追踪 Python 层内存分配。

```python
def build_records(n):
    return [
        {
            "id": i,
            "value": float(i % 7),
            "label": f"bucket_{i % 10}",
        }
        for i in range(n)
    ]
```

追踪内存：

```python
tracemalloc.start()

snapshot_before = tracemalloc.take_snapshot()
records = build_records(5_000)
snapshot_after = tracemalloc.take_snapshot()

current, peak = tracemalloc.get_traced_memory()

tracemalloc.stop()

print(current)
print(peak)
```

`current` 是当前追踪到的内存，`peak` 是追踪期间峰值。

## 对比快照

可以对比两次 snapshot，找出哪些代码行增加了内存分配。

```python
top_stats = snapshot_after.compare_to(snapshot_before, "lineno")

for stat in top_stats[:5]:
    print(stat)
```

输出会显示文件、行号和内存增量。

注意：`tracemalloc` 主要追踪 Python 层分配。NumPy 大数组的底层 native buffer 不一定能被完整反映。对 NumPy 内存，还要看 `arr.nbytes`、进程 RSS 或专门内存 profiler。

## NumPy 内存的简单估算

NumPy 数组的数据区大小可以直接看 `nbytes`。

```python
arr = np.empty((1_000, 100), dtype=np.float64)

print(arr.nbytes)
print(arr.nbytes / 1024 / 1024)
```

对数组表达式：

```python
a = np.ones(100_000, dtype=np.float64)
b = np.ones(100_000, dtype=np.float64)

c = (a + b) * 2.0
```

除了最终的 `c`，中间的 `a + b` 也可能产生临时数组。profiling 内存时，要关注峰值而不只是最终对象大小。

## I/O 计时

如果怀疑慢在 I/O，可以单独给读写阶段计时。

```python
def write_and_read_csv(frame):
    path = "/tmp/profiling_example.csv"
    frame.to_csv(path, index=False)
    loaded = pd.read_csv(path)
    return loaded


start = time.perf_counter()
loaded = write_and_read_csv(df.head(100))
io_seconds = time.perf_counter() - start

print(io_seconds)
print(loaded.shape)
```

I/O-bound 任务不一定适合 multiprocessing。很多时候，缓存、减少读写、批量读取、压缩格式选择，比盲目并行更有效。

## profiling 和 multiprocessing

多进程代码更难 profile，因为每个进程有自己的 profiler。

建议：

1. 先在单进程版本上 profile，确认真正热点。
2. 确认任务是 CPU-bound，并且单个任务足够大。
3. 再引入 multiprocessing。
4. 分别计时计算时间、数据序列化时间、结果合并时间。

如果还没确认瓶颈，就直接上多进程，很容易把问题从“计算慢”变成“数据传输慢”。

## 常见坑

第一，只跑一次计时。

单次计时容易受系统负载、缓存、JIT 或首次导入影响。用重复计时，并关注数量级。

第二，没有先验证正确性。

优化前后结果不一致，再快也没有意义。先 `assert np.allclose(...)` 或做业务级断言。

第三，只看总耗时。

总耗时告诉你慢，但不告诉你哪里慢。要用 `cProfile` 找函数级热点。

第四，拿小数据的结论套到大数据。

小数据上函数调用开销显著；大数据上内存带宽、临时数组和 I/O 可能更重要。

第五，误读 tracemalloc。

`tracemalloc` 不等于完整进程内存监控。它对 Python 层分配很有用，但 NumPy、BLAS、系统缓存等还需要其他证据。

## 实战提示

一个保守的 profiling 流程：

1. 用真实或接近真实的数据规模复现慢问题。
2. 用 `perf_counter` 给大阶段打点。
3. 用 `cProfile` 找函数级热点。
4. 用 `timeit` 比较候选替代实现。
5. 用 `tracemalloc` 或 `nbytes` 检查内存问题。
6. 优化一个热点后，验证结果一致。
7. 重跑同样的 benchmark，记录优化前后数字。
8. 如果还慢，再进入下一轮，不要一次改很多地方。

一个完整小模板：

```python
def profile_function(func, *args, top_n=10, **kwargs):
    profiler = cProfile.Profile()
    result = profiler.runcall(func, *args, **kwargs)

    stream = io.StringIO()
    stats = pstats.Stats(profiler, stream=stream)
    stats.strip_dirs()
    stats.sort_stats("cumtime")
    stats.print_stats(top_n)

    return result, stream.getvalue()


features, report = profile_function(build_features_slow, df, top_n=8)

print(report)
```

这个模板适合在实验代码里快速定位函数级瓶颈。

## 小结

本节的重点：

- profiling 的目标是用证据定位瓶颈，而不是凭感觉优化。
- `time.perf_counter` 适合阶段级计时。
- `timeit` 适合重复比较小函数。
- `cProfile` 和 `pstats` 适合找函数级热点。
- `tracemalloc` 适合追踪 Python 层内存分配。
- NumPy 数组内存要结合 `nbytes` 和进程级监控理解。
- 优化必须经过正确性验证和优化后复测。

## 自检问题

1. `perf_counter`、`timeit`、`cProfile` 分别适合什么场景？
2. `tottime` 和 `cumtime` 有什么区别？
3. 为什么优化前后必须先验证结果一致？
4. `tracemalloc` 为什么不能完全代表 NumPy 程序的内存使用？
5. 为什么 profiling 通常应该先在单进程版本上做？
