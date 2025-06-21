"""
主入口文件
启动隐私政策智能生成系统
"""

import uvicorn
from src.app import app
from src.utils.utils import get_config
config = get_config()
API_CONFIG = config.get('api', {})

if __name__ == "__main__":
    print("🚀 启动隐私政策智能生成系统...")
    print(f"📖 API文档地址: http://localhost:{API_CONFIG['port']}/docs")
    print(f"🔗 系统地址: http://localhost:{API_CONFIG['port']}")

    uvicorn.run(
        "src.app:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["reload"],
        log_level=API_CONFIG["log_level"]
    )

