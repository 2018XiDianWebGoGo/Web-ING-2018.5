# WeBlog

这是一个清新优美的博客系统。

## 项目用到的技术

- 语言：Python
- IDE：Pycharm
- Web框架：Flask
- 模板引擎：Jinja2
- 数据库连接：SQLAlchemy
- 数据库：MySQL
- 注册登录：Flask-Login
- Web应用服务器：Gunicorn
- HTTP服务器 ：Nginx
- 部分技术细节：
  - MVC，前后端分离
  - Flash Message传递消息
  - Flask-Script在命令行做一些管理操作
  - SQLAlchemy采用了对象关系映射（Object-Relational Mapping, ORM）
  - 密码salt加密

## 项目文件结构

![](https://ws1.sinaimg.cn/large/ea577d5dly1frmcd7jv03j20c20c00tv.jpg)

## 开发环境配置

- Python版本：2.7.12
- 所有依赖包及其版本号：

```
click==6.7
Flask==0.12.2
Flask-Login==0.4.1
Flask-MySQLdb==0.2.0
Flask-Script==2.0.6
Flask-SQLAlchemy==2.3.2
gunicorn==19.7.1
itsdangerous==0.24
Jinja2==2.10
MarkupSafe==1.0
mysqlclient==1.3.12
pkg-resources==0.0.0
SQLAlchemy==1.2.7
Werkzeug==0.14.1
```

## 部署说明

操作系统：Debian 7 32Bit

1. 安装：`apt-get install nginx mysql-server python-dev libmysqlclient-dev git --reinstall` 

2. 配置数据库

3. 安装依赖包：`pip install Flask-Script Flask-SQLAlchemy Flask-Login Flask-MySQLdb`

4. 上传代码

5. 启动服务器：`gunicorn -D -w 3 -b 127.0.0.1:8000 MyBlog:app`

6. 配置Nginx服务器

   ```nginx
   server {
       listen 80;
       server_name www.redarrow.top;
   	rewrite ^(.*) https://$server_name$1 permanent;
     }
   
   server {
       listen 443;
       server_name www.redarrow.top;
   
   	ssl on;
   	ssl_certificate /root/full_chain.pem;
   	ssl_certificate_key /root/private.key;
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
       }
     }
   ```

## WeBlog项目开发过程中遇到的问题及解决方案

1. 配置环境时数据库的连接问题：在windows下配置数据库连接时，出现了错误，无法使用pip安装mysql-python模块和flask-mysql模块。原因是某些依赖的包没有Windows版本。

   解决方案：在网上找到了Windows下的exe安装包MySQL-python-1.2.3.win32-py2.7.exe，暂时解决了问题。但是由于该安装包版本过于陈旧，又没有新版本的安装包，虽然它暂时可以正常使用，但是与新版MySQL的兼容性是未知的。为了保险起见，我们将项目迁移到Ubuntu下，这样就能方便地安装各种模块了。

2. 开发环境安装了很多插件，迁移环境比较麻烦，如何解决？

   解决方案：使用virtualenv用来创建隔离的Python环境。在开发Python应用程序的时候，系统安装的Python只有一个版本。所有第三方的包都会被pip安装到Python的site-packages目录下。如果我们要同时开发多个应用程序，那这些应用程序都会共用一个Python，就是安装在系统的Python。如果应用A需要jinja 2.7，而应用B需要jinja 2.6怎么办？这种情况下，每个应用可能需要各自拥有一套“独立”的Python运行环境。virtualenv就是用来为一个应用创建一套“隔离”的Python运行环境。使用virtualenv可以很方便地迁移环境。

3. 在注册时，如何提示用户“该账户已存在” ？

   解决方案：可以使用JavaScript弹窗，但是这样不够友好。我们觉得最好的方法是直接在页面上显示错误信息。因此我们使用了flash message的方法。当我们登录摸一个网站时，输入用户名和密码，如果密码输入错误，点击确定按钮后经常会出现一条提示密码错误的消息。这个消息就是flash消息，主要用来提示用户当前操作的结果。

4. 如何合理地操作数据库，预防SQL注入？

   解决方案：WeBlog项目使用类似Hibernate的数据映射模型的对象关系映射（ORM）工具——SQLAlchemy。在代码中，我们没有使用原生的SQL语句，而是使用ORM库来实现数据库的增删改查。ORM库是防SQL注入的好手。 当SQLAlchemy接收到字符串进行查询时，在构造SQL语句的时候，会默认使用单引号包裹字符串，如果字符串内含有单引号的话，会使用\进行转义，从而达到过滤单引号的效果。正确地使用SQLAlchemy，使本项目出现SQL注入的情况基本不会出现，因为ORM已经做好了大量的防御措施。

5. 如何处理一对多的关系的相互访问，从而通过Blog查找对应的User的同时，又能通过User查找对应的全部Blog？

   解决方案：User表和Blog表的一对多的关系通过下面语句确定：

   ```python
   blogs = db.relationship('Blog', backref='user', lazy='dynamic')  # 关联表，User对象可以通过.blogs查询它的所有Blog，加上backref='user'表示允许Blog通过.user来查询对应的User
   ```

   其中relationship描述了User和Blog的关系。

   在此语句中，第一个参数为对应参照的类"Blog"；

   第二个参数backref为类Blog声明新属性的方法；

   第三个参数lazy决定了什么时候SQLALchemy从数据库中加载数据。

6. 在已实现纯文本博客发布的前提下，如何使博客支持富文本编辑？

   解决方案：我们选择了使用简单、功能强大的富文本编辑器CKeditor。

   在Flask项目中使用CKeditor只需要执行两步就可以了：

   1. 在`<script>`标签引入CKeditor主脚本文件。可以引入本地的文件，也可以引用CDN上的文件。
   2. 使用`CKEDITOR.replace()`把现存的`<textarea>`标签替换成CKEditor。

7. 如何确保输入不为空？

   解决方案：判断输入为空的方式有很多，我们为了安全，在前端和后端均判断了输入是否为空。前端使用HTML5的`required="required"`语句，后端也对字符串判断是否为空。

8. 如何判断注册页面输入的“密码”和“确认密码”一致？

   解决方案：可以使用表单验证的插件来实现，也可以在前端使用JavaScript实现。为了提高速度，我们在前端实现。

   ```javascript
   function formCheck() {  
       var password = document.getElementById("inputPassword").value;  
       var repassword = document.getElementById("inputPassword2").value;  
            if(password!=repassword){  
                window.alert("两次输入的密码不一致");  
                reg.password2.focus();  
                return false;  
                }  
             return true;  
       }
   ```

9. 如何确保密码存储的安全？

   解决方案：明文存储密码是不可取的，我们的项目对密码使用了带salt的md5加密。

   md5加密算法是不可逆的，也就是说是不能够通过解码来获取源来的字符串的。如果需要验证密码是否正确，需要对待验证的密码进行同样的md5加密，然后和数据库中存放的加密后的结果进行对比。

   普通的md5加密不够安全，我们通过使用salt对字符串进行加密。

   具体的做法是：我们随机生成salt，然后和我们要加密的字符串进行拼接，之后再用md5进行加密，然后在拼接上我们刚刚的salt。

10. 如何处理用户登录会话和权限问题？

    解决方案：用户登录是个非常复杂的问题，花费了我们大量时间。我们的Flask项目使用session来进行基本的登录授权验证，并使用Flask-Login来进行会话管理，来处理我们的“登入、登出”问题。

11. 在文章中输入中文后提交会报错，输入英文正常，如何解决？

    解决方案：我们查阅资料后发现，MySQL需要指定字符集来存储中文，因此我们需要在数据模型中加入以下语句：

    ```python
    __table_args__ = {'mysql_collate': 'utf8_general_ci'}
    ```

12. 部分页面显示乱码，如何解决？

    解决方案：是因为几个HTML页面的编码没有统一，可以在view中加入以下语句：

    ```python
        if sys.getdefaultencoding() != 'utf-8':
            reload(sys)
            sys.setdefaultencoding('utf-8')
    ```

13. 在首页如何显示每篇文章的摘要？

    解决方案：先将HTML标签去除，再截取一定长度的字符串。

14. 如何为文章自动配图？

    解决方案：如果让用户自己上传图片，可能会影响页面的美观，因为用户上传的图片风格迥异。所以我们在后台准备了一个巨大的图片库，当用户发布文章时，后台会随机选择一张图片作为该文章的封面图片，既简化了用户的使用流程，又使网站更加和谐统一。

15. 服务器的响应慢、负载大如何解决？

    解决方案：我们使用Gunicorn作为Web应用服务器，不过Gunicorn的静态文件处理能力差，而且不能很好地支持多线程。因此我们使用了Nginx作为反向代理服务器负责负载均衡。Gunicorn、nginx和flask的关系如下：对于动态内容，也就是根据数据库动态生成的网页，Nginx会在本地请求127.0.0.1:8000，Gunicorn一直在监听127.0.0.1:8000，收到请求后会通知Flask，由Flask生成具体的内容。所以，在这个过程中，Nginx、Gunicorn和Flask都是必不可少的。

16. 如何进一步加快网站的访问速度？

    解决方案：我们的项目使用了jQuery和CKEditor，这两个文件原本是从本地加载的。由于这两个文件较大，加载需要耗费很长的时间，网站打开的速度会变慢。我们改用CDN来加快加载速度。现在有很多的免费前端静态资源库，例如75CDN，我们可以很方便地使用。

17. 使用Chrome访问部署好的网站时，在登录和注册的页面会提示“不安全”，如何解决？

    解决方案：出现这种情况的原因是，在2017年1月，Google发布了Chrome 56正式版本，首次向http网页发出不安全的警示，在地址栏左侧给予一个“感叹号”的标记。凡是对支付账号或密码信息的表单录入的http页面，Chrome会将页面标记为“不安全”。

    因此，我们对网站进行了加密。WeBlog采用全站HTTPS加密，无论是引用的外部CDN资源还是本地服务器都采用了SSL加密机制。我们申请了TrustAsia TLS ECC CA颁发的证书，并添加到了Nginx上。

    全站HTTPS更安全，HTTPS主要通过在SSL上传输数据来区分HTTP，确保传输的数据在传输过程中被加密，只有相应站点服务器或用户浏览器接收时才能被解密，HTTPS通过这种方式避免了第三方拦截。同时，HTTPS提供可信的服务器认证，这是一套黑客不能随意篡改的认证信息，使相关用户确定他们正与正确的服务器通信。

18. Nginx改为监听443端口后，原有的http开头的页面无法访问。解决方案：新添加一个server，监听80端口，将http链接重写为https开头，从而确保用户访问http链接时会自动跳转到https链接。

    ```nginx
       server {
           listen 80;
           server_name www.redarrow.top;
       	rewrite ^(.*) https://$server_name$1 permanent;
         }
    ```


19. 使用https后，部分页面的小锁出现感叹号。

    解决方案：浏览器提示“您与[www.redarrow.top](https://www.redarrow.top)之间的连接采用新型加密套件进行了加密。而且，此页中包含其他不安全的资源。他人能在这些资源传输过程中进行查看，攻击者也可以修改这些资源，从而改变此页的外观。”原因是某些页面使用的CDN链接是http开头的，而不是https开头的，改为https开头，使该问题解决。