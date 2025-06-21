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
    from ..utils.utils import get_memory_dir
try:
    from prompt.agent import PRIVACY_POLICY_GENERATOR_PROMPT, PRIVACY_POLICY_GENERATOR_DESCRIPTION
except ImportError:
    from ...prompt.agent import PRIVACY_POLICY_GENERATOR_PROMPT, PRIVACY_POLICY_GENERATOR_DESCRIPTION


class PrivacyPolicyGeneratorBuilder:
    """隐私政策生成Agent构建器"""
    
    def __init__(self, model_client, tools=None, memory_files=None):
        self.model_client = model_client
        self.tools = tools or []
        self.memory_files = memory_files or []

    async def build(self):
        """构建隐私政策生成Agent"""
        memories = []
        for name in self.memory_files:
            manager = ListMemoryManager(os.path.join(get_memory_dir(), name))
            memories.append(await manager.get_memory())
            
        return AssistantAgent(
            name="privacy_policy_generator",
            model_client=self.model_client,
            description=PRIVACY_POLICY_GENERATOR_DESCRIPTION,
            system_message=PRIVACY_POLICY_GENERATOR_PROMPT,
            tools=self.tools,
            memory=memories,
            handoffs=["compliance_checker", "readability_checker"],
            model_client_stream=True
        )