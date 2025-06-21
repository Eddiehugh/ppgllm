"""
隐私政策生成Agent
专门负责生成移动应用隐私政策
"""

from typing import Dict, Any, Optional
from loguru import logger
from .base_agent import BaseAgent


class PrivacyPolicyGeneratorAgent(BaseAgent):
    """隐私政策生成专家Agent"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("privacy_policy_generator", config)
    
    async def process(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        处理隐私政策生成请求
        
        Args:
            message: 用户的生成请求
            context: 应用信息等上下文
            
        Returns:
            生成结果
        """
        try:
            logger.info(f"开始处理隐私政策生成请求: {message[:100]}...")
            
            # 构建完整的提示信息
            full_message = self._build_generation_prompt(message, context)
            
            # 调用Agent进行生成
            response = await self.chat(full_message)
            
            result = {
                "success": True,
                "agent_type": "privacy_policy_generator",
                "response": response,
                "message": "隐私政策生成完成"
            }
            
            logger.info("隐私政策生成完成")
            return result
            
        except Exception as e:
            logger.error(f"隐私政策生成失败: {str(e)}")
            return {
                "success": False,
                "agent_type": "privacy_policy_generator", 
                "error": str(e),
                "message": "隐私政策生成失败"
            }
    
    def _build_generation_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """构建生成提示"""
        prompt_parts = [message]
        
        if context:
            if "app_info" in context:
                app_info = context["app_info"]
                prompt_parts.append(f"\n应用信息：")
                prompt_parts.append(f"- 应用名称: {app_info.get('name', '未提供')}")
                prompt_parts.append(f"- 应用类型: {app_info.get('type', '未提供')}")
                prompt_parts.append(f"- 数据收集类型: {app_info.get('data_types', '未提供')}")
                prompt_parts.append(f"- 目标地区: {app_info.get('regions', '未提供')}")
            
            if "requirements" in context:
                requirements = context["requirements"]
                prompt_parts.append(f"\n特殊要求：{requirements}")
        
        return "\n".join(prompt_parts)
    
    async def generate_privacy_policy(self, app_info: Dict[str, Any], requirements: Optional[str] = None) -> Dict[str, Any]:
        """
        生成隐私政策的便捷方法
        
        Args:
            app_info: 应用信息
            requirements: 特殊要求
            
        Returns:
            生成结果
        """
        message = "请为以下移动应用生成一份完整的隐私政策："
        context = {
            "app_info": app_info,
            "requirements": requirements
        }
        
        return await self.process(message, context)