# 82. 数据结构与算法：order book simulation 的价格档位、订单事件和撮合规则

## 核心概念

order book 是订单簿。

它记录某个交易标的当前未成交的买卖订单。

最基本的两侧是：

```text
bid  买盘，愿意买入的订单
ask  卖盘，愿意卖出的订单
```

最优价格：

```text
best bid = 最高买价
best ask = 最低卖价
```

如果：

```text
best bid = 100.00
best ask = 100.05
```

那么：

```text
spread = best ask - best bid = 0.05
mid    = (best ask + best bid) / 2 = 100.025
```

order book simulation 是用程序模拟订单如何进入订单簿、如何成交、如何撤销。

它适合训练：

- hashmap。
- heap。
- deque。
- sorting。
- stream processing。
- 事件驱动模拟。

## L1、L2 和 L3

行情深度常见三种层次。

L1 只看最优买卖价：

```text
best bid price / size
best ask price / size
```

L2 看价格档位：

```text
price -> total size
```

例如：

```text
bid:
100.00: 300
 99.95: 500

ask:
100.05: 200
100.10: 400
```

L3 看每个订单：

```text
order_id -> side, price, quantity, timestamp
```

同一个价格档位里，订单之间通常有时间优先级。

本篇主要用简化 L3 订单簿讲数据结构。

## 价格时间优先

很多撮合规则可以简化成：

```text
价格优先
时间优先
```

买单侧：

```text
价格越高，优先级越高
同一价格下，先来的订单先成交
```

卖单侧：

```text
价格越低，优先级越高
同一价格下，先来的订单先成交
```

所以数据结构通常是：

```text
side -> price -> FIFO queue of orders
```

在 Python 里可以用：

```text
dict[price] = deque([order_id_1, order_id_2, ...])
orders[order_id] = order detail
```

`dict` 用来定位价格档位。

`deque` 用来维护同一价格内的时间顺序。

## 基础 L2 订单簿

如果只模拟 L2，也就是每个价格档位的总量，可以非常简单。

```python
book = {
    "bid": {},
    "ask": {},
}

def apply_l2_update(book, side, price, size):
    levels = book[side]

    if size == 0:
        levels.pop(price, None)
    else:
        levels[price] = size

apply_l2_update(book, "bid", 100.00, 300)
apply_l2_update(book, "bid", 99.95, 500)
apply_l2_update(book, "ask", 100.05, 200)
apply_l2_update(book, "bid", 100.00, 0)

print(book)
```

结果：

```text
{'bid': {99.95: 500}, 'ask': {100.05: 200}}
```

L2 不知道每个订单是谁，也不知道同一价格档位内部的排队顺序。

它适合：

- 重建行情深度。
- 计算 spread 和 imbalance。
- 做较粗粒度回放。

但不适合精确模拟自己的订单排队位置。

## L1 指标

从 L2 book 里可以计算 best bid、best ask、spread 和 mid。

```python
def best_bid(book):
    if not book["bid"]:
        return None
    return max(book["bid"])

def best_ask(book):
    if not book["ask"]:
        return None
    return min(book["ask"])

def top_of_book(book):
    bid = best_bid(book)
    ask = best_ask(book)

    if bid is None or ask is None:
        return {"bid": bid, "ask": ask, "spread": None, "mid": None}

    return {
        "bid": bid,
        "ask": ask,
        "spread": ask - bid,
        "mid": (ask + bid) / 2,
    }

print(top_of_book({
    "bid": {100.00: 300, 99.95: 500},
    "ask": {100.05: 200, 100.10: 400},
}))
```

结果：

```text
{'bid': 100.0, 'ask': 100.05, 'spread': 0.04999999999999716, 'mid': 100.025}
```

浮点价格可能有精度问题。

生产系统常用整数 tick 表示价格，例如：

```text
100.05 -> 10005
```

## 简化 L3 订单簿

下面实现一个简化订单簿。

为了让逻辑清楚，它用：

```text
bids: price -> deque(order_id)
asks: price -> deque(order_id)
orders: order_id -> order detail
```

其中 order detail 保存：

```text
side
price
qty
```

这不是高性能撮合引擎，只是为了讲清楚数据结构。

```python
from collections import deque


class SimpleOrderBook:
    def __init__(self):
        self.bids = {}
        self.asks = {}
        self.orders = {}

    def best_bid(self):
        self._clean_empty_levels(self.bids)
        if not self.bids:
            return None
        return max(self.bids)

    def best_ask(self):
        self._clean_empty_levels(self.asks)
        if not self.asks:
            return None
        return min(self.asks)

    def top_of_book(self):
        bid = self.best_bid()
        ask = self.best_ask()

        if bid is None or ask is None:
            return {"bid": bid, "ask": ask, "spread": None, "mid": None}

        return {
            "bid": bid,
            "ask": ask,
            "spread": ask - bid,
            "mid": (ask + bid) / 2,
        }

    def add_limit_order(self, order_id, side, price, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if side not in {"buy", "sell"}:
            raise ValueError("side must be buy or sell")

        trades = []

        if side == "buy":
            qty = self._match_buy(order_id, price, qty, trades)
            if qty > 0:
                self._rest_order(order_id, side, price, qty)
        else:
            qty = self._match_sell(order_id, price, qty, trades)
            if qty > 0:
                self._rest_order(order_id, side, price, qty)

        return trades

    def add_market_order(self, order_id, side, qty):
        if qty <= 0:
            raise ValueError("qty must be positive")
        if side not in {"buy", "sell"}:
            raise ValueError("side must be buy or sell")

        trades = []

        if side == "buy":
            self._match_buy(order_id, float("inf"), qty, trades)
        else:
            self._match_sell(order_id, float("-inf"), qty, trades)

        return trades

    def cancel(self, order_id):
        order = self.orders.get(order_id)
        if order is None or order["qty"] == 0:
            return False

        order["qty"] = 0
        return True

    def depth(self):
        self._clean_empty_levels(self.bids)
        self._clean_empty_levels(self.asks)

        bid_depth = {
            price: sum(self.orders[oid]["qty"] for oid in queue)
            for price, queue in self.bids.items()
        }
        ask_depth = {
            price: sum(self.orders[oid]["qty"] for oid in queue)
            for price, queue in self.asks.items()
        }

        return {
            "bid": dict(sorted(bid_depth.items(), reverse=True)),
            "ask": dict(sorted(ask_depth.items())),
        }

    def _match_buy(self, taker_id, limit_price, qty, trades):
        while qty > 0:
            best = self.best_ask()
            if best is None or best > limit_price:
                break

            qty = self._trade_against_level(
                taker_id=taker_id,
                side="buy",
                price=best,
                qty=qty,
                trades=trades,
                opposite_book=self.asks,
            )

        return qty

    def _match_sell(self, taker_id, limit_price, qty, trades):
        while qty > 0:
            best = self.best_bid()
            if best is None or best < limit_price:
                break

            qty = self._trade_against_level(
                taker_id=taker_id,
                side="sell",
                price=best,
                qty=qty,
                trades=trades,
                opposite_book=self.bids,
            )

        return qty

    def _trade_against_level(self, taker_id, side, price, qty, trades, opposite_book):
        queue = opposite_book[price]

        while qty > 0 and queue:
            maker_id = queue[0]
            maker = self.orders[maker_id]

            if maker["qty"] == 0:
                queue.popleft()
                continue

            trade_qty = min(qty, maker["qty"])
            maker["qty"] -= trade_qty
            qty -= trade_qty

            trades.append({
                "taker_order_id": taker_id,
                "maker_order_id": maker_id,
                "side": side,
                "price": price,
                "qty": trade_qty,
            })

            if maker["qty"] == 0:
                queue.popleft()

        if not queue:
            opposite_book.pop(price, None)

        return qty

    def _rest_order(self, order_id, side, price, qty):
        self.orders[order_id] = {"side": side, "price": price, "qty": qty}
        book = self.bids if side == "buy" else self.asks
        book.setdefault(price, deque()).append(order_id)

    def _clean_empty_levels(self, book):
        empty_prices = []

        for price, queue in book.items():
            while queue and self.orders[queue[0]]["qty"] == 0:
                queue.popleft()
            if not queue:
                empty_prices.append(price)

        for price in empty_prices:
            book.pop(price, None)
```

## 限价单挂单

限价单 limit order 有价格。

买限价单表示：

```text
愿意以不高于 limit price 的价格买入
```

卖限价单表示：

```text
愿意以不低于 limit price 的价格卖出
```

如果不能立即成交，剩余数量会挂在订单簿里。

```python
book = SimpleOrderBook()

book.add_limit_order("s1", "sell", 101, 100)
book.add_limit_order("b1", "buy", 100, 50)

print(book.depth())
print(book.top_of_book())
```

结果：

```text
{'bid': {100: 50}, 'ask': {101: 100}}
{'bid': 100, 'ask': 101, 'spread': 1, 'mid': 100.5}
```

因为 `b1` 的买价 100 小于卖价 101，所以不会成交。

## 可成交限价单

如果新买单价格大于等于 best ask，它会吃掉卖盘。

```python
trades = book.add_limit_order("b2", "buy", 102, 70)

print(trades)
print(book.depth())
```

结果：

```text
[{'taker_order_id': 'b2', 'maker_order_id': 's1', 'side': 'buy', 'price': 101, 'qty': 70}]
{'bid': {100: 50}, 'ask': {101: 30}}
```

成交价格使用被动挂单价格，也就是 maker 的价格 `101`。

`s1` 原来有 100 股，成交 70 股后还剩 30 股。

## 部分成交和剩余挂单

如果买单数量超过当前可成交卖盘，它会先成交，剩余部分再挂单。

```python
trades = book.add_limit_order("b3", "buy", 102, 50)

print(trades)
print(book.depth())
```

结果：

```text
[{'taker_order_id': 'b3', 'maker_order_id': 's1', 'side': 'buy', 'price': 101, 'qty': 30}]
{'bid': {102: 20, 100: 50}, 'ask': {}}
```

`b3` 买 50 股。

它先吃掉 `s1` 剩下的 30 股。

还剩 20 股无法成交，于是挂在 bid 102。

## 市价单

市价单 market order 不指定价格，只尽可能立刻成交。

它可能：

- 全部成交。
- 部分成交。
- 如果对手盘不够，剩余部分取消。

在这个简化模型里，市价单不会挂单。

```python
book.add_limit_order("s2", "sell", 103, 40)
book.add_limit_order("s3", "sell", 104, 60)

trades = book.add_market_order("m1", "buy", 70)

print(trades)
print(book.depth())
```

结果：

```text
[{'taker_order_id': 'm1', 'maker_order_id': 's2', 'side': 'buy', 'price': 103, 'qty': 40}, {'taker_order_id': 'm1', 'maker_order_id': 's3', 'side': 'buy', 'price': 104, 'qty': 30}]
{'bid': {102: 20, 100: 50}, 'ask': {104: 30}}
```

市价买单先吃最低 ask 103，再吃 104。

## 撤单

撤单 cancel 通过 `order_id` 找到订单，并把剩余数量置为 0。

这里采用 lazy deletion：

```text
撤单时只标记 qty = 0
等它出现在价格队列头部时再清理
```

```python
book.cancel("b1")

print(book.depth())
```

结果：

```text
{'bid': {102: 20}, 'ask': {104: 30}}
```

`b1` 被撤掉，所以 bid 100 不再显示。

## 同价位 FIFO

同一价格档位内，先来的订单先成交。

```python
book = SimpleOrderBook()

book.add_limit_order("s1", "sell", 101, 10)
book.add_limit_order("s2", "sell", 101, 10)

trades = book.add_market_order("m1", "buy", 15)

print(trades)
print(book.depth())
```

结果：

```text
[{'taker_order_id': 'm1', 'maker_order_id': 's1', 'side': 'buy', 'price': 101, 'qty': 10}, {'taker_order_id': 'm1', 'maker_order_id': 's2', 'side': 'buy', 'price': 101, 'qty': 5}]
{'bid': {}, 'ask': {101: 5}}
```

`s1` 先来，所以先成交。

`s2` 只成交 5 股，还剩 5 股。

## 用事件流驱动订单簿

订单簿通常不是手动调用函数，而是被事件流驱动。

事件可以长这样：

```python
events = [
    {"type": "limit", "order_id": "s1", "side": "sell", "price": 101, "qty": 100},
    {"type": "limit", "order_id": "b1", "side": "buy", "price": 100, "qty": 50},
    {"type": "limit", "order_id": "b2", "side": "buy", "price": 102, "qty": 70},
    {"type": "cancel", "order_id": "b1"},
    {"type": "market", "order_id": "m1", "side": "buy", "qty": 10},
]
```

处理器：

```python
def apply_event(book, event):
    if event["type"] == "limit":
        return book.add_limit_order(
            event["order_id"],
            event["side"],
            event["price"],
            event["qty"],
        )

    if event["type"] == "market":
        return book.add_market_order(
            event["order_id"],
            event["side"],
            event["qty"],
        )

    if event["type"] == "cancel":
        book.cancel(event["order_id"])
        return []

    raise ValueError(f"unknown event type: {event['type']}")
```

回放：

```python
book = SimpleOrderBook()
all_trades = []

for event in events:
    all_trades.extend(apply_event(book, event))

print(all_trades)
print(book.depth())
```

这种结构和上一章 stream processing 是一致的：

```text
当前订单簿状态 + 新事件 -> 新订单簿状态 + trades
```

## 为什么不用普通排序每次找最优价

简化版里 `best_bid()` 用 `max(self.bids)`，`best_ask()` 用 `min(self.asks)`。

这很清楚，但复杂度是：

```text
O(number_of_price_levels)
```

真实系统中，价格档位很多、事件很多，通常会用更合适的数据结构：

- 平衡树。
- 跳表。
- heap + lazy deletion。
- 数组价格网格。
- 专门的撮合引擎结构。

Python 标准库没有内置平衡树。

讲算法时可以先用 `dict + deque` 写清楚语义，再讨论优化。

## 用 heap 维护最优价

如果用 heap：

```text
ask_heap 存 price，堆顶是最低 ask
bid_heap 存 -price，堆顶对应最高 bid
```

删除价格档位时，可以 lazy deletion。

简化示意：

```python
import heapq

bid_heap = []
ask_heap = []
bid_sizes = {}
ask_sizes = {}

def add_bid(price, size):
    bid_sizes[price] = bid_sizes.get(price, 0) + size
    heapq.heappush(bid_heap, -price)

def add_ask(price, size):
    ask_sizes[price] = ask_sizes.get(price, 0) + size
    heapq.heappush(ask_heap, price)

def heap_best_bid():
    while bid_heap and bid_sizes.get(-bid_heap[0], 0) == 0:
        heapq.heappop(bid_heap)
    return None if not bid_heap else -bid_heap[0]

def heap_best_ask():
    while ask_heap and ask_sizes.get(ask_heap[0], 0) == 0:
        heapq.heappop(ask_heap)
    return None if not ask_heap else ask_heap[0]

add_bid(100, 10)
add_bid(101, 5)
add_ask(103, 7)

print(heap_best_bid())
print(heap_best_ask())
```

结果：

```text
101
103
```

heap 适合快速拿最优价。

但它不擅长任意价格删除，所以仍然需要 lazy deletion 或额外索引。

## 常见指标

订单簿模拟后，经常计算：

```text
spread = best_ask - best_bid
mid = (best_ask + best_bid) / 2
bid_depth = sum(best N bid levels)
ask_depth = sum(best N ask levels)
imbalance = (bid_depth - ask_depth) / (bid_depth + ask_depth)
```

例子：

```python
def depth_imbalance(depth, levels=1):
    bid_sizes = list(depth["bid"].values())[:levels]
    ask_sizes = list(depth["ask"].values())[:levels]

    bid_total = sum(bid_sizes)
    ask_total = sum(ask_sizes)

    if bid_total + ask_total == 0:
        return 0

    return (bid_total - ask_total) / (bid_total + ask_total)

depth = {
    "bid": {100: 300, 99: 500},
    "ask": {101: 200, 102: 400},
}

print(depth_imbalance(depth, levels=1))
```

结果：

```text
0.2
```

这里 best bid size 是 300，best ask size 是 200。

所以：

```text
(300 - 200) / (300 + 200) = 0.2
```

## 现实撮合规则更复杂

本篇是数据结构小例子，不是完整交易所模拟器。

真实市场还会有：

- tick size。
- lot size。
- hidden order。
- iceberg order。
- maker/taker fee。
- auction。
- self-trade prevention。
- order type: IOC、FOK、post-only。
- 不同交易所的优先级规则。
- 延迟、撮合批次和网络时间戳。

所以如果用订单簿模拟做研究，要明确假设。

不要把简化撮合器的结果当成真实成交保证。

## 常见错误

### 错误 1：忽略价格时间优先

同价位订单必须按到达顺序排队。

如果只保存价格档位总量，就无法模拟自己的排队位置。

### 错误 2：买卖方向比较写反

买单成交条件：

```text
buy_limit_price >= best_ask
```

卖单成交条件：

```text
sell_limit_price <= best_bid
```

方向写反会导致本该成交的订单不成交，或本不该成交的订单成交。

### 错误 3：撤单后没有清理索引

撤单如果只改 `orders[order_id]`，价格队列里还可能残留 `order_id`。

要么立即从队列删除，要么用 lazy deletion 并在访问队首时清理。

### 错误 4：用浮点数表示价格

浮点价格可能出现：

```text
100.05 - 100.00 = 0.04999999999999716
```

交易系统里更常用整数 tick。

### 错误 5：假设市价单总能完全成交

如果对手盘不够，市价单可能只部分成交。

简化模拟里，剩余未成交部分通常直接取消。

## 什么时候用 order book simulation

适合使用的场景：

- 学习撮合规则。
- 回放订单事件。
- 测试策略对盘口变化的反应。
- 构造盘口特征。
- 估算简化成交和滑点。
- 练习事件驱动数据结构。

需要谨慎的场景：

- 真实成交概率预测。
- 高频延迟敏感策略。
- 含隐藏流动性的市场。
- 交易所规则复杂的品种。
- 缺少完整 L3 数据却想模拟排队位置。

## 记忆要点

- order book 有 bid 和 ask 两侧。
- best bid 是最高买价，best ask 是最低卖价。
- L2 保存价格档位总量，L3 保存每个订单。
- 同一价格档位通常按 FIFO 维护时间优先。
- 限价单可能成交，也可能剩余挂单。
- 市价单尽可能成交，未成交部分通常不挂单。
- 撤单需要通过 order_id 找到订单。
- `dict + deque` 很适合表达价格档位和同价位队列。
- 简化模拟清楚优先，生产撮合器需要更高效和更完整的规则。

## 自测题

1. best bid、best ask、spread 和 mid 分别是什么？
2. L2 和 L3 订单簿有什么区别？
3. 为什么同一价格档位要用 FIFO 队列？
4. 买限价单在什么条件下会立刻成交？
5. 为什么撤单常需要 lazy deletion 或额外索引？
