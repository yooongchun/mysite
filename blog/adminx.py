# Register your models here.
import xadmin
from xadmin.views import BaseAdminView, CommAdminView

from .models import Category, Blog, Comment, Message, InfoMsg, Visitor, CoverImage, Resource, FriendLink, \
    Collection, CollectionTag, PhotographyImageList, Icon, TagProfile, CommonDataCache, ArchiveFolder


# 主题
class ThemeSetting(object):
    enable_themes = True
    use_bootswatch = True


class CustomView(object):
    site_title = '后台管理'  # 网页头部导航
    site_footer = 'Blog@www.zhayongchun.com'  # 底部版权内容
    menu_style = 'accordion'  # 左侧导航折叠框


class BlogAdmin(object):
    fields = (
        'title', 'author', 'password', 'category', 'tags', 'cover', 'collection', 'collection_tag',
        'render_with_markdown', 'display', 'digest', 'content')
    list_display = ('title', 'author', 'password', 'display', 'category', 'collection', 'collection_tag', 'read_num',
                    'approval_num', 'comment_num', 'pub_date')
    search_fields = ['title', 'digest']
    list_filter = ['category', 'collection', 'collection_tag', 'render_with_markdown']
    list_editable = ['title', 'author', 'password', 'display', 'category', 'collection', 'collection_tag']


class CommentAdmin(object):
    fields = ['display']
    list_display = ('user', 'blog', 'display', 'is_informed', 'pub_date', 'parent', 'content')
    list_editable = ['display']


class MessageAdmin(object):
    fields = ['reply_content']
    list_display = ('user', 'title', 'display', 'is_informed', 'is_replied', 'pub_date', 'content', 'reply_content')
    list_editable = ['display', 'reply_content']


class VisitorAdmin(object):
    exclude = ['ip', 'city', 'coordination', 'times', 'approval_blog_list']
    list_display = ('ip', 'city', 'coordination', 'times')


class CoverImageAdmin(object):
    pass


class ResourceAdmin(object):
    fields = ['user', 'title', 'password', 'category', 'link', 'display', 'cover', 'content']
    list_display = ('user', 'title', 'password', 'category', 'display', 'download_num', 'cover', 'pub_date',)
    list_editable = ['user', 'title', 'password', 'category', 'display', 'cover']


class FriendLinkAdmin(object):
    exclude = ['add_time']
    list_display = ('name', 'url', 'click_num', 'display', 'description', 'add_time')
    list_editable = ['display']


class InfoMsgAdmin(object):
    fields = ['info', 'display']
    list_display = ('info', 'display')
    list_editable = ['info', 'display']


class CollectionAdmin(object):
    fields = ['collection', 'display']
    list_display = ('collection', 'display', 'read_num', 'pub_date')
    list_editable = ['collection', 'display']


class CollectionTagAdmin(object):
    fields = ['collection', 'tag_name', 'tag_id']
    list_display = ('collection', 'tag_name', 'tag_id')
    list_editable = ['collection', 'tag_name', 'tag_id']


class PhotographImageListAdmin(object):
    fields = ['author', 'url', 'collection', 'is_cover', 'display', 'description', 'story']
    list_display = ('author', 'collection', 'is_cover', 'read_num', 'display', 'description', 'story')
    list_editable = ('collection', 'is_cover', 'display', 'description', 'story')


class CategoryAdmin(object):
    list_display = ['category']
    list_editable = ['category']


class TagAdmin(object):
    list_display = ['tag', 'read_num']
    list_editable = ['tag']


class CommonDataCacheAdmin(object):
    list_display = ['total_visit_num', 'total_approval_num', 'total_comment_num', 'total_article_num']
    readonly_fields = ['total_visit_num', 'total_approval_num', 'total_comment_num', 'total_article_num']


class ArchiveFolderAdmin(object):
    list_display = ['archive_name', 'article_num', 'read_num', 'date']
    readonly_fields = ['archive_name', 'article_num', 'read_num', 'date']


xadmin.site.register(BaseAdminView, ThemeSetting)
xadmin.site.register(CommAdminView, CustomView)

xadmin.site.register(Blog, BlogAdmin)
xadmin.site.register(PhotographyImageList, PhotographImageListAdmin)
xadmin.site.register(Collection, CollectionAdmin)
xadmin.site.register(CollectionTag, CollectionTagAdmin)
xadmin.site.register(Resource, ResourceAdmin)

xadmin.site.register(TagProfile, TagAdmin)
xadmin.site.register(Category, CategoryAdmin)
xadmin.site.register(Icon)
xadmin.site.register(CoverImage, CoverImageAdmin)
xadmin.site.register(InfoMsg, InfoMsgAdmin)

xadmin.site.register(Message, MessageAdmin)
xadmin.site.register(Comment, CommentAdmin)
xadmin.site.register(Visitor, VisitorAdmin)

xadmin.site.register(FriendLink, FriendLinkAdmin)
xadmin.site.register(CommonDataCache, CommonDataCacheAdmin)
xadmin.site.register(ArchiveFolder, ArchiveFolderAdmin)
