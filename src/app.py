"""
FastAPI主应用
配置应用和中间件
"""

import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger

from config.agent_config import API_CONFIG, SYSTEM_CONFIG
from src.api.routes import router

# 创建FastAPI应用
app = FastAPI(
    title="隐私政策智能生成系统",
    description="基于AutoGen框架的多Agent隐私政策生成、合规检测和可读性检测系统",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 生产环境中应该限制具体域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(router, prefix="/api/v1")

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


@app.on_event("shutdown")
async def shutdown_event():
    """应用关闭事件"""
    logger.info("隐私政策智能生成系统正在关闭...")


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "隐私政策智能生成系统",
        "version": "1.0.0",
        "docs": "/docs",
        "api": "/api/v1"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app:app",
        host=API_CONFIG["host"],
        port=API_CONFIG["port"],
        reload=API_CONFIG["reload"],
        log_level=API_CONFIG["log_level"]
    )