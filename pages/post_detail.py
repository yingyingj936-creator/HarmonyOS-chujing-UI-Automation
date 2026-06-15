from pages.base_page import BasePage


class PostDetailPage(BasePage):
    """出境服务帖子详情页面对象。"""

    PAGE_NAME = "PostDetailPage"
    CONTENT_LIST_XPATH = '//List[@scrollable="true"]'
