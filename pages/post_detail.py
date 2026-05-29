from typing import Any
from hypium import BY
import time

from pages.common_locators import FAVORITE_BUTTON_XPATHS

class PostDetailPage:
    PAGE_NAME = "PostDetailPage"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def scroll_and_tap_favorite(self) -> None:
        """上滑并点击五角星收藏图标"""
        for _ in range(2):
            self.driver.swipe('UP', 80)
            time.sleep(0.3)

        for xpath in FAVORITE_BUTTON_XPATHS:
            if self.driver.wait_for_component(BY.xpath(xpath), timeout=4):
                component = self.driver.find_component(BY.xpath(xpath))
                if component:
                    component.click()
                    return

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 无法定位收藏按钮，候选定位器：{FAVORITE_BUTTON_XPATHS}"
        )
