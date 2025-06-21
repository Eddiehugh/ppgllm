"""
合规性检测Agent
专门负责检测隐私政策内容的合规性
"""

from typing import Dict, Any, Optional, List
from loguru import logger
from .base_agent import BaseAgent


class ComplianceCheckerAgent(BaseAgent):
    """合规性检测专家Agent"""
    
    def __init__(self, config: Dict[str, Any]):
        super().__init__("compliance_checker", config)
    
    async def process(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        处理合规性检测请求
        
        Args:
            message: 用户的检测请求
            context: 隐私政策内容等上下文
            
        Returns:
            检测结果
        """
        try:
            logger.info(f"开始处理合规性检测请求: {message[:100]}...")
            
            # 构建完整的检测提示
            full_message = self._build_compliance_prompt(message, context)
            
            # 调用Agent进行检测
            response = await self.chat(full_message)
            
            result = {
                "success": True,
                "agent_type": "compliance_checker",
                "response": response,
                "message": "合规性检测完成"
            }
            
            logger.info("合规性检测完成")
            return result
            
        except Exception as e:
            logger.error(f"合规性检测失败: {str(e)}")
            return {
                "success": False,
                "agent_type": "compliance_checker",
                "error": str(e),
                "message": "合规性检测失败"
            }
    
    def _build_compliance_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """构建合规性检测提示"""
        prompt_parts = [message]
        
        if context:
            if "privacy_policy" in context:
                policy_content = context["privacy_policy"]
                prompt_parts.append(f"\n待检测的隐私政策内容：")
                prompt_parts.append(f"{policy_content}")
            
            if "target_regions" in context:
                regions = context["target_regions"]
                prompt_parts.append(f"\n目标地区法规要求：{', '.join(regions)}")
            
            if "check_points" in context:
                check_points = context["check_points"]
                prompt_parts.append(f"\n重点检测项目：{', '.join(check_points)}")
        
        return "\n".join(prompt_parts)
    
    async def check_compliance(self, privacy_policy: str, target_regions: Optional[List[str]] = None, 
                             check_points: Optional[List[str]] = None) -> Dict[str, Any]:
        """
        检测隐私政策合规性的便捷方法
        
        Args:
            privacy_policy: 隐私政策内容
            target_regions: 目标地区列表
            check_points: 重点检测项目
            
        Returns:
            检测结果
        """
        message = "请对以下隐私政策进行全面的合规性检测，并提供详细的分析报告："
        context = {
            "privacy_policy": privacy_policy,
            "target_regions": target_regions or ["中国", "欧盟", "美国"],
            "check_points": check_points or [
                "数据收集合法性",
                "用户同意机制", 
                "数据处理目的说明",
                "第三方共享透明度",
                "用户权利保障",
                "数据安全措施"
            ]
        }
        
        return await self.process(message, context)
    
    async def quick_compliance_check(self, privacy_policy: str) -> Dict[str, Any]:
        """
        快速合规性检测
        
        Args:
            privacy_policy: 隐私政策内容
            
        Returns:
            快速检测结果
        """
        message = f"请对以下隐私政策进行快速合规性检测，重点关注明显的合规问题：\n\n{privacy_policy}"
        
        return await self.process(message)