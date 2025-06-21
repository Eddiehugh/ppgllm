"""
Agent工厂
根据前端参数构建指定的Agent
"""

from typing import Dict, Any, Optional, List
from loguru import logger

try:
    from src.utils.utils import get_config
except ImportError:
    from ppgllm.src.utils import get_config

try:
    from src.core.models.model_client import ModelClientFactory
except ImportError:
    from ..core.models.model_client import ModelClientFactory

# 导入各个Agent的构建器
from .privacy_policy_generator_builder import PrivacyPolicyGeneratorBuilder
from .compliance_checker_builder import ComplianceCheckerBuilder
from .readability_checker_builder import ReadabilityCheckerBuilder

# 导入各个Agent的描述信息
try:
    from prompt.privacy_policy_generator_prompt import DESCRIPTION as PPG_DESC
    from prompt.compliance_checker_prompt import DESCRIPTION as CC_DESC
    from prompt.readability_checker_prompt import DESCRIPTION as RC_DESC
except ImportError:
    from ...prompt.privacy_policy_generator_prompt import DESCRIPTION as PPG_DESC
    from ...prompt.compliance_checker_prompt import DESCRIPTION as CC_DESC
    from ...prompt.readability_checker_prompt import DESCRIPTION as RC_DESC


class AgentFactory:
    """Agent工厂类"""

    def __init__(self):
        self.model_client = self._create_model_client()
        self.agent_builders = {
            "privacy_policy_generator": PrivacyPolicyGeneratorBuilder,
            "compliance_checker": ComplianceCheckerBuilder,
            "readability_checker": ReadabilityCheckerBuilder
        }
        self._built_agents = {}  # 缓存已构建的Agent

    def _create_model_client(self):
        """创建模型客户端"""
        try:
            config = get_config()
            # 使用ModelClientFactory创建AutoGen兼容的客户端
            model_name = config.get("qwen_client", {}).get("model", "qwen-turbo")
            return ModelClientFactory.create_client(model_name=model_name)
        except Exception as e:
            logger.error(f"创建模型客户端失败: {str(e)}")
            raise

    async def build_agent(self, agent_type: str, tools=None, memory_files=None):
        """
        构建Agent
        Args:
            agent_type: Agent类型
            tools: 可选工具列表
            memory_files: 内存文件列表
        Returns:
            构建的Agent实例
        """
        # 生成缓存键
        cache_key = f"{agent_type}_{id(tools)}_{id(memory_files)}"
        # 检查缓存
        if cache_key in self._built_agents:
            return self._built_agents[cache_key]
        # 检查是否支持该Agent类型
        if agent_type not in self.agent_builders:
            raise ValueError(f"不支持的Agent类型: {agent_type}")
        try:
            # 获取构建器
            builder = self.agent_builders[agent_type](
                model_client=self.model_client,
                tools=tools,
                memory_files=memory_files
            )
            # 构建Agent
            agent = await builder.build()
            # 缓存Agent
            self._built_agents[cache_key] = agent
            return agent
        except Exception as e:
            logger.error(f"构建Agent失败 {agent_type}: {str(e)}")
            raise

    async def get_agent_info(self, agent_type: str) -> Dict[str, Any]:
        """
        获取Agent信息
        Args:
            agent_type: Agent类型
        Returns:
            Agent信息
        """
        if agent_type not in self.agent_builders:
            raise ValueError(f"不支持的Agent类型: {agent_type}")
        # 从prompt文件获取描述信息
        descriptions = {
            "privacy_policy_generator": PPG_DESC,
            "compliance_checker": CC_DESC,
            "readability_checker": RC_DESC
        }
        return {
            "type": agent_type,
            "name": agent_type.replace("_", " ").title(),
            "description": descriptions.get(agent_type, ""),
            "status": "available"
        }

    async def get_available_agents(self) -> List[Dict[str, Any]]:
        """获取所有可用的Agent信息"""
        agents = []
        for agent_type in self.agent_builders.keys():
            try:
                info = await self.get_agent_info(agent_type)
                agents.append(info)
            except Exception as e:
                logger.error(f"获取Agent信息失败 {agent_type}: {str(e)}")
        return agents

    async def chat_with_agent(self, agent_type: str, message: str,
                            tools: Optional[List] = None,
                            memory_files: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        与指定Agent进行对话
        Args:
            agent_type: Agent类型
            message: 用户消息
            tools: 工具列表
            memory_files: 内存文件列表
        Returns:
            对话结果
        """
        try:
            # 构建Agent
            agent = await self.build_agent(agent_type, tools, memory_files)
            # 根据agent_type选择不同的处理逻辑
            if agent_type == "privacy_policy_generator":
                response = await self._process_privacy_policy_request(agent, message)
            elif agent_type == "compliance_checker":
                response = await self._process_compliance_check_request(agent, message)
            elif agent_type == "readability_checker":
                response = await self._process_readability_check_request(agent, message)
            else:
                # 默认处理逻辑
                response = await self._default_process_request(agent, message)
            return {
                "success": True,
                "agent_type": agent_type,
                "agent_name": agent.name if hasattr(agent, 'name') else agent_type,
                "response": response,
                "message": f"{agent_type} 处理完成"
            }
        except Exception as e:
            logger.error(f"Agent对话失败 {agent_type}: {str(e)}")
            return {
                "success": False,
                "agent_type": agent_type,
                "error": str(e),
                "message": f"Agent {agent_type} 处理失败"
            }

    async def _process_privacy_policy_request(self, agent, message):
        """处理隐私政策生成请求"""
        try:
            # 使用OpenAI客户端发送请求
            response = await self._send_chat_request(agent, message)
            return response
        except Exception as e:
            logger.error(f"处理隐私政策请求失败: {str(e)}")
            raise

    async def _process_compliance_check_request(self, agent, message):
        """处理合规检查请求"""
        try:
            # 使用OpenAI客户端发送请求
            response = await self._send_chat_request(agent, message)
            return response
        except Exception as e:
            logger.error(f"处理合规检查请求失败: {str(e)}")
            raise

    async def _process_readability_check_request(self, agent, message):
        """处理可读性检查请求"""
        try:
            # 使用OpenAI客户端发送请求
            response = await self._send_chat_request(agent, message)
            return response
        except Exception as e:
            logger.error(f"处理可读性检查请求失败: {str(e)}")
            raise

    async def _default_process_request(self, agent, message):
        """默认处理请求"""
        try:
            # 使用OpenAI客户端发送请求
            response = await self._send_chat_request(agent, message)
            return response
        except Exception as e:
            logger.error(f"处理请求失败: {str(e)}")
            raise

    async def _send_chat_request(self, agent, message):
        """发送聊天请求"""
        try:
            # 获取系统消息
            system_message = agent.system_message if hasattr(agent, 'system_message') else ""
            
            # 打印可用方法，帮助调试
            logger.info(f"model_client类型: {type(self.model_client)}")
            logger.info(f"model_client可用方法: {dir(self.model_client)}")
            
            # 直接使用原生OpenAI客户端
            from openai import OpenAI
            
            qwen_config = get_config().get("qwen_client", {})
            api_key = qwen_config.get("api_key", "")
            base_url = qwen_config.get("base_url", "https://dashscope.aliyuncs.com/compatible-mode/v1")
            model = qwen_config.get("model", "qwen-turbo")
            max_tokens = qwen_config.get("max_tokens", 8000)
            
            client = OpenAI(
                api_key=api_key,
                base_url=base_url
            )
            
            response = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": message}
                ],
                temperature=0.1,
                max_tokens=max_tokens
            )
            # 返回响应内容
            return response.choices[0].message.content
        except Exception as e:
            logger.error(f"发送聊天请求失败: {str(e)}")
            raise

    def clear_cache(self):
        """清空Agent缓存"""
        self._built_agents.clear()
        logger.info("Agent缓存已清空")
