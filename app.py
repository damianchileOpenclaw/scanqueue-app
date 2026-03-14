#!/usr/bin/env python3
"""
ScanQueue 在线排队系统 - 版本 fixed para Render
"""

from flask import Flask, render_template, request, jsonify, session
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import sqlite3
import json
import time
import threading
from datetime import datetime
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'scanqueue_secret_key_2024'
CORS(app)
socketio = SocketIO(app, cors_allowed_origins="*")

# 初始化数据库
def init_db():
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 创建队列表
    c.execute('''CREATE TABLE IF NOT EXISTS queues
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  name TEXT NOT NULL,
                  description TEXT,
                  status TEXT DEFAULT 'active',
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # 创建排队号码表
    c.execute('''CREATE TABLE IF NOT EXISTS tickets
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  queue_id INTEGER,
                  ticket_number TEXT NOT NULL,
                  customer_name TEXT,
                  phone TEXT,
                  status TEXT DEFAULT 'waiting',
                  estimated_wait_time INTEGER,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  called_at TIMESTAMP,
                  completed_at TIMESTAMP,
                  FOREIGN KEY (queue_id) REFERENCES queues (id))''')
    
    # 创建叫号记录表
    c.execute('''CREATE TABLE IF NOT EXISTS call_logs
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  ticket_id INTEGER,
                  called_by TEXT,
                  called_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (ticket_id) REFERENCES tickets (id))''')
    
    # 插入默认队列（如果不存在）
    c.execute("SELECT COUNT(*) FROM queues")
    if c.fetchone()[0] == 0:
        default_queues = [
            ("普通服务", "常规排队服务", "active"),
            ("VIP服务", "VIP优先服务", "active"),
            ("快速通道", "快速处理服务", "active")
        ]
        c.executemany("INSERT INTO queues (name, description, status) VALUES (?, ?, ?)", default_queues)
        print("已创建默认队列")
    
    conn.commit()
    conn.close()

# 初始化数据库
init_db()

# ==================== API 路由 ====================

@app.route('/')
def index():
    """首页 - 实时监控"""
    return render_template('index.html')

@app.route('/customer')
def customer():
    """客户取号页面"""
    return render_template('customer.html')

@app.route('/admin')
def admin():
    """管理后台"""
    return render_template('admin.html')

# ==================== API 接口 ====================

@app.route('/api/queues', methods=['GET'])
def get_queues():
    """获取所有队列"""
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    c.execute("SELECT id, name, description, status FROM queues WHERE status='active'")
    queues = [{'id': row[0], 'name': row[1], 'description': row[2], 'status': row[3]} for row in c.fetchall()]
    conn.close()
    return jsonify({'queues': queues})

@app.route('/api/tickets', methods=['GET'])
def get_tickets():
    """获取所有排队号码"""
    queue_id = request.args.get('queue_id')
    status = request.args.get('status', 'waiting')
    
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    query = "SELECT t.id, t.ticket_number, t.customer_name, t.phone, t.status, t.created_at, q.name FROM tickets t JOIN queues q ON t.queue_id = q.id"
    params = []
    
    if queue_id:
        query += " WHERE t.queue_id = ?"
        params.append(queue_id)
    if status:
        if 'WHERE' in query:
            query += " AND t.status = ?"
        else:
            query += " WHERE t.status = ?"
        params.append(status)
    
    query += " ORDER BY t.created_at ASC"
    c.execute(query, params)
    
    tickets = []
    for row in c.fetchall():
        tickets.append({
            'id': row[0],
            'ticket_number': row[1],
            'customer_name': row[2],
            'phone': row[3],
            'status': row[4],
            'created_at': row[5],
            'queue_name': row[6]
        })
    
    conn.close()
    return jsonify({'tickets': tickets})

@app.route('/api/tickets', methods=['POST'])
def create_ticket():
    """创建新的排队号码"""
    data = request.json
    queue_id = data.get('queue_id')
    customer_name = data.get('customer_name', '')
    phone = data.get('phone', '')
    
    if not queue_id:
        return jsonify({'error': '请选择队列'}), 400
    
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 获取队列信息
    c.execute("SELECT name FROM queues WHERE id = ?", (queue_id,))
    queue = c.fetchone()
    if not queue:
        return jsonify({'error': '队列不存在'}), 400
    
    queue_name = queue[0]
    
    # 生成排队号码
    c.execute("SELECT COUNT(*) FROM tickets WHERE queue_id = ? AND DATE(created_at) = DATE('now')", (queue_id,))
    today_count = c.fetchone()[0] + 1
    ticket_number = f"{queue_name}{today_count:03d}"
    
    # 插入新号码
    c.execute("INSERT INTO tickets (queue_id, ticket_number, customer_name, phone, status) VALUES (?, ?, ?, ?, 'waiting')",
              (queue_id, ticket_number, customer_name, phone))
    ticket_id = c.lastrowid
    
    conn.commit()
    
    # 获取创建的号码信息
    c.execute("SELECT t.id, t.ticket_number, t.customer_name, t.phone, t.status, t.created_at, q.name FROM tickets t JOIN queues q ON t.queue_id = q.id WHERE t.id = ?", (ticket_id,))
    row = c.fetchone()
    
    ticket = {
        'id': row[0],
        'ticket_number': row[1],
        'customer_name': row[2],
        'phone': row[3],
        'status': row[4],
        'created_at': row[5],
        'queue_name': row[6]
    }
    
    conn.close()
    
    # 通过WebSocket通知所有客户端
    socketio.emit('new_ticket', ticket)
    
    return jsonify({'ticket': ticket, 'message': '取号成功'})

@app.route('/api/tickets/<int:ticket_id>/call', methods=['POST'])
def call_ticket(ticket_id):
    """叫号"""
    data = request.json
    called_by = data.get('called_by', '系统')
    
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 更新号码状态
    c.execute("UPDATE tickets SET status = 'called', called_at = CURRENT_TIMESTAMP WHERE id = ?", (ticket_id,))
    
    # 记录叫号日志
    c.execute("INSERT INTO call_logs (ticket_id, called_by) VALUES (?, ?)", (ticket_id, called_by))
    
    conn.commit()
    
    # 获取更新后的号码信息
    c.execute("SELECT t.id, t.ticket_number, t.customer_name, t.status, q.name FROM tickets t JOIN queues q ON t.queue_id = q.id WHERE t.id = ?", (ticket_id,))
    row = c.fetchone()
    
    ticket = {
        'id': row[0],
        'ticket_number': row[1],
        'customer_name': row[2],
        'status': row[3],
        'queue_name': row[4]
    }
    
    conn.close()
    
    # 通过WebSocket通知所有客户端
    socketio.emit('ticket_called', ticket)
    
    return jsonify({'ticket': ticket, 'message': '叫号成功'})

@app.route('/api/tickets/<int:ticket_id>/complete', methods=['POST'])
def complete_ticket(ticket_id):
    """完成服务"""
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 更新号码状态
    c.execute("UPDATE tickets SET status = 'completed', completed_at = CURRENT_TIMESTAMP WHERE id = ?", (ticket_id,))
    conn.commit()
    
    # 获取更新后的号码信息
    c.execute("SELECT t.id, t.ticket_number, t.customer_name, t.status, q.name FROM tickets t JOIN queues q ON t.queue_id = q.id WHERE t.id = ?", (ticket_id,))
    row = c.fetchone()
    
    ticket = {
        'id': row[0],
        'ticket_number': row[1],
        'customer_name': row[2],
        'status': row[3],
        'queue_name': row[4]
    }
    
    conn.close()
    
    # 通过WebSocket通知所有客户端
    socketio.emit('ticket_completed', ticket)
    
    return jsonify({'ticket': ticket, 'message': '服务完成'})

@app.route('/api/stats', methods=['GET'])
def get_stats():
    """获取统计信息"""
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 今日排队总数
    c.execute("SELECT COUNT(*) FROM tickets WHERE DATE(created_at) = DATE('now')")
    total_today = c.fetchone()[0]
    
    # 当前等待人数
    c.execute("SELECT COUNT(*) FROM tickets WHERE status = 'waiting'")
    waiting = c.fetchone()[0]
    
    # 平均等待时间（估算）
    c.execute("SELECT AVG((julianday(called_at) - julianday(created_at)) * 24 * 60) FROM tickets WHERE called_at IS NOT NULL")
    avg_wait = c.fetchone()[0] or 0
    
    conn.close()
    
    return jsonify({
        'total_today': total_today,
        'waiting': waiting,
        'avg_wait_minutes': round(avg_wait, 1)
    })

# ==================== WebSocket 事件 ====================

@socketio.on('connect')
def handle_connect():
    print('客户端连接')
    emit('connected', {'message': '连接成功'})

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端断开')

# ==================== 主程序 ====================

if __name__ == '__main__':
    print("="*50)
    print("ScanQueue 在线排队系统")
    print("="*50)
    print("访问地址:")
    print("1. 客户取号页面: http://localhost:5000/customer")
    print("2. 管理后台页面: http://localhost:5000/admin")
    print("3. 实时监控页面: http://localhost:5000/")
    print("="*50)
    
    port = int(os.environ.get('PORT', 5000))
    # FIX: Agregar allow_unsafe_werkzeug=True para producción
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)