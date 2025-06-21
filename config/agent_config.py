"""
Agent配置文件
定义系统中三个agent的基本配置信息
"""

from typing import Dict, Any
import os
from dotenv import load_dotenv

load_dotenv()

# LLM配置
LLM_CONFIG = {
    "config_list": [
        {
            "model": "glm-4-9b-chat",
            "api_key": os.getenv("GLM_API_KEY", "your-api-key"),
            "base_url": os.getenv("GLM_BASE_URL", "https://open.bigmodel.cn/api/paas/v4/"),
        }
    ],
    "temperature": 0.7,
    "timeout": 120,
}

# Agent配置
AGENT_CONFIGS = {
    "privacy_policy_generator": {
        "name": "隐私政策生成专家",
        "description": "专门负责生成移动应用隐私政策的AI助手",
        "system_message": "你是一个专业的隐私政策生成专家，擅长为移动应用创建符合法规要求的隐私政策文档。",
        "llm_config": LLM_CONFIG,
        "human_input_mode": "NEVER",
        "max_consecutive_auto_reply": 3,
    },
    
    "compliance_checker": {
        "name": "合规性检测专家", 
        "description": "专门负责检测隐私政策内容合规性的AI助手",
        "system_message": "你是一个专业的隐私政策合规性检测专家，能够识别隐私政策中的合规问题并提供改进建议。",
        "llm_config": LLM_CONFIG,
        "human_input_mode": "NEVER",
        "max_consecutive_auto_reply": 3,
    },
    
    "readability_checker": {
        "name": "可读性检测专家",
        "description": "专门负责检测隐私政策可读性的AI助手", 
        "system_message": "你是一个专业的文档可读性检测专家，能够评估隐私政策的可读性并提供优化建议。",
        "llm_config": LLM_CONFIG,
        "human_input_mode": "NEVER",
        "max_consecutive_auto_reply": 3,
    }
}

# API配置
API_CONFIG = {
    "host": "0.0.0.0",
    "port": 8000,
    "reload": True,
    "log_level": "info"
}

# 系统配置
SYSTEM_CONFIG = {
    "max_round": 10,
    "timeout": 300,
    "enable_logging": True,
    "log_file": "logs/agent_system.log"
}