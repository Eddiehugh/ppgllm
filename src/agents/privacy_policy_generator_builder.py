"""
隐私政策生成Agent构建器
"""

import os
from autogen_agentchat.agents import AssistantAgent

try:
    from src.core.memory.list_memory import ListMemoryManager
except ImportError:
    from ..core.memory.list_memory import ListMemoryManager
try:
    from src.utils.utils import get_memory_dir
except ImportError:
    from ppgllm.src.utils import get_memory_dir
try:
    from prompt.privacy_policy_generator_prompt import DESCRIPTION, SYSTEM_PROMPT
except ImportError:
    from ...prompt.privacy_policy_generator_prompt import DESCRIPTION, SYSTEM_PROMPT

class PrivacyPolicyGeneratorBuilder:
    """隐私政策生成Agent构建器"""

    def __init__(self, model_client, tools=None, memory_files=None):
        self.model_client = model_client
        self.tools = tools or []
        self.memory_files = memory_files or []

    async def build(self):
        """构建合规性检测Agent"""
        memories = []
        for name in self.memory_files:
            manager = ListMemoryManager(os.path.join(get_memory_dir(), name))
            memories.append(await manager.get_memory())

        return AssistantAgent(
            name="移动应用隐私政策内容生成agent",
            model_client=self.model_client,
            description=DESCRIPTION,
            system_message=SYSTEM_PROMPT,
            tools=self.tools,
            memory=memories,
            model_client_stream=True
        )