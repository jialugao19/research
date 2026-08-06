# 知识点小册子

本小册子根据 `knowledge/outline.md` 逐步生成。为了避免一次性生成过多内容，每次只写一个尽可能小的知识点，并配套可运行例子、常见坑和自检问题。

## 写作规则

1. 每个小知识点一个 Markdown 文件。
2. 文件按大纲顺序编号，先覆盖 Python，再覆盖概率统计、时间序列、数据结构与算法等后续部分。
3. 对于 `pandas`、`sklearn`、时间序列、机器学习、深度学习、市场微观结构等大主题，必须继续拆成更小的知识点。
4. 每篇默认包含：核心概念、代码或计算例子、常见坑、实战提示、自检问题。
5. 进度记录在 `progress.md`，下一次继续时从第一个未完成知识点开始。
6. 使用外部课程资料时只做原创归纳，必须在文章末尾注明来源、许可和交叉核对资料。

## 当前结构

| 节 | 目录 | 章节 | 主题 |
| --- | --- | ---: | --- |
| 1 | `01-python` | 1–50 | Python 科学计算、数据处理与工程基础 |
| 2 | `02-probability-timeseries` | 51–72 | 概率统计与时间序列 |
| 3 | `03-data-structures-algorithms` | 73–83 | 数据结构与算法 |
| 4 | `04-brain-teaser-green-book` | 84–90 | 概率、组合、博弈与估算题 |
| 5 | `05-machine-learning` | 91–107 | 经典机器学习、诊断与集成 |
| 6 | [`06-deep-learning`](06-deep-learning/README.md) | 108–118 | 基础、训练、序列模型、Transformer 与高效系统 |
| 7 | `07-market-microstructure` | 119–130 | 市场微观结构、组合与回测 |
| 8 | `08-computer-science` | 131–136 | 复杂度、数据结构、SQL、Linux、Git 与计算环境 |

章节号 1–136 全局连续。深度学习节进一步采用 `Part → Chapter → 小知识点` 结构，
其学习顺序和目录说明见 [`06-deep-learning/README.md`](06-deep-learning/README.md)。
