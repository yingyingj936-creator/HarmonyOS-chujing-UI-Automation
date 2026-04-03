from hypium import BY


class OutboundHomePage:
    """出境服务卡片首页对象。"""

    REGION_SELECTOR_TEXT = "香港"

    def __init__(self, driver):
        self.driver = driver

    def _find_by_text(self, text: str):
        """按文本查找组件。"""
        return self.driver.find_component(BY.text(text))

    def tap_region_selector(self):
        """点击首页右上角地区选择器（默认文案：香港）。"""
        self._find_by_text(self.REGION_SELECTOR_TEXT).click()

    def has_region_text(self, region_text: str) -> bool:
        """校验首页地区选择器文案是否已更新。"""
        return self._find_by_text(region_text) is not None
