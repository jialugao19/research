# 时间序列：Kalman filter 的状态空间模型、预测更新与简单跟踪例子

## 核心概念

Kalman filter 用来在有噪声的观测中估计隐藏状态。

它适用于线性高斯状态空间模型：

```text
state_t = F state_{t-1} + process_noise_t
observation_t = H state_t + measurement_noise_t
```

其中：

- `state_t`：真实但不可直接观测的隐藏状态。
- `observation_t`：带噪声的观测值。
- `F`：状态转移矩阵。
- `H`：观测矩阵。
- `process_noise`：状态自身变化的不确定性。
- `measurement_noise`：观测误差。

Kalman filter 的核心是两步：

```text
predict：根据上一期状态预测当前状态
update：用当前观测修正预测
```

它是在线算法：每来一个新观测，就更新一次当前状态估计。

## Kalman filter 回答的问题

它适合回答：

- 如何从 noisy price 中估计平滑的真实价格？
- 如何估计动态 beta、动态 hedge ratio？
- 如何跟踪不可直接观测的趋势、均值或状态？
- 如何在模型预测和新观测之间动态分配权重？

它不是简单移动平均。Kalman filter 会显式维护不确定性：

```text
预测越不确定，新观测权重越高；
观测越 noisy，新观测权重越低。
```

这个权重就是 Kalman gain。

## 准备环境

```python
import numpy as np
import pandas as pd
```

构造一个隐藏状态和带噪声观测。

这里使用一维 local level model：

```text
x_t = x_{t-1} + w_t
y_t = x_t + v_t
```

其中：

- `x_t` 是真实状态。
- `y_t` 是观测值。
- `w_t ~ N(0, q)` 是过程噪声。
- `v_t ~ N(0, r)` 是观测噪声。

代码：

```python
rng = np.random.default_rng(67)

n_obs = 120
dates = pd.bdate_range("2024-01-02", periods=n_obs)

q = 0.04
r = 1.00

true_state_values = np.empty(n_obs)
observation_values = np.empty(n_obs)

true_state_values[0] = 50.0
observation_values[0] = true_state_values[0] + rng.normal(
    loc=0.0,
    scale=np.sqrt(r),
)

for t in range(1, n_obs):
    true_state_values[t] = (
        true_state_values[t - 1]
        + rng.normal(loc=0.0, scale=np.sqrt(q))
    )
    observation_values[t] = (
        true_state_values[t]
        + rng.normal(loc=0.0, scale=np.sqrt(r))
    )

true_state = pd.Series(true_state_values, index=dates, name="true_state")
observation = pd.Series(observation_values, index=dates, name="observation")

print(pd.concat([true_state, observation], axis=1).head())
```

真实应用里没有 `true_state`，这里只是为了教学时评估滤波效果。

## 一维 Kalman filter 公式

在 local level model 中：

```text
x_t = x_{t-1} + w_t
y_t = x_t + v_t
```

预测步骤：

```text
x_pred_t = x_filt_{t-1}
p_pred_t = p_filt_{t-1} + q
```

更新步骤：

```text
innovation_t = y_t - x_pred_t
S_t = p_pred_t + r
K_t = p_pred_t / S_t
x_filt_t = x_pred_t + K_t * innovation_t
p_filt_t = (1 - K_t) * p_pred_t
```

其中：

- `p_pred_t` 是预测误差方差。
- `p_filt_t` 是更新后的估计误差方差。
- `innovation_t` 是新观测和预测之间的差。
- `K_t` 是 Kalman gain。

Kalman gain 越大，当前观测对状态估计影响越大。

## 手写 Kalman filter

```python
x_pred = np.empty(n_obs)
p_pred = np.empty(n_obs)
x_filt = np.empty(n_obs)
p_filt = np.empty(n_obs)
kalman_gain = np.empty(n_obs)
innovation = np.empty(n_obs)

x_filt[0] = observation.iloc[0]
p_filt[0] = 1.0
x_pred[0] = x_filt[0]
p_pred[0] = p_filt[0]
kalman_gain[0] = np.nan
innovation[0] = np.nan

for t in range(1, n_obs):
    x_pred[t] = x_filt[t - 1]
    p_pred[t] = p_filt[t - 1] + q

    innovation[t] = observation.iloc[t] - x_pred[t]
    innovation_var = p_pred[t] + r
    kalman_gain[t] = p_pred[t] / innovation_var

    x_filt[t] = x_pred[t] + kalman_gain[t] * innovation[t]
    p_filt[t] = (1 - kalman_gain[t]) * p_pred[t]

filtered_state = pd.Series(
    x_filt,
    index=dates,
    name="filtered_state",
)

filter_table = pd.DataFrame({
    "true_state": true_state,
    "observation": observation,
    "filtered_state": filtered_state,
    "kalman_gain": kalman_gain,
    "p_filt": p_filt,
})

print(filter_table.head())
print(filter_table.tail())
```

这个例子没有用任何专门库，目的是看清 predict / update 的结构。

## 滤波效果

比较原始观测和滤波估计对真实状态的误差：

```python
observation_rmse = np.sqrt(((observation - true_state) ** 2).mean())
filter_rmse = np.sqrt(((filtered_state - true_state) ** 2).mean())

print(observation_rmse)
print(filter_rmse)
```

在这个模拟中，滤波后的状态估计应该比原始观测更接近真实状态。

这不是因为滤波器知道未来，而是因为它把当前观测和过去状态估计按不确定性加权。

## Kalman gain 的含义

Kalman gain 决定新观测的权重：

```text
x_filt = x_pred + K * (observation - x_pred)
```

等价地：

```text
x_filt = (1 - K) * x_pred + K * observation
```

当 `K` 大：

- 更相信新观测。
- 估计反应更快。
- 噪声也更容易进入状态估计。

当 `K` 小：

- 更相信模型预测。
- 估计更平滑。
- 对真实状态突变反应更慢。

查看 Kalman gain：

```python
gain_series = pd.Series(kalman_gain, index=dates, name="kalman_gain")

print(gain_series.dropna().head())
print(gain_series.dropna().tail())
```

在参数固定的一维模型里，Kalman gain 往往会逐渐接近稳定值。

## 过程噪声 q 和观测噪声 r

`q` 和 `r` 是最关键的调参对象。

- `q` 大：认为真实状态变化快，滤波器更愿意跟随观测。
- `q` 小：认为真实状态变化慢，滤波器更平滑。
- `r` 大：认为观测噪声大，滤波器降低观测权重。
- `r` 小：认为观测更可靠，滤波器提高观测权重。

比较不同 `q`：

```python
def run_local_level_filter(observation, q_value, r_value):
    n = len(observation)
    x = np.empty(n)
    p = np.empty(n)
    gains = np.empty(n)

    x[0] = observation.iloc[0]
    p[0] = 1.0
    gains[0] = np.nan

    for t in range(1, n):
        x_pred_t = x[t - 1]
        p_pred_t = p[t - 1] + q_value
        gain_t = p_pred_t / (p_pred_t + r_value)

        x[t] = x_pred_t + gain_t * (observation.iloc[t] - x_pred_t)
        p[t] = (1 - gain_t) * p_pred_t
        gains[t] = gain_t

    return (
        pd.Series(x, index=observation.index, name="filtered"),
        pd.Series(gains, index=observation.index, name="gain"),
    )


sensitivity_rows = []

for q_try in [0.005, 0.04, 0.40]:
    filtered_try, gain_try = run_local_level_filter(observation, q_try, r)

    rmse_try = np.sqrt(((filtered_try - true_state) ** 2).mean())

    sensitivity_rows.append({
        "q": q_try,
        "rmse": rmse_try,
        "last_gain": gain_try.dropna().iloc[-1],
    })

sensitivity = pd.DataFrame(sensitivity_rows)

print(sensitivity)
```

这个例子中，中间的 `q` 比过小或过大的 `q` 更合适。

真实应用里 `q` 和 `r` 可以来自：

- 历史估计。
- 最大似然。
- EM 算法。
- 业务经验和调参。

## 动态 beta 的伪代码

Kalman filter 在量化中常用于估计动态 beta 或动态 hedge ratio。

假设：

```text
y_t = beta_t x_t + noise_t
beta_t = beta_{t-1} + state_noise_t
```

这里 `beta_t` 是隐藏状态，`x_t` 是可观测市场或对冲资产。

伪代码：

```text
initialize beta_estimate, beta_variance

for each date t:
    # predict
    beta_pred = beta_estimate
    variance_pred = beta_variance + process_variance

    # observation equation: y_t = x_t * beta_t + noise
    innovation = y_t - x_t * beta_pred
    innovation_var = x_t^2 * variance_pred + measurement_variance
    gain = variance_pred * x_t / innovation_var

    # update
    beta_estimate = beta_pred + gain * innovation
    beta_variance = (1 - gain * x_t) * variance_pred
```

这比滚动窗口回归更灵活，因为它自然处理了：

- 参数随时间变化。
- 估计不确定性。
- 新观测权重随噪声变化。

## 常见坑

第一，把 Kalman filter 当成没有延迟的未来信息工具。

标准滤波只使用当前及过去观测。若使用 smoother，会用到未来观测，不能直接用于实时交易信号。

第二，随意设置 `q` 和 `r`。

过程噪声和观测噪声决定平滑程度和反应速度。设置不合理会过度平滑或过度追噪声。

第三，忘记检查模型假设。

标准 Kalman filter 假设线性和高斯噪声。非线性或厚尾数据可能需要 extended Kalman filter、unscented Kalman filter、particle filter 或稳健处理。

第四，误把平滑状态当真实状态。

滤波估计仍然是估计，不是真值。它有不确定性，应该同时看估计方差。

第五，把离线平滑结果用于回测信号。

如果 smoother 用到了未来数据，回测会产生前视偏差。

## 实战提示

使用 Kalman filter 时可以按下面流程：

1. 明确隐藏状态是什么，例如趋势、均值、beta 或 hedge ratio。
2. 写出状态方程和观测方程。
3. 明确过程噪声 `q` 和观测噪声 `r` 的含义。
4. 先用一维模型手写 predict / update，确认方向正确。
5. 检查 innovation 是否近似白噪声。
6. 做 `q` / `r` 敏感性分析。
7. 区分 filter 和 smoother，实盘信号只能使用当时可见数据。
8. 与滚动均值、EWMA、滚动回归等简单基准比较。

## 小结

本节的重点：

- Kalman filter 用有噪声的观测估计隐藏状态。
- 它由 predict 和 update 两步组成。
- Kalman gain 决定新观测和模型预测的相对权重。
- `q` 控制状态变化速度，`r` 控制观测噪声大小。
- 滤波不同于平滑；平滑可能使用未来信息。
- 在量化中，Kalman filter 常用于趋势跟踪、动态 beta、动态 hedge ratio 和状态空间模型。

## 自检问题

1. Kalman filter 的状态方程和观测方程分别描述什么？
2. predict 步骤和 update 步骤分别做什么？
3. Kalman gain 大意味着什么？
4. `q` 和 `r` 分别如何影响滤波结果？
5. filter 和 smoother 在回测中有什么关键区别？
6. 为什么动态 beta 可以写成状态空间模型？
