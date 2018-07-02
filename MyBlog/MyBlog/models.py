# -*- encoding=UTF-8 -*-

from MyBlog import db, login_manager
from datetime import datetime


class Blog(db.Model):
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
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
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  # 数据库中的一列，整数类型，主键，自增长
    username = db.Column(db.String(80), unique=True)
    nickname = db.Column(db.String(80))
    password = db.Column(db.String(80))
    salt = db.Column(db.String(32))  # 盐
    blogs = db.relationship('Blog', backref='user', lazy='dynamic')  # 关联表，User对象可以通过.blogs查询它的所有Blog，加上backref='user'表示允许Blog通过.user来查询对应的User

    def __init__(self, username, nickname, password, salt=''):  # 此处的self，是个对象（Object），是当前类的实例
        self.username = username
        self.nickname = nickname
        self.password = password
        self.salt = salt
        # id是自动生成的

    def __repr__(self):  # 返回一个可以用来表示对象的可打印字符串
        return '<User %d %s %s>' % (self.id, self.username, self.nickname)

    # Flask Login接口
    def is_authenticated(self):
        print 'is_authenticated'
        return True

    def is_active(self):
        print 'is_active'
        return True

    def is_anonymous(self):
        print 'is_anonymous'
        return False

    def get_id(self):
        print 'get_id'
        return self.id


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


class Comment(db.Model):  # 第三张表：评论
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(1024))
    blog_id = db.Column(db.Integer, db.ForeignKey('blog.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    status = db.Column(db.Integer, default=0) # 0 正常 1 被删除
    user = db.relationship('User')  # 关联表

    def __init__(self, content, blog_id, user_id):
        self.content = content
        self.blog_id = blog_id
        self.user_id = user_id

    def __repr__(self):
        return '<Comment %d %s>' % (self.id, self.content)
