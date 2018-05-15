# -*- encoding=UTF-8 -*-

from MyBlog import app  # 导入app

@app.route('/')  # 首页
def index():
    return 'Hello'