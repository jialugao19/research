# 计算机基础：Linux 命令行基本操作、文件查看、搜索、管道和进程管理

## 核心概念

Linux 命令行是数据处理、服务器操作和策略部署的基础工具。

量化和数据工程里，经常需要：

```text
查看日志
检查文件大小
搜索代码和配置
批量移动文件
压缩和解压数据
查看进程
用管道快速统计
```

命令行的优势是：

```text
快
可脚本化
能远程操作服务器
适合处理大量文件和日志
```

## 示例目录

下面用一个小目录作为例子。

```bash
mkdir -p demo/logs demo/data
printf 'time,level,message\n09:30,INFO,start\n09:31,ERROR,missing_price\n09:32,INFO,done\n' > demo/logs/app.log
printf 'dt,symbol,close,volume\n2026-01-02,AAA,10.0,1000\n2026-01-02,BBB,20.0,800\n2026-01-03,AAA,10.5,1500\n' > demo/data/prices.csv
printf 'alpha\nbeta\ngamma\n' > demo/notes.txt
```

后面的命令假设你在 `demo` 目录中执行。

```bash
cd demo
```

## pwd、ls、cd

最基础的三个命令：

```text
pwd: 显示当前目录
ls: 列出目录内容
cd: 切换目录
```

查看当前目录下两层以内的文件：

```bash
find . -maxdepth 2 -type f | sort
```

结果：

```text
./data/prices.csv
./logs/app.log
./notes.txt
```

`find` 比 `ls` 更适合脚本化查找文件。

`sort` 让输出顺序稳定。

## 查看文件开头

查看文件前几行，用 `head`。

```bash
head -n 2 data/prices.csv
```

结果：

```text
dt,symbol,close,volume
2026-01-02,AAA,10.0,1000
```

常见用法：

```text
head -n 5 file
tail -n 20 file
```

`head` 看开头。

`tail` 看结尾。

日志排查时，`tail` 很常用。

## 查看指定行

用 `sed -n` 可以查看指定行范围。

```bash
sed -n '2,3p' logs/app.log
```

结果：

```text
09:30,INFO,start
09:31,ERROR,missing_price
```

这里：

```text
2,3 表示第 2 到第 3 行
p 表示 print
-n 表示只输出指定内容
```

## grep 搜索文本

搜索日志中的错误：

```bash
grep 'ERROR' logs/app.log
```

结果：

```text
09:31,ERROR,missing_price
```

常见选项：

```text
grep -n: 显示行号
grep -i: 忽略大小写
grep -r: 递归搜索目录
```

如果系统有 `rg`，通常优先用 `rg`。

它比传统递归 grep 更适合搜索代码仓库。

```bash
rg 'AAA|ERROR' . | sort
```

结果：

```text
./data/prices.csv:2026-01-02,AAA,10.0,1000
./data/prices.csv:2026-01-03,AAA,10.5,1500
./logs/app.log:09:31,ERROR,missing_price
```

## wc 统计行数

`wc` 用于统计行数、词数和字节数。

```bash
wc -l data/prices.csv
```

结果：

```text
4 data/prices.csv
```

这里 `4` 表示文件有四行。

行情文件检查中，行数很重要：

```text
今天有没有少文件？
某个股票是否缺日期？
JOIN 前后行数是否异常？
```

## cut 取列

CSV 文件可以用 `cut` 快速取列。

```bash
cut -d ',' -f 2,3 data/prices.csv
```

结果：

```text
symbol,close
AAA,10.0
BBB,20.0
AAA,10.5
```

这里：

```text
-d ',' 表示逗号分隔
-f 2,3 表示取第 2 和第 3 列
```

复杂 CSV 不建议长期靠 shell 解析。

但快速检查数据时很有用。

## 管道

管道 `|` 把前一个命令的输出传给后一个命令。

例如统计每个 symbol 出现次数：

```bash
cut -d ',' -f 2 data/prices.csv | tail -n +2 | sort | uniq -c
```

结果：

```text
      2 AAA
      1 BBB
```

这条命令的流程是：

```text
cut 取 symbol 列
tail 去掉表头
sort 排序
uniq -c 计数
```

管道是命令行最重要的思想之一。

小工具可以组合成复杂数据处理流程。

## 重定向

重定向把输出写入文件。

常见形式：

```text
command > file   覆盖写入
command >> file  追加写入
command 2> err   错误输出写入
```

例如：

```bash
grep 'ERROR' logs/app.log > errors.txt
```

这会把错误日志写到 `errors.txt`。

如果文件已存在，`>` 会覆盖。

追加时要用 `>>`。

## du 和 df

查看目录大小：

```bash
du -sh data | cut -f1
```

结果：

```text
4.0K
```

查看磁盘空间：

```bash
df -h
```

`du` 看目录或文件占用。

`df` 看文件系统剩余空间。

服务器上回测或训练任务失败，经常是磁盘空间不足。

## chmod 和可执行文件

脚本要执行，需要有执行权限。

```bash
printf '#!/usr/bin/env bash\necho run\n' > run.sh
chmod +x run.sh
./run.sh
```

结果：

```text
run
```

`chmod +x` 添加执行权限。

`./run.sh` 表示执行当前目录下的脚本。

如果只写 `run.sh`，shell 不一定会在当前目录查找。

## ps 和进程

查看当前 shell 进程名：

```bash
ps -o pid=,comm= -p $$ | awk '{print $2}'
```

结果：

```text
bash
```

常见进程相关命令：

```text
ps aux: 查看进程
top / htop: 动态查看资源
kill PID: 结束进程
kill -9 PID: 强制结束进程
```

不要随便 `kill -9`。

它不给程序清理资源的机会。

## tar 压缩和解压

常见压缩命令：

```bash
tar -czf demo.tar.gz data logs
```

含义：

```text
-c: create
-z: gzip
-f: file
```

解压：

```bash
tar -xzf demo.tar.gz
```

日志、模型结果、实验产物经常用 tar 打包。

## 命令行安全习惯

命令行很强，也很容易误删。

尤其小心：

```text
rm -rf
mv 覆盖文件
> 覆盖输出
通配符 *
在错误目录执行命令
```

更安全的习惯：

```text
先 pwd 确认目录
先 ls 或 find 看匹配范围
删除前用 echo 预览
重要文件先备份
脚本里使用 set -euo pipefail
```

## 策略开发中的常用场景

命令行在策略工作中的常见用途：

```text
查找某个因子名出现在哪些文件
统计某天行情文件行数
查看最新日志错误
压缩回测结果
检查磁盘空间
查看长时间运行的训练或回测进程
批量重命名和移动文件
```

熟练命令行不是为了替代 Python。

而是让你能更快定位数据、日志和环境问题。

## 小结

Linux 命令行要先掌握：

```text
pwd / cd / ls / find
head / tail / sed
grep / rg
wc / cut / sort / uniq
管道 |
重定向 > >>
du / df
chmod
ps / kill
tar
```

核心不是背命令。

而是理解：

```text
文件是输入输出
命令可以组合
管道连接处理步骤
先检查再执行破坏性操作
```

下一篇讨论 Git 版本控制。
