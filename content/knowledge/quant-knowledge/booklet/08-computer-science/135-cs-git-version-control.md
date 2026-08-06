# 135. 计算机基础：Git 版本控制、提交历史、分支、diff 和代码仓库展示

## 核心概念

Git 是版本控制工具。

它解决的问题是：

```text
代码改了什么？
谁改的？
什么时候改的？
为什么改？
能不能回到之前的版本？
能不能同时开发多个方向？
```

对策略开发来说，Git 很重要。

因为策略代码、配置、实验结果和报告都需要可追溯。

没有版本控制，很难回答：

```text
这次回测和上次有什么区别？
这个因子什么时候改过？
为什么线上策略和研究代码不一致？
```

## 仓库和工作区

Git 仓库是被 Git 跟踪的项目目录。

常见命令：

```bash
git init
git status
git add
git commit
```

一个最小例子：

```bash
git init -q
git config user.email demo@example.com
git config user.name Demo
printf 'alpha\n' > factor.txt
git status --short
```

结果：

```text
?? factor.txt
```

`??` 表示新文件还没有被 Git 跟踪。

## 暂存区

Git 有一个 staging area，中文常叫暂存区。

`git add` 把改动放进暂存区。

```bash
git add factor.txt
git status --short
```

结果：

```text
A  factor.txt
```

`A` 表示这个文件将作为新增文件进入下一次提交。

暂存区的好处是：

```text
你可以只提交一部分改动
把无关修改留在工作区
让每个 commit 更清晰
```

## commit

commit 是一次快照。

```bash
git commit -q -m 'add factor file'
git status --short
```

结果：

```text

```

这里输出为空，表示工作区干净。

好的 commit 应该有清楚的边界。

例如：

```text
add turnover cost model
fix lookahead in label alignment
update factor neutralization report
```

不要把无关改动全部塞进一个巨大 commit。

## diff

`git diff` 查看还没提交的修改。

```bash
printf 'alpha\nbeta\n' > factor.txt
git diff -- factor.txt
```

结果：

```text
@@ -1 +1,2 @@
 alpha
+beta
```

diff 里：

```text
- 表示删除
+ 表示新增
```

提交前看 diff 是好习惯。

它能发现：

```text
误删代码
调试输出
路径写错
无关格式化
临时配置
```

## status

`git status --short` 是日常最常用命令之一。

继续上面的例子：

```bash
git status --short
```

结果：

```text
 M factor.txt
```

`M` 表示文件被修改。

常见状态：

```text
?? 新文件未跟踪
A  新文件已暂存
 M 文件已修改但未暂存
M  文件修改已暂存
```

## log

`git log` 查看提交历史。

为了输出稳定，可以只看 commit message：

```bash
git add factor.txt
git commit -q -m 'extend factor file'
git log --pretty=format:%s
```

结果：

```text
extend factor file
add factor file
```

真实项目里，可以用：

```bash
git log --oneline --decorate --graph --all
```

它更适合查看分支结构。

## 分支

分支让你可以并行开发。

查看当前分支：

```bash
git branch --show-current
```

结果：

```text
master
```

不同环境的默认分支可能叫 `main`，也可能叫 `master`。

创建并切换分支：

```bash
git switch -c experiment
git branch --show-current
```

结果：

```text
experiment
```

分支适合：

```text
开发新因子
修复 bug
尝试新模型
写实验报告
处理线上紧急修复
```

## 比较分支

如果想看当前分支和基准分支差了哪些文件，可以用：

```bash
git diff --name-only master..experiment
```

结果：

```text
factor.txt
```

如果你的默认分支叫 `main`，就把 `master` 换成 `main`。

比较分支前先确认：

```bash
git branch --show-current
```

以及：

```bash
git branch
```

避免把错误分支当作基准。

## restore 和 reset

这两个命令都能改变工作区或暂存区，要谨慎。

常见安全用法：

```text
git restore file        丢弃工作区中某个文件的未暂存修改
git restore --staged file  从暂存区拿出来，但保留工作区修改
```

危险用法：

```text
git reset --hard
```

它会丢弃工作区修改。

如果不确定，不要直接运行。

先用：

```bash
git status
git diff
```

看清楚再操作。

## .gitignore

不是所有文件都应该进 Git。

通常不提交：

```text
大数据文件
模型 checkpoint
临时日志
缓存目录
本地虚拟环境
密钥和 token
```

`.gitignore` 用来告诉 Git 忽略这些文件。

例子：

```text
__pycache__/
.venv/
*.log
data-cache/
*.pt
```

策略项目里，大型行情数据和实验产物通常用外部存储或实验目录管理，不直接放进 Git。

## 展示代码仓库

能展示自己的代码仓库，不只是把代码放上去。

一个可读仓库通常包括：

```text
README.md
清晰目录结构
可复现实验或示例命令
依赖说明
配置样例
测试或验证脚本
干净的 commit 历史
没有密钥和大文件
```

面试或合作中，别人经常先看：

```text
README 是否能快速说明项目
代码能否运行
提交历史是否有真实开发痕迹
是否有测试和结果说明
```

## 策略开发中的 Git 习惯

实用习惯：

```text
每个独立改动一个 commit
提交前看 git diff
实验代码和生产代码分支隔离
配置文件示例化，不提交私人路径和密钥
重要实验记录 commit hash
报告里写清楚代码版本
```

例如实验记录里写：

```text
code_version: abc1234
config: configs/exp_001.yaml
data_version: 2026-01-03
```

这样以后才能复现实验。

## 常见错误

Git 常见错误包括：

```text
不看 diff 直接 commit
把大数据文件提交进仓库
把密钥提交进仓库
一个 commit 混入很多无关改动
在错误分支上开发
用 reset --hard 丢掉未保存工作
只会 push，不会看历史和 diff
```

Git 的目标不是制造流程负担。

它的目标是让代码变化可追踪、可回滚、可协作。

## 小结

Git 版本控制要掌握：

```text
git status
git add
git commit
git diff
git log
git branch
git switch
git restore
.gitignore
```

更重要的是工作习惯：

```text
提交前看 diff
commit 范围清晰
实验记录包含代码版本
不提交密钥、大文件和本地缓存
```

下一篇讨论 Docker 或分布式计算框架的基本概念。
