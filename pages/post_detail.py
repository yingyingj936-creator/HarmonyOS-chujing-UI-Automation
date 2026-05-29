from typing import Any
from hypium import BY
import time

class PostDetailPage:
    PAGE_NAME = "PostDetailPage"

    FAVORITE_LOCATORS = [
        '//ListItem//Row[2]/Row[3]',
        '//List/ListItem[2]/Row/Row[2]/Row[3]',
    ]

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def scroll_and_tap_favorite(self) -> None:
        """上滑并点击五角星收藏图标"""
        for _ in range(2):
            self.driver.swipe('UP', 70)
            time.sleep(0.3)

        for xpath in self.FAVORITE_LOCATORS:
            if self.driver.wait_for_component(BY.xpath(xpath), timeout=4):
                component = self.driver.find_component(BY.xpath(xpath))
                if component:
                    component.click()
                    return

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 无法定位收藏按钮，候选定位器：{self.FAVORITE_LOCATORS}"
        )
