# 机器学习：K-Means 的聚类目标、中心点更新、惯性、初始化和量化应用

## 核心概念

K-Means 是一种无监督聚类算法。

它不需要标签。

它要做的是：

```text
把样本分成 K 个簇，让同一簇内的样本尽量相似。
```

每个簇用一个中心点表示。

算法反复做两件事：

```text
1. 把每个样本分配给最近的中心点。
2. 用簇内样本均值更新中心点。
```

直到分配结果或中心点基本不变。

## K-Means 目标函数

K-Means 最小化的是簇内平方距离之和。

常叫 inertia 或 within-cluster sum of squares。

```text
inertia = sum(||x_i - center_assigned_to_i||^2)
```

inertia 越小，说明样本离自己的簇中心越近。

但 inertia 一定会随着 `K` 增大而下降。

所以不能只用最小 inertia 选 `K`。

## 距离计算

K-Means 默认使用欧氏距离。

两个二维点的平方距离：

```python
point = [1.0, 2.0]
center = [3.0, 5.0]

squared_distance = sum(
    (x - c) ** 2
    for x, c in zip(point, center)
)

print(squared_distance)
```

结果：

```text
13.0
```

这里距离平方是：

```text
(1 - 3)^2 + (2 - 5)^2 = 4 + 9 = 13
```

K-Means 使用距离，所以特征尺度非常重要。

## 分配样本到最近中心

给定两个中心点，把样本分配给距离最近的中心。

```python
point = [1.0, 1.0]
centers = {
    "A": [0.0, 0.0],
    "B": [5.0, 5.0],
}

def squared_distance(a, b):
    return sum((x - y) ** 2 for x, y in zip(a, b))

distances = {
    name: squared_distance(point, center)
    for name, center in centers.items()
}

assigned = min(distances, key=distances.get)

print(distances)
print(assigned)
```

结果：

```text
{'A': 2.0, 'B': 32.0}
A
```

样本 `[1, 1]` 离中心 `A` 更近。

所以它被分到簇 `A`。

## 更新中心点

一个簇的新中心点是簇内样本的均值。

```python
cluster_points = [
    [0.0, 0.0],
    [2.0, 0.0],
    [4.0, 3.0],
]

new_center = []
for dim in range(len(cluster_points[0])):
    dim_mean = sum(point[dim] for point in cluster_points) / len(cluster_points)
    new_center.append(dim_mean)

print(new_center)
```

结果：

```text
[2.0, 1.0]
```

中心点就是每个维度分别取平均。

## 一轮 K-Means

把分配和更新合在一起。

```python
points = [
    [0.0, 0.0],
    [1.0, 0.0],
    [5.0, 5.0],
    [6.0, 5.0],
]

centers = {
    "A": [0.0, 0.0],
    "B": [5.0, 5.0],
}

assignments = {}
for i, point in enumerate(points):
    distances = {
        name: squared_distance(point, center)
        for name, center in centers.items()
    }
    assignments[i] = min(distances, key=distances.get)

new_centers = {}
for name in centers:
    cluster = [
        point
        for i, point in enumerate(points)
        if assignments[i] == name
    ]
    new_centers[name] = [
        sum(point[dim] for point in cluster) / len(cluster)
        for dim in range(len(points[0]))
    ]

print(assignments)
print(new_centers)
```

结果：

```text
{0: 'A', 1: 'A', 2: 'B', 3: 'B'}
{'A': [0.5, 0.0], 'B': [5.5, 5.0]}
```

第一组点靠近 `A`。

第二组点靠近 `B`。

更新后中心分别移动到各自簇的均值。

## inertia

inertia 是每个样本到所属中心的平方距离总和。

```python
centers = {
    "A": [0.5, 0.0],
    "B": [5.5, 5.0],
}
assignments = {0: "A", 1: "A", 2: "B", 3: "B"}

inertia = 0.0
for i, point in enumerate(points):
    center = centers[assignments[i]]
    inertia += squared_distance(point, center)

print(inertia)
```

结果：

```text
1.0
```

四个点分别离中心的平方距离都是 `0.25`。

总和是 `1.0`。

## 迭代直到收敛

K-Means 会反复执行：

```text
assign step
update step
```

直到：

- 中心点变化很小。
- 样本分配不再变化。
- 达到最大迭代次数。

伪代码：

```python
centers = initialize_centers(points, k)

for step in range(max_iter):
    assignments = assign_points(points, centers)
    new_centers = recompute_centers(points, assignments)

    if center_shift(centers, new_centers) < tolerance:
        break

    centers = new_centers
```

K-Means 通常会收敛。

但可能收敛到局部最优。

## 初始化很重要

K-Means 对初始中心点敏感。

不同初始化可能得到不同聚类结果。

小例子：两个不同初始中心的距离。

```python
points = [[0.0], [1.0], [10.0], [11.0]]

init_good = [[0.0], [10.0]]
init_bad = [[0.0], [1.0]]

def total_distance_to_initial_centers(points, centers):
    total = 0.0
    for point in points:
        total += min(
            squared_distance(point, center)
            for center in centers
        )
    return total

print(total_distance_to_initial_centers(points, init_good))
print(total_distance_to_initial_centers(points, init_bad))
```

结果：

```text
2.0
181.0
```

好的初始化一开始就接近两个自然簇。

坏的初始化两个中心都在左边，初始 inertia 很大。

## K-Means++

K-Means++ 是一种更好的初始化方法。

直觉：

```text
第一个中心随机选。
后面的中心更倾向于选择离已有中心较远的点。
```

这样可以让初始中心更分散。

伪代码：

```python
centers = [random_point(points)]

while len(centers) < k:
    distances = [
        distance_to_nearest_center(point, centers)
        for point in points
    ]
    next_center = sample_point_with_probability_proportional_to_distance(distances)
    centers.append(next_center)
```

实际使用 sklearn 时，默认通常就是 `k-means++`。

## n_init

因为初始化有随机性，常常要运行多次 K-Means。

`n_init` 表示不同初始化运行多少次。

最后选择 inertia 最小的一次。

```python
run_inertias = [120.0, 95.0, 110.0]

best_inertia = min(run_inertias)
best_run = run_inertias.index(best_inertia)

print(best_inertia)
print(best_run)
```

结果：

```text
95.0
1
```

第 2 次运行效果最好。

这里索引从 `0` 开始，所以 `best_run = 1`。

## 选择 K

`K` 是簇数量。

选择太小，簇过粗。

选择太大，簇过细，可能只是把噪声拆开。

常见方法：

- elbow method。
- silhouette score。
- 业务解释。
- 样本外稳定性。
- 聚类后策略表现。

elbow method 看 inertia 随 K 增加下降是否开始变慢。

```python
inertia_by_k = {
    1: 300.0,
    2: 120.0,
    3: 80.0,
    4: 70.0,
}

improvements = {}
previous = None
for k, inertia_value in inertia_by_k.items():
    if previous is not None:
        improvements[k] = previous - inertia_value
    previous = inertia_value

print(improvements)
```

结果：

```text
{2: 180.0, 3: 40.0, 4: 10.0}
```

从 `K=2` 到 `K=3` 的改善明显变小。

这可能提示 `K=2` 是一个候选。

## silhouette 直觉

silhouette 衡量一个样本：

```text
离自己簇有多近，离其他簇有多远。
```

简化公式：

```text
score = (b - a) / max(a, b)
```

其中：

- `a` 是样本到同簇其他点的平均距离。
- `b` 是样本到最近其他簇的平均距离。

```python
a = 1.0
b = 4.0

silhouette = (b - a) / max(a, b)

print(silhouette)
```

结果：

```text
0.75
```

越接近 `1`，聚类越清晰。

越接近 `0`，样本在边界附近。

负数说明可能分错簇。

## 特征标准化

K-Means 对尺度非常敏感。

因为它直接使用欧氏距离。

```python
point_a = [100.0, 0.01]
point_b = [110.0, 0.02]

distance = squared_distance(point_a, point_b)

print(distance)
```

结果：

```text
100.0001
```

距离几乎完全由第一个维度决定。

如果两个特征是不同量纲，必须标准化。

而且标准化参数只能用训练期估计。

## 异常值影响

K-Means 用均值作为中心。

均值容易被异常值拉动。

```python
values = [0.0, 1.0, 2.0, 100.0]

mean_value = sum(values) / len(values)

print(mean_value)
```

结果：

```text
25.75
```

一个异常值 `100` 把中心拉到 `25.75`。

所以聚类前常要：

- winsorize。
- 去极端值。
- 标准化。
- 检查异常样本。

## K-Means 在量化中的用途

K-Means 可以用于：

- 股票风格聚类。
- 市场状态聚类。
- 因子暴露聚类。
- 行业外的相似股票分组。
- 风险特征聚类。
- 特征工程中的 regime 标签。

例如用两个特征聚类市场状态：

```text
realized volatility
cross-sectional dispersion
```

聚出来的簇可能对应：

```text
低波动低分散
高波动高分散
中等波动
```

但聚类标签本身没有天然含义。

需要研究者解释。

## 聚类标签不是预测标签

K-Means 是无监督学习。

它不知道未来收益。

所以：

```text
聚类清晰，不代表有预测收益。
```

如果把 K-Means 聚类用于量化策略，要继续验证：

- 每个簇的未来收益是否不同。
- 每个簇的风险是否不同。
- 簇标签是否样本外稳定。
- 簇切换是否带来过高换手。
- 扣成本后是否仍有价值。

小例子：

```python
future_returns_by_cluster = {
    0: [0.01, 0.02, 0.00],
    1: [-0.01, 0.00, -0.02],
}

mean_return_by_cluster = {
    cluster: sum(values) / len(values)
    for cluster, values in future_returns_by_cluster.items()
}

print(mean_return_by_cluster)
```

结果：

```text
{0: 0.01, 1: -0.01}
```

这个例子里，两个簇的未来收益不同。

真实研究中还需要样本外检验和显著性检查。

## 时间序列注意事项

如果用 K-Means 生成 regime 标签，也要避免未来信息泄露。

错误做法：

```text
用全样本 fit 聚类中心，再给历史每一天打标签
```

这会让历史标签使用未来分布信息。

更安全的做法：

```python
for train_period, valid_period in walk_forward_splits:
    scaler.fit(features[train_period])
    x_train = scaler.transform(features[train_period])
    x_valid = scaler.transform(features[valid_period])

    kmeans.fit(x_train)
    valid_cluster = kmeans.predict(x_valid)
```

聚类中心和标准化参数都只能从训练期估计。

## 常见误区

第一，不标准化特征。

第二，只看 inertia，直接选择最大 K。

第三，以为聚类标签天然有经济含义。

第四，用全样本 fit 聚类中心导致未来信息泄露。

第五，不检查不同初始化下聚类是否稳定。

第六，忽略异常值对中心点的影响。

第七，聚类清晰但不验证未来收益和交易成本。

## 小结

K-Means 是一种简单、常用的无监督聚类方法。

它反复执行：

```text
分配样本到最近中心
用簇内均值更新中心
```

目标是最小化簇内平方距离，也就是 inertia。

在量化机器学习里，K-Means 可以帮助做风格聚类、状态聚类和相似样本分组。

但它必须配合：

```text
标准化
稳健初始化
K 的合理选择
时间序列防泄露
样本外收益和风险验证
```
