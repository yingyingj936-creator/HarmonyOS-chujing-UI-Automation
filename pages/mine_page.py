import time

from hypium import BY

from pages.base_page import BasePage


class MinePage(BasePage):
    """出境服务“我的”页面对象。"""

    PAGE_NAME = "MinePage"
    FAVORITES_TITLE_XPATH = '//Text[@text="收藏"]'
    FAVORITE_SEARCH_XPATH = (
        '//TextInput[@hint="搜索收藏的地点、帖子"]'
    )
    FAVORITE_PLACES_TAB_XPATH = (
        '//Row[./Text[starts-with(@text, "地点·")]]'
    )
    PAGE_SCROLL_XPATH = '//List[@scrollable="true"]'

    @staticmethod
    def favorite_place_xpath(place_name: str) -> str:
        return f'//Text[@text="{place_name}"]'

    def tap_favorite_places_tab(self) -> None:
        """点击收藏区域的“地点”页签。"""
        self.tap_xpath(
            self.FAVORITE_PLACES_TAB_XPATH,
            "收藏地点页签",
        )

    def scroll_favorite_place_into_view(
        self,
        place_name: str,
        *,
        max_swipes: int = 5,
    ) -> None:
        """滚动“我的”页面，直到收藏地点进入可见区域。"""
        selector = BY.xpath(self.favorite_place_xpath(place_name))
        page_scroll = self.wait_xpath(
            self.PAGE_SCROLL_XPATH,
            "我的页面滚动列表",
        )

        for _ in range(max_swipes + 1):
            if self.driver.wait_for_component(selector, timeout=1) is not None:
                return
            self.driver.swipe(
                "UP",
                distance=35,
                area=page_scroll,
            )
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏地点列表未找到“{place_name}”"
        )
