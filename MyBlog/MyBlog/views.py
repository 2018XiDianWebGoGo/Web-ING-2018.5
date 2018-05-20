# -*- encoding=UTF-8 -*-

from MyBlog import app, db  # 导入app
from models import Blog, User
from flask import render_template, redirect, request

@app.route('/')  # 首页
def index():
    return render_template('index.html')