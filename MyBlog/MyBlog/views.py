# -*- encoding=UTF-8 -*-

from MyBlog import app, db  # 导入app
from models import Blog, User
from flask import render_template, redirect, request


@app.route('/')  # 首页
def index():
    blogs = Blog.query.order_by(db.desc(Blog.id)).limit(10).all()
    return render_template('index.html', blogs=blogs)


@app.route('/profile')
def profile():
    blogs = Blog.query.order_by(db.desc(Blog.id)).all()
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
def add():
    return render_template('add.html')