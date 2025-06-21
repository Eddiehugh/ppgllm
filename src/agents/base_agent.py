"""
基础Agent类
定义所有agent的通用接口和功能
"""

from abc import ABC, abstractmethod
from typing import Dict, Any, Optional
import autogen
from loguru import logger


class BaseAgent(ABC):
    """基础Agent抽象类"""
    
    def __init__(self, name: str, config: Dict[str, Any]):
        self.name = name
        self.config = config
        self.agent = None
        self._initialize_agent()
    
    def _initialize_agent(self):
        """初始化AutoGen Agent"""
        try:
            self.agent = autogen.AssistantAgent(
                name=self.config["name"],
                system_message=self.config["system_message"],
                llm_config=self.config["llm_config"],
                human_input_mode=self.config.get("human_input_mode", "NEVER"),
                max_consecutive_auto_reply=self.config.get("max_consecutive_auto_reply", 3),
            )
            logger.info(f"Agent {self.name} 初始化成功")
        except Exception as e:
            logger.error(f"Agent {self.name} 初始化失败: {str(e)}")
            raise
    
    @abstractmethod
    async def process(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        处理用户消息的抽象方法
        
        Args:
            message: 用户输入的消息
            context: 上下文信息
            
        Returns:
            处理结果字典
        """
        pass
    
    def get_agent_info(self) -> Dict[str, Any]:
        """获取Agent信息"""
        return {
            "name": self.name,
            "description": self.config.get("description", ""),
            "status": "active" if self.agent else "inactive"
        }
    
    async def chat(self, message: str, user_proxy: Optional[autogen.UserProxyAgent] = None) -> str:
        """
        与Agent进行对话
        
        Args:
            message: 用户消息
            user_proxy: 用户代理Agent
            
        Returns:
            Agent的回复
        """
        if not self.agent:
            raise RuntimeError(f"Agent {self.name} 未正确初始化")
        
        try:
            if user_proxy is None:
                # 创建临时的用户代理
                user_proxy = autogen.UserProxyAgent(
                    name="user",
                    human_input_mode="NEVER",
                    max_consecutive_auto_reply=0,
                )
            
            # 发起对话
            user_proxy.initiate_chat(self.agent, message=message)
            
            # 获取最后一条回复
            chat_history = user_proxy.chat_messages.get(self.agent, [])
            if chat_history:
                return chat_history[-1].get("content", "")
            else:
                return "Agent没有回复"
                
        except Exception as e:
            logger.error(f"Agent {self.name} 对话失败: {str(e)}")
            return f"对话过程中发生错误: {str(e)}"