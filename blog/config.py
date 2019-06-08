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
SUPER_USER = 'yooongchun'  # 后台账号用户名
WEB_DOMAIN = 'http://www.zhayongchun.com'  # 域名信息
# 百度地图使用授权AK，用于关于页面地图数据的请求，请查阅百度地图API获取授权
BAIDU_AK = 'x2ZTlRkWM2FYoQbvGOufPnFK3Fx4vFR1'
EMAIL_KEY = 'meeuskiyxnuxdcfj'  # QQ邮箱，用于发送邮件：通知用户或者通知作者，请查阅QQ邮箱使用相关教程获取授权
EMAIL_SEND_ACCOUNT = 'yooongchun@foxmail.com'  # 发送邮件的QQ邮箱账号
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
