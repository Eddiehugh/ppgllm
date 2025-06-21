#!/bin/bash

echo "🚀 启动隐私政策智能生成系统（开发环境）..."

# 检查是否安装了Node.js和npm
if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
    echo "❌ 错误：未找到Node.js或npm，请先安装Node.js和npm"
    exit 1
fi

# 检查是否安装了Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误：未找到Python3，请先安装Python3"
    exit 1
fi

# 启动后端服务
echo "🔧 启动后端服务..."
cd "$(dirname "$0")"
python3 main.py &
BACKEND_PID=$!

# 等待后端启动
echo "⏳ 等待后端服务启动..."
sleep 3

# 启动前端开发服务器
echo "🔧 启动前端开发服务器..."
cd frontend
npm install
npm start &
FRONTEND_PID=$!

# 捕获SIGINT信号（Ctrl+C）
trap cleanup INT
function cleanup() {
    echo "🛑 正在关闭服务..."
    kill $FRONTEND_PID
    kill $BACKEND_PID
    exit 0
}

# 保持脚本运行
echo "✅ 开发环境已启动"
echo "📊 后端API: http://localhost:8000/docs"
echo "🖥️ 前端界面: http://localhost:3000"
echo "按Ctrl+C停止服务"
wait