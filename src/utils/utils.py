"""
工具函数
提供系统通用的工具方法
"""

import os
from pathlib import Path


def get_memory_dir() -> str:
    """获取内存存储目录"""
    # 获取项目根目录
    project_root = Path(__file__).parent.parent.parent
    memory_dir = project_root / "memory"
    
    # 确保目录存在
    memory_dir.mkdir(exist_ok=True)
    
    return str(memory_dir)


def get_logs_dir() -> str:
    """获取日志目录"""
    project_root = Path(__file__).parent.parent.parent
    logs_dir = project_root / "logs"
    
    # 确保目录存在
    logs_dir.mkdir(exist_ok=True)
    
    return str(logs_dir)


def get_config_dir() -> str:
    """获取配置目录"""
    project_root = Path(__file__).parent.parent.parent
    config_dir = project_root / "config"
    
    return str(config_dir)


def ensure_dir(dir_path: str) -> str:
    """确保目录存在"""
    os.makedirs(dir_path, exist_ok=True)
    return dir_path


def get_project_root() -> str:
    """获取项目根目录"""
    return str(Path(__file__).parent.parent.parent)