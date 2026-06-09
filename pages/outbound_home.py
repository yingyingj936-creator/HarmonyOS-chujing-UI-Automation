import time
from typing import Any

from hypium import BY


class OutboundHomePage:
    """出境服务卡片首页对象。"""

    PAGE_NAME = "OutboundHomePage"
    REGION_DROPDOWN_XPATH_TEMPLATE = (
        '//*[@id="TabHomeCompRoot"]//Row[./Text[@text="{region_text}"]]'
    )
    REGION_DROPDOWN_XPATH = REGION_DROPDOWN_XPATH_TEMPLATE.format(
        region_text="中国香港"
    )
    REGION_SELECTOR_XPATH = (
        '//*[@id="TabHomeCompRoot"]/Column[1]/Column[1]/Column[1]/Row[1]'
    )
    HOME_ROOT_XPATH = '//*[@id="TabHomeCompRoot"]'
    SEARCH_BAR_TEXT = "搜索服务、地图、帖子"
    SEARCH_BAR_XPATH = '//*[@text="搜索服务、地图、帖子"]'
    # 该节点在首页首屏中承载顶部视觉区（含金刚区渲染区域）。
    KINGKONG_PROXY_XPATH = '//*[@id="TabHomeCompRoot"]/Stack[1]'
    HOT_ROUTES_SECTION_XPATH = '//*[@id="home_hot_routes_section"]'
    WATERFALL_SECTION_XPATH = '//*[@id="home_discovery_section"]'
    BOTTOM_HOME_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="首页"]'
    BOTTOM_TRIP_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="行程"]'
    BOTTOM_NEARBY_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="附近"]'
    BOTTOM_MINE_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="我的"]'
    TARGET_POST_TEXT = "首次办理港澳通行证攻略（手把手教你办理）"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def _find_by_text(self, text: str) -> Any | None:
        """按文本查找组件。"""
        return self.driver.find_component(BY.text(text))

    def _find_by_xpath(self, xpath: str) -> Any | None:
        """按 XPath 查找组件。"""
        return self.driver.find_component(BY.xpath(xpath))

    def _wait_by_text(self, text: str, timeout: float) -> bool:
        return self.driver.wait_for_component(BY.text(text), timeout=timeout)

    def _wait_by_xpath(self, xpath: str, timeout: float) -> bool:
        return self.driver.wait_for_component(BY.xpath(xpath), timeout=timeout)

    @classmethod
    def region_dropdown_xpath(cls, region_text: str) -> str:
        """生成首页左上角目的地入口 XPath。"""
        return cls.REGION_DROPDOWN_XPATH_TEMPLATE.format(region_text=region_text)

    def wait_first_screen_loaded(self, timeout: float = 5) -> bool:
        """
        首页首屏加载判定（总超时）。
        用于“超过 5 秒为空白”的冒烟断言。
        """
        deadline = time.time() + timeout

        def remaining() -> float:
            return max(0.1, deadline - time.time())

        if not self._wait_by_xpath(self.HOME_ROOT_XPATH, remaining()):
            return False
        if not self._wait_by_text("中国香港", remaining()):
            return False
        if not self._wait_by_text(self.SEARCH_BAR_TEXT, remaining()):
            return False
        return True

    def is_home_tab_active(self, timeout: float = 3) -> bool:
        """
        首页高亮判定（代理断言）。
        说明：UI 树中未提供 selected=true，可通过“首页专属容器+首屏模块可见”推断当前为首页激活态。
        """
        return (
            self._wait_by_xpath(self.HOME_ROOT_XPATH, timeout)
            and self._wait_by_xpath(self.BOTTOM_HOME_TAB_XPATH, timeout)
            and self._wait_by_xpath(self.HOT_ROUTES_SECTION_XPATH, timeout)
        )

    def tap_region_selector(self, region_text: str | None = None) -> None:
        """点击首页地区切换下拉按钮。"""
        xpath = self.REGION_SELECTOR_XPATH
        if not self._wait_by_xpath(xpath, timeout=8):
            raise RuntimeError(
                f"[{self.PAGE_NAME}.tap_region_selector] 未找到地区切换下拉按钮，"
                f"by=xpath, xpath={xpath}, current_region={region_text}"
            )
        component = self._find_by_xpath(xpath)
        if component is None:
            raise RuntimeError(
                f"[{self.PAGE_NAME}.tap_region_selector] 地区切换下拉按钮定位失败，"
                f"by=xpath, xpath={xpath}, current_region={region_text}"
            )
        component.click()

    def wait_loaded(self, timeout: float = 8) -> bool:
        """等待首页标识元素出现。"""
        return self._wait_by_xpath(self.BOTTOM_HOME_TAB_XPATH, timeout=timeout)

    def tap_hk_trip_entry(self) -> None:
        """点击首页‘香港逛吃两日游’"""
        if not self._wait_by_text("香港逛吃两日游", timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到文本为‘香港逛吃两日游’的入口")
        component = self._find_by_text("香港逛吃两日游")
        if component is None:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到文本为‘香港逛吃两日游’的入口")
        component.click()

    def tap_trip_tab(self) -> None:
        """点击底部‘行程’页签"""
        if not self._wait_by_xpath(self.BOTTOM_TRIP_TAB_XPATH, timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘行程’页签")
        component = self._find_by_xpath(self.BOTTOM_TRIP_TAB_XPATH)
        if component is None:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘行程’页签")
        component.click()

    def tap_entry_category(self) -> None:
        """点击‘入境’分类"""
        if not self._wait_by_text("入境", timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到‘入境’分类页签")
        component = self._find_by_text("入境")
        if not component:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到‘入境’分类页签")
        component.click()

    def tap_target_post(self) -> None:
        """根据唯一文本点击目标帖子卡片"""
        post_text = self.TARGET_POST_TEXT
        if not self._wait_by_text(post_text, timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到目标帖子：{post_text}")
        component = self._find_by_text(post_text)
        if not component:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到目标帖子：{post_text}")
        component.click()

    def tap_mine_tab(self) -> None:
        """点击底部导航栏‘我的’"""
        if not self._wait_by_xpath(self.BOTTOM_MINE_TAB_XPATH, timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘我的’页签")
        component = self._find_by_xpath(self.BOTTOM_MINE_TAB_XPATH)
        if not component:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘我的’页签")
        component.click()

    def is_at_home(self) -> bool:
        """
        判断当前是否在首页。
        逻辑：判断首页特有的、唯一的组件是否存在。
        """
        try:
            return self.driver.find_component(BY.xpath(self.SEARCH_BAR_XPATH)) is not None
        except Exception:
            return False
