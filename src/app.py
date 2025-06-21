"""
FastAPI主应用
配置应用和中间件
"""

import os
import sys
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from loguru import logger
from pathlib import Path

# 添加项目根目录到Python路径
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入配置获取函数
try:
    from src.utils.utils import get_config
except ImportError:
    from utils.utils import get_config

# 获取配置
config = get_config()
API_CONFIG = config.get("api", {})
SYSTEM_CONFIG = config.get("system", {})

# 导入路由
try:
    from src.api.routes import router
except ImportError:
    from api.routes import router

# 创建FastAPI应用
app = FastAPI(
    title="隐私政策智能生成系统",
    description="基于AutoGen框架的多Agent隐私政策生成、合规检测和可读性检测系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS - 允许React前端访问
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React默认端口
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1")

# 配置静态文件 - 用于生产环境部署React构建文件
frontend_build_dir = Path(__file__).parent.parent.parent / "frontend" / "build"
if frontend_build_dir.exists():
    app.mount("/", StaticFiles(directory=str(frontend_build_dir), html=True), name="frontend")

# 配置日志
if SYSTEM_CONFIG.get("enable_logging", True):
    log_file = SYSTEM_CONFIG.get("log_file", "logs/agent_system.log")
    os.makedirs(os.path.dirname(log_file), exist_ok=True)
    logger.add(log_file, rotation="1 day", retention="7 days")


@app.on_event("startup")
async def startup_event():
    """应用启动事件"""
    logger.info("隐私政策智能生成系统启动中...")
    logger.info(f"API文档地址: http://localhost:{API_CONFIG['port']}/docs")
    logger.info(f"前端地址: http://localhost:3000")


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("隐私政策智能生成系统正在关闭...")


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["reload"],
        log_level=API_CONFIG["log_level"]
    )