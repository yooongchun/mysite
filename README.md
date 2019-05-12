## Blog
基于Django2搭建的个人博客网站

访问地址：[永春小站](http://www.yooongchun.com)



### 网站特点：

- 基于`Bootstrap4` ，响应式布局
- 卡片式展现，美观易读
- 支持`Markdown` 语法
- 无需注册登录账号，直接留言、评论
- 留言、评论消息邮件通知

### 安装软件

本地部署需要安装`Python3`和`Mysql`数据库。

- 安装`Python3.6`：https://www.python.org/

- 安装`Mysql`数据库：https://www.mysql.com/

- 安装`Python`模块(`pip3`命令)

  必要的模块包括：`pymysql`、`django-mdeditor`、`django`、`jieba`、`qqwry-py3`、`pillow`、`xadmin`

### 下载本站代码项目

- 方式一：直接通过git命令下载（windows下需要安装git软件）：

  ```bash
  $ git clone https://github.com/yooongchun/mysite.git
  ```

- 方式二：直接从github下载：https://github.com/yooongchun/mysite

### 项目简要解释

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
		
	-templates //全局的html模板
	-manage.py //django项目管理程序
	-README.md //项目使用说明
```

我们对网站的修改操作几乎都在blog目录下完成，仅有部分全局设置需要在mysite目录下配置

### 快速使用

安装好相应软件后（python3，mysql及相应python模块），即可通过最简单的配置来使用这个网站：

第一步：创建数据库

```shell
mysql -uroot -p
CREATE DATABASE blog;
```

第二步：在`mysite/mysite/settings.py` 文件中配置数据库

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog', # 这里配置你的数据库名称
        'USER': 'root',# 这里配置你的数据库用户名
        'PASSWORD': '****',# 这里写你的数据库密码
        'HOST': '127.0.0.1',
        'POST': '3306',
    }
}
```

第三步：迁移数据库，打开windows命令行切换到mysite目录

```shell
python3 manage.py makemigrations
python3 manage.py migrate
```

第四步：运行

```shell
python3 manage.py runserver 127.0.0.1:8000
```


### 技术概要

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

### 在服务器上部署Django工程

把`Django` 工程部署到服务器上，使用`nginx`+`uwsgi` 两个工具，参考链接：http://www.cnblogs.com/jhao/p/6071790.html

**安装nginx** 

```shell
sudo apt-get install nginx
```

**安装uwsgi**

```shell
sudo apt-get install uwsgi
```

**安装mdeditor**

```powershell
pip3 install django-mdeditor
```

### 问题及总结

- `Django` 数据库迁移命令？

  ```shell
  python manage.py makemigrations
  python manage.py migrate
  ```

- `Django` 创建超级用户？

  ```shell
  python manage.py createsuperuser
  ```

- `windows` 平台下启动`mysql` 数据库

  以管理员身份运行命令行：

  ```shell
  net start mysql
  ```

- 如何获取`IP`地址对应的城市？

  方案一：淘宝`API`接口【频繁请求或多次请求会返回502错误，不推荐，但可作为测试使用】

  ```python
  # 根据IP地址获取城市名称
  def get_city_of_ip(ip):
      url = r"http://ip.taobao.com/service/getIpInfo.php"
      try:
          res = requests.get(url=url, params={"ip": ip})
          text = res.json()
          return text
      except:
          pass
  ```

  方案二：使用纯真`IP` 库：

  首先安装`Python`包

  ```shell
  pip install qqwry
  ```

  编写`Python` 下载代码

  ```python
  from qqwry import QQwry, updateQQwry
  def fetch_cz_ip_database():
      """每月下载纯真数据库"""
      try:
          updateQQwry('ip_list.dat')
      except:
      	pass
  ```

  编写查询代码：

  ```python
  def get_city_of_ip(ip):
      """根据IP地址获取城市名称"""
      q = QQwry()
      res = q.load_file('ip_list.dat', loadindex=False)
      if res:
          result = q.lookup(ip)
          q.clear()
          return result[0]
  ```

### TO-DO-LIST

接下来考虑添加的功能：

-[ ] 用户账号登录功能

### CHANGE-LOG
更新日志：

[2019.5.11] 

[1] 修改admin后台为xadmin

[2] 修复在特定日期多次下载纯真数据的bug

---

### BUG
目前已知bug：

[1] 后台删除数据库中文章后归档不更新

[2] django-mdeditor.js 渲染后代码无缩进

[3] typora_style.css 渲染后代码框不可变





