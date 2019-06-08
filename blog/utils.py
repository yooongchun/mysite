import os
import re
import smtplib
import threading
from datetime import datetime
from email.mime.text import MIMEText
from random import choice
import jieba
import requests
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q, Sum
from django.shortcuts import HttpResponse, get_object_or_404
from qqwry import QQwry, updateQQwry

from blog.models import Blog, Category, Comment, InfoMsg, Visitor, User, Icon, Message, FriendLink, Collection, \
    TagProfile, CommonDataCache, ArchiveFolder, CZDataDownloadList


class PARAS:
    """全局参数"""

    def __init__(self):
        self.POPULAR_BLOG_NUM = 3  # 最受欢迎文章展示数量
        self.LATEST_BLOG_NUM = 5  # 最新文章展示数量
        self.TYPE_FOR_QUERY_MAP_DATA = 'QUERY_FOR_MAP_DATA'  # 关于页面map数据请求标志
        self.TYPE_FOR_APPROVAL = 'APPROVAL'  # 点赞标志
        self.TYPE_FOR_COMMENT = 'COMMENT'  # 评论标志
        self.TYPE_FOR_RESOURCE = 'RESOURCE'  # 资源请求标志
        self.TYPE_FOR_FRIEND_LINK = 'FRIENDLINK'  # 申请友链标志
        self.BLOG_DEFAULT_PASSWORD = '0'  # 博客默认密码
        self.RESOURCE_DEFAULT_PASSWORD = '0'  # 资源默认密码
        self.COMMENT_DEFAULT_ID = 0  # 默认父评论id
        self.PAGE_DISPLAY_BLOG_NUM = 10  # 每页展示内容数
        self.PAGE_DISPLAY_MESSAGE_NUM = 10
        self.TYPE_FOR_QUERY_COMMENT_DATA = 'COMMENT_DATA'  # 请求评论数据
        self.DOWNLOAD_IP_DATA_DATE = 11  # 每月更新纯真数据库的时间
        self.MAX_PHOTOGRAPH_NUM = 2  # 避免耗时，摄影图片每次传送不超过该值
        self.LOADING_IMG_URL = "https://yooongchun-photograph.oss-cn-hangzhou.aliyuncs.com/loading2.gif"  # 加载过程动图
        self.TYPE_FOR_MESSAGE = 'MESSAGE'  # 留言标志
        self.HOME_PAGE_TITLE = '永春小站-首页'  # 页面标题
        self.ABOUT_PAGE_TITLE = '关于'
        self.CORPORATION_PAGE_TITLE = '合作'
        self.ESSAY_PAGE_TITLE = '随笔'
        self.MESSAGE_PAGE_TITLE = '留言'
        self.ARTICLE_PAGE_TITLE = '文章分类'
        self.DETAIL_PAGE_TITLE = '文章详情'

        self.IP_DATABASE_FILENAME = 'ip_list.dat'  # 纯真ip数据库保存文件名
        self.BAIDU_AK = '***'  # 百度地图使用授权AK
        self.APPROVAL_SUCCESS_RETURN_INFO = '太棒了，你赞了这篇文章~'  # 点赞行为提示信息
        self.APPROVAL_REPEAT_RETURN_INFO = '你已经点过赞啦~'
        self.COMMENT_SUCCESS_RETURN_INFO = '评论成功'  # 评论信息提示
        self.MESSAGE_SUCCESS_RETURN_INFO = '留言成功'  # 留言信息提示
        self.UNKNOWN_RETURN_INFO = '不知道该干嘛~'  # 未知信息提示

        self.EMAIL_KEY = '****'  # QQ邮箱
        self.EMAIL_SEND_ACCOUNT = '******'
        self.EMAIL_RECEIVE_ACCOUNT = '*****'
        # 关于页面个人信息展示
        self.ABOUT_PAGE_AUTHOR_INFO = {'name': '查永春',
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
        self.VISITOR_RANK_LENGTH = 7  # 访客排名展示长度


def package_article_archive(article_list):
    """文章归档信息"""
    res = dict()
    for article in article_list:
        read_num = article.read_num
        year = article.pub_date.year
        month = article.pub_date.month
        folder = str(year) + '年' + str(month) + '月'
        try:
            res[folder] = (folder, year, month, res[folder]
                           [3] + 1, res[folder][4] + read_num)
        except KeyError:
            res[folder] = (folder, year, month, 1, read_num)
    return list(res.values())


def get_client_ip(request):
    """获取访问用户的IP地址"""
    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


def record_visitor(request):
    """记录访客IP及频次"""
    ip = get_client_ip(request)

    try:
        visitor = Visitor.objects.get(ip=ip)
        visitor.times += 1
        visitor.save()
    except ObjectDoesNotExist:
        city = None
        try:
            city = get_city_of_ip(ip)
        except:
            pass
        if city:
            coordination = get_coordination(city)
            if coordination is None:
                coordination = ''
        else:
            city = ''
            coordination = ''
        Visitor.objects.create(ip=ip, times=1, city=city,
                               coordination=coordination).save()


def record_approval(request):
    """记录点赞"""
    ip = get_client_ip(request)  # 用户IP
    id = request.POST['article-id']
    article = get_object_or_404(Blog, id=id)
    if is_approved(ip, article.id):
        return HttpResponse(PARAS().APPROVAL_REPEAT_RETURN_INFO)
    # 更新文章点赞数
    article.approval_num += 1
    article.save()
    # 更新IP点赞记录
    visitor = Visitor.objects.get(ip=ip)
    visitor.approval_blog_list.add(article)
    visitor.save()
    return HttpResponse(PARAS().APPROVAL_SUCCESS_RETURN_INFO)


def record_message(request):
    """记录用户留言"""
    target = request.POST
    user_name = target['user-name']
    title = target['title']
    is_anonymous = target['is-anonymous']
    content = target['content']
    is_informed = False if target['need-reply'] == 'false' else True
    
    pub_date = datetime.now()
    user = is_user_exist(user_name)
    if is_anonymous and not is_user_exist(user_name):  # 如果匿名用户不存在则创建
        try:
            icon = Icon.objects.get(id=1)
            User.objects.create(username=user_name,
                                email="anonymous@as.com", icon=icon).save()
        except:
            return HttpResponse('创建用户出错~')
    # 创建留言
    user = get_object_or_404(User, username=user_name)
    try:
        Message.objects.create(user=user, title=title, pub_date=pub_date, is_informed=is_informed,
                               content=content).save()
    except:
        return HttpResponse('创建留言出错~')
    try:  # 当有用户留言时给作者发邮件
        threading.Thread(target=send_mail,
                         args=({'text': '标题：' + title + '\n内容：' + content, 'header': '用户[' + user_name + ']给你留言了'
                                }, PARAS().EMAIL_SEND_ACCOUNT, PARAS().EMAIL_KEY,
                               PARAS().EMAIL_RECEIVE_ACCOUNT)).start()
    except:
        pass
    return HttpResponse(PARAS().MESSAGE_SUCCESS_RETURN_INFO)


def record_comment(request, article):
    """记录用户评论"""
    # 添加评论
    target = request.POST
    user_name = target['user-name']
    content = target['content']
    is_informed = False if target['need-reply'] == 'false' else True
    is_anonymous = False if target['is-anonymous'] == 'false' else True
    parent_comment_id = target['parent-comment-id']
    article_id = target['article-id']
    pub_date = datetime.now()
    user = is_user_exist(user_name)
    if is_anonymous and not is_user_exist(user_name):  # 如果匿名用户不存在则创建
        try:
            icon = Icon.objects.get(id=1)
            User.objects.create(username=user_name,
                                email="anonymous@as.com", icon=icon).save()
        except:
            return HttpResponse('创建用户出错~')
    # 创建评论
    user = get_object_or_404(User, username=user_name)
    article = get_object_or_404(Blog, id=article_id)
    try:
        if int(parent_comment_id) == PARAS().COMMENT_DEFAULT_ID:
            Comment.objects.create(user=user, blog=article, content=content, is_informed=is_informed,
                                   pub_date=pub_date).save()
        else:
            parent = get_object_or_404(Comment, id=parent_comment_id)
            Comment.objects.create(user=user, blog=article, content=content, is_informed=is_informed,
                                   pub_date=pub_date, parent=parent).save()
    except:
        return HttpResponse('创建评论出错~')
    try:  # 当有用户评论时给作者发邮件
        if int(parent_comment_id) == PARAS().COMMENT_DEFAULT_ID:
            threading.Thread(target=send_mail, args=({'text': '评论内容：' + content,
                                                      'header': '用户[' + user_name + ']评论了你的文章[' + article.title + ']'
                                                      }, PARAS().EMAIL_SEND_ACCOUNT, PARAS().EMAIL_KEY,
                                                     PARAS().EMAIL_RECEIVE_ACCOUNT)).start()
        elif user_name != 'yooongchun':
            threading.Thread(target=send_mail, args=({'text': '评论内容：' + content,
                                                      'header': '用户[' + user_name + ']回复了' + get_object_or_404(Comment,
                                                                                                               id=parent_comment_id).user.username + '的评论'
                                                      }, PARAS().EMAIL_SEND_ACCOUNT, PARAS().EMAIL_KEY,
                                                     PARAS().EMAIL_RECEIVE_ACCOUNT)).start()
    except:
        pass
    try:  # 是否需给用户回复
        parent = get_object_or_404(Comment, id=parent_comment_id)
        if int(parent_comment_id) != PARAS().COMMENT_DEFAULT_ID:  # 初始评论，不需通知
            if parent.is_informed:  # 用户设定不需通知
                if user_name == 'yooongchun' or user.email == 'yooongchun@foxmail.com':  # 非作者回复，不需通知
                    user_email = parent.user.email
                    threading.Thread(target=send_mail, args=({
                        'text': '作者yooongchun回复了您对文章[' + parent.blog.title + ']的评论' + '\n您说：[' + parent.content + ']\n作者回复您：[' + content + ']\n\n\n这是自动回复，请勿回复此邮件，谢谢！\n更多资讯，可访问:http://www.yooongchun.cn\n祝您生活愉快！',
                        'header': '您在永春小站-文章[' + parent.blog.title + ']下的留言有新的回复啦~'
                    }, PARAS().EMAIL_SEND_ACCOUNT, PARAS().EMAIL_KEY,
                        user_email)).start()
    except:
        pass
    # 更新文章评论数
    article.comment_num += 1
    article.save()
    return HttpResponse(PARAS().COMMENT_SUCCESS_RETURN_INFO)


def record_friend_link(request):
    """申请友链"""
    target = request.POST
    name = target['site-name']
    url = target['url']
    if 'http' not in url:
        url = 'http://' + url
    description = target['description']
    if FriendLink.objects.filter(name=name).count() > 0:
        return '名称已存在，请重新选择或者联系作者更改！'
    try:
        res = requests.get(url=url, timeout=5)
        if res.status_code == 200:
            if FriendLink.objects.filter(url=url).count() > 0:
                return 'URL已存在！如需更改，请联系作者！'
            try:
                FriendLink.objects.create(
                    name=name, url=url, description=description).save()
            except:
                return '添加出错，请检查后重试！'
            try:  # 当有用户申请友情链接时给作者发邮件
                threading.Thread(target=send_mail,
                                 args=({'text': '名称：' + name + '\n链接：' + url, 'header': '新的友链申请:' + name
                                        }, PARAS().EMAIL_SEND_ACCOUNT, PARAS().EMAIL_KEY,
                                       PARAS().EMAIL_RECEIVE_ACCOUNT)).start()
            except:
                pass
            return '添加成功！'
        else:
            return 'URL访问出错,请检查后重试'
    except:
        return 'URL访问出错,请检查后重试！'


def is_approved(ip, id):
    """判断IP是否已点赞"""
    try:
        if Visitor.objects.get(ip=ip).approval_blog_list.get(id=id):
            return True
        else:
            return False
    except ObjectDoesNotExist:
        return False


def is_user_exist(user_name):
    """判断用户是否已存在"""
    try:
        user = User.objects.get(username=user_name)
        return user
    except ObjectDoesNotExist:
        return False


def group_comment(comment_list):
    """评论分组"""
    # 按添加时间排序
    comment_list = sorted(comment_list, key=lambda x: x.pub_date)
    # 挑选组别元素
    group_comment_dict = {}
    for comment in comment_list:
        if not comment.parent:
            group_comment_dict[comment] = []
    for comment in comment_list:
        if comment.parent:
            group_comment_dict[comment.parent].append(comment)
    return group_comment_dict


def get_city_of_ip(ip):
    """根据IP地址获取城市名称"""
    q = QQwry()
    res = q.load_file(PARAS().IP_DATABASE_FILENAME, loadindex=False)
    if res:
        result = q.lookup(ip)
        q.clear()
        return result[0]


def fetch_cz_ip_database():
    """每月下载纯真数据库"""
    try:
        updateQQwry(PARAS().IP_DATABASE_FILENAME)
        try:  # 发邮件通知
            threading.Thread(target=send_mail,
                             args=(
                                 {'text': '下载最新版纯真数据库', 'header': '当前纯真数据库下载完成，一切OK!'}, PARAS(
                                 ).EMAIL_SEND_ACCOUNT,
                                 PARAS().EMAIL_KEY, PARAS().EMAIL_RECEIVE_ACCOUNT)).start()
        except:
            pass
    except Exception as e:
        try:  # 发邮件通知
            threading.Thread(target=send_mail,
                             args=(
                                 {'text': '下载最新版纯真数据库失败', 'header': '当前纯真数据库出错：%s' % e}, PARAS(
                                 ).EMAIL_SEND_ACCOUNT,
                                 PARAS().EMAIL_KEY, PARAS().EMAIL_RECEIVE_ACCOUNT)).start()
        except:
            pass


def get_coordination(city):
    """根据地名获得经纬度信息"""
    url = 'http://api.map.baidu.com/geocoder/v2/'
    ak = PARAS().BAIDU_AK
    try:
        res = requests.get(
            url=url, params={"address": city, "output": "json", "ak": ak}, timeout=5)
        text = res.json()
        return str(text['result']['location']['lng']) + ',' + str(text['result']['location']['lat'])
    except:
        pass


def refresh(request):
    """更新公用数据"""
    category_list = Category.objects.all()  # 分类
    info_list = InfoMsg.objects.filter(display=True)  # 通知信息
    friend_link_list = FriendLink.objects.filter(display=True)  # 所有友情链接
    tag_list = TagProfile.objects.all()  # 标签
    collection_list = Collection.objects.filter(display=True)  # 专题
    archive_folder_list = ArchiveFolder.objects.all()
    icons = Icon.objects.all()  # 头像
    # 访问数据
    if CommonDataCache.objects.all().count() < 1:
        CommonDataCache.objects.create().save()
    common_data_cache = CommonDataCache.objects.all()[0]
    total_visit_num = common_data_cache.total_visit_num
    total_comment_num = common_data_cache.total_comment_num
    total_article_num = common_data_cache.total_article_num
    total_approval_num = common_data_cache.total_approval_num

    # 记录访客数据
    threading.Thread(target=record_visitor, args=(request,)).start()
    # 公用数据
    common_return_dict = {'category_list': category_list,
                          'info_list': info_list,
                          'friend_link_list': friend_link_list,
                          'tag_list': tag_list,
                          'total_visit_num': total_visit_num,
                          'total_comment_num': total_comment_num,
                          'total_article_num': total_article_num,
                          'total_approval_num': total_approval_num,
                          'collection_list': collection_list,
                          'archive_folder_list': archive_folder_list,
                          'default_password': PARAS().BLOG_DEFAULT_PASSWORD,
                          'image_list': [[i % 10 if i != 0 else 1, img] for i, img in enumerate(icons)],
                          'random_image': choice(icons), }
    return common_return_dict


def refresh_map_data():
    """更新关于页面的地图数据"""
    visitor = Visitor.objects.all()
    info = []
    for v in visitor:
        try:
            city = re.split(r'\s', v.city)[-1]
            lng = float(re.split(r',', v.coordination)[0])
            lat = float(re.split(r',', v.coordination)[1])
            if city in str(info):
                continue
            num = visitor.filter(city=v.city).count()
            info.append(
                {'name': city, 'lat': str(lat), 'lng': str(lng), 'num': str(num)})
        except:
            pass
    return HttpResponse(info)


def get_visitor_rank(num):
    """获取访客访问排名"""
    rank = []
    L = PARAS().VISITOR_RANK_LENGTH if len(
        str(num)) < PARAS().VISITOR_RANK_LENGTH else len(str(num))
    for ch in str('{:0>' + str(L) + 'd}').format(num):
        rank.append(int(ch))
    return rank


def search_result(keywords):
    """搜索结果"""
    if len(keywords) < 1:
        return []
    words = jieba.cut_for_search(keywords)
    blog_list = []
    for word in words:
        blog_list += Blog.objects.filter(Q(title__icontains=word) |
                                         Q(digest__icontains=word) |
                                         Q(tags__tag__icontains=word),
                                         Q(display=True))
    return list(set(blog_list))


def send_mail(Content, HostUserName, KEY, ToUserName):
    # 你的邮箱账号
    _user = HostUserName
    # 这里填写邮箱授权码，如何获得QQ邮箱授权码，请百度
    _pwd = KEY
    # 这里是接收方邮箱账号
    _to = ToUserName

    msg = MIMEText(Content['text'])
    msg["Subject"] = Content['header']
    msg["From"] = _user
    msg["To"] = _to

    try:
        s = smtplib.SMTP_SSL("smtp.qq.com", 465)
        s.login(_user, _pwd)
        s.sendmail(_user, _to, msg.as_string())
        s.quit()
    except smtplib.SMTPException as e:
        return e


def send_message_reply():
    """回复用户留言"""
    messages = Message.objects.filter(Q(is_informed=True), Q(is_replied=False))
    messages = [msg for msg in messages if len(msg.reply_content) > 1]
    for msg in messages:
        try:
            msg.is_replied = True
            msg.save()
            user_email = msg.user.email
            threading.Thread(target=send_mail, args=({
                'text': '您' + msg.pub_date.strftime(
                    '%Y年%m月%d日 %H:%M:%S') + '在永春小站的留言：' + msg.content + '\n作者回复：' + msg.reply_content + '\n\n\n这是自动回复，请勿回复此邮件，谢谢！\n更多资讯，可访问:http://yooongchun.cn\n祝您生活愉快！',
                'header': '您在永春小站的留言有新的回复啦~'
            }, PARAS().EMAIL_SEND_ACCOUNT, PARAS().EMAIL_KEY,
                user_email)).start()
        except:
            pass


def update_cache_data():
    """更新缓存数据库表"""
    common_data_cache = CommonDataCache.objects.get(id=1)

    archive_folder_list = ArchiveFolder.objects.all()

    articles = Blog.objects.filter(display=True)

    visit_num = 0
    comment_num = 0
    approval_num = 0

    archive_folder = {}
    for article in articles:
        year = article.pub_date.year
        month = article.pub_date.month
        folder = '{}年{}月'.format(year, month)
        if folder in archive_folder:
            archive_folder[folder].append(article.read_num)
        else:
            archive_folder[folder] = [article.read_num]

        visit_num += article.read_num
        approval_num += article.approval_num
        comment_num += article.comment_num

    common_data_cache.total_article_num = len(articles)
    common_data_cache.total_visit_num = visit_num
    common_data_cache.total_approval_num = approval_num
    common_data_cache.total_comment_num = comment_num
    common_data_cache.save()

    for k, v in archive_folder.items():
        archive = archive_folder_list.filter(archive_name=k)
        if len(archive) > 0:
            archive[0].read_num = sum(v)
            archive[0].article_num = len(v)
            archive[0].save()
        else:
            year = int(re.split(r'[年月]+', k)[0])
            month = int(re.split(r'[年月]+', k)[1])
            ArchiveFolder.objects.create(archive_name=k, date=datetime(year, month, 1), read_num=sum(v),
                                         article_num=len(v)).save()


def update_collection_data():
    """更新专栏阅读数"""
    collection_list = Collection.objects.all()
    for collection in collection_list:
        articles = Blog.objects.filter(collection=collection)
        collection.article_num = articles.count()
        read_num = articles.aggregate(read_num=Sum("read_num"))['read_num']
        if isinstance(read_num, int):
            collection.read_num = read_num
        collection.save()


def update_tag_data():
    """更新标签阅读量"""
    tag_list = TagProfile.objects.all()
    for tag in tag_list:
        read_num = Blog.objects.filter(tags__tag__exact=tag).aggregate(
            read_num=Sum("read_num"))['read_num']
        if isinstance(read_num, int):
            tag.read_num = read_num
            tag.save()


def update():
    threading.Thread(target=update_cache_data).start()  # 更新缓存数据库表
    threading.Thread(target=send_message_reply).start()  # 回复留言数据
    threading.Thread(target=update_collection_data).start()  # 更新专栏阅读数
    threading.Thread(target=update_tag_data).start()  # 更新标签阅读数

    if not os.path.isfile(PARAS().IP_DATABASE_FILENAME):
        threading.Thread(target=fetch_cz_ip_database).start()  # 下载纯真ip数据库

    elif CZDataDownloadList.objects.filter(Q(download_date__year=datetime.now().year),
                                           Q(download_date__month=datetime.now().month)).count() < 1 \
            and datetime.now().day == PARAS().DOWNLOAD_IP_DATA_DATE:
        CZDataDownloadList.objects.create(download_date=datetime.now()).save()
        threading.Thread(target=fetch_cz_ip_database).start()  # 下载纯真ip数据库
