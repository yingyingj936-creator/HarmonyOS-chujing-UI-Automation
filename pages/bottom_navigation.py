from typing import Any

from hypium import BY


class BottomNavigation:
    """出境服务底部导航栏。"""

    PAGE_NAME = "BottomNavigation"

    TRIP_MARKER_TEXT = "创建行程"
    NEARBY_MARKER_TEXT = "探索附近"
    MINE_MARKER_TEXT = "小星星的旅程"
    HOME_MARKER_TEXT = "搜索服务、地图、帖子"

    _TAB_XPATH_TEMPLATE = (
        '//*[@id="HwAuthDialog_rootId"]//Column[./Text[@text="{tab_name}"]]'
    )

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def _tap_tab(self, tab_name: str, timeout: float = 8) -> None:
        xpath = self._TAB_XPATH_TEMPLATE.format(tab_name=tab_name)
        selector = BY.xpath(xpath)

        if not self.driver.wait_for_component(selector, timeout=timeout):
            raise RuntimeError(
                f"[{self.PAGE_NAME}] 未找到可点击的底部‘{tab_name}’页签"
            )

        component = self.driver.find_component(selector)
        if component is None:
            raise RuntimeError(
                f"[{self.PAGE_NAME}] 底部‘{tab_name}’页签定位失败"
            )
        component.click()

    def tap_trip(self) -> None:
        self._tap_tab("行程")

    def tap_nearby(self) -> None:
        self._tap_tab("附近")

    def tap_mine(self) -> None:
        self._tap_tab("我的")

    def tap_home(self) -> None:
        self._tap_tab("首页")
