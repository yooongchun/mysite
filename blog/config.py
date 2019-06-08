"""
在这里配置参数
包括：
    1.网站参数
    2.依赖项目的参数
    3.密码，个人信息等等
"""


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

