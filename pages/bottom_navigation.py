from pages.base_page import BasePage


class BottomNavigation(BasePage):
    """出境服务底部导航栏。"""

    PAGE_NAME = "BottomNavigation"

    TRIP_MARKER_TEXT = "创建行程"
    NEARBY_MARKER_TEXT = "探索附近"
    MINE_MARKER_TEXT = "小星星的旅程"
    HOME_MARKER_TEXT = "搜索服务、地图、帖子"

    _TAB_XPATH_TEMPLATE = (
        '//*[@id="HwAuthDialog_rootId"]//Column[./Text[@text="{tab_name}"]]'
    )

    @classmethod
    def tab_xpath(cls, tab_name: str) -> str:
        return cls._TAB_XPATH_TEMPLATE.format(tab_name=tab_name)

    def _tap_tab(self, tab_name: str, timeout: float = 8) -> None:
        self.tap_xpath(
            self.tab_xpath(tab_name),
            f"底部“{tab_name}”页签",
            timeout=timeout,
        )

    def tap_trip(self) -> None:
        self._tap_tab("行程")

    def tap_nearby(self) -> None:
        self._tap_tab("附近")

    def tap_mine(self) -> None:
        self._tap_tab("我的")

    def tap_home(self, timeout: float = 8) -> None:
        self._tap_tab("首页", timeout=timeout)
