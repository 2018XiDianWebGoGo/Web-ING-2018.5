# -*- encoding=UTF-8 -*-

from flask import Flask  # 导入flask


app = Flask(__name__)  # 建立app
app.config.from_pyfile('app.conf')  # 导入配置文件，初始化app

from MyBlog import views, models  # 导出views, models
