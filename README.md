## Blog
基于Django2搭建的个人博客网站

访问地址：[永春小站](http://www.yooongchun.com)



### 网站特点：

- 基于`Bootstrap4` ，响应式布局
- 卡片式展现，美观易读
- 支持`Markdown` 语法
- 无需注册登录账号，直接留言、评论
- 留言、评论消息邮件通知

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






