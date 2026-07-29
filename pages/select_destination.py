from pages.base_page import BasePage


class SelectDestinationPage(BasePage):
    """选择旅行目的地页对象。"""

    PAGE_NAME = "SelectDestinationPage"
    PAGE_TITLE_TEXT = "选择旅行目的地"
    BACK_BUTTON_XPATH = '//Row[./Text[@text="选择旅行目的地"]]/Row[./Image]'

    # 热门分类
    HOT_CATEGORY_XPATH = (
        '//SideBarContainer/Column//Column[./Text[@text="热门"]]'
    )
    # 东南亚分类
    SOUTHEAST_ASIA_CATEGORY_XPATH = (
        '//SideBarContainer/Column//Column[./Text[@text="东南亚"]]'
    )
    # 历史分类
    CURRENT_HISTORY_XPATH = (
        '//SideBarContainer/Column//Column[./Text[@text="当前/历史"]]'
    )
    LETTER_G_XPATH = '//AlphabetIndexer//Text[@text="G"]'

    HOT_SECTION_XPATH = '//ListItemGroup/Text[@text="热门"]'
    SOUTHEAST_ASIA_SECTION_XPATH = '//ListItemGroup/Text[@text="泰国"]'
    CURRENT_LOCATION_SECTION_XPATH = (
        '//ListItemGroup/Text[@text="当前/历史"]'
    )

    def choose_destination(self, destination_name: str) -> None:
        """按目的地名称点击对应选项。"""
        try:
            self.tap_text(destination_name, f"目的地选项“{destination_name}”")
        except RuntimeError as error:
            raise AssertionError(str(error)) from error

    def tap_by_xpath(self, xpath: str, action_name: str) -> None:
        """点击指定 xpath 组件。"""
        try:
            self.tap_xpath(xpath, action_name)
        except RuntimeError as error:
            raise AssertionError(str(error)) from error

    def tap_hot_category(self) -> None:
        """点击左侧‘热门’分类。"""
        self.tap_by_xpath(self.HOT_CATEGORY_XPATH, "热门")

    def tap_southeast_asia_category(self) -> None:
        """点击左侧‘东南亚’分类。"""
        self.tap_by_xpath(self.SOUTHEAST_ASIA_CATEGORY_XPATH, "东南亚")

    def tap_first_current_history_entry(self) -> None:
        """点击左侧第一个‘当前/历史’入口。"""
        self.tap_by_xpath(self.CURRENT_HISTORY_XPATH, "当前/历史")

    def tap_letter_g(self) -> None:
        """点击右侧字母导航条‘G’。"""
        self.tap_by_xpath(self.LETTER_G_XPATH, "字母导航 G")

    def tap_back_button(self) -> None:
        """点击页面内左上角返回按钮。"""
        self.tap_by_xpath(self.BACK_BUTTON_XPATH, "页面内返回按钮")
