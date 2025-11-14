# Python程序——遇到问题与总结

## 函数导入

> [!NOTE]
>
> - **绝对导入：**从项目根目录开始的完整路径，清晰稳定。
> - **相对导入：**基于当前模块位置的导入，适用于包内部，简洁灵活但有限制。
> - **\_\_init\_\_.py：**定义包的存在，并可通过在此文件中导入内容来控制包级别的接口，简化外部对该包内资源的访问。

在 math_utils.py 中，有个函数 add：

```python
# math_utils.py
def add(a, b):
    return a + b
```

在另一个文件夹中的 main.py，导入 add 函数：

```python
# main.py

# 方法一：导入整个模块
import math_utils
result = math_utils.add(2, 3) # 需要使用模块名前缀

# 方法二：从模块导入特定函数
from math_utils import add
result = add(2, 3)

# 方法三：导入模块并重命名
import math_utils as mu
result = mu.add(2, 3)

# 方法四：从模块导入所有公共名称（不推荐）
# from math_utils import *
# result = add(2, 3) # 注意，这种方式可能导致命名冲突
```

### 绝对导入（Absolute Import）

​	绝对导入是从项目的**根目录**（或者说是 Python 解释器的模块搜索路径 `sys.path`中的某个顶级目录）开始，完整地指定模块的路径。

- **优点：**清晰明确，无论从哪个文件进行导入，路径都是一样的。易于理解和维护，不容易出错。
- **缺点：**如果项目结构很深，导入语句会比较长。

```
my_project/
│
├── main.py
├── package1/
│   ├── __init__.py
│   ├── module1.py
|	├── helper.py
│   └── subpackage1/
│       ├── __init__.py
|		├── sibling.py
│       └── module2.py
└── package2/
    ├── __init__.py
    └── module3.py
```

​	从项目根目录`my_project`开始计算完整模块路径，package1.module1`,`package1.subpackage1`,`package2.module3`：

- 在`main.py`中导入`module`中的函数：

```python
# main.py
from package1.module1 import some_function
```

- 在`package1/subpackage/module2.py`中导入`package2/module3.py`中的函数：

```python
# package1/subpackage1/module2.py
from package2.module3 import another_function
```

### 相对导入(Relative Import)

​	相对导入是相对于**当前模块所在包**的位置来指定要导入的模块。它只能在包内部使用，并且主要用于包内模块之间的相互引用。

- **优点：**当包被移动或重命名时，包内的相对导入不需要修改。语句通常较短。
- **缺点：**只能在包内使用，不能从主脚本（即不在任何包内的顶层脚本）中使用。对于不熟悉项目结构的人来说，可能不如绝对导入直观。

​	***语法：***

- 单个点`.`表示当前包目录。
- 两个点`..`表示上一级包目录。
- 三个点`...`表示上两级包目录，以此类推。

​	依旧使用上述项目目录（*1.1.1 绝对导入*）

- 在`package1/module1.py`中导入同一包下的其他模块：

```python
# package1/module1.py 
from . import helper # 导入同级的 helper 模块
from .helper import func # 从同级的 helper 模块导入 func
```

- 在`package1/subpackage1/module2.py`中导入：

```python
# package1/subpackage1/module2.py

# 导入父包 package1 中的 module1
from .. import module1
from ..module import some_function_in_module1

# 导入同级包 subpackage1 中的其他模块
from . import sibling
from .sibling import func_from_sibling

# 导入 package1 中的其他模块（通过父包）
from .. import module1
```

​	***重要限制：***相对导入**不能**从一个不是作为包一部分的脚本中执行。

```
如果你直接运行 python package1/subpackage1/module2.py，并且 module2.py 使用了相对导入，那么会报错 ImportError: attempted relative import with no known parent package。必须将包含该包的目录加入到 Python 路径中，然后从包外部以模块的方式运行，例如 python -m package1.subpackage1.module2。
```

### \_\_init.py\_\_导入

​	`__init__.py`文件对于Python包至关重要。它主要有以下几个作用，其中与导入密切相关的是前两个：

- **标识包：**Python 识别一个目录为包（Package）的标志就是该目录下存在`__init__.py`文件；
- **控制包导入：**到导入一个包（例如`import package1`）时，实际上是执行了`package1/__init__.py`文件中的代码；
- **简化导入路径：**可以在`__init__.py`中导入包内子模块或子包，甚至是具体函数 / 类，使得使用者可以通过包名直接访问它们，而无需知道具体的子模块路径。

```python
# package1/__init.py

# 方式一：直接导入子模块，使它们成为 package1 命名空间的一部分
# import package1.module1
# import package1.subpackage1

# 方式二：从子模块导入具体内容到包级别
from .module import important_function
from .subpackage1.module2 import specific_utility

# 方式三：定义 __all__ 控制 from package1 import * 导入的内容
__all__ = ['important_function', 'specific_utility']
```

​	这样做的效果是：

- 在`main.py`或其他地方使用`Import package1`后，可以直接调用`pacakage1.important_function()`和`package1.specific_utility()`，就像它们是在`__init__.py`中定义的一样；
- 如果定义了`__all__`，那么`from package1 import *`就只会导入`important_function`和`specific_utility`；
- 这极大地简化了包的使用者的导入语句，提供了更干净的 API 接口。

## docker

### docker 文件配置

#### Dockerfile

- python不知道自己的工作目录，需要指明python的工作目录【ModuleNotFoundError: No module named 'HTTP'】

  - ```dockerfile
    ENV PATH=$PATH:/app # 看 WORKDIR 的根目录
    ENV PYTHONPATH /app
    ```

```dockerfile
# 制定构建基础镜像
FROM hub.n2m.cn/library/python:3.11-slim
# 在后面路径文件中，匹配deb.....org，替换mirrors.....cn（中科大镜像源）
RUN sed -i 's/deb.debian.org/mirrors.ustc.edu.cn/g' /etc/apt/sources.list.d/debian.sources
# 设置pip的默认包源为清华大学PyPI
RUN pip config set global.index-url https://pypi.tuna.tsinghua.edu.cn/simple
# 在容器内创建并进入 /app 目录
WORKDIR /app

# 【ModuleNotFoundError: No module named 'HTTP'】
# python不知道自己的工作目录，需要指明python的工作目录
ENV PATH=$PATH:/app
ENV PYTHONPATH /app

# 安装 uv
RUN pip install uv
# 复制本地的 pyproject.toml 到 app 目录下
COPY pyproject.toml .
# 根据 pyproject.toml 创建项目依赖
RUN uv sync
# 类似与"pip install -r requirements.txt"
COPY . .
```

#### docker-compose.yml

```dockerfile
services:
  app:
    build: .
    container_name: ProcessSimplification
#    environment:
#      - PYTHONPATH=/app
    ports:
# 服务器端口 : 容器端口
      - 9527:8443
      - 9528:8444
      - 9529:8445
    volumes:
# 服务器路径:容器路径
#      - ./:/app
      - ./HTTP/files:/app/HTTP/files
      - ./HTTP/received_files:/app/HTTP/received_files
    command: uv run main.py
```

### docker 容器启动

- `docker-compose down -v`：停止并删除所有由 docker-compose.yml 定义的服务容器及相关资源。
- `docker-compose build --no-cache`：重新构建服务镜像，不使用之前的缓存层。
- `docker-compose up`：启动并运行所有服务。

|                  场景                  |        是否需要全套命令        |
| :------------------------------------: | :----------------------------: |
| 修改了`Dockerfile`或 `requirement.txt` |            强烈推荐            |
|      修改了源代码（如python文件)       |              推荐              |
|             第一次运行项目             |              推荐              |
|      只是重启服务（没有代码变化）      | 只需要`docker-compose restart` |
|         想保留数据（如数据库）         |          不需要用`-v`          |

## uv操作

### uv常见命令以及作用

​	uv 是Python的包管理工具，类似 pip。其核心优势就是速度快，设计目标就是比单独使用 `python -m venv` 和 `pip`快得多。其作用：

- 创建和管理 Python 虚拟环境（替代 `venv` ）
- 安装、升级和管理 Python 包（替代 `pip`）
- 管理 Python 项目的依赖关系（类似于 `Poetry` 或 `Pipenv`，但速度更快）

​	**uv 常见命令 以及 作用**：

1. 安装与验证
   - 安装 uv： `pip install uv`；
   - 验证 uv 是否正确安装： `uv --version`;
2. 管理 Python 版本（对项目至关重要）
   - 列出系统上可用的 Python 版本 ：`uv python list`
   - 安装特定的 Python 版本（首次需要 `--fetch`标志）： `uv python install 3.11`（或 `3.12`等）
   - 为项目锁定 Python 版本（会在项目目录下创建 `.python-version`文件）：在你的项目目录中运行 `uv python pin 3,11`。
     - 这确保了协作开发时大家使用相同的 Python 版本。
3. 创建虚拟环境（更快的`venv`替代品）：
   - 在当前目录下创建一个名为 `.venv`（标准名称）的新环境，使用已锁定/项目制定的 Python ：`uv venv`
   - 创建一个自定义名称 / 路径的环境：`uv env my_env_name`
   - 为环境制定 Python 版本：`uv venv --python 3.9`（如果系统中有 Python 3.9）
   - 【*注意：如果你是通过`pyproject.toml`管理依赖，通常不需要显示运行此命令`uv venv`：因为当你运行 `uv sync`（或者首次运行 `uv add`）时，如果它发现当前目录下没有虚拟环境（比如 `.venv` 文件夹），它会**自动为你创建一个**。你不需要先手动运行 `uv venv` 再去运行 `uv sync`*】
4. 安装包（更快的`pip install`替代品）：
   - 首先激活你的环境：`source .venv/bin/activate`(Linux/masOS) 或 `.venv/Scripts/activate`(Windows)。（或者，很多 `uv`命令可以通过`--python`标志直接指定环境路径，无需激活，但激活是一种常见做法）
   - 安装单个包：`uv pip install requests`
   - 安装多个包：`uv pip install numpy pandas flask`
   - 从`requirements.txt`安装：`uv pip install -r requirements.txt`
   - 【*注意：对于通过`pyproject.toml`管理的项目，更推荐使用下面的`uv sync`*】
5. 项目依赖管理（现代化工作流-类似 Poetry / Pipenv）：
   - 初始化项目：在你的项目根目录下，运行`uv init`。这里会创建一个基本`pyproject.toml`文件
   - 添加依赖：将一个包添加到项目的依赖项中（会记录在`pyproject.toml`中并安装到项目环境中）：`uv add requests`
   - 添加开发依赖：添加仅开发 / 测试时需要的包：`uv add pytest --group dev`(或 `--dev`)
   - 安装依赖（同步）：克隆项目或更新`pyproject.toml`后，安装其中列出的所有依赖：`uv sync`。他读取`pyproject.toml`并确保你的环境与定义的依赖一致。他还会自动创建`.venv`(如果不存在的话)
   - 移除依赖：`uv remove requests`
6. 运行脚本 / 命令（便携功能）：
   - 在项目的环境中运行命令，而无需激活环境：`uv run python script.py`或`uv run pytest`。
   - 运行已安装的工具 / 脚本：`uv run black`（如果环境中已安装`black`）

### 快速入门工作流程

1. 导航到你的项目根目录
2. 锁定所需的 Python 版本：`uv python pin 3.11`
3. 初始化项目（如果是新项目）：uv init
4. 添加依赖：`uv add <package_name>`
5. 同步/ 安装依赖：`uv sync`
6. 运行你的代码 / 测试：`uv run python ...` 或激活环境后正常运行

### 获取 requirement.txt 

1. **方法一：使用`pip freeze`**（最简单直接，依赖虚拟环境）

​	`pip freeze`会列出当前 Python 环境中所有已安装的包及其版本，适合在虚拟环境中使用（避免混入全局环境的无关包）。

```bash
# 一、创建并激活虚拟环境（推荐，避免冗余依赖）
## 1、创建虚拟环境（venv是Python自带模块）
python -m venv .venv

## 2.1、激活虚拟环境（Windows）
.venv\Scripts\activate
## 2.2、激活虚拟环境（Mac/Linus）
source .venv/bin/activate

# 二、安装项目所需依赖
## 在虚拟环境中，通过 pip install 安装项目用到的所有包（如 pip install requests pandas）

# 三、生成requirements.txt
pip freeze > requirements.txt
## 此时当前目录会生成 requirements.txt 包含虚拟环境中所有安装的包及其版本（例如 requests==2.31.0）
```

2. **方法二：使用`pipreqs`**（只提取项目实际使用的依赖，更精简）

- `pip freeze`的缺点是会包含环境中未被项目使用的冗余包（比如手动安装后没用到的包）
- `pipreqs`工具可以扫描**项目代码**，只提取实际被`import`的包，生成更加精简的`requirements.txt`

```bash
# 1.安装 pipreqs
pip install pipreqs

# 2.在项目根目录进行(扫描当前目录下的代码)
pipreqs ./ # 如果提示文件已存在，则可加 --force 覆盖。 pipreqs ./ --force
```

- 优点：只包含项目实际使用的依赖，体积更小；
- 缺点：可能会漏检动态导入的包（如`__import__("requests")`），需要手动检查补充。

3. **方法三：使用现代包管理工具（如`poetry` / `pipenv`）**

- 如果项目使用`poetry`或`pipenv`等工具管理依赖，可直接导出`requirements.txt`：

```bash
# peotry
## 1.安装 poetry (若未安装)
curl -sSL https://install.python-peotry.org | python3 -

## 2.导出依赖
peotry export -f requirements.txt --output requirements.txt

# pipenv
## 1.安装 pipenv (若未安装)
pip install pipenv

## 2.导出依赖
pipenv lock -r > requirements.txt
```

***【注意事项】***

- 生成`requirements.txt`后，建议手动检查是否包含多余或缺失的依赖（尤其是`pipreqs`可能漏检的情况）。
- 自己使用他人项目时，可通过 `pip install -r requirements.txt` 一键安装所有依赖 【也可按照1.3.2 快速XX流程中的4.安装包】

## Git 使用

### Git 是什么？

- Git 是一个**分布式版本控制系统**。简单来说，就像是一个强大的“时光机”和“多方协作笔记本”，记录项目文件的每一次变动，让你可以：

  - **追踪历史：**查看谁在什么时候修改了什么；

  - **回退版本：**不小心删错了，可以回到之前的某个状态；

  - **协作工作：**多人同时修改项目而不相互干扰（通过分支和合并）；

  - **备份代码：**代码存放在不同的地方（本地、远程仓库），不易丢失；

- **三个工作区域**：
  - **工作区（Working Directory）：**你当前看到和编辑的文件；
  - **暂存区（Staging Area / Index）：**一个临时区域，存放你准备提交（保存）到历史记录的更改；
  - **本地仓库（.git）：**存储项目完整历史记录的地方，位于你的项目目录下的`.git`文件夹中。
- **基本工作流程：**
  - 修改文件（工作区）=> `git add`（放到暂存区）=> `git commit`（保存到本地仓库）

### 核心命令与工作流程

1. **初始化与克隆（开始）：**
   - **初始化新仓库：**在你的项目根目录里运行`git init`，把这个文件夹变成一个 Git 仓库。
   - **克隆现有仓库：**从远程服务器（如 GitHub）获取一个仓库的完成副本到本地：`git clone <仓库URL>`。这会自动创建一个同名文件夹并下载代码和历史记录。
2. **查看状态与差异（了解现状）：**
   - **查看状态：**`git status`---显示工作区和暂存区的状态。【告诉你哪些文件被修改了、哪些已暂存等待提交、哪些未被跟踪】
   - **查看差异：**
     - `git diff`---显示**工作区**与**最后一次提交**之间的差异（即你做了哪些还没`add`的修改）。
     - `git diff --staged`(或`--cached`)---显示**暂存区**与**最后一次提交**之间的差异（即你准备提交哪些修改）。
3. **跟踪与提交（保存更改）：**
   - **添加到暂存区：**
     - `git add <文件名>`---将指定文件的修改添加到暂存区。
     - `git add .`---将当前目录下所有修改过的文件（包括新增的）一次性全部添加到暂存区。【高频使用】
   - **提交到本地仓库：**
     - `git commit -m "描述本次修改的信息"`---将暂存区的内容永久保存为一次新的提交（Commit），并附带一条说明信息。【高频使用】
   - **一步到位：**
     - `git commit -am "描述信息"`---结合了`add`和`commit`，对已跟踪的文件（之前提交过或add过的）直接暂存并提交。【高频使用，但注意不包括新文件】

4. **查看历史（追溯过去）：**
   - `git log`---显示提交历史，按时间倒序排列。【会看到每次提交的哈希值（ID）、作者、日期和提交信息】
   - `git log --oneline`---简洁地一行显示每次提交。【只显示简短 ID 和信息】
5. **撤销与回退（修正错误）：**
   - **撤销工作区修改**（未 `add`）：`git checkout -- <文件名>`---丢弃==工作区==中指定文件的修改，恢复到最后一次`add`或`commit`的状态。【*谨慎使用，修改会丢失*】
   - **撤销暂存区修改**（已`add`，未`commit`）：`git reset HEAD <文件名>`---将文件从暂存区移回工作区，取消暂存。（修改还在工作区，只是不在准备提交）
     - Git 的`reset HEAD`命令需要基于 “已有提交记录” 来操作，而仓库是新建的（No commits yet），HEAD 没有可指向的提交版本，所以会提示 “unknown revision or path”。
     - 只有仓库有至少一次提交后，`git reset`才能正常使用。
   - **回退到之前的提交**（已`commit`）：`git reset --hard <提交ID>`---将工作区和暂存区都回退到指定的提交状态。【非常危险，之后的提交会被丢弃，***谨慎使用***】
6. **远程仓库交互（协同与备份）：**
   - **第一次提交：**`git remote add <自己命名，默认名origin> <远程仓库的URL>`
   - **若输错 URL 需修正：：**`git remote set-url origin 新地址.git`
   - **查看远程仓库：**`git remote -v`---显示已配置的远程仓库地址
   - **推送（Push）：**`git push origin <分支名>`---将本地指定分支的提交推送到名为`origin`的远程仓库。【例如，首次推送主分支：`git push -u origin main`（`-u`设置上游关联），后续可直接`git push`（因为设置了 `-u`，会推送到关联的远程分支）高频使用】
   - **拉取（Pull）：**`git pull origin <分支名>`---从远程仓库获取指定分支的最新更改，并尝试自动合并到你的当前分支。【高频使用】
7. **分支（并行开发）：**
   - **查看分支：**`git branch`---列出本地所有分支，当前所在分支前会有`*`。
   - **创建分支：**`git branch <新分支名>`---基于当前提交创建一个新分支。
   - **切换分支：**`git switch <分支名>`（或旧命令`git checkout <分支名>`）---切换到指定分支。
   - **合并分支：**`git merge <要合并进来的分支名>`---将指定分支的更改合并到==当前所在分支==。【高频使用，尤其在功能完成后合并到主分支】
   - **删除分支：**`git branch -d <分支名>`---删除已合并的本地分支。

### 补充其他 Git 命令

1. `git rm`

- 执行以下命令，取消.idea 目录的暂存（不删除本地文件）：

```bash
git rm --cached -r .idea/
# -r 表示递归处理目录下所有文件，适配.idea 是文件夹的情况。
# 执行后，.idea 相关文件会从 “Changes to be committed” 回到未暂存状态。
```

- 验证结果：再次执行`git status`，会看到.idea 文件变成 “Untracked files”，暂存区已移除。

2. `git check-ignore`

```bash
git check-ignore -v 文件名  # 确认指定文件是否被忽略
```

## Python 库

### zipfile 库

​	`zipfile`模块的基本作用：创建、读取、写入和提取 ZIP 文件。能够执行常见的 ZIP 文件操作（创建压缩包、添加文件、解压文件）。

- `zipfile.ZipFile`类构造函数中的`mode`参数：

| 模式 | 含义                                                         | 作用                                          |
| :--: | :----------------------------------------------------------- | :-------------------------------------------- |
| `r`  | **读取模式（Read）**：打开一个现有的 ZIP 文件以供读取。      | 这是访问和提取 ZIP 文件内容的标准模式。       |
| `w`  | **写入模式（Write）**：创建一个新的 ZIP 文件（如果文件已存在则会覆盖）。 | 用于向新的归档文件中添加文件。                |
| `x`  | **独占创建模式（Exclusive Create）**：创建一个新的 ZIP 文件，如果该文件已经存在，则会引发 `FileExistsError`异常。 | 这确保不会意外覆盖现有文件。                  |
| `a`  | **追加模式（Append）**：打开一个现有的 ZIP 文件以供写入。如果文件不存在，则会创建一个新文件。 | 主要用于向现有的 ZIP 归档文件中添加更多文件。 |

- `compression`指定创建ZIP文件时使用的默认压缩方法：

|          模式          | 含义                | 作用                                             |
| :--------------------: | :------------------ | :----------------------------------------------- |
|  `zipfile.ZIP_STORED`  | 不压缩，仅存储文件  | 这是最快速但压缩率最低的方法                     |
| `zipfile.ZIP_DEFLATED` | 标准的 ZIP 压缩方法 | 提供了较好的压缩比和速度平衡，是最常见的压缩方式 |
|  `zipfile.ZIP_BAIP2`   | 使用 bzip2 算法压缩 | 通常提供最高的压缩比，但压缩和解压缩速度较慢     |
|   `zipfile.ZIP_LZMA`   | 使用 LZMA 算法压缩  | 也提供很高的压缩比，尤其适用于某些类型的数据     |



#### 模块导入

- 模块名称：`zipfile`
- 核心类：`zipfile.ZipFile`-代表一个 ZIP 归档文件对象，用于对其进行各种操作。

```python
# 导入方式
import zipfile
```

#### 创建 ZIP 文件（写模式）

​	将一些文件打包成一个`.zip`压缩包。

关键步骤：

- 使用`with`语句打开一个 ZIP 文件（类似操作文件），指定模式为`w`(write)。如果文件不存在会自动创建。
- 使用`ZipFile`对象的`.write(filename, arcname=None)`方法添加文件。
  - `filename`: 你要添加到压缩包中的本地文件路径；
  - `arcname`: （可选）文件在 ZIP 包内的名称。如果不指定，则使用 `filename` 的basename。

```python
import zipfile

files_to_zip = ['file1.txt', 'file2.txt']
zip_filename = 'my.archive.zip'

# 使用 with 语句确保文件正确关闭
with zipfile.ZipFile(zipfilename, 'w') as zipd:
    for file in files_to_zip:
        # 添加文件到压缩包，使用原始文件名
        zipf.write(file)
        print(f"已添加 {file} 到 {zip_filename}")

print(f"ZIP 文件 {zip_filename} 创建成功！")
```

#### 从 ZIP 文件中提取文件（读模式）

​	当你需要解压一个现有的`.zip`文件时，用该方法。

关键步骤：

- 使用`with`语句打开 ZIP 文件，指定模式为`r`(read)；
- 使用`ZipFile`对象的方法：
  - `.extract(member, path=None)`：提取单个成员（`member`是文件名）到指定路径（`path`），默认是当前目录。
  - `.extractall(path=None)`：提取所有成员到指定路径。

```python
import zipfile
import os

# 假定在“写模式”创建了“my_archive.zip”
zip_filename = 'my_archive.zip'
extract_to_folder = 'extracted_files'

# 确保目标文件夹存在
os.makedirs(extract_to_folder, exist_ok=True)

with zipfile.ZipFile(zip_filename, 'r') as zipf:
    # 方法一：提取所有文件
    zipf.extractall(path=extract_to_floder)
    print(f"所有文件已解压到‘{extract_to_floder}'")
    
    # 方法二：只提取特定文件
    # specific_file = 'file1.txt'
    # zipf.extract(specific_file, path=extract_to_folder)
    # print(f"文件'{specific_file}'已解压到‘{extract_to_floder}'")
```

#### 查看 ZIP 文件内容

​	在解压前，你要知道压缩包里有什么。

关键属性 / 方法：

- `ZipFile.namelist()`：返回 ZIP 文件中所有成员（文件和文件夹）名称的列表。

```python
import zipfile

zip_filename = 'my_archive.zip'

with zipfile.ZipFile(zip_filename, 'r') as zipf:
    # 获取 ZIP 文件内所有文件 / 目录的名称列表
    file_list = zipf.namelist()
    print(f"ZIP 文件'{zip_filename}'包含以下内容：")
    for filename in file_list:
        print(f" - {filename}")
```

#### 向现有 ZIP 文件追加文件（追加模式）

​	如果你已经有一个 ZIP 文件，并想往里面加点文件。

关键步骤：

- 使用`with`语句打开 ZIP 文件，指定模式为`a`(append)。
- 同样使用`.wirte()`方法添加新文件。

```python
import zipfile

# 假定在“写模式”创建了“my_archive.zip”
zip_filename = 'my_archive.zip'
new_file_to_add = 'another_file.txt' # 需要先创建 / 存在该文件

# 追加模式 'a'
with zipfile.ZipFile(zip_filename, 'a') as zipf:
    zipf.wirte(new_file_to_add)
    print(f"已将 '{new_file_to_add}' 追加到 '{zip_filename}'")
    
# 可以再次查看内容确认
with zipfile.ZipFile(zip_filename, 'r') as zipf:
    print("追加后的 ZIP 内容：", zipf.namelist())
```

#### 方法

假定类为`zip_file`，在代码中写入 `with zipfile.ZipFile(zip_filename_path, 'w') as zip_file`

##### `zip_file.infolist()`

​	`zip_file.infolist()`方法会返回 ZIP 包中所有成员（文件 / 目录）的`ZipInfo`对象列表，通过`file_info`可以获取每个成员的详细属性，方便对 ZIP 内的文件进行操作（如判断是否为目录、获取文件大小、提取文件等）

```python
with zipfile.ZipFile(zip_path, 'r') as zip_file:
    for file_info in zip_file.infolist():
        file_name = file_info.filename()
        # 返回该成员在 ZIP 包中的完整路径和文件名（如 小花钱包-报备/小花资金方/锡商银行-营业执照.pdf）
```

|      其他实用属性       |                      作用                       |
| :---------------------: | :---------------------------------------------: |
|   file_info.file_size   |         文件未压缩时的原始大小（Byte）          |
| file_info.compress_size |        文件在 ZIP 中压缩后的大小（Byte）        |
|   file_info.data_time   | 文件的修改时间（元组格式`(年,月,日,时,分,秒)`） |
|   file_info.is_dir()    |  判断该成员是否为目录（返回`True` / `False`）   |

### enumerate函数
