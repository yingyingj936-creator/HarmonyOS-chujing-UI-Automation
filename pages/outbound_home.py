from typing import Any

from hypium import BY


class OutboundHomePage:
    """出境服务卡片首页对象。"""

    PAGE_NAME = "OutboundHomePage"
    REGION_DROPDOWN_XPATH = '(//*[@id="TabHomeCompRoot"]//Row[./Image])[1]'
    HOME_TEXT = "首页"
    TARGET_POST_TEXT = "首次办理港澳通行证攻略（手把手教你办理）"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def _find_by_text(self, text: str) -> Any | None:
        """按文本查找组件。"""
        return self.driver.find_component(BY.text(text))

    def _find_by_xpath(self, xpath: str) -> Any | None:
        """按 XPath 查找组件。"""
        return self.driver.find_component(BY.xpath(xpath))

    def tap_region_selector(self) -> None:
        """点击首页地区切换下拉按钮。"""
        xpath = self.REGION_DROPDOWN_XPATH
        if not self.driver.wait_for_component(BY.xpath(xpath), timeout=8):
            raise RuntimeError(
                f"[{self.PAGE_NAME}.tap_region_selector] 未找到地区切换下拉按钮，"
                f"by=xpath, xpath={xpath}"
            )
        component = self._find_by_xpath(xpath)
        if component is None:
            raise RuntimeError(
                f"[{self.PAGE_NAME}.tap_region_selector] 未找到地区切换下拉按钮，"
                f"by=xpath, xpath={xpath}"
            )
        component.click()

    def has_region_text(self, region_text: str, timeout: float = 0) -> bool:
        """校验首页地区选择器文案是否已更新。"""
        if timeout > 0:
            return self.driver.wait_for_component(BY.text(region_text), timeout=timeout)
        return self._find_by_text(region_text) is not None

    def wait_loaded(self, timeout: float = 8) -> bool:
        """等待首页标识元素出现。"""
        return self.driver.wait_for_component(BY.text(self.HOME_TEXT), timeout=timeout)

    def tap_hk_trip_entry(self) -> None:
        """点击首页‘香港逛吃两日游’"""
        if not self.driver.wait_for_component(BY.text("香港逛吃两日游"), timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到文本为‘香港逛吃两日游’的入口")
        component = self._find_by_text("香港逛吃两日游")
        if component is None:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到文本为‘香港逛吃两日游’的入口")
        component.click()

    def tap_trip_tab(self) -> None:
        """点击底部‘行程’页签"""
        if not self.driver.wait_for_component(BY.text("行程"), timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘行程’页签")
        component = self._find_by_text("行程")
        if component is None:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘行程’页签")
        component.click()

    def tap_entry_category(self) -> None:
        """点击‘入境’分类"""
        if not self.driver.wait_for_component(BY.text("入境"), timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到‘入境’分类页签")
        component = self._find_by_text("入境")
        if not component:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到‘入境’分类页签")
        component.click()

    def tap_target_post(self) -> None:
        """根据唯一文本点击目标帖子卡片"""
        post_text = self.TARGET_POST_TEXT
        if not self.driver.wait_for_component(BY.text(post_text), timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到目标帖子：{post_text}")
        component = self._find_by_text(post_text)
        if not component:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到目标帖子：{post_text}")
        component.click()

    def tap_mine_tab(self) -> None:
        """点击底部导航栏‘我的’"""
        if not self.driver.wait_for_component(BY.text("我的"), timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘我的’页签")
        component = self._find_by_text("我的")
        if not component:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到底部‘我的’页签")
        component.click()

    def is_at_home(self) -> bool:
        """
        判断当前是否在首页。
        逻辑：判断首页特有的、唯一的组件是否存在。
        """
        try:
            return self.driver.find_component(BY.text(self.HOME_TEXT)) is not None
        except Exception:
            return False
