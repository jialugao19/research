---
title: Prediction-NN 全实验研究综述与报告索引
date: 2026-11-03
summary: 汇总33个历史实验, 分开说明流程成功/失败, 研究结果和当前复现条件.
tags:
- prediction-nn
- registry
- research-summary
featured: false
---

## 摘要

本综述覆盖中央registry的全部33个实验, 包含1min与两个独立1s合同. 本轮按内容hash核对报告, 补齐26份REPORT缺失HTML.

历史成功/失败按实验流程是否成功完成判断. 无增益, 成本后亏损, 归档和当前 artifact 缺失不改变历史成功事实. 失败的实验臂保留失败原因, 不填造未产生的 OOS 指标. 本次只整理已有材料, 未启动训练, 推理或回测.

## 研究背景与目标

解决报告散落, 旧综述过期, 实验与报告关联缺失的问题. 研究状态与证据可得性分开记录, 让历史成功结果及失败臂都可追溯. 旧0712/0714综合报告是17实验的历史快照; 0824生成物覆盖29实验, 均不替代当前33实验汇总.

## 数据与方法

只读取registry显式登记的manifest/results/summary, 原始报告及其轻量来源表. HTML按SHA256去重, 保留来源别名. Feature-family ablation归入multiscale父实验, 不新增重复实验.

| 比较维度 | 必要说明 |
| --- | --- |
| 样本 | split日期, test universe, 过滤条件和coverage必须明确 |
| 标签 | close/VWAP, horizon, entry lag各自解释 |
| 训练 | model/feature/sampler/budget与checkpoint候选网格明确 |
| 指标 | pooled IC与timestamp/day IC分开; gross, net, proxy分别解释 |
| 历史结果 | 流程成功/失败依据历史记录; 不以当前artifact存在性判断 |

## 主要结果

### 全实验索引

| experiment_id | 历史结果 | 关键发现与边界 | 报告 |
| --- | --- | --- | --- |
| reference-baseline | 历史成功 | 20k checkpoint 的 full-test pooled IC 为 0.0703447025, 保留为历史 close-label 锚点. 当前 run artifact 缺失只限制复现. | [证据报告](../../prediction-nn-1min/1103-reference-baseline-full-070110/) |
| day-pure-batch-1min | 历史成功 | 一个 epoch 的 date-pure 训练完成68659 steps, 1374次 purity 采样均为单日. Selected iter30000 test IC/RankIC 为0.103878/0.064245; 缺 matched mixed-date control. | [证据报告](../../prediction-nn/0811-day-pure-batch-1min/) |
| multiscale-market-features-1min | 历史成功 | 修正 mixed-normalization 评估后 full63 test IC/RankIC 为0.061496/0.051659. Matched family ablation 中 relative/liquidity9 为0.098183/0.075886; market16 在训练 gate 停止, 未读取 test. | [证据报告](../../prediction-nn/0812-multiscale-63feature-evaluation/) |
| reference-baseline-v2 | 历史成功 | 相同 paired_vwap_valid 样本上 VWAP 相对 close 的三个 paired seed IC 增量均为正. seed13 为 0.0744533729 vs 0.0605061430. 成本后结果仍负. | [证据报告](../../prediction-nn-1min/1103-reference-baseline-v2-full-071714/) |
| optimize-1min-model | 历史成功 | GRU192×2 last-hidden 在 seeds 7/11/13 的 IC 和 RankIC 均优于 attention, 平均 test IC 为 0.0789459. TCN 的 seed7 gate 未通过. | [证据报告](../../prediction-nn-1min/1103-optimize-1min-model-final-comparison-072504/) |
| loss-function-1min | 历史成功 | Stage B seed7 的 mse_std_floor_0p1 test IC 为 0.0777618206, 高于 MSE 的 0.0688795701. 这是单 seed 筛选, 输出 scale 问题未完全解决. | [证据报告](../../prediction-nn-1min/1103-loss-function-1min-final-comparison-072821/) |
| baseline-1s-0720 | 历史成功 | Fold0 step194640 的 conditional timestamp test IC 为 0.1068132851. Coverage selection bias 与成本后负收益仍限制使用, 不与独立 OHLCV-only v2 直接排名. | [证据报告](../../prediction-nn/0730-stock1s-feature-health-v2/) |
| baseline-main-20260622 | 待核对 | 在 REPORT, 网站及当前 checkout 中未定位到可归属于该实验的独立正式报告. 历史 capacity 报告引用它的数据目录, 不能据此确认其自身训练成功或失败. | [证据报告](../../prediction-nn-1min/1103-baseline-main-20260622-registry-evidence/) |
| test-all | 历史成功 | touch-test-all 诊断已产出, test pooled IC 为 0.088842. 它采用未过滤 test universe, 不能与 all/touch/limit 主矩阵直接排序. | [证据报告](../../prediction-nn-1min/1103-test-all-touch-test-all-061318/) |
| limit-pool | 历史成功 | all/touch/limit 主矩阵已完成. touch 的 test pooled IC 为 0.0691368, all 为 0.0686563. 改变总体的 touch-test-all 单列解释. | [证据报告](../../prediction-nn-1min/1103-test-all-touch-test-all-061318/) |
| near-zero-filter | 历史成功 | 三臂 full train/evaluation 已完成. ret-ge2-nz5e-4 在 pooled IC 与高预测组收益上领先, flat-ret123-oc 在 hit-rate 指标上领先, 不合成单一 winner. | [证据报告](../../prediction-nn-1min/1103-near-zero-filter-comparison-061720/) |
| learning-rate | 历史成功 | 固定 final iter110000 协议支持 warmup_cosine, lr=0.009, seeds 7/11/19 平均 test IC 为 0.0735400370. 更高学习率中的发散臂单列为失败. | [证据报告](../../prediction-nn-1min/1103-learning-rate-registry-evidence/) |
| rolling-purged-val | 历史成功 | 三个 rolling/purged fold 已记录验证 IC 0.0642117, 0.0647218, 0.0687591. 当前源报告和 run artifact 缺失, 不改变历史完成事实. | [证据报告](../../prediction-nn-1min/1103-rolling-purged-val-registry-evidence/) |
| val-select | 历史成功 | 历史 full-grid audit 支持三 fold, 最后20个验证日, IC mean−0.5 std, earliest top2 的选择规则. 该 audit 的 test 已被查看, 不能视为新的盲选验证. | [证据报告](../../prediction-nn-1min/1103-val-select-registry-evidence/) |
| capacity-robust-sampling | 历史成功 | 五臂 validation 矩阵已完成. 所有臂均在10k达到峰值, 降低容量改善后期保持率但未推迟峰值. 当前 run artifact 缺失只限制复现. | [证据报告](../../prediction-nn-1min/1103-capacity-robust-sampling-self-constrained-html/) |
| prediction-calibration | 历史成功 | 相同 paired_vwap_valid 总体上的 A2 VWAP endpoint 改动提高 IC, RankIC 和 spread. A3 robust-label 方案未通过 calibration promotion gate, 属于已完成的负结果. | [证据报告](../../prediction-nn-1min/1103-prediction-calibration-label-noise-070814/) |
| generalization-rolling-stride | 历史成功 | Rolling/stride 比较已完成. stride5 接近 reference, 原 stride10 selector 选择 iter0; 10k recovery 属于 post hoc 诊断. 不同年份的 fold 不直接排名. | [证据报告](../../prediction-nn-1min/1103-generalization-rolling-stride-comparison-070913/) |
| generalization-adjacent-window | 历史成功 | 单 seed 比较中 dense 的 pooled IC 最高, block70 epoch 的 block 方法 RankIC 和 gap 较好. Test 只覆盖至2024-07-26, 不与全年参考直接比较. | [证据报告](../../prediction-nn-1min/1103-generalization-adjacent-window-comparison/) |
| generalization-adjacent-window-multiseed | 历史成功 | Seeds 7/17/27 中 Dense 的平均 test IC 为 0.0779182, Block70 epoch 为 0.0642507; Block70 pooled-IC win rate 为0/3. 负增益不构成流程失败. | [证据报告](../../prediction-nn-1min/1103-generalization-adjacent-window-multiseed-comparison/) |
| generalization-block70-checkpoint-curve | 历史成功 | 11个 checkpoint 的诊断已完成. Block70 epoch 早期达峰, 后期 test IC 下降且 gap 扩大. 全曲线 test exposure 使其不能作为 blind checkpoint selection. | [证据报告](../../prediction-nn-1min/1103-generalization-block70-checkpoint-curve-report/) |
| main-combo-integration | 历史成功 | 四臂 seed7 比较与 baseline verification 已完成. 未过滤 baseline 的 test IC 为0.075855, 高于 touch, ret-ge2 及其组合, 不支持局部增益直接叠加. | [证据报告](../../prediction-nn-1min/1103-main-combo-integration-baseline-062916/) |
| zero-aware-normalization | 历史成功 | 四个 zero-aware transform 已有历史结果, F24 三臂 IC 约为0.0722-0.0725. 缺少 off control 且旧 model card 有不一致, 不能据此归因增益. | [证据报告](../../prediction-nn-1min/1103-zero-aware-normalization-comparison/) |
| l2-features | 历史成功 | L2 训练和评估已产生历史结果, all_fast12 观察 test IC 为0.0805. Baseline/LOO 与 only/all_fast12 的 checkpoint 候选数为11 vs 1, 因而贡献归因无效, 不等于实验流程失败. | [证据报告](../../prediction-nn-1min/1103-l2-features-attribution-070312/) |
| feature-cleaning-bundle-0609 | 历史成功 | F15 feature-cleaning full report 保留了历史训练与评估结果. 精确 launch overrides 和当前 run artifact 不齐, 该版本不作为当前 baseline. | [证据报告](../../prediction-nn-1min/1103-feature-cleaning-0609-04-061018/) |
| combo-touch-nz-lr | 历史成功, 限 old-LR arm | old-LR touch-ret-ge2 arm 已完成, test IC 为0.062477, 与 main-combo 的同臂为同一历史证据. 计划中的 lr=0.009 arm 未定位结果, 不对其判定失败. | [证据报告](../../prediction-nn-1min/1103-combo-touch-nz-lr-old-lr-062701/) |
| baseline-1min-0813 | 历史成功, 限 sanity | Native v2 的 causal/shuffled/shifted synthetic sanity 已成功, R²为0.999700/−0.445876/−0.083254. 独立正式63D模型报告仍未定位, 不写成训练失败. | [证据报告](../../prediction-nn-1min/1103-baseline-1min-0813-registry-evidence/) |
| baseline-1s-v2 | 历史成功 | 独立42D OHLCV-only v2 完成全量165740198个 test endpoint. pooled IC/RankIC 为0.009249/0.004643; 固定10 bps回测净累计收益−95.14%, 不支持部署. | [证据报告](../../prediction-nn-1s/1103-baseline-1s-v2-full-report-0812/) |
| crossday-rolling | 历史成功, 限 boundary diagnostics | A/B/C synthetic 与3日×128股票诊断成功. 真实 matched A/B差值为0, A/C最大差0.968504, B减少5120个 feature rows. 正式模型比较报告仍未定位. | [证据报告](../../prediction-nn-1min/1103-crossday-rolling-registry-evidence/) |
| horizon-labels | 历史成功 | 相同 test endpoints 上 h10/h15/h30 pooled IC 为0.076663/0.091156/0.090441. Horizon 改变收益分布, 不把IC或标签收益直接解释成净交易提升. | [证据报告](../../prediction-nn/0815-horizon-label-comparison/) |
| market-sample | 历史成功 | Matched 三臂 test IC: baseline 0.087928, panel mean/std 0.125979, market16 0.072220. 单 seed, 单 split, 三臂10M净Sharpe均负. | [证据报告](../../prediction-nn/0822-market-context-comparison/) |
| 0825-feature-audit | 历史成功 | 36D单臂完成全链路, iter6762覆盖176134322行test. Gross累计收益260.18%, 10M net累计收益−96.58%. 无 matched旧特征control, 中央结果未记录pooled IC scalar. | [证据报告](../../prediction-nn-1min/1103-0825-feature-audit-model-report-0827/) |
| 0827-market-cs | 历史成功, 四臂完成 | Control/CS rank/latent-z/Deep Sets R2 test IC为0.086462/0.123293/0.127345/0.121030. Induced attention 在test前失败; Deep Sets经历中断后R2成功恢复. 四个完成臂10M净Sharpe均负. | [证据报告](../../prediction-nn-1min/1103-0827-market-cs-comparison-0831/) |
| 0903-model | 历史成功 | 41D latent-z selected iter105343 的full-test IC/RankIC为0.1270440556/0.1012013681. 10M净累计收益−93.66%, 仅支持冻结的shadow inference与研究比较. | [证据报告](../../prediction-nn-1min/1103-0903-model-full-report/) |

### 失败, 恢复与负结果

| 实验臂 | 历史结果 | 原因 | 结果边界 |
| --- | --- | --- | --- |
| 0827-market-cs / induced attention | 历史失败 | prediction variance collapse, gate在test前失败 | 未产生OOS指标 |
| 0827-market-cs / Deep Sets原group | 历史中断, R2恢复成功 | group fail-fast中断后按immutable checkpoint做exact recovery | 最终R2 test IC 0.121030 |
| multiscale family / market16 | 历史失败, training gate终止 | iter6762触发train/val RankIC gap gate | 未读取test |
| learning-rate / lr0.010 seed11 | 历史失败 | invalid seed, 不进入最终均值 | 原协议记录 |
| learning-rate / lr0.011 seed11 | 历史失败 | 训练日志记录divergence, 无final summary | 原协议记录 |
| generalization / stride10 | 流程已完成, selector负结果 | 原selector选择iter0; iter10000是post hoc恢复 | 不把零IC或负增益判为流程失败 |

### 研究结论

B+VWAP的paired endpoint改动与compact GRU各有匹配证据; 新增信息中relative/liquidity family及market context出现信号增益. 过滤与Block70的优势没有稳定叠加或跨seed保持. 这些发现均受各自样本和选模合同约束. 1s v2与多个market-context模型的成本后收益为负, 不支持把信号质量直接外推为实盘净收益.

## 限制与适用边界

未定位结果不等于未执行或失败. baseline-main在历史capacity报告中只作为数据目录出现; baseline-1min-0813与crossday-rolling已有成功诊断, 正式模型结果仍待核对. 三个checkout历史中继承的report/index.html实际是stock1s v2报告, 不能按所在分支归属给1min实验.

Artifact当前缺失只记录为复现条件. L2选模网格不匹配, zero-aware缺control, 部分泛化研究test已反复查看, 都限制结论强度, 不撤销历史成功事实.

## 结论

本轮把历史实验, 原报告和网站实体连通. 后续研究应按同合同验证候选, 不从当前汇总重新选择checkpoint, 不把原有test重复作为新的盲测. 尚未定位的正式结果保留在下表, 不自动发起补跑.

| 待核对项目 | 已确认事实 | 尚未确认 |
| --- | --- | --- |
| baseline-main-20260622 | 数据准备目录曾被capacity实验引用 | 独立正式run/report身份 |
| baseline-1min-0813 | native v2 synthetic sanity成功 | 独立63D正式模型结果 |
| crossday-rolling | A/B/C synthetic与bounded real gate成功 | 正式全量训练与比较报告 |
| combo-touch-nz-lr | old-LR arm历史成功 | 计划lr=0.009 arm结果 |

## 附录

事实来源: `nn-registry/experiment-index.yaml`, `report-index.yaml`, 每实验的 `manifest.yaml`, `results.yaml` 和 `experiment-summary.md`. 原始图表与方法见上表证据报告. 本综述只复述已登记数值, 不重算实验指标. 本次材料整理日期为2026-11-03, 不代表实验运行日期.
