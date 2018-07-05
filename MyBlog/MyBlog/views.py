# -*- encoding=UTF-8 -*-

from MyBlog import app, db  # 导入app
from models import Blog, User
from flask import render_template, redirect, request, flash, get_flashed_messages
import hashlib
import random
import re
import sys
from flask_login import login_user, logout_user, current_user, login_required


@app.route('/')  # 首页
def index():
    blogs_three = Blog.query.order_by(Blog.id).limit(3).all()
    blogs = Blog.query.order_by(db.desc(Blog.id)).limit(10).all()
    return render_template('index.html', blogs_three=blogs_three, blogs=blogs)


@app.route('/profile')
@login_required
def profile():
    blogs = Blog.query.filter_by(user_id=current_user.id).all()
    return render_template('profile.html', blogs=blogs)


@app.route('/profile/<int:user_id>/')
def otherProfile(user_id):
    user = User.query.get(user_id)
    if user == None:
        return redirect('/')
    blogs = Blog.query.filter_by(user_id=user_id).order_by(db.desc(Blog.id)).all()
    return render_template('otherProfile.html', user=user, blogs=blogs)


@app.route('/article/<int:blog_id>/')
def article(blog_id):
    blog = Blog.query.get(blog_id)
    if blog == None:
        return redirect('/')
    return render_template('pageDetail.html', blog=blog)


@app.route('/add')
@login_required
def add():
    return render_template('add.html')


@app.route('/addblog/', methods={'get', 'post'})
@login_required
def addblog():
    if sys.getdefaultencoding() != 'utf-8':
        reload(sys)
        sys.setdefaultencoding('utf-8')
    title = request.values.get('articlename')
    content = request.values.get('editor1')
    dr = re.compile(r'<[^>]+>', re.S)
    dd = dr.sub('', content)
    content_outline = dd[0:135] + '……'
    user_id = current_user.id
    blog = Blog(title, content, content_outline, user_id)
    db.session.add(blog)
    db.session.commit()
    return redirect('/profile')


@app.route('/login/')
def login():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['log']):
        msg = msg + m
    return render_template('login.html', msg=msg)


@app.route('/register/')
def register():
    msg = ''
    for m in get_flashed_messages(with_categories=False, category_filter=['reg']):
        msg = msg + m
    return render_template('register.html', msg=msg)


def redirect_with_msg(target, msg, category):
    if msg != None:
        flash(msg, category=category)
    return redirect(target)


@app.route('/log/', methods={'get', 'post'})
def log():
    username = request.values.get('account').strip()
    password = request.values.get('password').strip()
    # 校验
    if username == '' or password == '':
        return redirect_with_msg('/login', u'用户名和密码不能为空', 'log')

    user = User.query.filter_by(username=username).first()
    if user == None:
        return redirect_with_msg('/login', u'用户名不存在', 'log')

    m = hashlib.md5()
    m.update(password + user.salt)
    if m.hexdigest() != user.password:
        return redirect_with_msg('/login', u'密码错误', 'log')

    login_user(user)

    return redirect('/profile')


@app.route('/reg/', methods={'get', 'post'})
def reg():
    username = request.values.get('account').strip()  # strip() 方法用于移除字符串头尾指定的字符(默认为空格)
    nickname = request.values.get('nickname').strip()
    password = request.values.get('password').strip()

    user = User.query.filter_by(username=username).first()
    if username == '' or password == '':
        return redirect_with_msg('/register', u'邮箱和密码不能为空', 'reg')
    if user != None:
        return redirect_with_msg('/register', u'该用户已存在', 'reg')

    salt = ''.join(random.sample('0123456789abcdefghigklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ', 10))
    m = hashlib.md5()
    m.update(password+salt)
    password = m.hexdigest()
    user = User(username, nickname, password, salt)
    db.session.add(user)
    db.session.commit()

    login_user(user)

    return redirect('/profile')


@app.route('/logout')
def logout():
    logout_user()
    return redirect('/')