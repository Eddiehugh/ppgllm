"""
Agent管理器
负责管理和调度所有agent
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from config.agent_config import AGENT_CONFIGS
from .privacy_policy_generator import PrivacyPolicyGeneratorAgent
from .compliance_checker import ComplianceCheckerAgent
from .readability_checker import ReadabilityCheckerAgent


class AgentManager:
    """Agent管理器"""
    
    def __init__(self):
        self.agents: Dict[str, Any] = {}
        self._initialize_agents()
    
    def _initialize_agents(self):
        """初始化所有agents"""
        try:
            # 初始化隐私政策生成Agent
            self.agents["privacy_policy_generator"] = PrivacyPolicyGeneratorAgent(
                AGENT_CONFIGS["privacy_policy_generator"]
            )
            
            # 初始化合规性检测Agent
            self.agents["compliance_checker"] = ComplianceCheckerAgent(
                AGENT_CONFIGS["compliance_checker"]
            )
            
            # 初始化可读性检测Agent
            self.agents["readability_checker"] = ReadabilityCheckerAgent(
                AGENT_CONFIGS["readability_checker"]
            )
            
            logger.info("所有Agent初始化完成")
            
        except Exception as e:
            logger.error(f"Agent初始化失败: {str(e)}")
            raise
    
    def get_agent(self, agent_type: str):
        """
        获取指定类型的Agent
        
        Args:
            agent_type: Agent类型
            
        Returns:
            Agent实例
        """
        if agent_type not in self.agents:
            raise ValueError(f"不支持的Agent类型: {agent_type}")
        
        return self.agents[agent_type]
    
    def get_available_agents(self) -> List[Dict[str, Any]]:
        """
        获取所有可用的Agent信息
        
        Returns:
            Agent信息列表
        """
        agent_info = []
        for agent_type, agent in self.agents.items():
            info = agent.get_agent_info()
            info["type"] = agent_type
            agent_info.append(info)
        
        return agent_info
    
    async def process_request(self, agent_type: str, message: str, 
                            context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        处理用户请求
        
        Args:
            agent_type: 选择的Agent类型
            message: 用户消息
            context: 上下文信息
            
        Returns:
            处理结果
        """
        try:
            agent = self.get_agent(agent_type)
            result = await agent.process(message, context)
            
            logger.info(f"Agent {agent_type} 处理请求完成")
            return result
            
        except Exception as e:
            logger.error(f"处理请求失败: {str(e)}")
            return {
                "success": False,
                "error": str(e),
                "message": f"Agent {agent_type} 处理请求失败"
            }
    
    def select_agent_by_intent(self, message: str) -> str:
        """
        根据用户意图自动选择合适的Agent
        
        Args:
            message: 用户消息
            
        Returns:
            推荐的Agent类型
        """
        message_lower = message.lower()
        
        # 简单的关键词匹配逻辑
        if any(keyword in message_lower for keyword in ["生成", "创建", "制作", "写"]):
            return "privacy_policy_generator"
        elif any(keyword in message_lower for keyword in ["合规", "检查", "审核", "法规"]):
            return "compliance_checker"
        elif any(keyword in message_lower for keyword in ["可读性", "易读", "理解", "优化"]):
            return "readability_checker"
        else:
            # 默认返回生成Agent
            return "privacy_policy_generator"
    
    async def auto_process_request(self, message: str, 
                                 context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        自动选择Agent并处理请求
        
        Args:
            message: 用户消息
            context: 上下文信息
            
        Returns:
            处理结果
        """
        # 自动选择Agent
        selected_agent = self.select_agent_by_intent(message)
        
        logger.info(f"自动选择Agent: {selected_agent}")
        
        # 处理请求
        result = await self.process_request(selected_agent, message, context)
        result["selected_agent"] = selected_agent
        
        return result
    
    def get_agent_status(self) -> Dict[str, Any]:
        """
        获取所有Agent的状态信息
        
        Returns:
            状态信息
        """
        status = {
            "total_agents": len(self.agents),
            "active_agents": 0,
            "agents": {}
        }
        
        for agent_type, agent in self.agents.items():
            agent_info = agent.get_agent_info()
            status["agents"][agent_type] = agent_info
            if agent_info["status"] == "active":
                status["active_agents"] += 1
        
        return status