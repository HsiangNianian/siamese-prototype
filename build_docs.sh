#!/bin/bash

# Siamese Prototype 文档构建脚本

set -e

echo "🚀 构建 Siamese Prototype 文档..."

# 检查是否在项目根目录
if [ ! -f "pyproject.toml" ]; then
    echo "❌ 错误: 请在项目根目录运行此脚本"
    exit 1
fi

# 安装文档依赖
echo "📦 安装文档依赖..."
uv sync --group docs

# 进入 docs 目录
cd docs

# 清理之前的构建
echo "🧹 清理之前的构建..."
make clean

# 构建文档
echo "🔨 构建 HTML 文档..."
make html

echo "✅ 文档构建完成！"
echo ""
echo "📖 文档位置: docs/_build/html/index.html"
echo "🌐 启动本地服务器: cd docs && make serve"
echo "🔧 开发模式: cd docs && make dev"
echo ""

# 询问是否启动服务器
read -p "是否启动本地服务器查看文档？(y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    echo "🌐 启动本地服务器在 http://localhost:8000"
    cd _build/html && python -m http.server 8000
fi 