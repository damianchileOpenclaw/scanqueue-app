#!/bin/bash

# ScanQueue 启动脚本
# 适用于快速测试和 desarrollo

echo "🚀 启动 ScanQueue 在线排队系统..."

# 检查Python
if ! command -v python3 &> /dev/null; then
    echo "❌ 错误: 未找到 Python3"
    echo "请先安装 Python3:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  macOS: brew install python"
    exit 1
fi

# 检查虚拟环境
if [ ! -d "venv" ]; then
    echo "📦 创建虚拟环境..."
    python3 -m venv venv
fi

# 激活虚拟环境
echo "🔧 激活虚拟环境..."
source venv/bin/activate

# 安装/更新依赖
echo "📦 检查依赖..."
pip install --upgrade pip
pip install -r requirements.txt

# 初始化数据库
echo "🗄️ 初始化数据库..."
python3 -c "
from app import init_db, init_default_queues
try:
    init_db()
    init_default_queues()
    print('✅ 数据库初始化完成')
except Exception as e:
    print(f'⚠️  数据库初始化警告: {e}')
"

# 检查端口
PORT=5000
if lsof -Pi :$PORT -sTCP:LISTEN -t >/dev/null ; then
    echo "⚠️  端口 $PORT 已被占用"
    read -p "是否使用其他端口？ (y/n): " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        read -p "请输入新端口号: " PORT
    else
        echo "❌ 启动中止"
        exit 1
    fi
fi

# 启动服务器
echo "🌐 启动服务器在端口 $PORT..."
echo ""
echo "=========================================="
echo "          ScanQueue 在线排队系统"
echo "=========================================="
echo ""
echo "📱 访问地址:"
echo "   客户页面: http://localhost:$PORT/customer"
echo "   管理后台: http://localhost:$PORT/admin"
echo "   监控页面: http://localhost:$PORT/"
echo ""
echo "📋 默认队列:"
echo "   • 普通服务 - 常规业务办理"
echo "   • VIP服务 - 优先服务通道"
echo "   • 快速通道 - 简单业务快速处理"
echo ""
echo "🔧 按 Ctrl+C 停止服务器"
echo "=========================================="
echo ""

# 设置环境变量并启动
export FLASK_DEBUG=1
python app.py --port $PORT