"""
可读性检测Agent
专门负责检测隐私政策的可读性
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from .base_agent import BaseAgent


class ReadabilityCheckerAgent(BaseAgent):
    """可读性检测专家Agent"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("readability_checker", config)
    
    async def process(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        处理可读性检测请求
        
        Args:
            message: 用户的检测请求
            context: 隐私政策内容等上下文
            
        Returns:
            检测结果
        """
        try:
            logger.info(f"开始处理可读性检测请求: {message[:100]}...")
            
            # 构建完整的检测提示
            full_message = self._build_readability_prompt(message, context)
            
            # 调用Agent进行检测
            response = await self.chat(full_message)
            
            result = {
                "success": True,
                "agent_type": "readability_checker",
                "response": response,
                "message": "可读性检测完成"
            }
            
            logger.info("可读性检测完成")
            return result
            
        except Exception as e:
            logger.error(f"可读性检测失败: {str(e)}")
            return {
                "success": False,
                "agent_type": "readability_checker",
                "error": str(e),
                "message": "可读性检测失败"
            }
    
    def _build_readability_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """构建可读性检测提示"""
        prompt_parts = [message]
        
        if context:
            if "privacy_policy" in context:
                policy_content = context["privacy_policy"]
                prompt_parts.append(f"\n待检测的隐私政策内容：")
                prompt_parts.append(f"{policy_content}")
            
            if "target_audience" in context:
                audience = context["target_audience"]
                prompt_parts.append(f"\n目标受众：{audience}")
            
            if "check_dimensions" in context:
                dimensions = context["check_dimensions"]
                prompt_parts.append(f"\n检测维度：{', '.join(dimensions)}")
        
        return "\n".join(prompt_parts)
    
    async def check_readability(self, privacy_policy: str, target_audience: Optional[str] = None,
                              check_dimensions: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        检测隐私政策可读性的便捷方法
        
        Args:
            privacy_policy: 隐私政策内容
            target_audience: 目标受众
            check_dimensions: 检测维度
            
        Returns:
            检测结果
        """
        message = "请对以下隐私政策进行全面的可读性检测，并提供详细的分析和改进建议："
        context = {
            "privacy_policy": privacy_policy,
            "target_audience": target_audience or "普通用户",
            "check_dimensions": check_dimensions or [
                "语言简洁性",
                "术语通俗性",
                "结构清晰度",
                "逻辑连贯性",
                "关键信息突出度",
                "用户友好性"
            ]
        }
        
        return await self.process(message, context)
    
    async def quick_readability_check(self, privacy_policy: str) -> Dict[str, Any]:
        """
        快速可读性检测
        
        Args:
            privacy_policy: 隐私政策内容
            
        Returns:
            快速检测结果
        """
        message = f"请对以下隐私政策进行快速可读性检测，重点关注明显的可读性问题：\n\n{privacy_policy}"
        
        return await self.process(message)
    
    async def get_readability_score(self, privacy_policy: str) -> Dict[str, Any]:
        """
        获取可读性评分
        
        Args:
            privacy_policy: 隐私政策内容
            
        Returns:
            评分结果
        """
        message = f"""请对以下隐私政策进行可读性评分（1-10分，10分为最佳），并给出具体的评分理由：

评分维度：
1. 语言简洁性 (1-10分)
2. 术语通俗性 (1-10分)  
3. 结构清晰度 (1-10分)
4. 逻辑连贯性 (1-10分)
5. 用户友好性 (1-10分)

隐私政策内容：
{privacy_policy}

请按照以下格式输出：
- 语言简洁性：X分 - 理由
- 术语通俗性：X分 - 理由
- 结构清晰度：X分 - 理由
- 逻辑连贯性：X分 - 理由
- 用户友好性：X分 - 理由
- 总体评分：X分
- 主要改进建议：...
"""
        
        return await self.process(message)