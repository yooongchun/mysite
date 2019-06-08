# Generated by Django 2.2.1 on 2019-06-06 21:44

import datetime
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0011_update_proxy_permissions'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name': '用户信息',
                'verbose_name_plural': '用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ArchiveFolder',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('archive_name', models.CharField(default='', max_length=50, verbose_name='归档')),
                ('article_num', models.IntegerField(default=0, verbose_name='文章数')),
                ('date', models.DateTimeField(default=datetime.datetime.now, verbose_name='归档时间')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读量')),
            ],
            options={
                'verbose_name': '文章归档',
                'verbose_name_plural': '文章归档',
            },
        ),
        migrations.CreateModel(
            name='Blog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=100, unique=True, verbose_name='标题')),
                ('password', models.CharField(default='0', max_length=256, verbose_name='密码')),
                ('render_with_markdown', models.BooleanField(default=True, verbose_name='Markdown渲染')),
                ('digest', models.TextField(default='', max_length=300, verbose_name='摘要')),
                ('content', models.TextField(default='', verbose_name='内容')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读')),
                ('comment_num', models.IntegerField(default=0, verbose_name='评论')),
                ('approval_num', models.IntegerField(default=0, verbose_name='点赞')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='发表时间')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '文章列表',
                'verbose_name_plural': '文章列表',
            },
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(default='', max_length=10, unique=True, verbose_name='类别')),
            ],
            options={
                'verbose_name': '文章分类',
                'verbose_name_plural': '文章分类',
            },
        ),
        migrations.CreateModel(
            name='Collection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('collection', models.CharField(default='', max_length=20, unique=True, verbose_name='专栏')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='时间')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读量')),
            ],
            options={
                'verbose_name': '专栏列表',
                'verbose_name_plural': '专栏列表',
            },
        ),
        migrations.CreateModel(
            name='CommonDataCache',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('total_visit_num', models.IntegerField(default=0, verbose_name='总访问量')),
                ('total_approval_num', models.IntegerField(default=0, verbose_name='总点赞数')),
                ('total_comment_num', models.IntegerField(default=0, verbose_name='总评论数')),
                ('total_article_num', models.IntegerField(default=0, verbose_name='总文章数')),
            ],
            options={
                'verbose_name': '缓存数据',
                'verbose_name_plural': '缓存数据',
            },
        ),
        migrations.CreateModel(
            name='CoverImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(default='', verbose_name='文章封面')),
            ],
            options={
                'verbose_name': '文章封面',
                'verbose_name_plural': '文章封面',
            },
        ),
        migrations.CreateModel(
            name='CZDataDownloadList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('download_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='下载时间')),
            ],
            options={
                'verbose_name': '下载时间',
                'verbose_name_plural': '下载时间',
            },
        ),
        migrations.CreateModel(
            name='FriendLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=50, verbose_name='名称')),
                ('url', models.URLField(default='', verbose_name='URL地址')),
                ('description', models.CharField(default='', max_length=100, verbose_name='描述信息')),
                ('add_time', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
                ('click_num', models.IntegerField(default=0, verbose_name='点击次数')),
            ],
            options={
                'verbose_name': '友情链接',
                'verbose_name_plural': '友情链接',
            },
        ),
        migrations.CreateModel(
            name='Icon',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(default='', unique=True, verbose_name='用户头像')),
            ],
            options={
                'verbose_name': '用户头像',
                'verbose_name_plural': '用户头像',
            },
        ),
        migrations.CreateModel(
            name='InfoMsg',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('info', models.CharField(default='', max_length=20, unique=True, verbose_name='通知信息')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
            ],
            options={
                'verbose_name': '网站通知',
                'verbose_name_plural': '网站通知',
            },
        ),
        migrations.CreateModel(
            name='TagProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag', models.CharField(default='', max_length=20, verbose_name='标签')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读量')),
            ],
            options={
                'verbose_name': '标签列表',
                'verbose_name_plural': '标签列表',
            },
        ),
        migrations.CreateModel(
            name='Visitor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ip', models.CharField(max_length=20, unique=True, verbose_name='IP地址')),
                ('city', models.CharField(default='', max_length=50, verbose_name='城市')),
                ('coordination', models.CharField(default='', max_length=50, verbose_name='经纬度')),
                ('times', models.IntegerField(default=0, verbose_name='访问次数')),
                ('approval_blog_list', models.ManyToManyField(to='blog.Blog', verbose_name='已赞文章')),
            ],
            options={
                'verbose_name': '访客列表',
                'verbose_name_plural': '访客列表',
            },
        ),
        migrations.CreateModel(
            name='Resource',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=30, verbose_name='标题')),
                ('content', models.TextField(default='', max_length=1000, verbose_name='内容')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('password', models.CharField(default='0', max_length=128, verbose_name='访问密码')),
                ('category', models.CharField(default='', max_length=20, verbose_name='类别')),
                ('link', models.CharField(default='', max_length=200, verbose_name='链接')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
                ('download_num', models.IntegerField(default=0, verbose_name='下载量')),
                ('cover', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.CoverImage', verbose_name='图片')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '资源信息',
                'verbose_name_plural': '资源信息',
            },
        ),
        migrations.CreateModel(
            name='PhotographyImageList',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.URLField(default='', verbose_name='URL')),
                ('collection', models.CharField(default='', max_length=20, verbose_name='标签')),
                ('description', models.TextField(default='', max_length=200, verbose_name='描述')),
                ('story', models.TextField(default='', verbose_name='图片故事')),
                ('is_cover', models.BooleanField(default=False, verbose_name='是否为封面')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='日期')),
                ('read_num', models.IntegerField(default=0, verbose_name='阅读数')),
                ('author', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='作者')),
            ],
            options={
                'verbose_name': '摄影图展',
                'verbose_name_plural': '摄影图展',
            },
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(default='', max_length=30, verbose_name='标题')),
                ('content', models.TextField(default='', max_length=1000, verbose_name='留言')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='时间')),
                ('is_informed', models.BooleanField(default=True, verbose_name='是否通知')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
                ('reply_content', models.TextField(default='', max_length=500, verbose_name='留言回复')),
                ('is_replied', models.BooleanField(default=False, verbose_name='是否已通知')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='用户')),
            ],
            options={
                'verbose_name': '留言信息',
                'verbose_name_plural': '留言信息',
            },
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField(default='', max_length=1000, verbose_name='评论内容')),
                ('pub_date', models.DateTimeField(default=datetime.datetime.now, verbose_name='添加时间')),
                ('is_informed', models.BooleanField(default=True, verbose_name='是否通知')),
                ('display', models.BooleanField(default=True, verbose_name='是否展示')),
                ('blog', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.Blog', verbose_name='评论文章')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.Comment', verbose_name='父评论')),
                ('user', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='评论用户')),
            ],
            options={
                'verbose_name': '评论列表',
                'verbose_name_plural': '评论列表',
            },
        ),
        migrations.CreateModel(
            name='CollectionTag',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tag_name', models.CharField(default='', max_length=20, verbose_name='专栏标签')),
                ('tag_id', models.IntegerField(default=0, verbose_name='标签序号')),
                ('collection', models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='blog.Collection', verbose_name='专栏名称')),
            ],
            options={
                'verbose_name': '专栏标签',
                'verbose_name_plural': '专栏标签',
            },
        ),
        migrations.AddField(
            model_name='blog',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Category', verbose_name='类别'),
        ),
        migrations.AddField(
            model_name='blog',
            name='collection',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Collection', verbose_name='专栏'),
        ),
        migrations.AddField(
            model_name='blog',
            name='collection_tag',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.CollectionTag', verbose_name='专栏标签'),
        ),
        migrations.AddField(
            model_name='blog',
            name='cover',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.CoverImage', verbose_name='封面'),
        ),
        migrations.AddField(
            model_name='blog',
            name='tags',
            field=models.ManyToManyField(default='', to='blog.TagProfile', verbose_name='标签'),
        ),
        migrations.AddField(
            model_name='user',
            name='icon',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='blog.Icon', verbose_name='用户头像'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]