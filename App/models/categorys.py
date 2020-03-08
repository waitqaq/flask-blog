from App.extensions import db
from .db_base import DB_Base


class Categorys(DB_Base, db.Model):
    __tablename__ = 'categorys'
    id = db.Column(db.Integer, primary_key=True)
    categorys = db.Column(db.String(20),index=True, unique=True)

    posts = db.relationship('Posts', backref='categorys', lazy='dynamic')
