from App.extensions import db
from .db_base import DB_Base
from datetime import datetime

posts_categorys = db.Table('posts_categorys',
                       db.Column('posts_id', db.Integer, db.ForeignKey('posts.id'), primary_key=True),
                       db.Column('categorys_id', db.Integer, db.ForeignKey('categorys.id'), primary_key=True)
                       )
# 博客模型
class Posts(DB_Base, db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(20), index=True)  # 标题
    article = db.Column(db.Text)  # md格式正文
    pid = db.Column(db.Integer, default=0)  # 父id
    path = db.Column(db.Text, default='0,')  # 路径
    visit = db.Column(db.Integer, default=0)  # 文章访问量
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)  # 发表时间
    state = db.Column(db.Integer, default=0)  # 是否所有人可见
    img = db.Column(db.String(70))  # 图片

    tags = db.relationship('Categorys', secondary=posts_categorys, backref=db.backref('posts'))

    u_id = db.Column(db.Integer, db.ForeignKey('user.id'))  # 关联主表user的自增id



class Categorys(DB_Base, db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    categorys = db.Column(db.String(20),index=True, unique=True)









