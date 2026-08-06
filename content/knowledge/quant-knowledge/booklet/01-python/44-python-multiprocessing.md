# 44. Python 理解项：multiprocessing 进程并行、数据传递与适用边界

## 核心概念

Python 里的并行经常要先区分两类任务：

- CPU-bound：主要消耗 CPU，例如纯 Python 循环、复杂模拟、逐样本计算。
- I/O-bound：主要等待文件、网络、数据库，例如下载数据、读写远程存储。

`multiprocessing` 主要解决 CPU-bound 任务。它通过多个进程并行执行代码，每个进程有自己的 Python 解释器和内存空间，因此可以绕开 GIL 对 Python 字节码并行执行的限制。

但进程并行不是免费午餐：

- 创建进程有开销。
- 进程之间传数据通常要 pickle 序列化。
- 大数组在进程间传来传去会复制，可能比计算还慢。
- NumPy / pandas / BLAS 自己可能已经用了底层并行。
- 过多进程会造成 CPU 争用和内存压力。

所以 multiprocessing 的核心判断是：

```text
并行节省的计算时间 > 进程创建、调度、序列化和数据传输成本
```

## 准备环境

```python
import os
import multiprocessing as mp
from concurrent.futures import ProcessPoolExecutor, as_completed
from multiprocessing import shared_memory

import numpy as np
import pandas as pd
```

查看 CPU 数量和当前启动方式：

```python
print(os.cpu_count())
print(mp.get_start_method())
```

在 Linux 上常见默认启动方式是 `fork`；在 Windows 和很多 macOS 场景中是 `spawn`。为了可移植，脚本里要使用：

```python
if __name__ == "__main__":
    ...
```

并且 worker 函数要定义在模块顶层，不要定义成 lambda 或嵌套函数。

## GIL 和进程并行

GIL 是 Global Interpreter Lock。它限制同一个 Python 进程里多个线程同时执行 Python 字节码。

对纯 Python CPU 循环，线程不一定能带来真正 CPU 并行。多进程可以绕开这个限制，因为每个进程有自己的解释器和 GIL。

注意：

- GIL 不代表 Python 永远不能并行。
- NumPy、SciPy、BLAS 等底层代码可能释放 GIL 或自己开线程。
- I/O 等待任务更适合线程或异步，不一定需要多进程。

## 最小 ProcessPoolExecutor 例子

先写一个可并行的顶层函数：

```python
def sum_squares_range(bounds):
    start, stop = bounds
    values = np.arange(start, stop, dtype=np.float64)
    return float(np.sum(values * values))
```

把任务拆成多个区间：

```python
n = 100_000
bounds = [
    (0, 25_000),
    (25_000, 50_000),
    (50_000, 75_000),
    (75_000, 100_000),
]
```

并行计算：

```python
if __name__ == "__main__":
    workers = min(4, os.cpu_count() or 1)

    with ProcessPoolExecutor(max_workers=workers) as executor:
        partial = list(executor.map(sum_squares_range, bounds))

    total = sum(partial)
    expected = sum_squares_range((0, n))

    print(np.isclose(total, expected))
```

`executor.map` 会保持输入顺序。这里每个进程负责一个区间，最后在主进程汇总。

## as_completed：谁先完成先处理

如果不同任务耗时差异很大，可以用 `as_completed`。

```python
def task_with_label(item):
    label, start, stop = item
    value = sum_squares_range((start, stop))
    return label, value


tasks = [
    ("a", 0, 10_000),
    ("b", 10_000, 40_000),
    ("c", 40_000, 100_000),
]

if __name__ == "__main__":
    results = {}

    with ProcessPoolExecutor(max_workers=3) as executor:
        futures = [executor.submit(task_with_label, task) for task in tasks]

        for future in as_completed(futures):
            label, value = future.result()
            results[label] = value

    print(results)
```

`as_completed` 不保证顺序，它适合边完成边写结果、边更新进度、边处理异常。

## chunksize：减少调度开销

任务非常碎时，调度开销会变大。`executor.map` 支持 `chunksize`。

```python
small_tasks = [(i, i + 1) for i in range(10_000)]

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        values = list(
            executor.map(
                sum_squares_range,
                small_tasks,
                chunksize=200,
            )
        )

    print(sum(values))
```

`chunksize` 表示一次给 worker 分发一批任务，能减少大量小任务的调度成本。

## worker 函数必须可 pickle

进程间传递任务时，需要序列化函数和参数。通常要求：

- 函数定义在模块顶层。
- 参数和返回值可以 pickle。
- 不要把打开的文件句柄、数据库连接、线程锁等不可序列化对象直接传给 worker。

不推荐：

```python
# 不推荐：lambda 通常不能被 multiprocessing 稳定 pickle
# executor.map(lambda x: x * x, values)
```

推荐：

```python
def square(value):
    return value * value
```

如果在 notebook 或交互环境中遇到 pickle 问题，优先改成脚本运行，并把 worker 函数放到 `.py` 文件顶层。

## 数据传递成本

多进程的常见误区是：把大数组传给每个任务。

```python
def mean_of_array(arr):
    return float(np.mean(arr))
```

如果这样提交任务：

```python
# 不推荐：每个任务都可能序列化并传输大数组
# executor.submit(mean_of_array, huge_array)
```

大数组会被 pickle，进程间传输和反序列化可能非常慢，还会增加内存占用。

更好的思路：

- 让 worker 自己从文件读取它负责的分片。
- 只传小参数，例如文件路径、日期范围、行号区间。
- 使用共享内存或 memory map。
- 先用向量化或批量算法减少需要并行的工作量。

## 传小参数，不传大数据

例如只传区间，让 worker 自己生成或读取数据：

```python
def simulate_chunk(args):
    seed, n = args
    rng = np.random.default_rng(seed)
    sample = rng.normal(0.0, 1.0, size=n)
    return float(sample.mean()), float(sample.std())


jobs = [(100, 10_000), (101, 10_000), (102, 10_000), (103, 10_000)]

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        simulation_stats = list(executor.map(simulate_chunk, jobs))

    print(simulation_stats)
```

这种写法只传 seed 和样本量，避免把大数组复制给多个进程。

## 共享内存基础

如果多个进程需要读同一个大 NumPy 数组，可以用 `multiprocessing.shared_memory`。

worker 函数：

```python
def shared_mean(args):
    name, shape, dtype_str, start, stop = args

    existing = shared_memory.SharedMemory(name=name)
    try:
        arr = np.ndarray(
            shape,
            dtype=np.dtype(dtype_str),
            buffer=existing.buf,
        )
        return float(arr[start:stop].mean())
    finally:
        existing.close()
```

主进程创建共享内存：

```python
if __name__ == "__main__":
    data = np.arange(100_000, dtype=np.float64)

    shm = shared_memory.SharedMemory(create=True, size=data.nbytes)
    shared_arr = np.ndarray(data.shape, dtype=data.dtype, buffer=shm.buf)
    shared_arr[:] = data

    jobs = [
        (shm.name, data.shape, data.dtype.str, 0, 25_000),
        (shm.name, data.shape, data.dtype.str, 25_000, 50_000),
        (shm.name, data.shape, data.dtype.str, 50_000, 75_000),
        (shm.name, data.shape, data.dtype.str, 75_000, 100_000),
    ]

    try:
        with ProcessPoolExecutor(max_workers=4) as executor:
            means = list(executor.map(shared_mean, jobs))
    finally:
        shm.close()
        shm.unlink()

    print(means)
```

共享内存减少了大数组复制，但增加了资源管理复杂度。一定要 `close()` 和 `unlink()`，否则可能泄露共享内存资源。

## pandas 并行的注意点

pandas DataFrame 在进程间传递时也需要 pickle。大 DataFrame 复制成本很高。

更稳妥的方式：

- 按日期、资产、文件分片。
- 每个进程读取自己的分片。
- 每个进程输出小结果，例如指标表或文件路径。
- 主进程负责合并结果。

例子：按资产分片计算均值。

```python
def summarize_asset(group):
    asset, frame = group
    return {
        "asset": asset,
        "mean_return": frame["return"].mean(),
        "volatility": frame["return"].std(),
    }


panel = pd.DataFrame({
    "asset": ["AAA", "AAA", "BBB", "BBB", "CCC", "CCC"],
    "return": [0.01, -0.02, 0.03, 0.01, -0.01, 0.02],
})

groups = list(panel.groupby("asset"))

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=2) as executor:
        rows = list(executor.map(summarize_asset, groups))

    summary = pd.DataFrame(rows).sort_values("asset").reset_index(drop=True)

    print(summary)
```

这个例子数据很小，只是说明接口。真实任务中要警惕把大量 DataFrame group 直接 pickle 给 worker。

## 随机数和可复现性

多进程里不要让所有 worker 使用同一个隐式随机状态。应该给每个任务明确 seed。

```python
def random_stat(seed):
    rng = np.random.default_rng(seed)
    sample = rng.normal(size=1_000)
    return float(sample.mean())


seeds = [10, 11, 12, 13]

if __name__ == "__main__":
    with ProcessPoolExecutor(max_workers=4) as executor:
        stats = list(executor.map(random_stat, seeds))

    print(stats)
```

每个 worker 根据自己的 seed 创建随机数生成器，结果更容易复现。

## 进程数不是越多越好

常见选择：

```python
workers = min(4, os.cpu_count() or 1)
```

不要盲目使用全部 CPU。原因：

- 每个进程都需要内存。
- NumPy / BLAS 可能内部已经开多线程。
- 太多进程会造成上下文切换。
- 机器上可能还有其他任务。

在数值计算中，如果每个进程内部又调用多线程 BLAS，可能出现过度并行。必要时用环境变量限制底层线程数，例如 `OMP_NUM_THREADS`、`MKL_NUM_THREADS`、`OPENBLAS_NUM_THREADS`。

## 什么时候不该用 multiprocessing

不适合的场景：

- 数据很小，进程启动和通信开销超过计算时间。
- 任务主要是 NumPy 大矩阵运算，底层已经高效并行。
- 每个任务都要传输巨大 DataFrame 或数组。
- 任务之间共享大量可变状态。
- 逻辑主要等待网络或磁盘，线程或异步可能更合适。

适合的场景：

- 每个任务相对独立。
- 每个任务计算量大。
- 输入输出参数较小，或者能按文件/分片读取。
- 结果可以在主进程简单合并。
- 需要绕开纯 Python CPU 循环的 GIL 限制。

## 常见坑

第一，忘记 `if __name__ == "__main__"`。

在 `spawn` 启动方式下，子进程会重新导入主模块。没有主入口保护，可能无限创建子进程。

第二，把 lambda 或嵌套函数交给进程池。

worker 函数要能被 pickle。最稳妥的方式是定义在模块顶层。

第三，把大数组当参数传给每个任务。

这可能导致大量序列化、复制和内存峰值。优先传路径、区间、小参数，或者使用共享内存。

第四，进程数开太多。

进程数太多会造成内存压力和调度开销。先从少量 worker 开始测试。

第五，没有处理异常。

worker 中的异常会在 `future.result()` 或 `executor.map` 消费结果时抛出。要让主进程能记录失败任务。

## 实战提示

使用 multiprocessing 前，先问：

1. 任务是不是 CPU-bound？
2. 单个任务是否足够大？
3. 参数和返回值是否足够小？
4. worker 函数是否在模块顶层？
5. 是否需要共享内存、文件分片或 memory map？
6. NumPy / BLAS 是否已经在内部并行？
7. 是否已经用 profiler 确认瓶颈？

一个保守模板：

```python
def worker(task):
    task_id, seed, n = task
    rng = np.random.default_rng(seed)
    sample = rng.normal(size=n)
    return {
        "task_id": task_id,
        "mean": float(sample.mean()),
        "std": float(sample.std()),
    }


def run_parallel(tasks, max_workers=None):
    if max_workers is None:
        max_workers = min(4, os.cpu_count() or 1)

    rows = []

    with ProcessPoolExecutor(max_workers=max_workers) as executor:
        futures = [executor.submit(worker, task) for task in tasks]

        for future in as_completed(futures):
            rows.append(future.result())

    return pd.DataFrame(rows).sort_values("task_id").reset_index(drop=True)


if __name__ == "__main__":
    tasks = [
        (0, 100, 10_000),
        (1, 101, 10_000),
        (2, 102, 10_000),
        (3, 103, 10_000),
    ]

    result = run_parallel(tasks)
    print(result)
```

这个模板有几个优点：worker 顶层定义、任务参数小、结果小、主进程统一合并、worker 数量有上限。

## 小结

本节的重点：

- multiprocessing 用多个进程绕开 GIL，适合 CPU-bound 的独立任务。
- 进程之间传数据通常要 pickle，大对象传输成本很高。
- worker 函数应定义在模块顶层，脚本入口使用 `if __name__ == "__main__"`。
- `ProcessPoolExecutor.map` 适合顺序收集结果，`as_completed` 适合谁先完成先处理。
- `chunksize` 能减少大量小任务的调度开销。
- 大数组可以考虑共享内存，但要正确 `close` 和 `unlink`。
- 进程数不是越多越好，要警惕内存压力和底层库过度并行。

## 自检问题

1. multiprocessing 为什么能绕开 GIL？
2. 为什么不建议把大 NumPy 数组直接作为参数传给每个 worker？
3. `executor.map` 和 `as_completed` 在结果顺序上有什么区别？
4. 为什么跨平台脚本要写 `if __name__ == "__main__"`？
5. 哪些场景不适合使用 multiprocessing？
