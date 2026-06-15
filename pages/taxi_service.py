from pages.base_page import BasePage


class TaxiServicePage(BasePage):
    """首页金刚区打车服务页面对象。"""

    PAGE_NAME = "TaxiServicePage"
    PAGE_TITLE_XPATH = '//Text[@text="打车"]'
    APP_LIST_XPATH = '//List'
    GAODE_APP_XPATH = '//Text[@text="高德打车"]'
    UBER_APP_ROW_XPATH = (
        '//Row[@clickable="true" and ./Column/Text[@text="Uber"]]'
    )
    UBER_PAGE_TITLE_XPATH = '//Text[@id="title" and @text="Uber"]'
    BACK_BUTTON_XPATH = (
        '//Row[./Text[@text="打车"]]/Row[@clickable="true" and ./Image]'
    )

    def tap_uber(self) -> None:
        """点击打车应用列表中的 Uber。"""
        self.tap_xpath(self.UBER_APP_ROW_XPATH, "Uber 打车服务")

    def system_gesture_back(self) -> None:
        """从屏幕右边缘向左侧滑，执行 HarmonyOS 系统返回手势。"""
        self.driver.swipe_to_back(side="RIGHT")

    def tap_back_button(self) -> None:
        """点击打车列表页左上角页面内返回按钮。"""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "打车列表页返回按钮")
