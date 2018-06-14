# -*- encoding=UTF-8 -*-

from MyBlog import db
from datetime import datetime


class Blog(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 数据库中的一列，整数类型，主键，自增长
    title = db.Column(db.String(160))
    content = db.Column(db.Text)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    created_date = db.Column(db.DateTime)
    status = db.Column(db.Integer, default=0)  # 0 正常 1删除

    def __init__(self, title, content, user_id):
        self.title = title
        self.content = content
        self.user_id = user_id
        self.created_date = datetime.now()  # 现在的时间
        # id是自动生成的

    def __repr__(self):  # 返回一个可以用来表示对象的可打印字符串
        return '<Blog %d %s %s>' % (self.id, self.title, self.content)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 数据库中的一列，整数类型，主键，自增长
    username = db.Column(db.String(80), unique=True)
    password = db.Column(db.String(30), unique=True)
    blogs = db.relationship('Blog', backref='user', lazy='dynamic')  # 关联表，User对象可以通过.blogs查询它的所有Blog，加上backref='user'表示允许Blog通过.user来查询对应的User

    def __init__(self, username, password):  # 此处的self，是个对象（Object），是当前类的实例
        self.username = username
        self.password = password
        # id是自动生成的

    def __repr__(self):  # 返回一个可以用来表示对象的可打印字符串
        return '<User %d %s>' % (self.id, self.username)