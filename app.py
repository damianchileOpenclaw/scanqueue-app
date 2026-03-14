#!/usr/bin/env python3
"""
ScanQueue 在线排队系统 - 后端服务器
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
    
    conn.commit()
    conn.close()

# 初始化默认队列
def init_default_queues():
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 检查是否已有队列
    c.execute("SELECT COUNT(*) FROM queues")
    count = c.fetchone()[0]
    
    if count == 0:
        # 添加默认队列
        queues = [
            ('普通服务', '常规业务办理'),
            ('VIP服务', '优先服务通道'),
            ('快速通道', '简单业务快速处理')
        ]
        
        for name, desc in queues:
            c.execute("INSERT INTO queues (name, description) VALUES (?, ?)", (name, desc))
        
        conn.commit()
        print("已创建默认队列")
    
    conn.close()

# 首页
@app.route('/')
def index():
    return render_template('index.html')

# 客户取号页面
@app.route('/customer')
def customer_page():
    return render_template('customer.html')

# 管理后台页面
@app.route('/admin')
def admin_page():
    return render_template('admin.html')

# 获取所有队列
@app.route('/api/queues', methods=['GET'])
def get_queues():
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    c.execute("SELECT * FROM queues WHERE status='active'")
    queues = c.fetchall()
    conn.close()
    
    result = []
    for q in queues:
        result.append({
            'id': q[0],
            'name': q[1],
            'description': q[2],
            'status': q[3],
            'created_at': q[4]
        })
    
    return jsonify(result)

# 获取队列详情
@app.route('/api/queue/<int:queue_id>', methods=['GET'])
def get_queue(queue_id):
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 获取队列信息
    c.execute("SELECT * FROM queues WHERE id=?", (queue_id,))
    queue = c.fetchone()
    
    if not queue:
        return jsonify({'error': '队列不存在'}), 404
    
    # 获取等待中的号码
    c.execute('''SELECT * FROM tickets 
                 WHERE queue_id=? AND status='waiting' 
                 ORDER BY created_at''', (queue_id,))
    waiting_tickets = c.fetchall()
    
    # 获取正在处理的号码
    c.execute('''SELECT * FROM tickets 
                 WHERE queue_id=? AND status='calling' 
                 ORDER BY called_at DESC LIMIT 1''', (queue_id,))
    current_ticket = c.fetchone()
    
    # 获取已完成的号码
    c.execute('''SELECT COUNT(*) FROM tickets 
                 WHERE queue_id=? AND status='completed' 
                 AND date(completed_at)=date('now')''', (queue_id,))
    completed_count = c.fetchone()[0]
    
    conn.close()
    
    result = {
        'queue': {
            'id': queue[0],
            'name': queue[1],
            'description': queue[2]
        },
        'waiting_count': len(waiting_tickets),
        'current_ticket': None,
        'completed_today': completed_count,
        'waiting_tickets': []
    }
    
    if current_ticket:
        result['current_ticket'] = {
            'ticket_number': current_ticket[2],
            'customer_name': current_ticket[3]
        }
    
    for ticket in waiting_tickets:
        result['waiting_tickets'].append({
            'ticket_number': ticket[2],
            'customer_name': ticket[3],
            'created_at': ticket[7]
        })
    
    return jsonify(result)

# 客户取号
@app.route('/api/ticket/take', methods=['POST'])
def take_ticket():
    data = request.json
    queue_id = data.get('queue_id')
    customer_name = data.get('customer_name', '匿名客户')
    phone = data.get('phone', '')
    
    if not queue_id:
        return jsonify({'error': '请选择队列'}), 400
    
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 检查队列是否存在
    c.execute("SELECT * FROM queues WHERE id=?", (queue_id,))
    queue = c.fetchone()
    if not queue:
        conn.close()
        return jsonify({'error': '队列不存在'}), 404
    
    # 生成排队号码
    today = datetime.now().strftime('%Y%m%d')
    c.execute('''SELECT COUNT(*) FROM tickets 
                 WHERE queue_id=? AND date(created_at)=date('now')''', (queue_id,))
    today_count = c.fetchone()[0] + 1
    
    ticket_number = f"{queue[1][:2]}{today[-4:]}-{today_count:03d}"
    
    # 计算预计等待时间（简单估算：每人3分钟）
    c.execute('''SELECT COUNT(*) FROM tickets 
                 WHERE queue_id=? AND status='waiting' ''', (queue_id,))
    waiting_count = c.fetchone()[0]
    estimated_wait_time = waiting_count * 3
    
    # 插入新号码
    c.execute('''INSERT INTO tickets 
                 (queue_id, ticket_number, customer_name, phone, estimated_wait_time) 
                 VALUES (?, ?, ?, ?, ?)''',
              (queue_id, ticket_number, customer_name, phone, estimated_wait_time))
    
    ticket_id = c.lastrowid
    conn.commit()
    conn.close()
    
    # 广播新号码通知
    socketio.emit('new_ticket', {
        'queue_id': queue_id,
        'ticket_number': ticket_number,
        'customer_name': customer_name,
        'waiting_count': waiting_count + 1
    })
    
    return jsonify({
        'success': True,
        'ticket_number': ticket_number,
        'estimated_wait_time': estimated_wait_time,
        'message': f'取号成功！您的号码是 {ticket_number}，前面有 {waiting_count} 人等待，预计等待 {estimated_wait_time} 分钟'
    })

# 查询排队状态
@app.route('/api/ticket/status/<ticket_number>', methods=['GET'])
def get_ticket_status(ticket_number):
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    c.execute('''SELECT t.*, q.name as queue_name 
                 FROM tickets t 
                 JOIN queues q ON t.queue_id = q.id 
                 WHERE t.ticket_number=?''', (ticket_number,))
    ticket = c.fetchone()
    
    if not ticket:
        conn.close()
        return jsonify({'error': '号码不存在'}), 404
    
    # 获取前面等待人数
    c.execute('''SELECT COUNT(*) FROM tickets 
                 WHERE queue_id=? AND status='waiting' 
                 AND created_at < ?''', 
              (ticket[1], ticket[7]))
    ahead_count = c.fetchone()[0]
    
    conn.close()
    
    return jsonify({
        'ticket_number': ticket[2],
        'customer_name': ticket[3],
        'queue_name': ticket[9],
        'status': ticket[5],
        'created_at': ticket[7],
        'called_at': ticket[8],
        'ahead_count': ahead_count,
        'estimated_wait_time': ahead_count * 3
    })

# 管理端叫号
@app.route('/api/ticket/call', methods=['POST'])
def call_ticket():
    data = request.json
    ticket_number = data.get('ticket_number')
    called_by = data.get('called_by', '管理员')
    
    if not ticket_number:
        return jsonify({'error': '请输入号码'}), 400
    
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 查找号码
    c.execute('''SELECT * FROM tickets WHERE ticket_number=?''', (ticket_number,))
    ticket = c.fetchone()
    
    if not ticket:
        conn.close()
        return jsonify({'error': '号码不存在'}), 404
    
    if ticket[5] != 'waiting':
        conn.close()
        return jsonify({'error': '该号码不在等待状态'}), 400
    
    # 更新号码状态
    called_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''UPDATE tickets 
                 SET status='calling', called_at=?
                 WHERE ticket_number=?''', (called_at, ticket_number))
    
    # 记录叫号日志
    c.execute('''INSERT INTO call_logs (ticket_id, called_by) 
                 VALUES (?, ?)''', (ticket[0], called_by))
    
    conn.commit()
    conn.close()
    
    # 广播叫号通知
    socketio.emit('ticket_called', {
        'ticket_number': ticket_number,
        'customer_name': ticket[3],
        'called_by': called_by,
        'called_at': called_at,
        'queue_id': ticket[1]
    })
    
    return jsonify({
        'success': True,
        'message': f'已叫号：{ticket_number} - {ticket[3]}'
    })

# 完成服务
@app.route('/api/ticket/complete', methods=['POST'])
def complete_ticket():
    data = request.json
    ticket_number = data.get('ticket_number')
    
    if not ticket_number:
        return jsonify({'error': '请输入号码'}), 400
    
    conn = sqlite3.connect('scanqueue.db')
    c = conn.cursor()
    
    # 查找号码
    c.execute('''SELECT * FROM tickets WHERE ticket_number=?''', (ticket_number,))
    ticket = c.fetchone()
    
    if not ticket:
        conn.close()
        return jsonify({'error': '号码不存在'}), 404
    
    # 更新号码状态
    completed_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    c.execute('''UPDATE tickets 
                 SET status='completed', completed_at=?
                 WHERE ticket_number=?''', (completed_at, ticket_number))
    
    conn.commit()
    conn.close()
    
    # 广播完成通知
    socketio.emit('ticket_completed', {
        'ticket_number': ticket_number,
        'queue_id': ticket[1]
    })
    
    return jsonify({
        'success': True,
        'message': f'已完成服务：{ticket_number}'
    })

# WebSocket 连接事件
@socketio.on('connect')
def handle_connect():
    print('客户端已连接')
    emit('connected', {'message': '已连接到排队系统'})

@socketio.on('disconnect')
def handle_disconnect():
    print('客户端已断开')

# 启动时初始化
if __name__ == '__main__':
    # 初始化数据库
    init_db()
    init_default_queues()
    
    print("=" * 50)
    print("ScanQueue 在线排队系统")
    print("=" * 50)
    print("访问地址:")
    print("1. 客户取号页面: http://localhost:5000/customer")
    print("2. 管理后台页面: http://localhost:5000/admin")
    print("3. 实时监控页面: http://localhost:5000/")
    print("=" * 50)
    
    # 创建模板目录
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    
    socketio.run(app, host='0.0.0.0', port=8080, debug=True, allow_unsafe_werkzeug=True)