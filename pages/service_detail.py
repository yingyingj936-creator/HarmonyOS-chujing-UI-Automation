from pages.base_page import BasePage


class ServiceDetailPage(BasePage):
    """搜索结果中的外部服务详情页。"""

    PAGE_NAME = "ServiceDetailPage"
    TITLE_XPATH_TEMPLATE = '//Text[@id="title" and @text="{service_name}"]'

    @classmethod
    def title_xpath(cls, service_name: str) -> str:
        return cls.TITLE_XPATH_TEMPLATE.format(
            service_name=service_name,
        )

    def press_system_back(self) -> None:
        """服务页没有页面内返回按钮，使用系统返回键回搜索结果页。"""
        self.driver.press_back()
