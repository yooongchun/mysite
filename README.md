## Blog

基于Django2搭建的个人博客网站

访问地址：[永春小站](http://www.yooongchun.com)

---

## 网站特点：

- 基于`Bootstrap4` ，响应式布局
- 卡片式展现，美观易读
- 支持`Markdown` 语法
- 用户注册登录账号、留言、评论
- 留言、评论消息邮件通知

---

## 技术概要

完成本站建设，你需要以下技能：

前端：

- `HTML5`
- `Bootstrap4`
- `CSS3`
- `JAVASCRIPT/jQuery` 
- `Django2`

后端：

- `Python3`
- `云服务器部署`

如果以上哪个部分你未掌握，可根据以下推荐酌情学习！

关于前端的学习，我的建议是快速学习一遍这里的教程，了解什么功能用什么方式实现即可：

- 菜鸟教程：[Bootstrap](http://www.runoob.com/bootstrap4/bootstrap4-tutorial.html)
- 菜鸟教程：[Javascript](http://www.runoob.com/js/js-tutorial.html)
- 菜鸟教程：[jQuery](http://www.runoob.com/jquery/jquery-tutorial.html)
- 菜鸟教程：[HTML](http://www.runoob.com/html/html-tutorial.html)
- 菜鸟教程：[CSS](http://www.runoob.com/css/css-tutorial.html)
- `Django`教程：[编写你的第一个Django应用](https://docs.djangoproject.com/zh-hans/2.1/intro/tutorial01/)，看完一至七即可

关于后端，建议学习以下教程：

- `Python3` 学习：[廖雪峰的Python3教程](https://www.liaoxuefeng.com/wiki/0014316089557264a6b348958f449949df42a6d3a2e542c000)
- `云服务器部署`：本文后面会有讲解

---



## 项目简要解释

项目结构如下：

```
mysite
	-blog //保存该项目的所有代码
		-migrations //数据库迁移文件
		-static //静态文件，包括images、js、css等
		-templates //html模板文件
		-adminx.py //xadmin后台
		-apps.py //网站应用注册
		-models.py //数据库model文件
		-tests.py //测试
		-urls.py //路由转发
		-utils.py //功能函数
		-views.py //视图：路由转发
		
	-mysite //保存全局的设置、配置等信息
		-settings.py //配置全局参数
		-urls.py //路由转发终端
		-wsgi.py //wsgi，不用管
	-script
		-log //保存日志
		-mysite //服务器nginx配置文件
		-uwsgi.ini //服务器uwsgi配置文件
		-restart.sh //启动脚本
	-templates //全局的html模板
	-manage.py //django项目管理程序
	-README.md //项目使用说明
```



---

### 服务器部署

#### 第一步：购买云服务器

我买的是阿里云服务器，2cpu 4gb配置。购买之后需要在安全组中开放80端口和22端口。

#### 第二步：配置服务器环境

1.安装python3：检查python3是否已安装：`python3 -V`  

```shell
Python 3.5.2
```

如果没有安装则使用以下命令安装

```shell
apt install python3
```

2.安装pip3：检查pip3是否已安装：`pip3 -V`

```shell
pip 8.1.1 from /usr/lib/python3/dist-packages (python 3.5)
```

如果没有则安装：

```shell
apt install python3-pip
```

3.安装python3依赖包：

```shell
pip3 install pymysql django-mdeditor django jieba qqwry-py3 pillow uwsgi xadmin2
```

4.安装mysql数据库：

```shell
apt install mysql-server
```

安装过程中会提示你设置密码并确认。

5.配置mysql：修改默认用户名

首先进入mysql：

```shell
mysql -uroot -p
```

输入你刚才设定的密码并进入mysql环境。

接下来切换到mysql数据库并修改用户名：

```mysql
USE mysql;
UPDATE user SET user='你的用户名' WHERE user='root';
```

正常的话会出现以下提示：

```mysql
Query OK, 1 row affected (0.00 sec)
Rows matched: 1  Changed: 1  Warnings: 0
```

创建数据库：

```mysql
CREATE DATABASE blog CHARACTER SET utf8;
```

退出mysql环境：

```mysql
quit
```

重启数据库：

```shell
service mysql restart
```

6.安装nginx：

```shell
apt install nginx
```

#### 第三步：下载项目代码

使用git命令从博主的github地址下载：

注意：为了保证后续脚本运行正确，请在`/home` 目录下运行以下命令：

注意：如果找不到`git` 命令则使用以下命令安装：`apt install git`

```shell
git clone -b dev https://github.com/yooongchun/mysite.git
```

此时你下载的项目`mysite`目录为：`/home/mysite`

#### 第四步：配置nginx和uwsgi

切换到`/home/mysite/script/` 打开`mysite`这个配置文件：

```shell
vim mysite
```

编辑这个文件，将域名修改为你的域名地址或者ip地址。注意：我的配置文件中配置了四个域名地址，如果你没有这么多的域名，则删除多余的行了，以下是一个域名对应的配置，只需要修改`server_name`对应的内容：

```shell
server{
    listen 80;
    server_name www.zhayongchun.com;
    location /static/ {
        alias /home/mysite/blog/static/;
    }
    location / {
        include uwsgi_params;
        uwsgi_pass unix:/home/mysite/script/mysite.sock;
    }
}
```

接下来将配置文件`mysite` 拷贝到`/etc/nginx/sites-enabled/`位置：

```shell
# 先切换到目标目录
cd /etc/nginx/sites-enabled/
# 拷贝文件
cp /home/mysite/script/mysite ./
```

然后启动`nginx`服务：

```shell
service nginx start
```

#### 第五步：迁移数据库

先切换到`/home/mysite` 目录

```shell
cd /home/mysite
```

然后迁移数据库：

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

此时会发现出现了一个错误：

```shell
django.core.exceptions.ImproperlyConfigured: mysqlclient 1.3.13 or newer is required; you have 0.9.3.
```

观察报错信息发现这是由于版本限制造成的，为了修复这个问题，首先切换到以下目录：

```shell
cd /usr/local/lib/python3.5/dist-packages/django/db/backends/mysql/
```

然后使用`vim`打开修改`base.py`文件：

```shell
vim base.py
```

只需要将以下两行代码注释即可：

```shell
if version < (1, 3, 13):
    raise ImproperlyConfigured('mysqlclient 1.3.13 or newer is required; you have %s.' % Database.__version__)
```

然后保存退出！

接下来不要切换目录，打开`operations.py`

将以下代码中的`decode`修改为`encode`即可，保存退出。

```shell
if query is not None:
            query = query.decode(errors='replace')
```

完成后迁移数据库：

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

然后收集静态文件：

```shell
python3 manage.py collectstatic
```

此时程序会提示输入`yes`以继续。

创建超级用户（后台管理）：

```shell
python3 manage.py createsuperuser
```



#### 第六步：配置站点信息

首先，配置`mysite/config.py`文件,根据自己的实际情况修改即可

```python
# 配置全局参数
DEBUG_MODE = False  # 调试模式：在本地测试时使用True
# Mysql数据库连接信息
MYSQL_PARAS = {
    'NAME': 'blog',
    'USER': '***',
    'PASSWORD': '***',
    'HOST': '127.0.0.1',
    'PORT': '3306', }
```

接下来，修改`blog/config.py`文件：同样根据提示修改即可，百度AK是用来展示关于页面的地图的，不填则无法请求数据，测试时可以不填写。QQ邮箱KEY是用来自动发邮件通知的，也可以不填；其他信息按需填写

```python
"""
在这里配置参数
包括：
    1.网站参数
    2.依赖项目的参数
    3.密码，个人信息等等
"""

#-------------------以下参数可根据自己情况修改--------------------#
POPULAR_BLOG_NUM = 3  # 最受欢迎文章展示数量
LATEST_BLOG_NUM = 5  # 最新文章展示数量
PAGE_DISPLAY_BLOG_NUM = 10  # 每页展示内容数
PAGE_DISPLAY_MESSAGE_NUM = 10
DOWNLOAD_IP_DATA_DATE = 1  # 每月更新纯真数据库的时间
MAX_PHOTOGRAPH_NUM = 2  # 避免耗时，摄影图片每次传送不超过该值
VISITOR_RANK_LENGTH = 7  # 访客排名展示长度：多余部分前面补0，比如第一位访问的访客：0000001

IP_DATABASE_FILENAME = 'ip_list.dat'  # 纯真ip数据库保存文件名
HOME_PAGE_TITLE = '永春小站-首页'  # 站点标题
SITE_TITLE = '永春小站'
ABOUT_PAGE_TITLE = '关于'
CORPORATION_PAGE_TITLE = '合作'
ESSAY_PAGE_TITLE = '随笔'
RESOURSE_TITLE = '资源'
MESSAGE_PAGE_TITLE = '留言'
FRIEND_LINK_TITLE = '友链申请'
SPONSOR_CATEGORY = '赞助'
SPONSOR_TITLE = '赞助作者'
COLLECTION_TITLE = '专栏'
CATEGORY_PHOTOGRAPH = '摄影'
PHOTOGRAPH_COLLECTION_TITLE = '永春影展'
ARCHIVE_TITLE = '归档'
ARTICLE_PAGE_TITLE = '文章分类'
DETAIL_PAGE_TITLE = '文章详情'
DEFAULT_PHOTOGRAPH_STORY = '正在加载中，请稍后...'

APPROVAL_SUCCESS_RETURN_INFO = '太棒了，你赞了这篇文章~'  # 点赞行为提示信息
APPROVAL_REPEAT_RETURN_INFO = '你已经点过赞啦~'
COMMENT_SUCCESS_RETURN_INFO = '评论成功'  # 评论信息提示
MESSAGE_SUCCESS_RETURN_INFO = '留言成功'  # 留言信息提示
UNKNOWN_RETURN_INFO = '不知道该干嘛~'  # 未知信息提示

LOADING_IMG_URL = "https://yooongchun-photograph.oss-cn-hangzhou.aliyuncs.com/loading2.gif"  # 加载过程动图

#-------------------以下参数不可修改--------------------#
TYPE_FOR_QUERY_MAP_DATA = 'QUERY_FOR_MAP_DATA'  # 关于页面map数据请求标志
TYPE_FOR_APPROVAL = 'APPROVAL'  # 点赞标志
TYPE_FOR_COMMENT = 'COMMENT'  # 评论标志
TYPE_FOR_RESOURCE = 'RESOURCE'  # 资源请求标志
TYPE_FOR_FRIEND_LINK = 'FRIENDLINK'  # 申请友链标志
TYPE_FOR_QUERY_COMMENT_DATA = 'COMMENT_DATA'  # 请求评论数据
TYPE_FOR_MESSAGE = 'MESSAGE'  # 留言标志

BLOG_DEFAULT_PASSWORD = '0'  # 博客默认密码：这些文章默认可以被所有用户访问
RESOURCE_DEFAULT_PASSWORD = '0'  # 资源默认密码
COMMENT_DEFAULT_ID = 0  # 默认父评论id：区别于回复评论的评论，这些评论是父评论


#-------------------以下参数必须修改为自己的信息--------------------#
SUPER_USER = '***'  # 后台账号用户名
WEB_DOMAIN = 'http://www.zhayongchun.com'  # 域名信息
# 百度地图使用授权AK，用于关于页面地图数据的请求，请查阅百度地图API获取授权
BAIDU_AK = '***'
EMAIL_KEY = '***'  # QQ邮箱，用于发送邮件：通知用户或者通知作者，请查阅QQ邮箱使用相关教程获取授权
EMAIL_SEND_ACCOUNT = '***'  # 发送邮件的QQ邮箱账号
EMAIL_RECEIVE_ACCOUNT = EMAIL_SEND_ACCOUNT

# 关于页面作者信息展示
ABOUT_PAGE_AUTHOR_INFO = {'name': '查永春',
                          'description': '这是一名想去看遍世界的技术宅！',
                          'birth_year': '1994',
                          'birth_month': '06',
                          'birth_day': '01',
                          'education_school': '上海交通大学',
                          'education_degree': '学士',
                          'education_start_year': '2014',
                          'education_start_month': '09',
                          'education_finish_year': '2018',
                          'education_finish_month': '06',
                          'education_profession': '能源动力工程',
                          'education_profession_degree': '本科',
                          'education_profession_start_year': '2014',
                          'education_profession_start_month': '09',
                          'education_profession_finish_year': '2018',
                          'education_profession_finish_month': '06'}
# 项目合作信息
PROJECT_COOPARATION_INFO = '承接项目，范围包括但不限于爬虫、Web开发、机器学习、数据建模、UG工程建模、PDF数据批提取等项目，如有意向合作可以加我微信！'

```

#### 第七步：运行启动脚本

```shell
# 切换到script目录
cd /home/mysite/scipt
# 启动
./restart.sh
```

## 本地开发

本地部署需要安装`Python3`和`Mysql`数据库。

- 安装`Python3.6`：https://www.python.org/

- 安装`Mysql`数据库：https://www.mysql.com/

- 安装`Python`模块(`pip3`命令)

  ```shell
  pip3 install pymysql django-mdeditor django jieba qqwry-py3 pillow uwsgi xadmin2
  ```

------

### 下载代码

- 方式一：直接通过git命令下载（windows下需要安装git软件）：

  ```bash
  $ git clone https://github.com/yooongchun/mysite.git
  ```

- 方式二：直接从github下载：https://github.com/yooongchun/mysite



其他过程同服务器部署，只是本地在完成数据库迁移之后不用使用nginx和uwsgi服务，只需要直接使用以下命令启动即可：

```shell
python3 manage.py runserver
```

然后使用浏览器访问`localhost:8000`

---

## TO-DO-LIST

接下来考虑添加的功能：

- 文章推荐功能
- 搜索优化


------

## CHANGE-LOG

更新日志：

[2019.5.11] 

[1] 修改admin后台为xadmin

[2] 修复在特定日期多次下载纯真数据的bug

[2019.6.9]

增加用户登录注册功能



------

### BUG

目前已知bug：

[1] 后台删除数据库中文章后归档不更新

[2] django-mdeditor.js 渲染后代码无缩进

[3] typora_style.css 渲染后代码框不可变



