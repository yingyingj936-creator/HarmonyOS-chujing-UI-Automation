import time

from hypium import BY

from pages.base_page import BasePage


class ReferenceHotRoutesPage(BasePage):
    """行程页参考热门路线列表页。"""

    PAGE_NAME = "ReferenceHotRoutesPage"

    CURRENT_REGION_TEXT = "中国香港"
    CURRENT_REGION_XPATH = (
        '//Text[@text="中国香港" or @text="香港" or contains(@text, "香港")]'
    )
    ROUTE_LIST_XPATH = '//List[@scrollable="true"]'
    HOT_ROUTE_TITLE_XPATH = (
        '//List[@scrollable="true"]//Text'
        '[contains(@text, "游") or contains(@text, "路线")]'
    )
    HOT_ROUTE_CARD_XPATH = (
        '//List[@scrollable="true"]//*[@clickable="true" '
        'and .//Text[contains(@text, "游") or contains(@text, "路线")]]'
    )
    BACK_BUTTON_XPATH = (
        '//Row[@clickable="true" and ./Image]'
    )

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
    def route_title_xpath(cls, route_name: str) -> str:
        return (
            f'//List[@scrollable="true"]//Text'
            f'[@text={cls._xpath_literal(route_name)}]'
        )

    @classmethod
    def route_card_xpath(cls, route_name: str) -> str:
        return (
            f'//List[@scrollable="true"]//*[@clickable="true" '
            f'and .//Text[@text={cls._xpath_literal(route_name)}]]'
        )

    def wait_loaded(self, *, timeout: float = 8) -> None:
        """等待参考热门路线页加载完成。"""
        self.wait_xpath(
            self.CURRENT_REGION_XPATH,
            f"当前地区{self.CURRENT_REGION_TEXT}",
            timeout=timeout,
        )
        self.wait_xpath(self.ROUTE_LIST_XPATH, "参考热门路线列表", timeout=timeout)
        self.wait_xpath(self.HOT_ROUTE_TITLE_XPATH, "热门路线标题", timeout=timeout)

    def wait_hot_route_card(self, *, timeout: float = 8) -> None:
        """等待至少一张热门路线卡片展示。"""
        self.wait_xpath(
            self.HOT_ROUTE_CARD_XPATH,
            "热门路线卡片",
            timeout=timeout,
        )

    def swipe_hot_route_list(self) -> None:
        """滑动热门路线列表。"""
        route_list = self.wait_xpath(
            self.ROUTE_LIST_XPATH,
            "参考热门路线列表",
        )
        self.driver.swipe(
            "UP",
            distance=55,
            area=route_list,
        )
        time.sleep(1)
        self.wait_xpath(self.ROUTE_LIST_XPATH, "滑动后的参考热门路线列表")

    def tap_back(self, *, timeout: float = 8) -> None:
        """点击页面返回按钮。"""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "参考热门路线页返回按钮", timeout=timeout)

    def scroll_route_into_view(
        self,
        route_name: str,
        *,
        max_swipes: int = 8,
    ) -> None:
        """滚动热门路线列表，直到目标路线进入可视区域。"""
        route_list = self.wait_xpath(
            self.ROUTE_LIST_XPATH,
            "参考热门路线列表",
        )
        target_xpath = self.route_title_xpath(route_name)
        for swipe_count in range(max_swipes + 1):
            if self.find_xpath(target_xpath) is not None:
                return
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=55,
                area=route_list,
            )
            time.sleep(0.8)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 热门路线列表未找到“{route_name}”"
        )

    def tap_route_card(self, route_name: str, *, timeout: float = 8) -> None:
        """点击指定热门路线卡片。"""
        self.scroll_route_into_view(route_name)
        self.tap_xpath(
            self.route_card_xpath(route_name),
            f"热门路线卡片“{route_name}”",
            timeout=timeout,
        )
