# 78. 数据结构与算法：graph basics 的表示、遍历和依赖关系应用

## 核心概念

graph 是图。

图由两类对象组成：

```text
vertex / node  节点
edge           边
```

例如：

```text
A -> B
A -> C
B -> D
C -> D
```

这里 `A`、`B`、`C`、`D` 是节点，箭头是边。

图适合描述：

- 关系。
- 路径。
- 依赖。
- 连接性。
- 传播过程。
- 状态转移。

在量化和工程中，图可以表示：

```text
因子计算依赖关系
数据任务调度顺序
交易事件处理链路
股票之间的相关性网络
订单路由中的 venue 连接
风控规则之间的依赖
```

## 有向图和无向图

有向图的边有方向：

```text
A -> B
```

表示可以从 `A` 到 `B`，但不一定能从 `B` 到 `A`。

适合表示依赖关系：

```text
raw_price -> return -> rolling_vol -> risk_feature
```

无向图的边没有方向：

```text
A -- B
```

表示 `A` 和 `B` 互相连接。

适合表示对称关系：

```text
股票 A 和股票 B 的相关性超过阈值
服务器 A 和服务器 B 之间有连接
```

## 加权图

边也可以带权重。

```text
A -- B, weight = 0.8
B -- C, weight = 0.3
```

权重可以表示：

- 距离。
- 成本。
- 延迟。
- 相关性。
- 转移概率。
- 交易成本。

本篇先关注 graph basics：表示、遍历和依赖顺序。

加权最短路、最小生成树等属于更具体的图算法。

## 邻接表

最常见的图表示方式是 adjacency list，邻接表。

有向图：

```python
graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D"],
    "D": [],
}
```

含义：

```text
A 可以到 B、C
B 可以到 D
C 可以到 D
D 没有后继
```

邻接表适合稀疏图。

如果节点很多，但边不算太多，邻接表比邻接矩阵更省空间。

复杂度通常是：

```text
遍历某个节点的邻居：O(degree(node))
遍历整张图：O(V + E)
```

其中：

```text
V = 节点数
E = 边数
```

## 无向图的邻接表

无向边要在两个方向都记录。

```python
from collections import defaultdict

edges = [
    ("AAPL", "MSFT"),
    ("MSFT", "NVDA"),
    ("JPM", "BAC"),
]

graph = defaultdict(list)

for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)

print(dict(graph))
```

结果：

```text
{'AAPL': ['MSFT'], 'MSFT': ['AAPL', 'NVDA'], 'NVDA': ['MSFT'], 'JPM': ['BAC'], 'BAC': ['JPM']}
```

这可以表示一个简单的相关性网络：

```text
AAPL -- MSFT -- NVDA
JPM  -- BAC
```

## 邻接矩阵

另一种表示是 adjacency matrix，邻接矩阵。

如果有 `n` 个节点，就建一个 `n x n` 矩阵：

```text
matrix[i][j] = 1 表示 i -> j 有边
matrix[i][j] = 0 表示 i -> j 无边
```

例子：

```python
nodes = ["A", "B", "C"]
index = {node: i for i, node in enumerate(nodes)}

matrix = [
    [0, 1, 1],
    [0, 0, 1],
    [0, 0, 0],
]

has_edge = matrix[index["A"]][index["C"]]
print(has_edge)
```

结果：

```text
1
```

邻接矩阵的特点：

- 查询某条边是否存在：`O(1)`。
- 空间复杂度：`O(V^2)`。
- 稀疏图会浪费空间。
- 稠密图或矩阵运算场景中可能有用。

## BFS：广度优先搜索

BFS 是 breadth-first search。

它从一个起点出发，先访问距离起点最近的一层，再访问下一层。

常用 `deque` 实现。

```python
from collections import deque

graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": ["F"],
    "E": [],
    "F": [],
}

def bfs(graph, start):
    visited = {start}
    queue = deque([start])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for nxt in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append(nxt)

    return order

print(bfs(graph, "A"))
```

结果：

```text
['A', 'B', 'C', 'D', 'E', 'F']
```

BFS 适合：

- 找无权图最短步数。
- 分层传播。
- 从一个节点找可达范围。
- 在依赖链上找影响范围。

时间复杂度：

```text
O(V + E)
```

## BFS 求最少边数路径

如果每条边成本相同，BFS 可以求最少边数路径。

```python
from collections import deque

graph = {
    "raw_price": ["return"],
    "return": ["rolling_mean", "rolling_vol"],
    "rolling_mean": ["signal"],
    "rolling_vol": ["signal"],
    "signal": ["portfolio"],
    "portfolio": [],
}

def shortest_path_unweighted(graph, start, target):
    queue = deque([(start, [start])])
    visited = {start}

    while queue:
        node, path = queue.popleft()

        if node == target:
            return path

        for nxt in graph[node]:
            if nxt not in visited:
                visited.add(nxt)
                queue.append((nxt, path + [nxt]))

    return None

path = shortest_path_unweighted(graph, "raw_price", "portfolio")
print(path)
```

结果：

```text
['raw_price', 'return', 'rolling_mean', 'signal', 'portfolio']
```

这里返回的是一条最少边数路径。

如果边有不同权重，就不能直接用 BFS 求最短成本，需要 Dijkstra 等算法。

## DFS：深度优先搜索

DFS 是 depth-first search。

它沿着一条路径尽可能往深处走，走不下去再回退。

递归写法：

```python
graph = {
    "A": ["B", "C"],
    "B": ["D"],
    "C": ["D", "E"],
    "D": ["F"],
    "E": [],
    "F": [],
}

def dfs_recursive(graph, node, visited=None, order=None):
    if visited is None:
        visited = set()
    if order is None:
        order = []

    visited.add(node)
    order.append(node)

    for nxt in graph[node]:
        if nxt not in visited:
            dfs_recursive(graph, nxt, visited, order)

    return order

print(dfs_recursive(graph, "A"))
```

一种可能结果：

```text
['A', 'B', 'D', 'F', 'C', 'E']
```

DFS 适合：

- 检查可达性。
- 找连通分量。
- 检测环。
- 拓扑排序。
- 遍历组合状态空间。

时间复杂度同样是：

```text
O(V + E)
```

## 迭代 DFS

递归 DFS 对很深的图可能遇到递归深度限制。

可以用 stack 改成迭代版。

```python
def dfs_iterative(graph, start):
    visited = set()
    stack = [start]
    order = []

    while stack:
        node = stack.pop()

        if node in visited:
            continue

        visited.add(node)
        order.append(node)

        for nxt in reversed(graph[node]):
            if nxt not in visited:
                stack.append(nxt)

    return order

print(dfs_iterative(graph, "A"))
```

这里用 `reversed(graph[node])` 是为了让结果顺序更接近递归 DFS。

## 连通分量

在无向图中，connected component 是连通分量。

如果两个股票在同一个连通分量里，说明它们可以通过若干条边连接起来。

例子：

```python
from collections import defaultdict, deque

edges = [
    ("AAPL", "MSFT"),
    ("MSFT", "NVDA"),
    ("JPM", "BAC"),
]

graph = defaultdict(list)
for a, b in edges:
    graph[a].append(b)
    graph[b].append(a)

def connected_components(graph):
    visited = set()
    components = []

    for start in graph:
        if start in visited:
            continue

        queue = deque([start])
        visited.add(start)
        component = []

        while queue:
            node = queue.popleft()
            component.append(node)

            for nxt in graph[node]:
                if nxt not in visited:
                    visited.add(nxt)
                    queue.append(nxt)

        components.append(component)

    return components

print(connected_components(graph))
```

结果：

```text
[['AAPL', 'MSFT', 'NVDA'], ['JPM', 'BAC']]
```

这可以用来粗略识别：

- 相关性网络中的簇。
- 风险暴露类似的股票组。
- 数据依赖中互相影响的模块组。

## DAG 与拓扑排序

DAG 是 directed acyclic graph。

意思是：

```text
有向无环图
```

依赖关系通常应该是一张 DAG。

例如：

```text
raw_price -> return -> rolling_vol -> signal -> portfolio
```

如果出现：

```text
signal -> rolling_vol -> signal
```

就形成了环，计算顺序会变得不明确。

拓扑排序用于给 DAG 找一个合法执行顺序。

如果 `A -> B` 表示 `B` 依赖 `A`，那么排序结果里 `A` 必须排在 `B` 前面。

## Kahn 算法：拓扑排序

Kahn 算法维护每个节点的入度。

入度是指：

```text
有多少条边指向这个节点
```

入度为 0 的节点表示没有未完成依赖，可以先执行。

```python
from collections import defaultdict, deque

dependencies = {
    "raw_price": ["return"],
    "return": ["rolling_mean", "rolling_vol"],
    "rolling_mean": ["signal"],
    "rolling_vol": ["signal"],
    "signal": ["portfolio"],
    "portfolio": [],
}

def topological_sort(graph):
    indegree = {node: 0 for node in graph}

    for node, neighbors in graph.items():
        for nxt in neighbors:
            indegree.setdefault(nxt, 0)
            indegree[nxt] += 1

    queue = deque([node for node, deg in indegree.items() if deg == 0])
    order = []

    while queue:
        node = queue.popleft()
        order.append(node)

        for nxt in graph.get(node, []):
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)

    if len(order) != len(indegree):
        raise ValueError("graph has a cycle")

    return order

print(topological_sort(dependencies))
```

一种合法结果：

```text
['raw_price', 'return', 'rolling_mean', 'rolling_vol', 'signal', 'portfolio']
```

`rolling_mean` 和 `rolling_vol` 谁先谁后都可以，因为它们都只依赖 `return`，并且都被 `signal` 依赖。

## 检测依赖环

如果依赖图中有环，拓扑排序无法覆盖所有节点。

```python
bad_dependencies = {
    "return": ["signal"],
    "signal": ["rolling_vol"],
    "rolling_vol": ["signal"],
}

try:
    topological_sort(bad_dependencies)
except ValueError as exc:
    print(str(exc))
```

结果：

```text
graph has a cycle
```

这对 feature pipeline 很重要。

如果计算依赖出现环，系统应该在运行前报错，而不是在运行中死循环或得到不可靠结果。

## 反向图：找下游影响

有时候你拿到的是：

```text
A -> B 表示 B 依赖 A
```

如果 `A` 改了，想知道哪些节点受影响，可以沿原图往下游走。

如果想从某个输出反查它依赖哪些输入，可以建立 reverse graph。

```python
from collections import defaultdict

graph = {
    "raw_price": ["return"],
    "return": ["rolling_mean", "rolling_vol"],
    "rolling_mean": ["signal"],
    "rolling_vol": ["signal"],
    "signal": ["portfolio"],
    "portfolio": [],
}

reverse_graph = defaultdict(list)

for node, neighbors in graph.items():
    reverse_graph.setdefault(node, [])
    for nxt in neighbors:
        reverse_graph[nxt].append(node)

print(dict(reverse_graph))
```

结果：

```text
{'raw_price': [], 'return': ['raw_price'], 'rolling_mean': ['return'], 'rolling_vol': ['return'], 'signal': ['rolling_mean', 'rolling_vol'], 'portfolio': ['signal']}
```

这样从 `portfolio` 出发，就能反查它依赖哪些上游节点。

## 小例子：找一个输出的全部上游依赖

```python
def collect_upstream(reverse_graph, target):
    stack = [target]
    visited = set()

    while stack:
        node = stack.pop()

        for parent in reverse_graph.get(node, []):
            if parent not in visited:
                visited.add(parent)
                stack.append(parent)

    return visited

upstream = collect_upstream(reverse_graph, "portfolio")
print(sorted(upstream))
```

结果：

```text
['raw_price', 'return', 'rolling_mean', 'rolling_vol', 'signal']
```

这类逻辑可用于：

- 判断某个因子改动会影响哪些组合结果。
- 解释某个模型输入来自哪些原始字段。
- 做缓存失效和增量计算。

## 图遍历中的常见错误

### 错误 1：忘记 visited

如果图里有环，遍历时不维护 `visited`，可能无限循环。

```text
A -> B -> A
```

BFS 和 DFS 通常都需要 `visited`。

### 错误 2：默认所有节点都出现在 graph 的 key 里

有些节点只作为邻居出现。

```python
graph = {
    "A": ["B"],
}
```

这里 `B` 没有作为 key 出现。

遍历时如果写 `graph[node]`，访问 `B` 时可能报错。

更稳妥：

```python
for nxt in graph.get(node, []):
    ...
```

或者构建图时保证每个节点都有 key。

### 错误 3：把有向图当无向图

如果 `A -> B` 表示依赖关系，不能随便认为 `B -> A` 也成立。

方向错了会导致：

- 执行顺序错。
- 影响范围错。
- 上游和下游解释反了。

### 错误 4：拓扑排序没检查环

依赖图必须检查是否有环。

如果没有检查 `len(order) != len(nodes)`，可能只得到部分排序结果，然后误以为依赖顺序有效。

### 错误 5：递归 DFS 太深

很深的图可能触发 Python 递归深度限制。

生产代码中，如果图深度不可控，优先考虑迭代 DFS 或显式栈。

## 什么时候用图

适合用图的场景：

- 你关心对象之间的关系。
- 你需要从一个节点找可达范围。
- 你需要检查多个模块之间的依赖顺序。
- 你需要检测依赖环。
- 你需要把相关资产分成若干连接簇。
- 你需要追踪某个字段或因子的上下游影响。

不一定需要图的场景：

- 数据只是单纯表格，没有关系结构。
- 只需要线性扫描。
- 只需要按时间排序。
- 依赖关系可以用简单列表清楚表达。

## 记忆要点

- 图由节点和边组成。
- 有向图适合表达依赖，无向图适合表达对称连接。
- 邻接表适合稀疏图，邻接矩阵适合快速查边或稠密图。
- BFS 按层遍历，常用于无权最短步数和影响范围。
- DFS 沿路径深入，常用于可达性、连通分量和环检测。
- 整图遍历复杂度通常是 `O(V + E)`。
- DAG 可以做拓扑排序。
- 依赖图要检查环。
- reverse graph 可以反查上游依赖。

## 自测题

1. 邻接表和邻接矩阵分别适合什么情况？
2. BFS 和 DFS 的遍历方式有什么区别？
3. 为什么依赖图通常应该是 DAG？
4. 拓扑排序中入度为 0 的节点代表什么？
5. 如果 `A -> B` 表示 `B` 依赖 `A`，如何找 `B` 的全部上游依赖？
