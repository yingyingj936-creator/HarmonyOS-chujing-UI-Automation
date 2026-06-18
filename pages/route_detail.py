import time

from pages.base_page import BasePage


class RouteDetailPage(BasePage):
    """Route detail page."""

    PAGE_NAME = "RouteDetailPage"
    ROOT_XPATH = '//*[@id="mapPageRoot"]'
    MAP_VIEW_XPATH = '//*[@id="mapview"]'
    BOTTOM_PANEL_XPATH = '//*[@id="map_bottom_panel"]'
    TITLE_XPATH_TEMPLATE = '//*[@id="mapPageRoot"]//Text[@text="{route_name}"]'
    OVERVIEW_TITLE_XPATH_TEMPLATE = '//Text[@text="{route_name}\u00b7\u6982\u89c8"]'
    KEY_SCENIC_SPOTS_XPATH = '//Text[starts-with(@text, "\u5173\u952e\u666f\u70b9\uff1a")]'
    ITINERARY_PLANNING_XPATH = '//Text[@text="\u884c\u7a0b\u89c4\u5212"]'
    HIGHLIGHT_TEXTS = (
        "\u6e38\u73a9\u98ce\u683c",
        "\u6700\u4f73\u65f6\u95f4",
        "\u666f\u70b9\u7c7b\u578b",
    )
    WARM_TIPS_XPATH = '//Text[contains(@text, "\u6e29\u99a8\u63d0\u793a")]'
    BACK_BUTTON_XPATH = (
        '//*[@id="mapPageRoot"]//Row[@clickable="true" and ./Image]'
    )

    OVERVIEW_TAB_XPATH = '//Text[@text="\u5168\u89c8" and @clickable="true"]'
    DAY_1_TAB_XPATH = '//Text[@text="\u7b2c 1 \u5929" and @clickable="true"]'
    DAY_2_TAB_XPATH = '//Text[@text="\u7b2c 2 \u5929" and @clickable="true"]'
    DAY_1_CARD_XPATH = '//Text[@text="\u7b2c 1 \u5929" and @clickable="false"]'
    DAY_2_CARD_XPATH = '//Text[@text="\u7b2c 2 \u5929" and @clickable="false"]'
    OVERVIEW_SELECTED_TAB_XPATH = '//Text[@text="\u5168\u89c8" and @clickable="true" and @backgroundColor="#E6000000"]'
    DAY_1_SELECTED_TAB_XPATH = '//Text[@text="\u7b2c 1 \u5929" and @clickable="true" and @backgroundColor="#E6000000"]'
    DAY_2_SELECTED_TAB_XPATH = '//Text[@text="\u7b2c 2 \u5929" and @clickable="true" and @backgroundColor="#E6000000"]'
    DAY_1_TITLE_XPATH = '//Text[@text="\u5e02\u4e95\u7e41\u534e\u00b7\u7ef4\u6e2f\u591c\u8272"]'
    DAY_2_TITLE_XPATH = '//Text[@text="\u8857\u533a\u6587\u827a\u00b7\u5c71\u6d77\u65e5\u843d"]'
    DAY_1_SPOT_XPATH = '//Text[@text="\u901a\u83dc\u8857"]'
    DAY_2_SPOT_XPATH = '//Text[@text="\u575a\u5c3c\u5730\u57ce"]'
    DAY_1_POI_COUNT_XPATH = '//Text[@text="\u51718\u4e2a\u5730\u70b9"]'
    DAY_2_POI_COUNT_XPATH = '//Text[@text="\u51716\u4e2a\u5730\u70b9"]'
    DAY_1_OVERVIEW_CARD_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="\u7b2c 1 \u5929"] '
        'and .//Text[@text="\u51718\u4e2a\u5730\u70b9"]]'
    )

    @classmethod
    def title_xpath(cls, route_name: str) -> str:
        return cls.TITLE_XPATH_TEMPLATE.format(route_name=route_name)

    @classmethod
    def overview_title_xpath(cls, route_name: str) -> str:
        return cls.OVERVIEW_TITLE_XPATH_TEMPLATE.format(route_name=route_name)

    def wait_loaded(self, route_name: str, *, timeout: float = 12) -> None:
        """Wait until the route detail map, title, and overview card load."""
        self.wait_xpath(self.ROOT_XPATH, "route detail root", timeout=timeout)
        self.wait_xpath(self.MAP_VIEW_XPATH, "route map background", timeout=timeout)
        self.wait_xpath(self.title_xpath(route_name), "route detail title", timeout=timeout)
        self.wait_xpath(
            self.overview_title_xpath(route_name),
            "route overview title",
            timeout=timeout,
        )

    def wait_overview_modules(self, *, timeout: float = 8) -> None:
        """Verify overview highlights, key spots, and itinerary modules."""
        for text in self.HIGHLIGHT_TEXTS:
            self.wait_text(text, f"route overview module {text}", timeout=timeout)
        self.wait_xpath(
            self.KEY_SCENIC_SPOTS_XPATH,
            "route key scenic spots",
            timeout=timeout,
        )
        self.wait_xpath(
            self.ITINERARY_PLANNING_XPATH,
            "route itinerary planning",
            timeout=timeout,
        )

    def swipe_card_up(self) -> None:
        """Swipe the bottom route card upward."""
        panel = self.wait_xpath(self.BOTTOM_PANEL_XPATH, "route bottom card")
        self.driver.swipe("UP", distance=60, area=panel, swipe_time=0.55)
        time.sleep(0.8)

    def swipe_card_down(self) -> None:
        """Swipe the bottom route card downward."""
        panel = self.wait_xpath(self.BOTTOM_PANEL_XPATH, "route bottom card")
        self.driver.swipe("DOWN", distance=60, area=panel, swipe_time=0.55)
        time.sleep(0.8)

    def scroll_to_warm_tips(self, *, max_swipes: int = 8) -> None:
        """Scroll the route card until warm tips are visible."""
        for swipe_count in range(max_swipes + 1):
            if self.find_xpath(self.WARM_TIPS_XPATH) is not None:
                return
            if swipe_count == max_swipes:
                break
            self.swipe_card_up()
        raise RuntimeError(f"[{self.PAGE_NAME}] warm tips module was not found")


    def wait_itinerary_tabs(self, *, timeout: float = 8) -> None:
        """Verify the itinerary tab bar is visible."""
        self.wait_xpath(self.ITINERARY_PLANNING_XPATH, "route itinerary planning", timeout=timeout)
        self.wait_xpath(self.OVERVIEW_TAB_XPATH, "overview itinerary tab", timeout=timeout)
        self.wait_xpath(self.DAY_1_TAB_XPATH, "day 1 itinerary tab", timeout=timeout)
        self.wait_xpath(self.DAY_2_TAB_XPATH, "day 2 itinerary tab", timeout=timeout)

    def wait_overview_itinerary(self, *, timeout: float = 8) -> None:
        """Verify overview shows both day route lists and the map is rendered."""
        self.wait_xpath(self.MAP_VIEW_XPATH, "route map background", timeout=timeout)
        self.wait_xpath(self.DAY_1_TITLE_XPATH, "day 1 overview route title", timeout=timeout)
        self.wait_xpath(self.DAY_1_CARD_XPATH, "day 1 overview card", timeout=timeout)
        self.wait_xpath(self.DAY_2_TITLE_XPATH, "day 2 overview route title", timeout=timeout)
        self.wait_xpath(self.DAY_2_CARD_XPATH, "day 2 overview card", timeout=timeout)


    def wait_overview_day_cards(self, *, timeout: float = 8) -> None:
        """Verify overview day cards include route summaries, POI counts, and POI entries."""
        self.wait_xpath(self.MAP_VIEW_XPATH, "overview map background", timeout=timeout)
        self.wait_xpath(self.OVERVIEW_SELECTED_TAB_XPATH, "selected overview tab", timeout=timeout)
        self.wait_xpath(self.DAY_1_OVERVIEW_CARD_XPATH, "day 1 overview card", timeout=timeout)
        self.wait_xpath(self.DAY_1_TITLE_XPATH, "day 1 route summary", timeout=timeout)
        self.wait_xpath(self.DAY_1_POI_COUNT_XPATH, "day 1 POI count", timeout=timeout)
        self.wait_xpath(self.DAY_1_SPOT_XPATH, "day 1 POI entry", timeout=timeout)
        self.wait_xpath(self.DAY_2_TITLE_XPATH, "day 2 route summary", timeout=timeout)
        self.wait_xpath(self.DAY_2_POI_COUNT_XPATH, "day 2 POI count", timeout=timeout)

    def tap_day_1_overview_card(self, *, timeout: float = 8) -> None:
        """Tap the first day card in overview and wait for day 1 view."""
        self.tap_xpath(self.DAY_1_OVERVIEW_CARD_XPATH, "day 1 overview card", timeout=timeout)
        time.sleep(0.8)
        self.wait_day_1_itinerary(timeout=timeout)

    def tap_itinerary_tab(
        self,
        tab_xpath: str,
        selected_tab_xpath: str,
        name: str,
        *,
        timeout: float = 8,
    ) -> None:
        """Tap an itinerary tab and wait for the selected tab plus map."""
        self.tap_xpath(tab_xpath, name, timeout=timeout)
        time.sleep(0.8)
        self.wait_xpath(selected_tab_xpath, f"selected {name}", timeout=timeout)
        self.wait_xpath(self.MAP_VIEW_XPATH, "route map background", timeout=timeout)

    def tap_day_1_tab(self, *, timeout: float = 8) -> None:
        self.tap_itinerary_tab(
            self.DAY_1_TAB_XPATH,
            self.DAY_1_SELECTED_TAB_XPATH,
            "day 1 itinerary tab",
            timeout=timeout,
        )

    def tap_day_2_tab(self, *, timeout: float = 8) -> None:
        self.tap_itinerary_tab(
            self.DAY_2_TAB_XPATH,
            self.DAY_2_SELECTED_TAB_XPATH,
            "day 2 itinerary tab",
            timeout=timeout,
        )

    def tap_overview_tab(self, *, timeout: float = 8) -> None:
        self.tap_itinerary_tab(
            self.OVERVIEW_TAB_XPATH,
            self.OVERVIEW_SELECTED_TAB_XPATH,
            "overview itinerary tab",
            timeout=timeout,
        )


    def scroll_until_xpath_visible(
        self,
        xpath: str,
        name: str,
        *,
        max_swipes: int = 3,
        timeout: float = 8,
    ) -> None:
        """Scroll the bottom card until the target content becomes visible."""
        for swipe_count in range(max_swipes + 1):
            if self.find_xpath(xpath) is not None:
                self.wait_xpath(xpath, name, timeout=timeout)
                return
            if swipe_count == max_swipes:
                break
            self.swipe_card_up()
        raise RuntimeError(f"[{self.PAGE_NAME}] {name} was not found after scrolling")

    def wait_day_1_itinerary(self, *, timeout: float = 8) -> None:
        """Verify the day 1 tab is selected and the day map is rendered."""
        self.wait_xpath(self.MAP_VIEW_XPATH, "day 1 map background", timeout=timeout)
        self.wait_xpath(self.DAY_1_SELECTED_TAB_XPATH, "selected day 1 tab", timeout=timeout)

    def wait_day_2_itinerary(self, *, timeout: float = 8) -> None:
        """Verify the day 2 tab is selected and the day map is rendered."""
        self.wait_xpath(self.MAP_VIEW_XPATH, "day 2 map background", timeout=timeout)
        self.wait_xpath(self.DAY_2_SELECTED_TAB_XPATH, "selected day 2 tab", timeout=timeout)

    def tap_back_button(self) -> None:
        """Tap the route detail in-page back button."""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "route detail back button")
