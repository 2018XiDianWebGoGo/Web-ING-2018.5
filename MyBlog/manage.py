# -*- encoding=UTF-8 -*-

from MyBlog import app, db
from flask_script import Manager
from MyBlog.models import User, Blog
import random

manager = Manager(app)


def get_blog_content():  # 生成随机的列表内容，用于测试
    return str(random.randint(0, 100000000))


@manager.command   # 在命令行中执行python manage.py init_database
def init_database():
    db.drop_all()  # 删除数据库中原有的所有表
    db.create_all()  # 根据这个项目中已定义的数据类，在数据库中创建对应的表
    # 测试：创建一个用户
    db.session.add(User('123@123.com', 'sdcxdfrd'))
    db.session.add(Blog(get_blog_content(), get_blog_content(), 1))
    db.session.commit()  # 不能忘记，否则数据库中查不到！
    print 1, User.query.all()  # 查询全部
    print 2, User.query.get(1)  # primary key = 1
    print 3, User.query.get(1).blogs.all()  # 关联查询，打印用户对应的清单
    a = User.query.get(1)
    print 4, a.blogs.all()
    b = Blog.query.get(1)
    print 5, b.user


if __name__ == '__main__':
    manager.run()

