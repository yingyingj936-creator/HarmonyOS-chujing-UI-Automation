from hypium import BY

from pages.base_page import BasePage


class ServiceDetailPage(BasePage):
    """搜索结果中的外部服务详情页。"""

    PAGE_NAME = "ServiceDetailPage"
    ANY_TITLE_XPATH = '//Text[@id="title"]'
    TITLE_XPATH_TEMPLATE = '//Text[@id="title" and @text="{service_name}"]'

    @classmethod
    def title_xpath(cls, service_name: str) -> str:
        return cls.TITLE_XPATH_TEMPLATE.format(
            service_name=service_name,
        )

    def wait_loaded(self, service_name: str | None = None, *, timeout: float = 12):
        """等待三方服务页加载；优先校验指定标题，失败时接受任意服务页标题。"""
        if service_name:
            component = self.driver.wait_for_component(
                BY.xpath(self.title_xpath(service_name)),
                timeout=3,
            )
            if component is not None:
                return component
        return self.wait_xpath(self.ANY_TITLE_XPATH, "三方服务页标题", timeout=timeout)

    def press_system_back(self) -> None:
        """服务页没有页面内返回按钮，使用系统返回键回搜索结果页。"""
        self.driver.press_back()
