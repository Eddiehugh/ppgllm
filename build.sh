#!/bin/bash

echo "🏗️ 构建隐私政策智能生成系统..."

# 检查是否安装了Node.js和npm
if ! command -v node &> /dev/null || ! command -v npm &> /dev/null; then
    echo "❌ 错误：未找到Node.js或npm，请先安装Node.js和npm"
    exit 1
fi

# 构建前端
echo "🔧 构建React前端..."
cd "$(dirname "$0")/frontend"
npm install
npm run build

echo "✅ 构建完成！"
echo "🚀 使用 ./start.sh 启动系统"