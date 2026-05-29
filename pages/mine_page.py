from typing import Any
from hypium import BY
import time

from pages.common_locators import FAVORITE_BUTTON_XPATHS


class MinePage:
    PAGE_NAME = "MinePage"
    POSTS_TAB_XPATH = "//Text[starts-with(@text, '帖子')]"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def tap_posts_tab(self) -> None:

        # 定位包含“帖子”二字的组件，不管它是“帖子 10”还是“帖子(5)”
        posts_selector = self.POSTS_TAB_XPATH
        if not self.driver.wait_for_component(BY.xpath(posts_selector), timeout=8):
            raise RuntimeError("未找到包含‘帖子’文本的组件")
        component = self.driver.find_component(BY.xpath(posts_selector))

        if component:
            component.click()
        else:
            raise RuntimeError("未找到包含‘帖子’文本的组件")


    def verify_and_unfavorite(self, post_title: str) -> None:
        """在列表中定位帖子，进入并利用绝对路径取消收藏"""
        # 1. 校验目标帖子标题是否存在并点击进入
        if not self.driver.wait_for_component(BY.text(post_title), timeout=5):
            raise AssertionError(f"收藏列表中未找到目标帖子：{post_title}")
        self.driver.find_component(BY.text(post_title)).click()

        # 2. 进入详情后，执行上滑
        for _ in range(2):
            self.driver.swipe('UP', 80)
            time.sleep(0.3)

        for xpath in FAVORITE_BUTTON_XPATHS:
            if self.driver.wait_for_component(BY.xpath(xpath), timeout=4):
                star_btn = self.driver.find_component(BY.xpath(xpath))
                if star_btn:
                    star_btn.click()
                    return

        raise RuntimeError("进入帖子详情后，无法定位五角星按钮")
