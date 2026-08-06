# 训练正确性：梯度检查与完整 checkpoint

## 核心概念

训练“能跑”不等于训练“正确”。至少要分别回答两个问题：

```text
当前 backward 算出的局部梯度对不对？
任务中断后，恢复的下一步是否和原训练现场一致？
```

梯度检查验证局部导数。checkpoint 恢复验证训练状态连续性。前者主要用于自定义算子、手写反向传播和新损失函数；后者用于长训练、抢占式任务和故障恢复。

## 用中心差分检查梯度

对参数 `theta[i]` 做一个很小的正负扰动：

```text
numeric_grad = (loss(theta + h) - loss(theta - h)) / (2h)
```

再和 backward 给出的解析梯度比较。下面用纯 Python 检查 `loss(w) = (w*x-y)^2`：

```python
def loss(w, x=3.0, y=7.0):
    return (w * x - y) ** 2


def analytic_grad(w, x=3.0, y=7.0):
    return 2.0 * (w * x - y) * x


w = 2.0
h = 1e-6
numeric = (loss(w + h) - loss(w - h)) / (2.0 * h)
analytic = analytic_grad(w)
relative_error = abs(numeric - analytic) / max(1.0, abs(numeric), abs(analytic))

print(numeric, analytic, relative_error)
```

相对误差比绝对误差更稳，因为梯度本身可能很大或很小。

## 梯度检查的正确姿势

检查时应尽量满足：

- 使用小张量和少量参数，不对整个大模型逐元素扰动。
- 使用双精度，减小浮点消减误差。
- 固定随机种子，关闭 dropout 和随机增强。
- 避开 ReLU 的零点等不可微位置。
- 保证数值梯度和解析梯度使用相同 batch、loss reduction 和参数。

差分步长 `h` 也不是越小越好。太大有截断误差，太小会让两次非常接近的浮点数相减，真实变化被舍入误差淹没。

## checkpoint 应保存什么

只保存模型权重足以恢复推理，但通常不足以继续训练。一个可恢复训练现场至少包含：

- 模型参数和 buffer。
- 优化器的一阶、二阶矩或动量。
- 当前 epoch、global step 和 batch 位置。
- 学习率 scheduler 状态。
- 混合精度 scaler 状态。
- 需要严格复现时的随机数和 sampler 状态。
- 数据版本、配置版本和代码提交标识。

可以先用普通字典明确状态契约：

```python
checkpoint_contract = {
    "model": "model.state_dict()",
    "optimizer": "optimizer.state_dict()",
    "scheduler": "scheduler.state_dict()",
    "scaler": "scaler.state_dict()",
    "global_step": 12000,
    "epoch": 4,
    "next_batch": 83,
    "config_hash": "example-hash",
}

for key in checkpoint_contract:
    print(key)
```

## 恢复顺序

安全流程是：

```text
用同一配置重建模型和优化器
加载 model state
加载 optimizer / scheduler / scaler state
恢复进度、随机状态和数据位置
跑一个短区间做连续性检查
确认后再启动长训练
```

短区间检查要比较恢复前后的学习率、loss、参数更新范数和样本位置。若 world size、batch size 或梯度累积改变，后续轨迹通常已经变化，应作为新实验条件记录。

## 常见坑

- 只加载模型，Adam 的动量从零开始，后续曲线突然跳变。
- 保存的是“已完成 step”，恢复时却再次执行同一个 step。
- 参数组顺序变化，优化器状态加载到错误参数。
- 训练中直接覆盖 checkpoint，中断后留下不完整文件。
- 加载不可信 checkpoint 时允许任意对象反序列化。
- 梯度检查在 dropout 开启时运行，每次 loss 都不同。

## 实战提示

checkpoint 最好先写到临时文件，完成后再原子替换正式文件。保留最近一次、最佳一次和少量里程碑版本，比只保留一个持续覆盖的文件更容易恢复。

梯度检查应变成自定义算子的自动测试，而不是出错后才临时运行。它验证局部导数，但不能替代数据泄漏、标签对齐和样本外评估检查。

## 自检问题

1. 为什么模型权重完全相同，恢复后的下一步更新仍可能不同？
2. 梯度检查为什么要关闭随机层并使用双精度？
3. global step 和“下一个 batch”记录错误会造成什么后果？
4. world size 改变后还能否宣称训练轨迹完全连续？

## 延伸阅读与来源

- [Datawhale / jshn9515 Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)：用于核对 PyTorch 梯度检查与断点续训的教学边界；原资料采用 CC BY-NC 4.0。
- [PyTorch documentation](https://pytorch.org/docs/stable/index.html)：核对 `state_dict`、自动求导和序列化 API。
- 本文为面向实验工程的原创归纳，不复刻上游示例与章节表述。
