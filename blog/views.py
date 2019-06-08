import threading
from random import choice
from django.contrib.auth.hashers import make_password
from django.contrib.auth import authenticate
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, HttpResponse
from django.views.generic import View
from blog import config
from blog import utils
from blog.models import User, Blog, Comment, Icon, Visitor, Message, Resource, PhotographyImageList, CommonDataCache


class LoginCheck(View):
    """用户登录验证"""

    def get(self, request):
        return HttpResponse("不知道该干嘛哎~~")

    def post(self, request):
        username = request.POST["user_name"]
        password = request.POST["password"]
        if User.objects.filter(username=username).count() != 1:
            return HttpResponse("user-not-exists")
        user = authenticate(username=username, password=password)
        if user:
            return HttpResponse("200|"+user.icon.url)
        else:
            return HttpResponse("404")


class Register(View):
    """用户注册账号"""

    def get(self, request):
        return HttpResponse(config.UNKNOWN_RETURN_INFO)

    def post(self, request):
        username = request.POST["username"]
        password = request.POST["password"]
        email = request.POST["email"]
        url = request.POST["icon"]
        if User.objects.filter(username=username).count() > 0:
            return HttpResponse("user-exists")
        try:
            icon = Icon.objects.get(url=url)
            User.objects.create_user(
                username=username, password=password, email=email, icon=icon).save()
            return HttpResponse("200")
        except:
            return HttpResponse("create-user-error")


class Index(View):
    """首页显示"""

    def get(self, request):
        utils.update()  # 更新缓存数据
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()

        # 获取特定页面的信息
        article_latest_list = Blog.objects.all().filter(display=True).order_by('-pub_date')[
            :config.LATEST_BLOG_NUM]  # 最新文章
        article_popular_list = Blog.objects.all().filter(display=True).order_by('-read_num')[
            :config.POPULAR_BLOG_NUM]  # 最热门文章
        common_return_dict['article_popular_list'] = article_popular_list
        common_return_dict['article_latest_list'] = article_latest_list
        common_return_dict['title'] = config.HOME_PAGE_TITLE
        return render(request, 'blog/index.html', common_return_dict)


class About(View):
    """关于"""

    def get(self, request):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 页面请求地图显示所需要的数据
        if 'type' in request.GET.keys() and request.GET['type'] == config.TYPE_FOR_QUERY_MAP_DATA:
            MAP_DATA = utils.refresh_map_data()
            return MAP_DATA if MAP_DATA else HttpResponse([])
        ip = utils.get_client_ip(request)
        visitor = get_object_or_404(Visitor, ip=ip)
        common_return_dict['title'] = config.ABOUT_PAGE_TITLE
        common_return_dict.update(config.ABOUT_PAGE_AUTHOR_INFO)
        common_return_dict['visit_rank'] = utils.get_visitor_rank(visitor.id)
        common_return_dict['category'] = config.ABOUT_PAGE_TITLE
        return render(request, 'blog/about.html', common_return_dict)


class Articles(View):
    """博客文章"""

    def get(self, request, name, page):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取页面特定的信息
        tag_list = common_return_dict['tag_list']
        category_list = common_return_dict['category_list']
        tag_name_list = [tag.tag for tag in tag_list]
        category_name_list = [category.category for category in category_list]
        # 分类转发
        if name in category_name_list:
            article_category_list = Blog.objects.filter(
                Q(category__category=name), Q(display=True))
            article_cat_or_tag_list = article_category_list
            type = 'category'
            title = name
        # 标签转发
        elif name in tag_name_list:
            article_tag_list = Blog.objects.filter(
                Q(tags__tag=name), Q(display=True))
            article_cat_or_tag_list = article_tag_list
            type = 'tag'
            title = name
        else:
            article_cat_or_tag_list = []
            type = ''
            title = config.UNKNOWN_RETURN_INFO

        # 筛选页面内容
        num = config.PAGE_DISPLAY_BLOG_NUM
        cur_num = len(article_cat_or_tag_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            article_cat_or_tag_list = article_cat_or_tag_list[start:end]
        common_return_dict['article_cat_or_tag_list'] = article_cat_or_tag_list
        common_return_dict['title'] = title
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = type
        common_return_dict['category'] = name
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [
            i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/article.html', common_return_dict)


class Archive(View):
    """归档"""

    def get(self, request, year, month, page):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取页面特定的信息
        article_archive_list = Blog.objects.filter(Q(display=True), Q(pub_date__year=year),
                                                   Q(pub_date__month=month)).order_by('-pub_date')
        # 筛选页面内容
        num = config.PAGE_DISPLAY_BLOG_NUM
        cur_num = len(article_archive_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            article_archive_list = article_archive_list[start:end]
        common_return_dict['article_archive_list'] = article_archive_list
        common_return_dict['title'] = str(year) + '年' + str(month) + '月'
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'archive'
        common_return_dict['category'] = config.ARCHIVE_TITLE
        common_return_dict['year'] = year
        common_return_dict['month'] = month
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [
            i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/archive.html', common_return_dict)


class MessageInfo(View):
    """留言"""

    def get(self, request, page):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取用户特定的数据
        user_image_list = Icon.objects.all()
        message_list = Message.objects.filter(display=True)
        # 筛选页面内容
        num = config.PAGE_DISPLAY_MESSAGE_NUM
        cur_num = len(message_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            message_list = message_list[start:end]
        common_return_dict['image_list'] = [
            [i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
        common_return_dict['random_image'] = choice(user_image_list)
        common_return_dict['title'] = config.MESSAGE_PAGE_TITLE
        common_return_dict['message_list'] = message_list
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'message'
        common_return_dict['category'] = config.MESSAGE_PAGE_TITLE
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [
            i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/message.html', common_return_dict)

    def post(self, request, page):
        # 用户留言
        if request.POST['type'] == config.TYPE_FOR_MESSAGE:
            response = utils.record_message(request)
            return response


class Search(View):
    """搜索"""

    def get(self, request, page):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取特定页面信息
        keywords = request.GET.get('keywords', '').lower()
        blog_list = utils.search_result(keywords)
        # 筛选页面内容
        num = config.PAGE_DISPLAY_BLOG_NUM
        cur_num = len(blog_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            blog_list = blog_list[start:end]
        common_return_dict['searched_blog_list'] = blog_list
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'search'
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [
            i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/search.html', common_return_dict)


class Detail(View):
    """博客详情页"""

    def get(self, request, pk):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取特定页面信息
        article = get_object_or_404(Blog, id=pk)
        # 加密文章判断密码正确性
        if article.password != config.BLOG_DEFAULT_PASSWORD:
            if not request.GET.get('psd') or request.GET.get('psd') != article.password:
                return render(request, 'blog/wrong_password.html', common_return_dict)
        user_image_list = Icon.objects.all()
        comment_list = Comment.objects.filter(Q(blog=article), Q(display=True))
        group_comment_dict = utils.group_comment(comment_list)
        common_return_dict['article'] = article
        common_return_dict['group_comment_dict'] = group_comment_dict
        common_return_dict['image_list'] = [
            [i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
        common_return_dict['category'] = article.category.category
        common_return_dict['random_image'] = choice(user_image_list)

        # 更新阅读量
        article.read_num += 1
        article.save()

        return render(request, 'blog/detail.html', common_return_dict)


class CommentRecorder(View):
    def get(self, request, pk):
        return HttpResponse(config.UNKNOWN_RETURN_INFO)

    def post(self, request, pk):
        article = get_object_or_404(Blog, id=pk)
        # 记录评论
        if request.POST['type'] == config.TYPE_FOR_COMMENT:
            response = utils.record_comment(request, article)
        else:
            response = HttpResponse(config.UNKNOWN_RETURN_INFO)
        return response


class ResourceInfo(View):
    """资源"""

    def get(self, request, page):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 获取用户特定的数据
        user_image_list = Icon.objects.all()
        resource_list = Resource.objects.filter(display=True)
        # 筛选页面内容
        num = config.PAGE_DISPLAY_MESSAGE_NUM
        cur_num = len(resource_list)
        last_page = 1 if cur_num % num else 0
        if cur_num > num:
            start = (page - 1) * num
            end = page * num if page * num < cur_num else cur_num  # 页面内容
            resource_list = resource_list[start:end]
        common_return_dict['image_list'] = [
            [i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
        common_return_dict['random_image'] = choice(user_image_list)
        common_return_dict['title'] = config.RESOURSE_TITLE
        common_return_dict['resource_list'] = resource_list
        common_return_dict['page'] = page
        common_return_dict['next_page'] = page + 1
        common_return_dict['pre_page'] = page - 1
        common_return_dict['type'] = 'resource'
        common_return_dict['category'] = config.RESOURSE_TITLE
        common_return_dict['page_num'] = int(cur_num / num) + last_page
        common_return_dict['page_list'] = [
            i + 1 for i in range(int(cur_num / num) + last_page)]
        return render(request, 'blog/resource.html', common_return_dict)

    def post(self, request, page):
        # 用户请求资源
        if request.POST['type'] == config.TYPE_FOR_RESOURCE:
            resource_id = int(request.POST['resource-id'])
            resource = get_object_or_404(Resource, id=resource_id)
            resource.download_num += 1  # 更新下载量
            resource.save()
            return HttpResponse(str({'password': resource.password, 'link': resource.link}))


class Approval(View):
    """点赞"""

    def post(self, request):
        if request.POST['type'] == config.TYPE_FOR_APPROVAL:
            response = utils.record_approval(request)
            return response


class ApplyFriendLink(View):
    """申请友情链接"""

    def post(self, request):
        # 获取公用数据
        common_return_dict = utils.refresh(request)

        response = utils.record_friend_link(request)
        common_return_dict['title'] = config.FRIEND_LINK_TITLE
        common_return_dict['result'] = response
        return render(request, 'blog/friend-link.html', common_return_dict)


class Sponsor(View):
    """赞助作者"""

    def get(self, request):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        common_return_dict['title'] = config.SPONSOR_TITLE
        common_return_dict['category'] = config.SPONSOR_CATEGORY
        return render(request, 'blog/sponsor.html', common_return_dict)


class Collection(View):
    """专栏"""

    def get(self, request, name, pk):
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        # 获取公用数据
        common_return_dict = utils.refresh(request)

        common_return_dict['title'] = config.COLLECTION_TITLE+':' + name
        common_return_dict['category'] = config.COLLECTION_TITLE

        article_collection_list = dict()
        article_collection_list_all = Blog.objects.filter(
            Q(collection__collection=name), Q(display=True))

        # 获取专栏文章列表
        for a in article_collection_list_all:
            if a.collection_tag is None:
                if -1 in article_collection_list.keys():
                    article_collection_list[-1].append(a)
                else:
                    article_collection_list[-1] = [a]
            elif a.collection_tag.tag_id in article_collection_list.keys():
                article_collection_list[a.collection_tag.tag_id].append(a)
            else:
                article_collection_list[a.collection_tag.tag_id] = [a]
        article_collection_list = sorted(
            article_collection_list.items(), key=lambda item: item[0])

        if len(article_collection_list) > 0:
            if pk == 0:
                article = article_collection_list[0][1][0]
            else:
                article = get_object_or_404(Blog, id=pk)
            # 加密文章判断密码正确性
            if article.password != config.BLOG_DEFAULT_PASSWORD:
                if not request.GET.get('psd') or request.GET.get('psd') != article.password:
                    return render(request, 'blog/wrong_password.html', common_return_dict)
            user_image_list = Icon.objects.all()
            comment_list = Comment.objects.filter(
                Q(blog=article), Q(display=True))
            group_comment_dict = utils.group_comment(comment_list)

            common_return_dict['article'] = article
            common_return_dict['group_comment_dict'] = group_comment_dict
            common_return_dict['image_list'] = [
                [i % 10 if i != 0 else 1, img] for i, img in enumerate(user_image_list)]
            common_return_dict['category'] = article.category.category
            common_return_dict['random_image'] = choice(user_image_list)

            # 更新阅读量
            article.read_num += 1
            article.save()

            common_data_cache = CommonDataCache.objects.get(id=1)
            common_data_cache.total_visit_num += 1
            common_data_cache.save()

        common_return_dict['article_collection_list'] = article_collection_list
        common_return_dict['collection_name'] = name
        return render(request, 'blog/collect.html', common_return_dict)

    def post(self, request, name, pk):
        article = get_object_or_404(Blog, id=pk)
        # 记录评论
        if request.POST['type'] == config.TYPE_FOR_COMMENT:
            response = utils.record_comment(request, article)
        else:
            response = HttpResponse(config.UNKNOWN_RETURN_INFO)
        return response


class PhotoGraphList(View):
    """摄影列表页"""

    def get(self, request):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        common_return_dict['title'] = config.PHOTOGRAPH_COLLECTION_TITLE
        common_return_dict['category'] = config.CATEGORY_PHOTOGRAPH

        image_list = PhotographyImageList.objects.filter(
            Q(is_cover=True), Q(display=True))
        common_return_dict['img_list'] = image_list
        return render(request, 'blog/photograph.html', common_return_dict)


class PhotoGraphTag(View):
    """摄影详情页"""

    def get(self, request, collection):
        # 获取公用数据
        common_return_dict = utils.refresh(request)
        # 记录访客
        threading.Thread(target=utils.record_visitor, args=(request,)).start()
        common_return_dict['title'] = collection
        img_list = PhotographyImageList.objects.filter(
            Q(collection=collection), Q(display=True))
        for i, _ in enumerate(img_list):
            if i >= config.MAX_PHOTOGRAPH_NUM:
                img_list[i].url = config.LOADING_IMG_URL
                img_list[i].story = config.DEFAULT_PHOTOGRAPH_STORY
        common_return_dict['image_list'] = img_list
        return render(request, 'blog/photograph-display.html', common_return_dict)

    def post(self, request, collection):
        img_id = request.POST['id']
        img = get_object_or_404(PhotographyImageList, id=int(img_id))
        return HttpResponse(img.url + '|' + img.story)
