"""
Agent管理器
负责管理所有Agent并处理前端请求
"""

import asyncio
from typing import Dict, Any, List, Optional
from loguru import logger

from .agent_factory import AgentFactory

class AgentManager:
    """Agent管理器类"""
    def __init__(self):
        self.factory = AgentFactory()
        self.agents = {}  # 缓存已初始化的Agent
        
    async def get_available_agents(self) -> List[Dict[str, Any]]:
        """获取所有可用的Agent信息"""
        # 直接调用异步方法，不使用asyncio.run()
        return await self.factory.get_available_agents()
    def get_agent(self, agent_type: str):
        """获取指定类型的Agent"""
        if agent_type not in self.agents:
            # 使用事件循环运行异步方法
            loop = asyncio.get_event_loop()
            self.agents[agent_type] = loop.run_until_complete(self.factory.build_agent(agent_type))
        return self.agents[agent_type]
    def get_agent_status(self) -> Dict[str, Any]:
        """获取所有Agent的状态"""
        # 使用事件循环运行异步方法
        loop = asyncio.get_event_loop()
        agents = loop.run_until_complete(self.get_available_agents())
        return {
            "total_agents": len(agents),
            "active_agents": len(self.agents),
            "agents": {agent["type"]: {"status": agent["status"]} for agent in agents}
        }
    def select_agent_by_intent(self, message: str) -> str:
        """根据用户意图自动选择合适的Agent"""
        # 简单的关键词匹配逻辑
        if "生成" in message or "创建" in message or "写一个" in message:
            return "privacy_policy_generator"
        elif "合规" in message or "检查" in message or "符合法规" in message:
            return "compliance_checker"
        elif "可读性" in message or "易读" in message or "理解" in message:
            return "readability_checker"
        else:
            # 默认使用隐私政策生成器
            return "privacy_policy_generator"
    async def process_request(self, agent_type: str, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """处理前端请求"""
        try:
            # 获取上下文参数
            tools = context.get("tools", []) if context else []
            memory_files = context.get("memory_files", []) if context else []
            # 构建Agent
            agent = await self.factory.build_agent(
                agent_type=agent_type,
                tools=tools,
                memory_files=memory_files
            )
            # 与Agent对话
            result = await self.factory.chat_with_agent(
                agent_type=agent_type,
                message=message,
                tools=tools,
                memory_files=memory_files
            )
            return {
                "success": True,
                "agent_type": agent_type,
                "response": result.get("response"),
                "message": "请求处理成功"
            }
        except Exception as e:
            logger.error(f"处理请求失败: {str(e)}")
            return {
                "success": False,
                "agent_type": agent_type,
                "message": "处理请求失败",
                "error": str(e)
            }
    async def auto_process_request(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """自动选择Agent处理请求"""
        # 自动选择Agent
        selected_agent = self.select_agent_by_intent(message)
        # 处理请求
        result = await self.process_request(
            agent_type=selected_agent,
            message=message,
            context=context
        )
        # 添加选择的Agent信息
        result["selected_agent"] = selected_agent
        return result
