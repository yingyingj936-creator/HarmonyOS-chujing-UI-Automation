from typing import Any

from hypium import BY


class OutboundHomePage:
    """出境服务卡片首页对象。"""

    PAGE_NAME = "OutboundHomePage"
    REGION_DROPDOWN_XPATH = '//*[@id="TabHomeCompRoot"]/Column[1]/Column[1]/Row[1]'

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
        component = self._find_by_xpath(xpath)
        if component is None:
            raise RuntimeError(
                f"[{self.PAGE_NAME}.tap_region_selector] 未找到地区切换下拉按钮，"
                f"by=xpath, xpath={xpath}"
            )
        component.click()

    def has_region_text(self, region_text: str) -> bool:
        """校验首页地区选择器文案是否已更新。"""
        return self._find_by_text(region_text) is not None
