from typing import Any
from hypium import BY

class RouteDetailPage:
    PAGE_NAME = "RouteDetailPage"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def tap_add_to_my_trip(self) -> None:
        """点击‘加入我的行程’"""
        if not self.driver.wait_for_component(BY.text("加入我的行程"), timeout=8):
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到‘加入我的行程’文本按钮")
        component = self.driver.find_component(BY.text("加入我的行程"))
        if not component:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到‘加入我的行程’文本按钮")
        component.click()

    def tap_create_and_add(self) -> None:
        """点击‘创建并添加’"""
        # 弹窗通常需要显式等待
        if self.driver.wait_for_component(BY.text("创建并添加"), timeout=5):
            self.driver.find_component(BY.text("创建并添加")).click()
        else:
            raise RuntimeError(f"[{self.PAGE_NAME}] 等待‘创建并添加’文本超时")
