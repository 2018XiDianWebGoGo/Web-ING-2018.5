# -*- encoding=UTF-8 -*-

from MyBlog import app
from flask_script import Manager

manager = Manager(app)

if __name__ == '__main__':  # 主函数
    manager.run()