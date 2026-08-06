# 136. 计算机基础：Docker、容器、镜像、环境复现和分布式计算框架

## 核心概念

Docker 和分布式计算解决的是两个不同问题。

Docker 主要解决：

```text
同一份代码在不同机器上环境不一致
```

分布式计算主要解决：

```text
单机算不动或放不下的数据，如何拆到多台机器上处理
```

在量化和机器学习项目里，这两个问题都很常见。

例如：

```text
本地回测能跑，服务器缺依赖
研究环境和生产环境 Python 版本不同
单机处理全市场 tick 数据太慢
大规模特征工程需要并行处理
```

## 环境不一致

环境不一致会导致非常隐蔽的问题。

例如：

```python
local_env = {
    "python": "3.11",
    "numpy": "1.26",
}
prod_env = {
    "python": "3.10",
    "numpy": "1.26",
}

differences = {
    key: (local_env[key], prod_env[key])
    for key in local_env
    if local_env[key] != prod_env.get(key)
}

print(differences)
```

结果：

```text
{'python': ('3.11', '3.10')}
```

这表示本地和生产环境 Python 版本不同。

有些库行为、类型提示、性能和依赖解析可能因此不同。

Docker 的价值就是把运行环境写成代码。

## 镜像和容器

Docker 里有两个基础概念：

```text
image: 镜像，静态模板
container: 容器，从镜像启动出来的运行实例
```

可以类比成：

```text
image 像 class
container 像 object
```

小例子：

```python
image = "research-env:2026-01"
container = "run-42"

print(f"image={image}")
print(f"container={container}")
```

结果：

```text
image=research-env:2026-01
container=run-42
```

同一个 image 可以启动很多 container。

每个 container 可以运行不同任务。

## Dockerfile

Dockerfile 描述如何构建镜像。

一个极简例子：

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .
CMD ["python", "main.py"]
```

含义：

```text
FROM: 基础镜像
WORKDIR: 容器内工作目录
COPY: 把文件复制进镜像
RUN: 构建镜像时执行命令
CMD: 容器启动时默认执行命令
```

Dockerfile 应该和代码一起版本控制。

这样别人能知道环境如何构建。

## build 和 run

常见命令：

```bash
docker build -t research-env:2026-01 .
docker run --rm research-env:2026-01
```

含义：

```text
docker build: 根据 Dockerfile 构建 image
docker run: 从 image 启动 container
--rm: 运行结束后删除 container
```

如果需要把本地目录挂进容器：

```bash
docker run --rm -v "$PWD":/app research-env:2026-01
```

`-v` 是 volume mount。

它让容器能读写宿主机目录。

## 不要把状态都塞进容器

容器应该尽量是可重建的。

不要依赖：

```text
手动进入容器安装包
在容器里临时改代码
把唯一数据存在容器内部
```

更好的做法：

```text
代码进 Git
环境进 Dockerfile
依赖进 requirements.txt 或 lock 文件
数据挂载或外部存储
结果写到明确输出目录
```

这样容器删掉也不怕。

因为环境可以重新构建。

## Docker 在策略项目中的用途

常见用途：

```text
固定 Python 和系统依赖版本
统一研究、回测和生产环境
封装模型推理服务
在 CI 中运行测试
隔离不同项目依赖
复现实验报告
```

例如一个回测项目可以规定：

```text
image: backtest-env:2026-01
command: python run_backtest.py --config configs/base.yaml
data mounted at: /data
outputs written to: /outputs
```

这比只说“我本地能跑”可靠得多。

## 分布式计算

分布式计算把任务拆到多台机器或多个进程上。

基本思想是：

```text
把数据切成多个 partition
每个 worker 处理一部分
最后合并结果
```

小例子，把数据分成三个 partition：

```python
data = list(range(10))
num_partitions = 3

partitions = [
    data[i::num_partitions]
    for i in range(num_partitions)
]

print(partitions)
```

结果：

```text
[[0, 3, 6, 9], [1, 4, 7], [2, 5, 8]]
```

每个 partition 可以交给不同 worker。

## map 和 reduce

分布式计算常见模式是 map-reduce。

```text
map: 每个分区独立计算
reduce: 合并分区结果
```

例如分区求和：

```python
partitions = [
    [1, 2, 3],
    [4, 5],
    [6],
]

partial_sums = [
    sum(partition)
    for partition in partitions
]
total = sum(partial_sums)

print(partial_sums)
print(total)
```

结果：

```text
[6, 9, 6]
21
```

每个分区先独立求和。

最后把局部结果加起来。

## shuffle

不是所有任务都能只靠独立分区完成。

按 key 聚合时，需要把相同 key 的数据放到一起。

这叫 shuffle。

```python
records = [
    ("AAA", 10),
    ("BBB", 20),
    ("AAA", 15),
    ("BBB", 5),
]

groups = {}
for key, value in records:
    groups.setdefault(key, []).append(value)

aggregated = {
    key: sum(values)
    for key, values in groups.items()
}

print(aggregated)
```

结果：

```text
{'AAA': 25, 'BBB': 25}
```

在真实分布式系统里，shuffle 可能很贵。

因为它需要跨机器移动数据。

很多 Spark 性能问题都来自 shuffle 太多或数据倾斜。

## Spark 基本概念

Spark 是常见分布式计算框架。

核心概念：

```text
driver: 负责任务调度的主程序
executor: 执行具体计算的工作进程
partition: 数据切片
job / stage / task: Spark 的执行层级
shuffle: 跨分区重分布数据
```

写 Spark 程序时，要关心：

```text
数据分区是否合理
是否频繁 shuffle
是否有数据倾斜
中间结果是否需要缓存
输出文件数量是否过多
```

Spark 不是自动让所有代码变快。

如果任务很小，Spark 的调度开销可能比计算本身更大。

## 分区规模

分区太少，并行度不够。

分区太多，调度开销变大。

例如 `1,000,000` 行数据分成 `100` 个 partition：

```python
rows = 1_000_000
partitions = 100

rows_per_partition = rows // partitions

print(rows_per_partition)
```

结果：

```text
10000
```

平均每个 partition 有 `10,000` 行。

真实数据里还要考虑：

```text
行大小
压缩格式
机器内存
任务耗时
key 分布是否均匀
```

## 文件过滤

大数据任务通常先筛选文件，再读取。

例如只处理价格文件：

```python
files = [
    "prices_2026_01.csv",
    "prices_2026_02.csv",
    "fundamentals.csv",
]

price_files = [
    name
    for name in files
    if name.startswith("prices_")
]

print(price_files)
```

结果：

```text
['prices_2026_01.csv', 'prices_2026_02.csv']
```

真实系统里，如果文件组织得好，可以减少大量无效扫描。

例如：

```text
/data/prices/date=2026-01-01/
/data/prices/date=2026-01-02/
```

这种分区目录能帮助查询只读取需要的日期。

## 什么时候需要分布式

不是什么任务都应该上 Spark。

适合分布式的场景：

```text
单机内存放不下
单机运行时间太长
数据天然可以按日期或资产分片
需要处理 TB 级日志、tick 或特征
需要定期批处理大规模数据
```

不适合的场景：

```text
数据只有几 MB
逻辑强依赖全局顺序
频繁小任务交互
本地 pandas 几秒能完成
```

先用简单工具解决问题。

只有瓶颈明确时，再引入分布式系统。

## Docker 和 Spark 的关系

Docker 可以封装 Spark 作业运行环境。

例如：

```text
同一个镜像里固定 Python、Java、依赖库和作业代码
在集群上用这个镜像启动 executor
保证 driver 和 executor 环境一致
```

但 Docker 不是分布式计算本身。

它是环境封装工具。

Spark 才是任务调度和分布式计算框架。

两者可以一起用，但解决的问题不同。

## 常见错误

Docker 常见错误：

```text
镜像里写死本地绝对路径
把密钥打进镜像
不固定依赖版本
在容器里手动改环境但不更新 Dockerfile
把大数据复制进镜像
```

分布式计算常见错误：

```text
数据很小却上 Spark
以为 Spark 会自动优化所有 Python 代码
shuffle 太多
分区太少或太多
key 倾斜导致少数 worker 特别慢
没有记录输入数据版本和作业代码版本
```

这些错误都会影响复现性和性能。

## 小结

Docker 解决环境复现问题。

核心概念：

```text
image
container
Dockerfile
build
run
volume mount
```

分布式计算解决大规模数据处理问题。

核心概念：

```text
partition
worker / executor
driver
map
reduce
shuffle
data skew
```

在策略和数据项目中，判断顺序应该是：

```text
先确认单机是否足够
再固定环境
再优化算法和数据布局
最后才引入分布式框架
```

到这里，`knowledge/outline.md` 中的小册子知识点已经全部覆盖。
