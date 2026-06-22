import time

from hypium import BY

from pages.base_page import BasePage


class MinePage(BasePage):
    """出境服务“我的”页面对象。"""

    PAGE_NAME = "MinePage"
    LOADING_XPATH = '//Text[@text="加载中..."]'
    PROFILE_TITLE_XPATH = '//Text[@text="小星星的旅程"]'
    FAVORITES_TITLE_XPATH = '//Text[@text="收藏"]'
    FAVORITE_SEARCH_XPATH = (
        '//TextInput[@hint="搜索收藏的地点、帖子"]'
    )
    FAVORITE_PLACES_TAB_XPATH = (
        '//Row[./Text[contains(@text, "地点")]]'
    )
    FAVORITE_POSTS_TAB_XPATH = (
        '//Row[./Text[contains(@text, "帖子")]]'
    )
    FAVORITE_POSTS_TEXT_XPATH = '//Text[contains(@text, "帖子")]'
    PAGE_SCROLL_XPATH = '//List[@scrollable="true"]'

    @staticmethod
    def favorite_place_xpath(place_name: str) -> str:
        return f'//Text[@text="{place_name}"]'

    @staticmethod
    def _xpath_literal(value: str) -> str:
        if '"' not in value:
            return f'"{value}"'
        if "'" not in value:
            return f"'{value}'"
        parts = value.split('"')
        concat_parts = []
        for index, part in enumerate(parts):
            if part:
                concat_parts.append(f'"{part}"')
            if index != len(parts) - 1:
                concat_parts.append("'\"'")
        return "concat(" + ", ".join(concat_parts) + ")"

    @classmethod
    def favorite_post_xpath(cls, post_title: str) -> str:
        title_prefix = post_title.strip()[:18]
        return (
            f'//Text[starts-with(@text, {cls._xpath_literal(title_prefix)})]'
        )

    def wait_content_loaded(self, *, timeout: float = 25) -> None:
        """等待“我的”页从 loading 态切到真实内容，避免过早查找收藏标签。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            loading = self.find_xpath(self.LOADING_XPATH)
            if loading is None and (
                self.find_xpath(self.PROFILE_TITLE_XPATH) is not None
                or self.find_xpath(self.FAVORITES_TITLE_XPATH) is not None
                or self.find_xpath(self.FAVORITE_POSTS_TAB_XPATH) is not None
            ):
                return
            time.sleep(0.5)

        raise RuntimeError(f"[{self.PAGE_NAME}] 我的页内容加载超时")

    def scroll_favorites_area_into_view(self, *, max_swipes: int = 6) -> None:
        """滚动“我的”页面，直到收藏区域进入可见区域。"""
        self.wait_content_loaded()
        for swipe_count in range(max_swipes + 1):
            if self.driver.wait_for_component(
                BY.xpath(self.FAVORITES_TITLE_XPATH),
                timeout=1,
            ) is not None:
                return
            if swipe_count == max_swipes:
                break
            page_scroll = self.wait_xpath(
                self.PAGE_SCROLL_XPATH,
                "我的页面滚动列表",
            )
            self.driver.swipe(
                "UP",
                distance=45,
                area=page_scroll,
            )
            time.sleep(0.5)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到收藏区域")

    def tap_favorite_places_tab(self) -> None:
        """点击收藏区域的“地点”页签。"""
        self.scroll_favorites_area_into_view()
        self.tap_xpath(
            self.FAVORITE_PLACES_TAB_XPATH,
            "收藏地点页签",
        )

    def tap_favorite_posts_tab(self) -> None:
        """点击收藏区域的“帖子”页签。"""
        self.wait_content_loaded()
        self.scroll_favorites_area_into_view()
        page_scroll = self.wait_xpath(
            self.PAGE_SCROLL_XPATH,
            "我的页面滚动列表",
        )
        for _ in range(8):
            tab = self.find_xpath(self.FAVORITE_POSTS_TAB_XPATH)
            if tab is not None:
                tab.click()
                return

            tab_text = self.find_xpath(self.FAVORITE_POSTS_TEXT_XPATH)
            if tab_text is not None:
                tab_text.click()
                return

            self.driver.swipe(
                "UP",
                distance=30,
                area=page_scroll,
            )
            time.sleep(0.4)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到收藏帖子页签")

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

    def scroll_favorite_post_into_view(
        self,
        post_title: str,
        *,
        max_swipes: int = 8,
    ) -> None:
        """滚动“我的”页面，直到收藏帖子进入可见区域。"""
        selector = BY.xpath(self.favorite_post_xpath(post_title))
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
            f"[{self.PAGE_NAME}] 收藏帖子列表未找到“{post_title}”"
        )

