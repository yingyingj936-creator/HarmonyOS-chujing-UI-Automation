from pages.base_page import BasePage


class ScenicServicePage(BasePage):
    """首页金刚区景区门票服务页面对象。"""

    PAGE_NAME = "ScenicServicePage"
    LIST_WEB_XPATH = '//Web'
    FIRST_SCENIC_XPATH = '//*[@text="香港迪士尼乐园"]'
    BACK_BUTTON_XPATH = '//image[@text="back" and @clickable="true"]'

    def tap_back_button(self) -> None:
        """点击景区列表页左上角页面内返回按钮。"""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "景区列表页返回按钮")
