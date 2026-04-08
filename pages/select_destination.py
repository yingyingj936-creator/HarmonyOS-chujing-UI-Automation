from typing import Any

from hypium import BY


class SelectDestinationPage:
    """选择旅行目的地页对象。"""

    PAGE_TITLE_TEXT = "选择旅行目的地"
    HOT_CATEGORY_XPATH = (
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Column[1]/Column[3]'
    )
    HK_MACAO_CATEGORY_XPATH = (
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Column[1]/Column[4]'
    )
    CURRENT_HISTORY_XPATH = (
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Column[1]/Column[2]'
    )

    HOT_SECTION_XPATH = '//*[@text="热门"]'
    HK_MACAO_SECTION_XPATH = '//*[@text="港澳"]'
    CURRENT_LOCATION_SECTION_XPATH = (
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Row[1]/List[1]/ListItemGroup[1]/Grid[1]/GridItem[1]/Row[1]/Image[1]'
    )

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def _find_by_text(self, text: str):
        """按文本查找组件。"""
        return self.driver.find_component(BY.text(text))

    def _find_by_xpath(self, xpath: str):
        """按 xpath 查找组件。"""
        return self.driver.find_component(BY.xpath(xpath))

    def is_loaded(self) -> bool:
        """判断‘选择旅行目的地’页面是否加载成功。"""
        return self._find_by_text(self.PAGE_TITLE_TEXT) is not None

    def choose_destination(self, destination_name: str) -> None:
        """按目的地名称点击对应选项。"""
        destination_component = self._find_by_text(destination_name)
        if destination_component is None:
            raise AssertionError(f"未找到目的地选项：{destination_name}")
        destination_component.click()

    def tap_by_xpath(self, xpath: str, action_name: str) -> None:
        """点击指定 xpath 组件。"""
        target_component = self._find_by_xpath(xpath)
        if target_component is None:
            raise AssertionError(f"未找到可点击元素（{action_name}），xpath：{xpath}")
        target_component.click()

    def is_xpath_displayed(self, xpath: str) -> bool:
        """判断指定 xpath 对应组件是否存在。"""
        return self._find_by_xpath(xpath) is not None

    def is_element_displayed_by_xpath(self, xpath: str, action_name: str) -> bool:
        """判断断言目标 xpath 对应组件是否已展示。"""
        is_displayed = self.is_xpath_displayed(xpath)
        if not is_displayed:
            raise AssertionError(f"未找到断言元素（{action_name}），xpath：{xpath}")
        return True

    def tap_hot_category(self) -> None:
        """点击左侧‘热门’分类。"""
        self.tap_by_xpath(self.HOT_CATEGORY_XPATH, "热门")

    def tap_hk_macao_category(self) -> None:
        """点击左侧‘港澳’分类。"""
        self.tap_by_xpath(self.HK_MACAO_CATEGORY_XPATH, "港澳")

    def tap_first_current_history_entry(self) -> None:
        """点击左侧第一个‘当前/历史’入口。"""
        self.tap_by_xpath(self.CURRENT_HISTORY_XPATH, "当前/历史")

    def is_hot_section_displayed(self) -> bool:
        """是否展示热门地区列表。"""
        return self.is_element_displayed_by_xpath(self.HOT_SECTION_XPATH, "热门")

    def is_hk_macao_section_displayed(self) -> bool:
        """是否展示港澳地区列表。"""
        return self.is_element_displayed_by_xpath(self.HK_MACAO_SECTION_XPATH, "港澳")

    def is_current_location_section_displayed(self) -> bool:
        """是否展示当前定位地区区域。"""
        return self.is_element_displayed_by_xpath(
            self.CURRENT_LOCATION_SECTION_XPATH, "当前/历史"
        )
