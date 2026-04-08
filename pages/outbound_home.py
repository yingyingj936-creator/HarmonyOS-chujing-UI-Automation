from typing import Any

from hypium import BY


class OutboundHomePage:
    """出境服务卡片首页对象。"""

    REGION_DROPDOWN_ID = "109"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def _find_by_text(self, text: str):
        """按文本查找组件。"""
        return self.driver.find_component(BY.text(text))

    def _find_by_id(self, component_id: str | int):
        """按组件 ID 查找组件。"""
        return self.driver.find_component(BY.id(str(component_id)))

    def tap_region_selector(self) -> None:
        """点击首页地区切换下拉按钮。"""
        component_id = self.REGION_DROPDOWN_ID
        component = self._find_by_id(component_id)
        if component is None:
            raise RuntimeError(
                "[OutboundHomePage.tap_region_selector] "
                f"未找到地区切换下拉按钮，component_id={component_id}"
            )
        component.click()

    def has_region_text(self, region_text: str) -> bool:
        """校验首页地区选择器文案是否已更新。"""
        return self._find_by_text(region_text) is not None
