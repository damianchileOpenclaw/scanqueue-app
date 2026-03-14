"""
ScanQueue 配置文件
"""

import os
from datetime import timedelta

class Config:
    """基础配置"""
    # 安全密钥
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'scanqueue_secret_key_2024_change_in_production'
    
    # 数据库配置
    DATABASE_PATH = 'scanqueue.db'
    
    # 会话配置
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_SECURE = False  # 生产环境设为True
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    
    # 服务器配置
    HOST = '0.0.0.0'
    PORT = 5000
    DEBUG = True
    
    # WebSocket配置
    SOCKETIO_ASYNC_MODE = 'eventlet'
    SOCKETIO_PING_TIMEOUT = 60
    SOCKETIO_PING_INTERVAL = 25
    SOCKETIO_MAX_HTTP_BUFFER_SIZE = 10 * 1024 * 1024  # 10MB
    
    # 业务配置
    DEFAULT_QUEUES = [
        {'name': '普通服务', 'description': '常规业务办理'},
        {'name': 'VIP服务', 'description': '优先服务通道'},
        {'name': '快速通道', 'description': '简单业务快速处理'}
    ]
    
    # 排队配置
    ESTIMATED_WAIT_TIME_PER_PERSON = 3  # 分钟
    MAX_WAITING_TICKETS = 100  # 最大等待人数
    TICKET_NUMBER_FORMAT = '{queue_prefix}{date_suffix}-{sequence:03d}'
    
    # 通知配置
    ENABLE_BROWSER_NOTIFICATIONS = True
    ENABLE_SMS_NOTIFICATIONS = False  # 需要配置SMS服务
    ENABLE_EMAIL_NOTIFICATIONS = False  # 需要配置邮件服务
    
    # 安全配置
    RATE_LIMIT_ENABLED = True
    MAX_REQUESTS_PER_MINUTE = 60
    CORS_ENABLED = True
    CORS_ORIGINS = ['*']  # 生产环境应限制域名
    
    # 日志配置
    LOG_LEVEL = 'INFO'
    LOG_FILE = 'scanqueue.log'
    LOG_FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # 备份配置
    BACKUP_ENABLED = True
    BACKUP_DIR = 'backups'
    BACKUP_INTERVAL_HOURS = 24
    MAX_BACKUP_FILES = 30


class DevelopmentConfig(Config):
    """开发环境配置"""
    DEBUG = True
    LOG_LEVEL = 'DEBUG'
    CORS_ORIGINS = ['http://localhost:3000', 'http://localhost:5000']


class ProductionConfig(Config):
    """生产环境配置"""
    DEBUG = False
    SECRET_KEY = os.environ.get('SECRET_KEY', '必须设置强密钥')
    SESSION_COOKIE_SECURE = True
    CORS_ORIGINS = ['https://tudominio.com']  # 替换为你的域名
    LOG_LEVEL = 'WARNING'
    
    # 生产环境使用外部数据库
    DATABASE_URL = os.environ.get('DATABASE_URL')
    if DATABASE_URL:
        # 如果是MySQL/PostgreSQL URL
        DATABASE_PATH = DATABASE_URL
    else:
        # 使用SQLite但放在安全位置
        DATABASE_PATH = '/var/lib/scanqueue/scanqueue.db'


class TestingConfig(Config):
    """测试环境配置"""
    TESTING = True
    DEBUG = True
    DATABASE_PATH = ':memory:'  # 内存数据库
    WTF_CSRF_ENABLED = False


# 配置映射
config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
    'default': DevelopmentConfig
}

def get_config(config_name=None):
    """获取配置"""
    if config_name is None:
        config_name = os.environ.get('FLASK_ENV', 'default')
    
    config_class = config.get(config_name.lower())
    if config_class is None:
        raise ValueError(f"未知的配置环境: {config_name}")
    
    return config_class()