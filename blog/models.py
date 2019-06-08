import os
from datetime import datetime

from django.contrib.auth.models import AbstractUser
from django.db import models


class CoverImage(models.Model):
    """博客封面"""
    url = models.URLField(verbose_name='文章封面', max_length=200, default='')

    class Meta:
        verbose_name = '文章封面'
        verbose_name_plural = verbose_name

    def __str__(self):
        return os.path.basename(self.url)


class Icon(models.Model):
    """用户头像"""
    url = models.URLField(verbose_name="用户头像", max_length=200, unique=True, default='')

    class Meta:
        verbose_name = "用户头像"
        verbose_name_plural = verbose_name

    def __str__(self):
        return os.path.basename(self.url)


class User(AbstractUser):
    """用户信息"""
    icon = models.ForeignKey(Icon, on_delete=models.SET_NULL, verbose_name='用户头像', blank=True, null=True)

    class Meta:
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Category(models.Model):
    """文章分类"""
    category = models.CharField(verbose_name='类别', max_length=10, unique=True, default='')

    class Meta:
        verbose_name = '文章分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.category


class InfoMsg(models.Model):
    """网站通知"""
    info = models.CharField(verbose_name='通知信息', unique=True, default='', max_length=20)
    display = models.BooleanField(verbose_name='是否展示', default=True)

    class Meta:
        verbose_name = '网站通知'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.info


class Collection(models.Model):
    """专栏列表"""
    collection = models.CharField(verbose_name='专栏', unique=True, default='', max_length=20)
    pub_date = models.DateTimeField(verbose_name='时间', default=datetime.now)
    display = models.BooleanField(verbose_name='是否展示', default=True)
    read_num = models.IntegerField(verbose_name='阅读量', default=0)

    class Meta:
        verbose_name = '专栏列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.collection


class CollectionTag(models.Model):
    """专栏标签"""
    collection = models.ForeignKey(Collection, verbose_name='专栏名称', on_delete=models.CASCADE, default='')
    tag_name = models.CharField(verbose_name='专栏标签', default='', max_length=20)
    tag_id = models.IntegerField(verbose_name='标签序号', default=0)

    class Meta:
        verbose_name = '专栏标签'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag_name


class TagProfile(models.Model):
    tag = models.CharField(verbose_name='标签', max_length=20, default='')
    read_num = models.IntegerField(verbose_name='阅读量', default=0)

    class Meta:
        verbose_name = '标签列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.tag


class Blog(models.Model):
    """博客文章"""
    title = models.CharField(verbose_name='标题', max_length=100, default='', unique=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', default='')
    password = models.CharField(verbose_name='密码', max_length=256, default='0')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='类别')
    tags = models.ManyToManyField(TagProfile, verbose_name='标签', default='')
    cover = models.ForeignKey(CoverImage, verbose_name='封面', on_delete=models.SET_NULL, null=True, blank=True)
    collection = models.ForeignKey(Collection, on_delete=models.SET_NULL, verbose_name='专栏', null=True, blank=True)
    collection_tag = models.ForeignKey(CollectionTag, on_delete=models.SET_NULL, verbose_name='专栏标签', null=True,
                                       blank=True)
    render_with_markdown = models.BooleanField(verbose_name='Markdown渲染', default=True)
    digest = models.TextField(verbose_name='摘要', default='', max_length=300)
    content = models.TextField(verbose_name='内容', default='')

    read_num = models.IntegerField(verbose_name='阅读', default=0)
    comment_num = models.IntegerField(verbose_name='评论', default=0)
    approval_num = models.IntegerField(verbose_name='点赞', default=0)
    pub_date = models.DateTimeField(verbose_name='发表时间', default=datetime.now)
    display = models.BooleanField(verbose_name='是否展示', default=True)

    class Meta:
        verbose_name = '文章列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Visitor(models.Model):
    """访客信息"""
    ip = models.CharField(verbose_name='IP地址', max_length=20, unique=True)
    city = models.CharField(verbose_name='城市', default='', max_length=50)
    coordination = models.CharField(verbose_name='经纬度', default='', max_length=50)
    times = models.IntegerField(verbose_name='访问次数', default=0)
    approval_blog_list = models.ManyToManyField(Blog, verbose_name='已赞文章')

    class Meta:
        verbose_name = '访客列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.ip


class Comment(models.Model):
    """博客评论"""
    user = models.ForeignKey(User, verbose_name='评论用户', on_delete=models.CASCADE, default='')
    blog = models.ForeignKey(Blog, verbose_name='评论文章', on_delete=models.CASCADE, default='')
    content = models.TextField(verbose_name='评论内容', default='', max_length=1000)
    pub_date = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    is_informed = models.BooleanField(verbose_name='是否通知', default=True)
    parent = models.ForeignKey('self', verbose_name='父评论', on_delete=models.CASCADE, null=True, blank=True)
    display = models.BooleanField(verbose_name='是否展示', default=True)

    class Meta:
        verbose_name = '评论列表'
        verbose_name_plural = verbose_name

    def __str__(self):
        return str(self.content)


class Message(models.Model):
    """留言"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', default='')
    title = models.CharField(verbose_name='标题', default='', max_length=30)
    content = models.TextField(verbose_name='留言', default='', max_length=1000)
    pub_date = models.DateTimeField(verbose_name='时间', default=datetime.now)
    is_informed = models.BooleanField(verbose_name='是否通知', default=True)
    display = models.BooleanField(verbose_name='是否展示', default=True)
    reply_content = models.TextField(verbose_name='留言回复', default='', max_length=500)
    is_replied = models.BooleanField(verbose_name='是否已通知', default=False)

    class Meta:
        verbose_name = '留言信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Resource(models.Model):
    """资源"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='用户', default='')
    title = models.CharField(verbose_name='标题', default='', max_length=30)
    content = models.TextField(verbose_name='内容', default='', max_length=1000)
    pub_date = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    password = models.CharField(verbose_name='访问密码', default='0', max_length=128)
    category = models.CharField(verbose_name='类别', default='', max_length=20)
    link = models.CharField(verbose_name='链接', default='', max_length=200)
    cover = models.ForeignKey(CoverImage, verbose_name='图片', null=True, blank=True, on_delete=models.SET_NULL)
    display = models.BooleanField(verbose_name='是否展示', default=True)
    download_num = models.IntegerField(verbose_name='下载量', default=0)

    class Meta:
        verbose_name = '资源信息'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class FriendLink(models.Model):
    """友情链接"""
    name = models.CharField(verbose_name='名称', default='', max_length=50)
    url = models.URLField(verbose_name='URL地址', default='', max_length=200)
    description = models.CharField(verbose_name='描述信息', default='', max_length=100)
    add_time = models.DateTimeField(verbose_name='添加时间', default=datetime.now)
    display = models.BooleanField(verbose_name='是否展示', default=True)
    click_num = models.IntegerField(verbose_name='点击次数', default=0)

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class PhotographyImageList(models.Model):
    """摄影图展"""
    url = models.URLField(verbose_name='URL', default='', max_length=200)
    collection = models.CharField(verbose_name='标签', default='', max_length=20)
    description = models.TextField(verbose_name='描述', default='', max_length=200)
    story = models.TextField(verbose_name='图片故事', default='')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='作者', default='')
    is_cover = models.BooleanField(verbose_name='是否为封面', default=False)
    display = models.BooleanField(verbose_name='是否展示', default=True)
    pub_date = models.DateTimeField(verbose_name='日期', default=datetime.now)
    read_num = models.IntegerField(verbose_name='阅读数', default=0)

    class Meta:
        verbose_name = '摄影图展'
        verbose_name_plural = verbose_name

    def __str__(self):
        return os.path.basename(self.url)


class CommonDataCache(models.Model):
    """公用数据缓存:减轻数据库请求压力"""
    total_visit_num = models.IntegerField(verbose_name='总访问量', default=0)
    total_approval_num = models.IntegerField(verbose_name='总点赞数', default=0)
    total_comment_num = models.IntegerField(verbose_name='总评论数', default=0)
    total_article_num = models.IntegerField(verbose_name='总文章数', default=0)

    class Meta:
        verbose_name = '缓存数据'
        verbose_name_plural = verbose_name

    def __str__(self):
        return "缓存数据"


class ArchiveFolder(models.Model):
    """公用数据缓存：文章归档信息"""
    archive_name = models.CharField(verbose_name='归档', default='', max_length=50)
    article_num = models.IntegerField(verbose_name='文章数', default=0)
    date = models.DateTimeField(verbose_name='归档时间', default=datetime.now)
    read_num = models.IntegerField(verbose_name='阅读量', default=0)

    class Meta:
        verbose_name = "文章归档"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.archive_name


class CZDataDownloadList(models.Model):
    """纯真数据库下载标志：年月"""
    download_date = models.DateTimeField(verbose_name="下载时间", default=datetime.now)

    class Meta:
        verbose_name = "下载时间"
        verbose_name_plural = verbose_name

    def __str__(self):
        return "下载时间"
