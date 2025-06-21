"""
模型客户端工厂模块
"""

from autogen_ext.models.openai import OpenAIChatCompletionClient
from autogen_core.models import ModelFamily
try:
    from src.utils.utils import get_config
except ImportError:
    from ppgllm.src.utils import get_config


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
        max_tokens = model_config.get('max_tokens', 16000)

        if "model" in model_config:
            del model_config["model"]
        if "max_tokens" in model_config:
            del model_config["max_tokens"]



        if "qwen" in model_name or "deepseek" in model_name:
            # 针对Qwen和DeepSeek模型的配置
            return OpenAIChatCompletionClient(
                model=model_name,
                max_tokens=max_tokens,
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
                max_tokens=max_tokens,
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
