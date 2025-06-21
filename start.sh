#!/bin/bash

echo "🚀 启动隐私政策智能生成系统..."

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3，请先安装Python3"
    exit 1
fi

# 检查是否存在虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装依赖
echo "📥 安装依赖包..."
pip install -r requirements.txt

# 检查环境变量文件
if [ ! -f ".env" ]; then
    echo "⚠️  警告：未找到.env文件，请复制.env.example并配置API密钥"
    cp .env.example .env
    echo "📝 已创建.env文件，请编辑并配置GLM_API_KEY"
fi

# 创建日志目录
mkdir -p logs

# 启动系统
echo "🎯 启动系统..."
python main.py