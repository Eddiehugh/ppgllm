"""
模型客户端工厂模块
"""

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
try:
    from src.utils.utils import get_config
except ImportError:
    from ...utils.utils import get_config


class ModelClientFactory:
    """模型客户端工厂"""
    
    @staticmethod
    def create_client(model_name: str):
        """
        创建模型客户端
        
        Args:
            model_name: 模型名称
            
        Returns:
            模型客户端实例
        """
        model_config = get_config()['qwen_client']
        
        if "gpt" in model_name:
            return OpenAIChatCompletionClient(
                model=model_name,
                temperature=0.01,
                model_info={
                    "vision": False,
                    "function_calling": True,
                    "json_output": False,
                    "family": ModelFamily.UNKNOWN
                },
                **model_config,
            )
        elif "claude" in model_name:
            return OpenAIChatCompletionClient(
                model=model_name,
                max_tokens=2000,
                timeout=2000,
                model_info={
                    "vision": False,
                    "function_calling": True,
                    "json_output": False,
                    "family": ModelFamily.UNKNOWN
                },
                **model_config
            )
        elif "qwen" in model_name or "deepseek" in model_name:
            # 针对Qwen和DeepSeek模型的配置
            return OpenAIChatCompletionClient(
                model=model_name,
                max_tokens=16000,
                temperature=0.1,
                model_info={
                    "vision": False,
                    "function_calling": True,
                    "json_output": False,
                    "structured_output": True,
                    "family": ModelFamily.UNKNOWN
                },
                **model_config
            )
        else:
            # 默认配置
            return OpenAIChatCompletionClient(
                model=model_name,
                max_tokens=16000,
                temperature=0.1,
                model_info={
                    "vision": False,
                    "function_calling": True,
                    "json_output": False,
                    "structured_output": True,
                    "family": ModelFamily.UNKNOWN
                },
                **model_config
            )