# 深度学习

本节将深度学习从“机器学习补充章节”提升为独立学习线，采用
`Part → Chapter → 小知识点` 的层次组织。结构参考 Datawhale Deep Learning Notes
由基础逐步推进到架构和系统的目录方式；章节内容与顺序按本知识库的量化研究场景重新编排。

## 学习顺序

| Part | 目录 | 重点 | 章节 |
| --- | --- | --- | --- |
| 1 | `01-foundations` | 网络基本闭环与训练正确性 | 108–109 |
| 2 | `02-training-optimization` | 优化器与归一化统计 | 110–111 |
| 3 | `03-sequence-models` | 循环网络、窗口和标签对齐 | 112–114 |
| 4 | `04-attention-transformers` | Attention、时间表示与 Transformer | 115–117 |
| 5 | `05-efficient-systems` | Attention 的 IO 复杂度与工程实现 | 118 |

## 组织原则

1. 先建立“前向—损失—反向—更新”的训练闭环，再讨论具体架构。
2. 把正确性与优化放在模型规模扩展之前，避免只记 API 和模型名称。
3. 从序列建模问题引出 Attention 和 Transformer，而不是孤立罗列组件。
4. 最后补充系统效率，明确数学等价、数值稳定与硬件 IO 是不同层面的问题。

## 来源说明

目录结构与概念表述交叉参考
[Datawhale Deep Learning Notes](https://datawhalechina.github.io/deep-learning-notes/zh/index.html)；
正文均为原创归纳，沿用各篇末尾的来源、许可和论文引用说明。
