# -*- encoding=UTF-8 -*-

from MyBlog import app, db  # 导入app
from models import Blog, User
from flask import render_template, redirect, request


@app.route('/')  # 首页
def index():
    blogs = Blog.query.order_by(db.desc(Blog.id)).limit(10).all()
    return render_template('index.html', blogs=blogs)