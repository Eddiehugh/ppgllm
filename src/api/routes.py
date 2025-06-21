"""
API路由
定义所有的API端点
"""

from datetime import datetime

from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from .models import (
    ChatRequest, ChatResponse,
    AgentListResponse, HealthResponse
)

# 修改这些导入
try:
    from src.agents.agent_factory import AgentFactory
except ImportError:
    from ..agents.agent_factory import AgentFactory
try:
    from src.agents import AgentManager
except ImportError:
    from ..agents import AgentManager

# 改为
try:
    from src.agents.agent_factory import AgentFactory
except ImportError:
    from ..agents.agent_factory import AgentFactory
try:
    from src.agents import AgentManager
except ImportError:
    from ..agents import AgentManager

# 创建路由器
router = APIRouter()

# 全局Agent工厂实例
agent_factory = None

# 全局Agent管理器实例
agent_manager = None

def get_agent_factory() -> AgentFactory:
    """获取Agent工厂实例"""
    global agent_factory
    if agent_factory is None:
        agent_factory = AgentFactory()
    return agent_factory

def get_agent_manager() -> AgentManager:
    """获取Agent管理器实例"""
    global agent_manager
    if agent_manager is None:
        agent_manager = AgentManager()
    return agent_manager

@router.get("/health", response_model=HealthResponse)
async def health_check():
    """健康检查端点"""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now().isoformat(),
        version="1.0.0"
    )

@router.get("/agents", response_model=AgentListResponse)
async def get_agents(factory: AgentFactory = Depends(get_agent_factory)):
    """获取所有可用的Agent列表"""
    try:
        agents = await factory.get_available_agents()
        return AgentListResponse(agents=agents)
    except Exception as e:
        logger.error(f"获取Agent列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取Agent列表失败")

@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, factory: AgentFactory = Depends(get_agent_factory)):
    """与指定Agent进行对话"""
    try:
        result = await factory.chat_with_agent(
            agent_type=request.agent_type,
            message=request.message,
            tools=request.context.get("tools") if request.context else None,
            memory_files=request.context.get("memory_files") if request.context else None
        )

        return ChatResponse(**result)

    except Exception as e:
        logger.error(f"对话处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="对话处理失败")
