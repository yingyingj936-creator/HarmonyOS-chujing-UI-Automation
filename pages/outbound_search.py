from typing import Any
from hypium import BY


class OutboundSearchPage:
    """出境服务搜索页面对象"""

    # --- 定位器 (基于 JSON 树精准提取) ---

    # 首页搜索入口：使用包含“搜索”的模糊匹配，兼容“搜索服务、帖子”
    HOME_SEARCH_BAR_XPATH = '//*[@text="搜索服务、地图、帖子"]'

    # 搜索启动页输入框：兼容“在中国香港中搜索”或“搜索目的地/景点”
    # 采用类型定位配合包含“搜索”的提示词，最为稳健
    SEARCH_INPUT_XPATH = '//TextInput'

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

    def tap_home_search(self):
        """步骤：从首页点击搜索框进入搜索页"""
        if not self.driver.wait_for_component(BY.xpath(self.HOME_SEARCH_BAR_XPATH), timeout=8):
            raise RuntimeError("首页搜索框未出现，无法进入搜索页")
        self._find_by_xpath(self.HOME_SEARCH_BAR_XPATH).click()

    def input_and_search(self, keyword: str):
        """步骤：输入关键词并执行搜索动作"""
        if not self.driver.wait_for_component(BY.xpath(self.SEARCH_INPUT_XPATH), timeout=8):
            raise RuntimeError("搜索输入框未出现")
        search_input = self._find_by_xpath(self.SEARCH_INPUT_XPATH)
        # 输入目标文字
        search_input.inputText(keyword)
        # 模拟键盘回车/确认键 (2054 为 HarmonyOS 标准搜索键值)
        self.driver.press_key(2054)

    def is_search_results_displayed(self) -> bool:
        """断言：验证搜索结果页的核心板块是否展示"""
        # 定义需要校验的板块及其名称
        check_list = [
            (self.TAB_SERVICE, "服务"),
            (self.TAB_ROUTE, "路线"),
            (self.TAB_LOCATION, "地点"),
            (self.TAB_STRATEGY, "最新攻略")
        ]

        for xpath, name in check_list:
            if not self.driver.wait_for_component(BY.xpath(xpath), timeout=8):
                raise AssertionError(f"搜索结果页加载异常：未找到【{name}】板块")
        return True
