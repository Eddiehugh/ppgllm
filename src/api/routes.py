"""
API路由
定义所有的API端点
"""

from datetime import datetime
from typing import Dict, Any
from fastapi import APIRouter, HTTPException, Depends
from loguru import logger

from .models import (
    ChatRequest, AutoChatRequest, ChatResponse,
    AgentListResponse, AgentStatusResponse,
    PrivacyPolicyGenerateRequest, ComplianceCheckRequest, ReadabilityCheckRequest,
    HealthResponse
)
from src.agents import AgentManager

# 创建路由器
router = APIRouter()

# 全局Agent管理器实例
agent_manager = None


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
async def get_agents(manager: AgentManager = Depends(get_agent_manager)):
    """获取所有可用的Agent列表"""
    try:
        agents = manager.get_available_agents()
        return AgentListResponse(agents=agents)
    except Exception as e:
        logger.error(f"获取Agent列表失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取Agent列表失败")


@router.get("/agents/status", response_model=AgentStatusResponse)
async def get_agent_status(manager: AgentManager = Depends(get_agent_manager)):
    """获取Agent状态信息"""
    try:
        status = manager.get_agent_status()
        return AgentStatusResponse(**status)
    except Exception as e:
        logger.error(f"获取Agent状态失败: {str(e)}")
        raise HTTPException(status_code=500, detail="获取Agent状态失败")


@router.post("/chat", response_model=ChatResponse)
async def chat_with_agent(request: ChatRequest, manager: AgentManager = Depends(get_agent_manager)):
    """与指定Agent进行对话"""
    try:
        result = await manager.process_request(
            agent_type=request.agent_type,
            message=request.message,
            context=request.context
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"对话处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="对话处理失败")


@router.post("/chat/auto", response_model=ChatResponse)
async def auto_chat(request: AutoChatRequest, manager: AgentManager = Depends(get_agent_manager)):
    """自动选择Agent进行对话"""
    try:
        result = await manager.auto_process_request(
            message=request.message,
            context=request.context
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"自动对话处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="自动对话处理失败")


@router.post("/generate", response_model=ChatResponse)
async def generate_privacy_policy(request: PrivacyPolicyGenerateRequest, 
                                manager: AgentManager = Depends(get_agent_manager)):
    """生成隐私政策"""
    try:
        # 构建应用信息
        app_info = {
            "name": request.app_name,
            "type": request.app_type,
            "data_types": request.data_types,
            "regions": request.regions
        }
        
        # 获取生成Agent
        generator = manager.get_agent("privacy_policy_generator")
        
        # 生成隐私政策
        result = await generator.generate_privacy_policy(
            app_info=app_info,
            requirements=request.requirements
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"隐私政策生成失败: {str(e)}")
        raise HTTPException(status_code=500, detail="隐私政策生成失败")


@router.post("/check/compliance", response_model=ChatResponse)
async def check_compliance(request: ComplianceCheckRequest,
                         manager: AgentManager = Depends(get_agent_manager)):
    """检测隐私政策合规性"""
    try:
        # 获取合规检测Agent
        checker = manager.get_agent("compliance_checker")
        
        # 进行合规性检测
        result = await checker.check_compliance(
            privacy_policy=request.privacy_policy,
            target_regions=request.target_regions,
            check_points=request.check_points
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"合规性检测失败: {str(e)}")
        raise HTTPException(status_code=500, detail="合规性检测失败")


@router.post("/check/readability", response_model=ChatResponse)
async def check_readability(request: ReadabilityCheckRequest,
                          manager: AgentManager = Depends(get_agent_manager)):
    """检测隐私政策可读性"""
    try:
        # 获取可读性检测Agent
        checker = manager.get_agent("readability_checker")
        
        # 进行可读性检测
        result = await checker.check_readability(
            privacy_policy=request.privacy_policy,
            target_audience=request.target_audience,
            check_dimensions=request.check_dimensions
        )
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"可读性检测失败: {str(e)}")
        raise HTTPException(status_code=500, detail="可读性检测失败")


@router.post("/check/readability/score", response_model=ChatResponse)
async def get_readability_score(request: ReadabilityCheckRequest,
                              manager: AgentManager = Depends(get_agent_manager)):
    """获取隐私政策可读性评分"""
    try:
        # 获取可读性检测Agent
        checker = manager.get_agent("readability_checker")
        
        # 获取可读性评分
        result = await checker.get_readability_score(request.privacy_policy)
        
        return ChatResponse(**result)
        
    except Exception as e:
        logger.error(f"可读性评分失败: {str(e)}")
        raise HTTPException(status_code=500, detail="可读性评分失败")