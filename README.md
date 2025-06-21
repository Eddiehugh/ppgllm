# 隐私政策智能生成系统

基于AutoGen AgentChat框架的多Agent隐私政策生成、合规检测和可读性检测系统。

## 🏗️ 系统架构

本系统采用**构建器模式 + Agent工厂**架构，实现了灵活高效的多Agent管理：

### 核心组件
- **AgentFactory**: Agent工厂，负责根据前端参数构建指定的Agent
- **Agent构建器**: 每个Agent都有独立的构建器，支持自定义配置
- **内存管理**: 支持Agent记忆存储和检索
- **工具集成**: 支持为Agent配置专用工具

### Agent列表
1. **隐私政策生成专家** (`privacy_policy_generator`)
   - 专门负责生成移动应用隐私政策
   - 支持多地区法规要求
   - 可根据应用类型和数据收集情况定制

2. **合规性检测专家** (`compliance_checker`)
   - 检测隐私政策的合规性
   - 支持多地区法规检测（中国、欧盟、美国等）
   - 提供详细的合规分析报告

3. **可读性检测专家** (`readability_checker`)
   - 评估隐私政策的可读性
   - 提供可读性评分和改进建议
   - 支持多维度可读性分析

## 📁 项目结构

\`\`\`
ppgllm/
├── config/                                    # 配置文件
│   ├── __init__.py
│   └── agent_config.py                       # Agent配置
├── prompt/                                    # Prompt模板
│   ├── __init__.py
│   ├── base_prompts.py                       # 基础Prompt模板
│   └── agent.py                              # Agent专用Prompt
├── src/                                      # 源代码
│   ├── __init__.py
│   ├── app.py                                # FastAPI主应用
│   ├── agents/                               # Agent实现
│   │   ├── __init__.py
│   │   ├── agent_factory.py                 # Agent工厂
│   │   ├── privacy_policy_generator_builder.py
│   │   ├── compliance_checker_builder.py
│   │   └── readability_checker_builder.py
│   ├── core/                                 # 核心功能
│   │   ├── __init__.py
│   │   └── memory/                           # 内存管理
│   │       ├── __init__.py
│   │       └── list_memory.py
│   ├── utils/                                # 工具函数
│   │   ├── __init__.py
│   │   └── utils.py
│   └── api/                                  # API接口
│       ├── __init__.py
│       ├── models.py                         # 数据模型
│       └── routes.py                         # 路由定义
├── memory/                                   # 内存存储目录
├── logs/                                     # 日志文件
├── main.py                                   # 主入口文件
├── test_agent_factory.py                    # Agent工厂测试
├── test_qwen_api.py                         # API连接测试
├── requirements.txt                          # 依赖包
├── .env.example                             # 环境变量示例
└── README.md                                # 项目说明
\`\`\`

## 🚀 安装和配置

### 1. 安装依赖

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### 2. 配置环境变量

复制 `.env.example` 为 `.env` 并配置：

\`\`\`bash
cp .env.example .env
\`\`\`

编辑 `.env` 文件，配置Qwen API密钥：

\`\`\`
# Qwen API配置
DASHSCOPE_API_KEY=your-dashscope-api-key-here
QWEN_BASE_URL=https://dashscope.aliyuncs.com/compatible-mode/v1
QWEN_MODEL=qwen-turbo

# 系统配置
LOG_LEVEL=INFO
DEBUG=False
\`\`\`

**获取API密钥**：
1. 访问[阿里云百炼平台](https://dashscope.console.aliyun.com/)
2. 注册并获取API Key
3. 将API Key配置到 `DASHSCOPE_API_KEY` 环境变量中

**可用模型**：
- `qwen-turbo` - 通用模型，响应速度快
- `qwen-plus` - 能力更强的模型
- `qwen-max` - 最强能力模型

### 3. 测试系统

\`\`\`bash
# 测试API连接
python test_qwen_api.py

# 测试Agent工厂系统
python test_agent_factory.py
\`\`\`

### 4. 启动系统

\`\`\`bash
python main.py
\`\`\`

或使用启动脚本：

\`\`\`bash
./start.sh
\`\`\`

系统启动后，访问：
- API文档：http://localhost:8000/docs
- 系统首页：http://localhost:8000

## 🔌 API接口

### 基础接口

- `GET /` - 系统信息
- `GET /api/v1/health` - 健康检查
- `GET /api/v1/agents` - 获取Agent列表
- `GET /api/v1/agents/status` - 获取Agent状态

### 对话接口

- `POST /api/v1/chat` - 与指定Agent进行对话
- `POST /api/v1/chat/auto` - 自动选择Agent进行对话

### 专业功能接口

- `POST /api/v1/generate` - 生成隐私政策
- `POST /api/v1/check/compliance` - 合规性检测
- `POST /api/v1/check/readability` - 可读性检测
- `POST /api/v1/check/readability/score` - 可读性评分

## 💡 使用示例

### 1. 指定Agent对话

\`\`\`python
import requests

# 前端指定使用隐私政策生成Agent
data = {
    "agent_type": "privacy_policy_generator",
    "message": "请为一个购物应用生成隐私政策",
    "context": {
        "tools": [],  # 可选：指定工具
        "memory_files": ["conversation_history.json"]  # 可选：指定内存文件
    }
}
response = requests.post("http://localhost:8000/api/v1/chat", json=data)
print(response.json())
\`\`\`

### 2. 自动选择Agent对话

\`\`\`python
import requests

# 系统会自动选择合适的Agent
data = {"message": "请帮我生成一个购物应用的隐私政策"}
response = requests.post("http://localhost:8000/api/v1/chat/auto", json=data)
print(response.json())
\`\`\`

### 3. 生成隐私政策

\`\`\`python
import requests

data = {
    "app_name": "我的应用",
    "app_type": "社交应用",
    "data_types": ["用户信息", "设备信息", "位置信息"],
    "regions": ["中国", "欧盟"],
    "requirements": "需要特别注意GDPR合规"
}

response = requests.post("http://localhost:8000/api/v1/generate", json=data)
print(response.json())
\`\`\`

## 🎯 构建器模式架构优势

1. **独立构建**: 每个Agent独立构建，互不干扰
2. **灵活配置**: 支持为每个Agent配置不同的工具和内存
3. **按需加载**: 根据前端参数只构建需要的Agent
4. **缓存机制**: 相同配置的Agent会被缓存，提高性能
5. **易于扩展**: 添加新Agent只需创建对应的构建器
6. **内存管理**: 支持Agent记忆存储和检索

## 🔧 自定义开发

### 添加新的Agent

1. 创建Agent构建器类（继承基础构建器模式）
2. 在 `prompt/agent.py` 中定义Agent的Prompt和描述
3. 在 `AgentFactory` 中注册新的构建器
4. 更新API路由支持新Agent

### 自定义工具和内存

\`\`\`python
# 为Agent配置专用工具
tools = [custom_tool1, custom_tool2]

# 为Agent配置内存文件
memory_files = ["agent_memory.json", "conversation_history.json"]

# 构建Agent
agent = await factory.build_agent(
    agent_type="privacy_policy_generator",
    tools=tools,
    memory_files=memory_files
)
\`\`\`

## 📊 技术栈

- **框架**: FastAPI + AutoGen AgentChat
- **LLM**: Qwen系列模型（通义千问）
- **数据验证**: Pydantic
- **日志**: Loguru
- **异步**: asyncio
- **内存管理**: 自定义JSON存储

## 📝 注意事项

1. 确保Qwen API密钥配置正确
2. 生产环境中需要限制CORS域名
3. 建议配置日志轮转和监控
4. 可根据需要调整Agent的配置参数
5. 注意API调用频率限制
6. 内存文件会自动创建在 `memory/` 目录下

## 📄 许可证

MIT License

