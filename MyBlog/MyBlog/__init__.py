# -*- encoding=UTF-8 -*-

from flask import Flask  # 导入flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


app = Flask(__name__)  # 建立app
app.config.from_pyfile('app.conf')  # 导入配置文件，初始化app
app.secret_key = '123'
db = SQLAlchemy(app)  # 建立数据库
login_manager = LoginManager(app)
login_manager.login_view = '/login/'  # 未登录则跳转到登录页

from MyBlog import views, models  # 导出views, models
