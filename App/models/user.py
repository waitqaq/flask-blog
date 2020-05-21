from App.extensions import db  # 导入模型对象
from .db_base import DB_Base  # 导入自定义模型基类
from datetime import datetime
# 导入生成与验证密码的方法
from werkzeug.security import generate_password_hash, check_password_hash
from itsdangerous import TimedJSONWebSignatureSerializer as Seralize  # 导入序列化方法
from flask import current_app
from flask_login import UserMixin  # 包含了判断是否登录等等方法饿基类
from App.extensions import login_manager


# User  模型类
class User(UserMixin,db.Model, DB_Base):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)  # 自增id
    username = db.Column(db.String(12), index=True, unique=True)  # 用户名
    password_hash = db.Column(db.String(128))  # 加密的密码
    sex = db.Column(db.Boolean, default=True)  # 性别
    age = db.Column(db.Integer, default=18)  # 年龄
    email = db.Column(db.String(50), unique=True)  # 邮箱
    icon = db.Column(db.String(70), default='default.jpg')  # 头像
    lastLogin = db.Column(db.DateTime)  # 上次登录时间
    registerTime = db.Column(db.DateTime, default=datetime.utcnow)  # 注册时间
    confirm = db.Column(db.Boolean, default=False)  # 激活状态，默认未激活

    # 设置模型引用关系
    """
    Posts : 建立引用关系的模型
    backref : 是给关联的模型添加一个查询的属性  叫user
    lazy : 加载的时机  返回查询集（可以添加连贯操作）
    """
    posts = db.relationship('Posts',backref='user',lazy='dynamic')

    # 密码加密处理的装饰器
    @property
    def password(self):
        raise AttributeError

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    # 检验密码正确性的方法
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    # 生成token用于账户激活（也就是知道事哪个用户激活的）
    def generate_token(self):
        s = Seralize(current_app.config['SECRET_KEY'])
        return s.dumps({'id': self.id})  # 返回加密的字符串

    #  检测传递过来的token值， 进行账户激活
    @staticmethod
    def check_token(token):
        s = Seralize(current_app.config['SECRET_KEY'])
        try:
            id = s.loads(token)['id']
            u = User.query.get(id)
            if not u:
                return False
            u.confirm = True
            u.save()
            return True
        except:
            return False


# 这是一个回调的方法，实时获取当前表中用户数据的对象
@login_manager.user_loader
def user_loader(userid):
    return User.query.get(int(userid))


