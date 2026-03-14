#!/bin/bash

# ScanQueue 部署脚本
# 适用于 Ubuntu/Debian 系统

set -e

echo "🚀 开始部署 ScanQueue 在线排队系统..."

# 检查Python版本
if ! command -v python3 &> /dev/null; then
    echo "❌ 未找到 Python3，请先安装 Python3"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✅ Python 版本: $PYTHON_VERSION"

# 创建虚拟环境
echo "📦 创建虚拟环境..."
if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

# 激活虚拟环境
source venv/bin/activate

# 安装依赖
echo "📦 安装依赖包..."
pip install --upgrade pip
pip install -r requirements.txt

# 创建必要的目录
echo "📁 创建目录结构..."
mkdir -p static
mkdir -p templates

# 初始化数据库
echo "🗄️ 初始化数据库..."
python3 -c "
from app import init_db, init_default_queues
init_db()
init_default_queues()
print('✅ 数据库初始化完成')
"

# 设置防火墙（如果需要）
echo "🛡️ 配置防火墙..."
if command -v ufw &> /dev/null; then
    sudo ufw allow 5000/tcp
    echo "✅ 已开放端口 5000"
fi

# 创建系统服务
echo "🔧 创建系统服务..."
cat > scanqueue.service << EOF
[Unit]
Description=ScanQueue Online Queue System
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$(pwd)
Environment="PATH=$(pwd)/venv/bin"
ExecStart=$(pwd)/venv/bin/python app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# 安装服务
if [ "$EUID" -eq 0 ]; then
    cp scanqueue.service /etc/systemd/system/
    systemctl daemon-reload
    systemctl enable scanqueue
    systemctl start scanqueue
    echo "✅ 系统服务已安装并启动"
else
    echo "📝 请以root权限运行以下命令安装服务："
    echo "sudo cp scanqueue.service /etc/systemd/system/"
    echo "sudo systemctl daemon-reload"
    echo "sudo systemctl enable scanqueue"
    echo "sudo systemctl start scanqueue"
fi

# 创建Nginx配置（可选）
if command -v nginx &> /dev/null; then
    echo "🌐 创建Nginx配置..."
    cat > scanqueue.nginx.conf << EOF
server {
    listen 80;
    server_name your-domain.com;  # 修改为你的域名
    
    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto \$scheme;
    }
    
    location /socket.io {
        proxy_pass http://127.0.0.1:5000/socket.io;
        proxy_http_version 1.1;
        proxy_set_header Upgrade \$http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host \$host;
        proxy_set_header X-Real-IP \$remote_addr;
        proxy_set_header X-Forwarded-For \$proxy_add_x_forwarded_for;
    }
}
EOF
    echo "✅ Nginx配置已生成到 scanqueue.nginx.conf"
    echo "📝 请将配置复制到 /etc/nginx/sites-available/ 并启用"
fi

echo ""
echo "🎉 部署完成！"
echo ""
echo "📋 访问地址："
echo "   - 客户页面: http://$(hostname -I | awk '{print $1}'):5000/customer"
echo "   - 管理后台: http://$(hostname -I | awk '{print $1}'):5000/admin"
echo "   - 监控页面: http://$(hostname -I | awk '{print $1}'):5000/"
echo ""
echo "🔧 管理命令："
echo "   - 启动服务: systemctl start scanqueue"
echo "   - 停止服务: systemctl stop scanqueue"
echo "   - 重启服务: systemctl restart scanqueue"
echo "   - 查看日志: journalctl -u scanqueue -f"
echo ""
echo "📱 使用建议："
echo "   1. 为客户生成二维码，方便快速访问"
echo "   2. 在管理后台设置不同的服务队列"
echo "   3. 培训员工使用叫号功能"
echo "   4. 定期备份数据库文件: scanqueue.db"
echo ""
echo "💡 提示：首次访问时，系统已创建3个默认队列："
echo "   - 普通服务：常规业务办理"
echo "   - VIP服务：优先服务通道"
echo "   - 快速通道：简单业务快速处理"