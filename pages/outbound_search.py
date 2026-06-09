from typing import Any
from hypium import BY


class OutboundSearchPage:
    """出境服务搜索页面对象"""

    HOME_SEARCH_BAR_XPATH = '//*[@text="搜索服务、地图、帖子"]'
    SEARCH_INPUT_XPATH = '//TextInput'
    SEARCH_BUTTON_XPATH = '//Text[@text="搜索" and @clickable="true"]'
    BACK_BUTTON_XPATH = '//Row[./Text[@text="搜索"]]/Row[./Image]'

    # 搜索结果页分类板块
    TAB_SERVICE = '//Text[@text="服务"]'
    TAB_ROUTE = '//Text[@text="路线"]'
    TAB_LOCATION = '//Text[@text="地点"]'
    TAB_STRATEGY = '//Text[@text="最新攻略"]'

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def _find_by_xpath(self, xpath: str):
        """基础定位方法"""
        return self.driver.find_component(BY.xpath(xpath))

    @staticmethod
    def placeholder_xpath(destination: str) -> str:
        """生成指定目的地对应的搜索框 placeholder XPath。"""
        return f'//TextInput[@hint="在{destination}中搜索"]'

    def tap_home_search(self) -> None:
        """步骤：从首页点击搜索框进入搜索页"""
        if not self.driver.wait_for_component(BY.xpath(self.HOME_SEARCH_BAR_XPATH), timeout=8):
            raise RuntimeError("首页搜索框未出现，无法进入搜索页")
        self._find_by_xpath(self.HOME_SEARCH_BAR_XPATH).click()

    def input_keyword(self, keyword: str) -> None:
        """在搜索框中输入关键词。"""
        if not self.driver.wait_for_component(BY.xpath(self.SEARCH_INPUT_XPATH), timeout=8):
            raise RuntimeError("搜索输入框未出现")
        search_input = self._find_by_xpath(self.SEARCH_INPUT_XPATH)
        if search_input is None:
            raise RuntimeError("搜索输入框定位失败")
        search_input.inputText(keyword)

    def tap_search_button(self) -> None:
        """点击搜索框右侧的页面内“搜索”按钮。"""
        if not self.driver.wait_for_component(BY.xpath(self.SEARCH_BUTTON_XPATH), timeout=8):
            raise RuntimeError("搜索按钮未出现")
        search_button = self._find_by_xpath(self.SEARCH_BUTTON_XPATH)
        if search_button is None:
            raise RuntimeError("搜索按钮定位失败")
        search_button.click()

    def input_and_tap_search(self, keyword: str) -> None:
        """输入关键词并点击页面内搜索按钮。"""
        self.input_keyword(keyword)
        self.tap_search_button()

    def input_and_search(self, keyword: str) -> None:
        """步骤：输入关键词并执行搜索动作"""
        self.input_keyword(keyword)
        # 模拟键盘回车/确认键 (2054 为 HarmonyOS 标准搜索键值)
        self.driver.press_key(2054)

    def tap_back_button(self) -> None:
        """点击搜索页左上角页面内返回按钮。"""
        if not self.driver.wait_for_component(BY.xpath(self.BACK_BUTTON_XPATH), timeout=8):
            raise RuntimeError("搜索页页面内返回按钮未出现")
        back_button = self._find_by_xpath(self.BACK_BUTTON_XPATH)
        if back_button is None:
            raise RuntimeError("搜索页页面内返回按钮定位失败")
        back_button.click()

    def is_search_results_displayed(self) -> bool:
        """断言：验证搜索结果页的核心板块是否展示"""
        # 定义需要校验的板块及其名称
        check_list = [
            (self.TAB_SERVICE, "服务"),
            (self.TAB_ROUTE, "路线"),
            (self.TAB_LOCATION, "地点"),
            (self.TAB_STRATEGY, "最新攻略"),
        ]

        for xpath, name in check_list:
            if not self.driver.wait_for_component(BY.xpath(xpath), timeout=8):
                raise AssertionError(f"搜索结果页加载异常：未找到【{name}】板块")
        return True
