import os
from datetime import timedelta

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


# 配置类的基类
class Config:
    SECRET_KEY = 'alone'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    BOOTSTRAP_SERVER_LOCAL = True  # 加载本地静态资源文件
    # 邮件发送配置
    # 端口号
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    # 邮箱服务器
    MAIL_SERVER = 'smtp.163.com'
    # 用户名
    MAIL_USERNAME = 'alone_3@163.com'
    # 密码
    MAIL_PASSWORD = 'ZYOVHEHBEHIPWBZW'
    # 分页每页显示数据条数
    PAGE_NUM = 6
    # 文件上传配置
    UPLOADED_PHOTOS_DEST = os.path.join(BASE_DIR, 'static/upload')
    MAX_CONTENT_LENGTH = 1024 * 1024 * 64
    # 七牛云上传配置
    QINIU_ACCESS_KEY = "mJZ9wIcnIojbofK8RsH-Dk8g_foWdC5B1DHNzME5"
    QINIU_SECRET_KEY = "zvGGpYbqKJV_2_V6dAacPGyijmbkH21lAJHKyFoA"
    QINIU_BUCKET_NAME = "aloneblog"
    QINIU_BUCKET_DOMAIN = 'cdnonline.top'


# 开发环境
class DevelopmentConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:128114@127.0.0.1:3306/alone_blog'
    DEBUG = True
    TESTING = False


# 测试环境
class TestingConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:128114@127.0.0.1:3306/test_blog'
    DEBUG = False
    TESTING = True


# 生产环境
class ProductionConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://root:128114@127.0.0.1:3306/blog'
    DEBUG = False
    TESTING = False


# 配置类的字典,给类起别名
configDict = {
    'default': DevelopmentConfig,
    'dev': DevelopmentConfig,
    'Test': TestingConfig,
    'production': ProductionConfig,
}
