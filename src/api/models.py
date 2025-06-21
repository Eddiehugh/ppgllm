"""
API数据模型
定义请求和响应的数据结构
"""

from typing import Dict, Any, Optional, List
from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    """聊天请求模型"""
    agent_type: str = Field(..., description="选择的Agent类型")
    message: str = Field(..., description="用户消息")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")


class AutoChatRequest(BaseModel):
    """自动选择Agent的聊天请求模型"""
    message: str = Field(..., description="用户消息")
    context: Optional[Dict[str, Any]] = Field(None, description="上下文信息")


class ChatResponse(BaseModel):
    """聊天响应模型"""
    success: bool = Field(..., description="是否成功")
    agent_type: str = Field(..., description="处理的Agent类型")
    response: Optional[str] = Field(None, description="Agent回复")
    message: str = Field(..., description="状态消息")
    error: Optional[str] = Field(None, description="错误信息")
    selected_agent: Optional[str] = Field(None, description="自动选择的Agent")


class AgentInfo(BaseModel):
    """Agent信息模型"""
    type: str = Field(..., description="Agent类型")
    name: str = Field(..., description="Agent名称")
    description: str = Field(..., description="Agent描述")
    status: str = Field(..., description="Agent状态")


class AgentListResponse(BaseModel):
    """Agent列表响应模型"""
    agents: List[AgentInfo] = Field(..., description="Agent列表")


class AgentStatusResponse(BaseModel):
    """Agent状态响应模型"""
    total_agents: int = Field(..., description="总Agent数量")
    active_agents: int = Field(..., description="活跃Agent数量")
    agents: Dict[str, Dict[str, Any]] = Field(..., description="Agent详细状态")


class PrivacyPolicyGenerateRequest(BaseModel):
    """隐私政策生成请求模型"""
    app_name: str = Field(..., description="应用名称")
    app_type: str = Field(..., description="应用类型")
    data_types: List[str] = Field(..., description="收集的数据类型")
    regions: List[str] = Field(default=["中国"], description="目标地区")
    requirements: Optional[str] = Field(None, description="特殊要求")


class ComplianceCheckRequest(BaseModel):
    """合规性检测请求模型"""
    privacy_policy: str = Field(..., description="隐私政策内容")
    target_regions: Optional[List[str]] = Field(None, description="目标地区")
    check_points: Optional[List[str]] = Field(None, description="检测要点")


class ReadabilityCheckRequest(BaseModel):
    """可读性检测请求模型"""
    privacy_policy: str = Field(..., description="隐私政策内容")
    target_audience: Optional[str] = Field(None, description="目标受众")
    check_dimensions: Optional[List[str]] = Field(None, description="检测维度")


class HealthResponse(BaseModel):
    """健康检查响应模型"""
    status: str = Field(..., description="服务状态")
    timestamp: str = Field(..., description="检查时间")
    version: str = Field(..., description="版本信息")