---
title: Loss function Stage B | loss-function-1min-final-comparison-072821
date: 2026-11-03
summary: Stage B seed7 的 mse_std_floor_0p1 test IC 为 0.0777618206, 高于 MSE 的 0.0688795701. 这是单 seed 筛选, 输出 scale 问题未完全解决.
tags:
- prediction-nn
- registry-sync
- historical-evidence
featured: false
---

## 摘要

**历史结果: 历史成功.** Stage B seed7 的 mse_std_floor_0p1 test IC 为 0.0777618206, 高于 MSE 的 0.0688795701. 这是单 seed 筛选, 输出 scale 问题未完全解决.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

### Executive Summary

The comparison keeps data, label, optimizer, checkpoint policy, and architecture fixed. The model is GruMlpRegressor with input (B, T=60, F=14), GRU hidden size 256, 2 GRU layers, one MLP hidden layer of width 512, and 735745 trainable parameters. The primary control is `mse` ; all deltas are computed against that control.

Best test pooled IC in this Stage B table: **mse_std_floor_0p1** (0.0777618). Best test scale error by prediction-std/target-std closeness: **mse_moment_0p05** (0.752865).

## 研究背景与目标

本报告围绕Loss function Stage B整理原始研究证据. 当前材料对应 registry report `loss-function-1min-final-comparison-072821`, 来源SHA256为 `90711245d529f1f8613bb9b5029c5a7b5c7dd4f2f76d5daca482db4241e68dc7`. 原报告的实验方法, 图表, 结果和解释保留在下文.

## 数据与方法

实验身份为 `loss-function-1min`. Split, label, sampler, feature与checkpoint定义按原报告记录, 不从其他实验借用缺失字段. 汇总入口见[全实验综述](../../prediction-nn-1min/1103-nn-registry-summary/).

## 主要结果

| 记录项 | 当前解释 |
| --- | --- |
| 实验 | loss-function-1min |
| 报告类型 | comparison_report_html |
| 历史状态 | 历史成功 |
| 证据 | loss-function-1min-final-comparison-072821 |

Generated at 2026-07-28 21:49:13 CST.

This is a Stage B single-seed screening report for seed 7. It is not a final promotion report: multi-seed Stage C confirmation is still required before making a retained-model claim.

### Model Summary

| variant | role | trainable_parameters | input_tensor | gru_hidden_size | gru_num_layers | mlp_effective_hidden_width | learning_rate | best_iter | selection_score | val_pooled_ic | val_rank_ic | test_pooled_ic | test_rank_ic | test_std_ratio | test_abs_mean_gap |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| mse | control | 735745 | (B, T=60, F=14) | 256 | 2 | 512 | 0.001 | 20000 | 0.0430747 | 0.07372 | 0.0371628 | 0.0688796 | 0.0435469 | 0.203302 | 1.00922e-05 |
| mse_corr_0p1 | ranking | 735745 | (B, T=60, F=14) | 256 | 2 | 512 | 0.001 | 20000 | 0.0551606 | 0.0602571 | 0.0300442 | 0.0685276 | 0.0452961 | 0.207138 | 2.95886e-05 |
| mse_moment_0p05 | scale_sensitive | 735745 | (B, T=60, F=14) | 256 | 2 | 512 | 0.001 | 20000 | 0.049957 | 0.0693838 | 0.0357891 | 0.0669827 | 0.0434909 | 0.247135 | 1.31659e-05 |
| mse_std_floor_0p1 | scale_sensitive | 735745 | (B, T=60, F=14) | 256 | 2 | 512 | 0.001 | 10000 | 0.0437776 | 0.0847228 | 0.03421 | 0.0777618 | 0.04534 | 0.229421 | 5.90039e-05 |
| mse_corr_moment_0p1 | ranking_scale | 735745 | (B, T=60, F=14) | 256 | 2 | 512 | 0.001 | 10000 | 0.0449985 | 0.0799975 | 0.0283903 | 0.0751742 | 0.0392051 | 0.237164 | 3.38581e-05 |

### Deltas Versus MSE

| variant | test_pooled_ic_delta_vs_mse | test_rank_ic_delta_vs_mse | test_std_ratio_error_delta_vs_mse | test_abs_mean_gap_delta_vs_mse | selection_score_delta_vs_mse |
| --- | --- | --- | --- | --- | --- |
| mse | 0 | 0 | 0 | 0 | 0 |
| mse_corr_0p1 | -0.000351976 | 0.0017492 | -0.0038363 | 1.94963e-05 | 0.0120859 |
| mse_moment_0p05 | -0.00189684 | -5.6097e-05 | -0.0438335 | 3.07366e-06 | 0.00688231 |
| mse_std_floor_0p1 | 0.00888225 | 0.00179308 | -0.026119 | 4.89116e-05 | 0.000702892 |
| mse_corr_moment_0p1 | 0.00629459 | -0.00434189 | -0.0338618 | 2.37658e-05 | 0.00192383 |

### Monthly Test IC

| variant | month | pearson_ic | rank_ic | sample_count |
| --- | --- | --- | --- | --- |
| mse | 2024/03 | 0.0800991 | 0.0439206 | 2.39682e+07 |
| mse | 2024/04 | 0.074559 | 0.0665727 | 2.04837e+07 |
| mse | 2024/05 | 0.0618614 | 0.0423604 | 2.23963e+07 |
| mse | 2024/06 | 0.0599785 | 0.0277558 | 2.04841e+07 |
| mse | 2024/07 | 0.0610819 | 0.0352796 | 2.13379e+07 |
| mse_corr_0p1 | 2024/03 | 0.0777522 | 0.0453346 | 2.39682e+07 |
| mse_corr_0p1 | 2024/04 | 0.0762894 | 0.0682283 | 2.04837e+07 |
| mse_corr_0p1 | 2024/05 | 0.0682027 | 0.0499939 | 2.23963e+07 |
| mse_corr_0p1 | 2024/06 | 0.0558162 | 0.0277299 | 2.04841e+07 |
| mse_corr_0p1 | 2024/07 | 0.0588705 | 0.0335392 | 2.13379e+07 |
| mse_moment_0p05 | 2024/03 | 0.077314 | 0.0432849 | 2.39682e+07 |
| mse_moment_0p05 | 2024/04 | 0.0794859 | 0.0713333 | 2.04837e+07 |
| mse_moment_0p05 | 2024/05 | 0.0621098 | 0.0446444 | 2.23963e+07 |
| mse_moment_0p05 | 2024/06 | 0.0515028 | 0.0235609 | 2.04841e+07 |
| mse_moment_0p05 | 2024/07 | 0.0572782 | 0.0329651 | 2.13379e+07 |
| mse_std_floor_0p1 | 2024/03 | 0.0851298 | 0.0429515 | 2.39682e+07 |
| mse_std_floor_0p1 | 2024/04 | 0.0908576 | 0.0761676 | 2.04837e+07 |
| mse_std_floor_0p1 | 2024/05 | 0.0728026 | 0.0382098 | 2.23963e+07 |
| mse_std_floor_0p1 | 2024/06 | 0.0635471 | 0.0272699 | 2.04841e+07 |
| mse_std_floor_0p1 | 2024/07 | 0.0701568 | 0.0397332 | 2.13379e+07 |
| mse_corr_moment_0p1 | 2024/03 | 0.0833485 | 0.037515 | 2.39682e+07 |
| mse_corr_moment_0p1 | 2024/04 | 0.0854534 | 0.0721162 | 2.04837e+07 |
| mse_corr_moment_0p1 | 2024/05 | 0.0708899 | 0.0303239 | 2.23963e+07 |
| mse_corr_moment_0p1 | 2024/06 | 0.0680269 | 0.0283804 | 2.04841e+07 |
| mse_corr_moment_0p1 | 2024/07 | 0.0618829 | 0.0253634 | 2.13379e+07 |

### ADV Liquidity Slices

| variant | adv_bucket | bucket_label | mean_ic | mean_rank_ic | top5_return_bps | top5_hit_rate |
| --- | --- | --- | --- | --- | --- | --- |
| mse | 1 | Bottom20% | 0.0540723 | 0.0304125 | 3.42535 | 0.483493 |
| mse | 2 | 20~40% | 0.0658649 | 0.0405173 | 4.10656 | 0.493092 |
| mse | 3 | 40~60% | 0.0746353 | 0.0479113 | 4.82047 | 0.498565 |
| mse | 4 | 60~80% | 0.0837653 | 0.0568292 | 6.48666 | 0.508779 |
| mse | 5 | Top20% | 0.0869467 | 0.0602586 | 6.801 | 0.50854 |
| mse_corr_0p1 | 1 | Bottom20% | 0.0524411 | 0.0320856 | 3.40729 | 0.48487 |
| mse_corr_0p1 | 2 | 20~40% | 0.0692242 | 0.0430892 | 4.14331 | 0.495626 |
| mse_corr_0p1 | 3 | 40~60% | 0.0776201 | 0.052085 | 4.99542 | 0.502312 |
| mse_corr_0p1 | 4 | 60~80% | 0.0869704 | 0.0609506 | 6.62503 | 0.513152 |
| mse_corr_0p1 | 5 | Top20% | 0.0867762 | 0.0665815 | 6.88724 | 0.513441 |
| mse_moment_0p05 | 1 | Bottom20% | 0.0534804 | 0.032733 | 3.32425 | 0.484526 |
| mse_moment_0p05 | 2 | 20~40% | 0.0654126 | 0.0424996 | 3.95376 | 0.495633 |
| mse_moment_0p05 | 3 | 40~60% | 0.07351 | 0.0508522 | 4.72938 | 0.501698 |
| mse_moment_0p05 | 4 | 60~80% | 0.0808603 | 0.0587166 | 6.43507 | 0.510629 |
| mse_moment_0p05 | 5 | Top20% | 0.0845271 | 0.0614063 | 6.87104 | 0.511545 |
| mse_std_floor_0p1 | 1 | Bottom20% | 0.0548782 | 0.0311248 | 3.48152 | 0.481285 |
| mse_std_floor_0p1 | 2 | 20~40% | 0.0698843 | 0.0411877 | 4.10036 | 0.493161 |
| mse_std_floor_0p1 | 3 | 40~60% | 0.0807435 | 0.0499895 | 5.10655 | 0.501027 |
| mse_std_floor_0p1 | 4 | 60~80% | 0.0939298 | 0.0587111 | 6.83967 | 0.510512 |
| mse_std_floor_0p1 | 5 | Top20% | 0.0994846 | 0.0637316 | 7.63414 | 0.51432 |
| mse_corr_moment_0p1 | 1 | Bottom20% | 0.0530095 | 0.0288784 | 3.34816 | 0.481069 |
| mse_corr_moment_0p1 | 2 | 20~40% | 0.0687279 | 0.0385288 | 3.95181 | 0.491603 |
| mse_corr_moment_0p1 | 3 | 40~60% | 0.0798163 | 0.046574 | 4.82059 | 0.499097 |
| mse_corr_moment_0p1 | 4 | 60~80% | 0.0931717 | 0.0551104 | 6.75418 | 0.509581 |
| mse_corr_moment_0p1 | 5 | Top20% | 0.0983028 | 0.0603303 | 7.39662 | 0.514222 |

### Cost Sensitivity Endpoint

| variant | pool | single_side_cost_bps | net_strategy_cumulative_return |
| --- | --- | --- | --- |
| mse | csi1000_etf_sh | 0 | 0.012584 |
| mse | csi1000_etf_sh | 1 | -0.0154732 |
| mse | csi1000_etf_sh | 2 | -0.0427557 |
| mse | csi1000_etf_sh | 5 | -0.120165 |
| mse | csi1000_etf_sh | 10 | -0.235564 |
| mse | csi300_etf_sh | 0 | 0.0242168 |
| mse | csi300_etf_sh | 1 | -0.00346608 |
| mse | csi300_etf_sh | 2 | -0.0304034 |
| mse | csi300_etf_sh | 5 | -0.106939 |
| mse | csi300_etf_sh | 10 | -0.221354 |
| mse | csi500_etf_sh | 0 | 0.0375565 |
| mse | csi500_etf_sh | 1 | 0.00800021 |
| mse | csi500_etf_sh | 2 | -0.0207169 |
| mse | csi500_etf_sh | 5 | -0.102068 |
| mse | csi500_etf_sh | 10 | -0.222959 |
| mse_corr_0p1 | csi1000_etf_sh | 0 | 0.0218747 |
| mse_corr_0p1 | csi1000_etf_sh | 1 | -0.00822514 |
| mse_corr_0p1 | csi1000_etf_sh | 2 | -0.0374412 |
| mse_corr_0p1 | csi1000_etf_sh | 5 | -0.120042 |
| mse_corr_0p1 | csi1000_etf_sh | 10 | -0.242306 |
| mse_corr_0p1 | csi300_etf_sh | 0 | 0.0261226 |
| mse_corr_0p1 | csi300_etf_sh | 1 | -0.00490176 |
| mse_corr_0p1 | csi300_etf_sh | 2 | -0.0349911 |
| mse_corr_0p1 | csi300_etf_sh | 5 | -0.119926 |
| mse_corr_0p1 | csi300_etf_sh | 10 | -0.245245 |
| mse_corr_0p1 | csi500_etf_sh | 0 | 0.0339983 |
| mse_corr_0p1 | csi500_etf_sh | 1 | 0.00293949 |
| mse_corr_0p1 | csi500_etf_sh | 2 | -0.0271894 |
| mse_corr_0p1 | csi500_etf_sh | 5 | -0.11227 |
| mse_corr_0p1 | csi500_etf_sh | 10 | -0.237905 |
| mse_moment_0p05 | csi1000_etf_sh | 0 | -0.000895117 |
| mse_moment_0p05 | csi1000_etf_sh | 1 | -0.0265363 |
| mse_moment_0p05 | csi1000_etf_sh | 2 | -0.0515219 |
| mse_moment_0p05 | csi1000_etf_sh | 5 | -0.12271 |
| mse_moment_0p05 | csi1000_etf_sh | 10 | -0.229723 |
| mse_moment_0p05 | csi300_etf_sh | 0 | 0.0309264 |
| mse_moment_0p05 | csi300_etf_sh | 1 | -0.00024043 |
| mse_moment_0p05 | csi300_etf_sh | 2 | -0.030468 |
| mse_moment_0p05 | csi300_etf_sh | 5 | -0.115793 |
| mse_moment_0p05 | csi300_etf_sh | 10 | -0.24169 |
| mse_moment_0p05 | csi500_etf_sh | 0 | -0.012869 |
| mse_moment_0p05 | csi500_etf_sh | 1 | -0.0427164 |
| mse_moment_0p05 | csi500_etf_sh | 2 | -0.0716642 |
| mse_moment_0p05 | csi500_etf_sh | 5 | -0.153376 |
| mse_moment_0p05 | csi500_etf_sh | 10 | -0.273939 |
| mse_std_floor_0p1 | csi1000_etf_sh | 0 | 0.088334 |
| mse_std_floor_0p1 | csi1000_etf_sh | 1 | 0.0612533 |
| mse_std_floor_0p1 | csi1000_etf_sh | 2 | 0.0348438 |
| mse_std_floor_0p1 | csi1000_etf_sh | 5 | -0.040521 |
| mse_std_floor_0p1 | csi1000_etf_sh | 10 | -0.154173 |
| mse_std_floor_0p1 | csi300_etf_sh | 0 | 0.0363938 |
| mse_std_floor_0p1 | csi300_etf_sh | 1 | 0.0120197 |
| mse_std_floor_0p1 | csi300_etf_sh | 2 | -0.0117834 |
| mse_std_floor_0p1 | csi300_etf_sh | 5 | -0.0798992 |
| mse_std_floor_0p1 | csi300_etf_sh | 10 | -0.183192 |
| mse_std_floor_0p1 | csi500_etf_sh | 0 | 0.0729665 |
| mse_std_floor_0p1 | csi500_etf_sh | 1 | 0.0484673 |
| mse_std_floor_0p1 | csi500_etf_sh | 2 | 0.0245252 |
| mse_std_floor_0p1 | csi500_etf_sh | 5 | -0.0440838 |
| mse_std_floor_0p1 | csi500_etf_sh | 10 | -0.148414 |
| mse_corr_moment_0p1 | csi1000_etf_sh | 0 | 0.0153305 |
| mse_corr_moment_0p1 | csi1000_etf_sh | 1 | -0.0123097 |
| mse_corr_moment_0p1 | csi1000_etf_sh | 2 | -0.0392 |
| mse_corr_moment_0p1 | csi1000_etf_sh | 5 | -0.115572 |
| mse_corr_moment_0p1 | csi1000_etf_sh | 10 | -0.229651 |
| mse_corr_moment_0p1 | csi300_etf_sh | 0 | 0.0337337 |
| mse_corr_moment_0p1 | csi300_etf_sh | 1 | 0.00599554 |
| mse_corr_moment_0p1 | csi300_etf_sh | 2 | -0.021001 |
| mse_corr_moment_0p1 | csi300_etf_sh | 5 | -0.0977358 |
| mse_corr_moment_0p1 | csi300_etf_sh | 10 | -0.212539 |
| mse_corr_moment_0p1 | csi500_etf_sh | 0 | 0.0543254 |
| mse_corr_moment_0p1 | csi500_etf_sh | 1 | 0.0266526 |
| mse_corr_moment_0p1 | csi500_etf_sh | 2 | -0.000296513 |
| mse_corr_moment_0p1 | csi500_etf_sh | 5 | -0.076988 |
| mse_corr_moment_0p1 | csi500_etf_sh | 10 | -0.192 |

### Individual Full Reports

- mse : [artifact-root]/nn/loss-function-1min/stage_b/mse-seed7/research_report/072817_mse-seed7_full_evaluation_report.html
- mse_corr_0p1 : [artifact-root]/nn/loss-function-1min/stage_b/mse_corr_0p1-seed7/research_report/072817_mse_corr_0p1-seed7_full_evaluation_report.html
- mse_moment_0p05 : [artifact-root]/nn/loss-function-1min/stage_b/mse_moment_0p05-seed7/research_report/072820_mse_moment_0p05-seed7_full_evaluation_report.html
- mse_std_floor_0p1 : [artifact-root]/nn/loss-function-1min/stage_b/mse_std_floor_0p1-seed7/research_report/072821_mse_std_floor_0p1-seed7_full_evaluation_report.html
- mse_corr_moment_0p1 : [artifact-root]/nn/loss-function-1min/stage_b/mse_corr_moment_0p1-seed7/research_report/072820_mse_corr_moment_0p1-seed7_full_evaluation_report.html

## 限制与适用边界

Stage B seed7 的 mse_std_floor_0p1 test IC 为 0.0777618206, 高于 MSE 的 0.0688795701. 这是单 seed 筛选, 输出 scale 问题未完全解决. 当前artifact可得性只影响复现, 不作为历史成功/失败判据. 只有matched合同内的结果可以直接比较.

## 结论

本次归档保留上述历史事实. 研究结论, 推广门槛和执行限制分别解释, 不把模型无增益或净收益为负改写成实验流程失败.
