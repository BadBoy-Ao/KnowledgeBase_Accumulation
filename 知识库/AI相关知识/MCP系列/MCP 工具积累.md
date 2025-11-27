# LLM 中的网页工具：Fetch 与 GeneralSearch

## Fetch 与 GeneralSearch 工具对比

### 基本定位与功能

- **Fetch**：“单发手枪”，一次获取一个已知URL的完整内容，将 HTML 转换为 LLM 友好格式（如 Markdown），专注**单页抓取**和简单转换；【定点提取网页内容】
- **GeneralSearch**：“搜索雷达”，通过关键词在全网范围内**发现**相关网页，返回 **URL列表** 和 摘要，供后续 Fetch 提取详细内容；【关键词全网搜索】

| 工具         | Fetch                                 | GeneralSearch                    |
| ------------ | ------------------------------------- | -------------------------------- |
| **核心功能** | 从***已知URL***提取网页内容           | 基于***查询关键词***搜索相关页面 |
| **输入要求** | 完整 URL                              | 查询字符串（关键字）             |
| **输出结果** | 网页内容（HTML转Markdown/结构化数据） | 相关 URL 列表及摘要              |
| **典型场景** | 精读指定文章、文档                    | 发现新信息、多源内容收集         |

### 工作流程差异

- **Fetch**：URL => 内容提取 => 格式转换 => 返回 LLM；
- **GeneralSearch**：查询 => 搜索匹配 => 返回 URL 列表 => （需配合 Fetch 获取详情）；

### 技术实现要点

- **Fetch**：轻量级解析器，支持**基本网页**和简单 JavaScript 渲染内容，专注**内容转换**；
- **GeneralSearch**：依赖商业搜索引擎 API （如 Bing、Google）或自建搜索服务，返回**相关性排序**和URL结果；

### 使用策略

1. 先用 **GeneralSearch** 发现相关 URL，再用 **Fetch** 深度提取具体内容，形成“搜索 -> 阅读 -> 分析 ” 闭环。

2. 对**已知有价值**的链接（如权威文章、报告），直接使用 **Fetch** 获取内容

## 与传统爬虫的本质区别

### 设计目标与核心能力

| 工具         | LLM网页工具 (Fetch / GeneralSearch)    | 传统爬虫(Scrapy / BeautifulSoup)   |
| ------------ | -------------------------------------- | ---------------------------------- |
| **核心目的** | 增强 LLM 回答能力，提供实时信息补充    | 数据采集，构建索引或数据集         |
| **智能程度** | 高度依赖LLM决策，具有语义理解能力      | 基于预设规则和模式匹配，无理解能力 |
| **内容处理** | 自动提取 有价值内容 （过滤广告、导航） | 提取所有内容，需人工后续处理       |
| **自主性**   | 完全由 LLM 控制，按需调用              | 自主爬行，**主动发现**内容         |

### 工作机制差异

- **LLM工具**：被动响应——LLM请求，不主动爬行，仅在需要时获取指定内容，单次调用处理单个 URL 或查询；
- **传统爬虫**：主动发现（遵循 robots.txt）—— 按预设策略（广度 / 深度优先）批量抓取，持续运行，构建完整索引；

### 技术实现对比

| 工具         | LLM工具                                    | 传统爬虫                                      |
| ------------ | ------------------------------------------ | --------------------------------------------- |
| **内容解析** | LLM 驱动语义理解，自适应识别正文、标题等   | 依赖 XPath / CSS 选择器等固定规则，需人工维护 |
| **复杂度**   | 轻量级，集成简单，API调用方式              | 需复杂配置，处理并发、反爬等问题              |
| **灵活性**   | 动态适应 绝大多数 网页结构变化，维护成本低 | 遇新网站，常需手动调整规则，维护成本高        |
| **输出格式** | 直接生成 LLM 友好格式（Markdown / JSON）   | 原始 HTML，需额外解析                         |

### 应用场景对比

- **LLM 工具**：

  1. 回答实时性问题（新闻、天气、价格）；
  2. 增强 RAG 系统（检索增强生成），提供最新知识；

  3. 支持 智能体 完成复杂任务（如旅游规划、产品比较）；

- **传统爬虫**：

  1. 构建 搜索引擎索引 （如Google、Bing）；
  2. 大规模 数据采集 （如市场分析、舆情预测）；
  3. 内容存档 和 知识库 建设

## 三种技术的互补关系

- **GeneralSearch**：帮助 LLM 发现新信息源，解决“不知道该查什么”的问题；

- **Fetch**：帮助 LLM 深度理解特定内容，解决“如何获取并处理内容”的问题；

- **传统爬虫**：专注 大规模数据收集 和 索引构建，适合长期、系统的数据获取；

  **核心区别**：

  1. *LLM 工具* 是 LLM 能力的延伸，由模型按需调用，注意语义理解和内容适配；

  2. *传统爬虫* 是 独立的数据采集系统，自主运行，注意 全面性 和 规模；

  **选择建议**：

  1. 若需 快速获取特定页面内容：用 Fetch；
  2. 若需 发现未知相关信息：用 GeneralSearch + Fetch 组合；
  3. 若需 系统性、大规模数据收集：用传统爬虫；
  4. 若需 LLM 应用中补充实时信息：优先使用 LLM 工具；

## 通用调用流程（底层逻辑）

​	要在 LLM 中调用 Fetch 和 GeneralSearch 工具，核心是遵循“LLM 决策 -> 工具参数构造 -> 工具执行 -> 结果回传 -> LLM 生成回答”的闭环流程。实际开发中，通常依赖成熟和工具调用框架（如 LangChain、LLaMAIndex、AutoGPT）简化流程，无需从零开发工具逻辑。

​	无论使用哪种框架，LLM 调用网页工具的核心步骤一致，可分为 5 步：

1. **触发判断**： LLM 分析用户问题，判断是否需要外部信息（如“2024年诺贝尔物理学奖得主”需实时信息，触发工具；“1 + 1等于几”无需直接回答）；
2. **参数构造**：LLM 根据工具类型，生成符合要求的参数（如 Fetch 需 url，GeneralSearch 需 query）；
3. **工具执行**：框架 将参数传递给工具，执行网络请求（Fetch 拉取 URL 内容，GeneralSearch 调用搜索引擎 API）；
4. **结果清洗**：工具将原始结果（如 HTML、搜索结果 JSON）转换为 LLM 友好格式（Markdown、结构化摘要）；
5. **回答生成**：LLM 结合清洗后的工具结果和自身知识，生成最终回答；

## Fetch 工具调用：定点提取已知 URL 内容

​	Fetch 的核心是 “已知 URL -> 提取干净内容”，适合需精读特定网页（如新闻、报告、文档等）场景。

​	以下以常用的 LangChain 为例，结合 OpenAI LLM 演示调用方法：

### 关键参数

| 参数名        | 作用说明                          | 示例值                                                       |
| ------------- | --------------------------------- | ------------------------------------------------------------ |
| url           | 目标页面的完整 URL (必填)         | `https://www.nobelprize.org/prizes/physics/2024/press-release/` |
| render_js     | 是否渲染动态JS (可选，默认 False) | `True`(应对需加载 js 的网页，如 SPA 应用)                    |
| output_format | 输出格式 (可选，默认 Markdown)    | `markdown` / `plain_text` / `json`                           |

### 调用示例（LangChain + OpenAI + FetchTool）

```python
# 一、安装依赖
pip install langchain openai python-dotenv # langchain 框架、OpenAI SDK、环境变量管理

# 二、编写代码
from langchain.agents import initialize_agent, AgentType
from langchain.tools import FetchTool  # LangChain内置的Fetch工具
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# 1. 加载环境变量（OpenAI API密钥，从.env文件读取）
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")

# 2. 初始化LLM（使用GPT-4，需确保API密钥有访问权限）
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,  # 降低随机性，确保工具调用逻辑稳定
    api_key=openai_api_key
)

# 3. 初始化Fetch工具（可配置是否渲染JS）
fetch_tool = FetchTool(
    render_js=True,  # 目标网页若有动态内容，需开启JS渲染
    output_format="markdown"  # 输出Markdown格式，方便LLM解析
)
tools = [fetch_tool]  # 工具列表（可后续添加其他工具）

# 4. 初始化智能体（Agent）：负责协调LLM与工具
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,  # 适合工具调用的Agent类型
    verbose=True  # 打印详细流程（便于调试，看到工具调用过程）
)

# 5. 触发工具调用：让智能体提取指定URL内容并总结
user_question = "请提取并总结2024年诺贝尔物理学奖官网公告的核心内容：https://www.nobelprize.org/prizes/physics/2024/press-release/"
result = agent.run(user_question)

# 6. 输出结果
print("LLM最终回答：")
print(result)
```

## GeneralSearch 工具调用：关键词全网搜索

​	GeneralSearch 的核心是“关键词 -> 获取相关 URL 列表 + 摘要”，适合“未知信息源”场景（如“2024年AI领域重大突破”，“最新IPhone 16发布时间”）。实际调用需依赖 搜索引擎API（如 Bing Search API、SerpAPI）。

### 关键参数

| 参数名      | 作用说明                             | 示例值                             |
| ----------- | ------------------------------------ | ---------------------------------- |
| query       | 搜索关键词（必填，需精准）           | 2024 AI领域重大突破 权威报告       |
| num_results | 返回结果数量（可选，默认值 5 ）      | 10                                 |
| search_type | 搜索类型（可选，如新闻、学术）       | news (仅搜索新闻) / scholar (学术) |
| api_key     | 搜索引擎 API 密钥（必填，如SerpAPI） |                                    |

### 调用示例 （LangChain + SerpAPI + GeneralSearch）

```python
# 一、准备前置条件——申请 SerpAPI 密钥（免费额度足够测试，官网：https://serpapi.com/）,用于调用 Google 搜索结果。
pip install langchain-openai serpapi

# 二、编写代码
from langchain.agents import initialize_agent, AgentType
from langchain.tools import SerpAPIQueryRun  # 基于SerpAPI的GeneralSearch工具
from langchain.chat_models import ChatOpenAI
from dotenv import load_dotenv
import os

# 1. 加载环境变量（OpenAI API密钥 + SerpAPI密钥）
load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
serpapi_api_key = os.getenv("SERPAPI_API_KEY")

# 2. 初始化LLM（GPT-4）
llm = ChatOpenAI(
    model_name="gpt-4",
    temperature=0,
    api_key=openai_api_key
)

# 3. 初始化GeneralSearch工具（SerpAPIQueryRun）
general_search = SerpAPIQueryRun(
    api_key=serpapi_api_key,
    params={
        "q": "",  # 搜索关键词留空，由LLM动态生成
        "num": 5,  # 返回5条结果
        "hl": "en",  # 搜索语言（en=英文，zh-CN=中文）
        "tbm": "nws"  # 搜索类型：nws=新闻，默认是web（全网）
    }
)
tools = [general_search]

# 4. 初始化智能体
agent = initialize_agent(
    tools,
    llm,
    agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True  # 打印调试信息，查看搜索过程
)

# 5. 触发工具调用：让智能体搜索并总结
user_question = "2024年AI领域有哪些重大技术突破？请基于权威新闻来源总结。"
result = agent.run(user_question)

# 6. 输出结果
print("LLM最终回答：")
print(result)
```

## Fetch 与 GeneralSearch 的配合场景

| 需求类型              | 工具选择               | 流程示例                                                     |
| --------------------- | ---------------------- | ------------------------------------------------------------ |
| 精读单篇已知网页      | 单独使用 Fetch         | 用户提供报告 URL -> Fetch 提取内容 -> LLM 总结核心观点       |
| 获取时效性 / 未知信息 | 单独使用 GeneralSearch | 用户问“最新新能源汽车政策” -> 搜索获取政策摘要 -> LLM 解读   |
| 深度调研（多源整合）  | GeneralSearch + Fetch  | 搜索“2024碳中和进展” -> 获取 10 个权威 URL -> Fetch 逐个提取 -> LLM 整合分析 |

​	通过以上方法，可让 LLM 具备“实时获取外部信息”的能力，突破自身知识截止日期的限制，适用 RAG 系统、智能问答机器人、AI助手等场景。