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
    DAY_1_SECOND_SPOT_XPATH = '//Text[@text="\u65fa\u89d2"]'
    DAY_1_DISTANCE_TO_SECOND_XPATH = (
        '//Text[@text="\u8ddd\u79bb 0.3km\u00b7\u6b65\u884c\u9884\u8ba1 5\u5206\u949f"]'
    )
    DAY_1_FIRST_POI_CARD_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="\u901a\u83dc\u8857"] '
        'and .//Text[contains(@text, "\u901a\u83dc\u8857\u8d2f\u7a7f\u65fa\u89d2")]]'
    )
    DAY_2_SPOT_XPATH = '//Text[@text="\u575a\u5c3c\u5730\u57ce"]'
    DAY_1_POI_COUNT_XPATH = '//Text[@text="\u51718\u4e2a\u5730\u70b9"]'
    DAY_2_POI_COUNT_XPATH = '//Text[@text="\u51716\u4e2a\u5730\u70b9"]'
    DAY_1_OVERVIEW_CARD_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="\u7b2c 1 \u5929"] '
        'and .//Text[@text="\u51718\u4e2a\u5730\u70b9"]]'
    )
    POI_DETAIL_ROOT_XPATH = '//*[@id="map_panel_poidetail"]'
    POI_DETAIL_HEADER_XPATH = (
        '//*[@id="map_bottom_panel"]//Column'
        '[./Text[@text="\u901a\u83dc\u8857"] and ./Text[@text="Tung Choi Street"]]'
    )
    POI_DETAIL_ENGLISH_NAME_XPATH = '//Text[@text="Tung Choi Street"]'
    POI_DETAIL_TAG_XPATH = '//*[@id="map_panel_poidetail"]//Text[@text="\u666f\u70b9"]'
    POI_DETAIL_RATING_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[starts-with(@text, "\u8bc4\u5206 ")]'
    )
    POI_DETAIL_GALLERY_XPATH = (
        '//*[@id="map_panel_poidetail"]//ListItem/__Common__[@clickable="true"]'
    )
    POI_DETAIL_INTRO_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[contains(@text, '
        '"\u901a\u83dc\u8857\u8d2f\u7a7f\u65fa\u89d2")]'
    )
    POI_DETAIL_INLINE_ADD_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[@text="\u6dfb\u52a0\u5230\u6211\u7684\u884c\u7a0b"]'
    )
    POI_DETAIL_TIPS_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[contains(@text, "\u4ef7\u683c\u53ef\u8c08")]'
    )
    POI_DETAIL_SURROUNDING_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[@text="\u5468\u8fb9\u63a8\u8350"]'
    )
    POI_DETAIL_FAVORITE_BUTTON_XPATH = (
        '//*[@id="map_bottom_panel"]//Row[@clickable="true" and ./Image]'
    )
    POI_DETAIL_SERVICE_XPATH = '//*[@id="map_bottom_panel"]//Text[@text="\u8ddf\u56e2\u6e38"]'
    POI_DETAIL_NAVIGATION_XPATH = '//*[@id="map_bottom_panel"]//Text[@text="\u5bfc\u822a"]'
    POI_DETAIL_CLOSE_XPATH = '//*[@id="map_bottom_panel"]//Image[@clickable="true"]'
    ROUTE_JOIN_TRIP_BUTTON_XPATH = '//*[@id="copyPlanBtn"]'
    ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH = (
        '//Text[@text="\u4e00\u952e\u8ddf\u73a9" and @clickable="true"]'
    )
    PLAY_MODE_EXIT_TITLE_XPATH = '//Text[@text="\u9000\u51fa\u6e38\u73a9\u6a21\u5f0f"]'
    PLAY_MODE_EXIT_BUTTON_XPATH = (
        '//*[@id="mapPageRoot"]//Row[@clickable="true" and ./Image]'
    )
    PLAY_MODE_TAB_BAR_XPATH = '//*[@id="map_top_dateChoose"]'
    PLAY_MODE_OVERVIEW_TAB_XPATH = (
        '//*[@id="map_top_dateChoose"]//Text[@text="\u5168\u89c8"]'
    )
    PLAY_MODE_DAY_1_TAB_XPATH = (
        '//*[@id="map_top_dateChoose"]//Text[@text="\u7b2c 1 \u5929"]'
    )
    PLAY_MODE_DAY_2_TAB_XPATH = (
        '//*[@id="map_top_dateChoose"]//Text[@text="\u7b2c 2 \u5929"]'
    )
    PLAY_MODE_LEFT_SIDEBAR_XPATH = '//*[@id="map_left_bottom_tip"]'
    PLAY_MODE_EDIT_ROUTE_XPATH = (
        '//Text[contains(@text, "\u7f16\u8f91") '
        'and contains(@text, "\u8def\u7ebf") and @clickable="true"]'
    )
    PLAY_MODE_ROUTE_INTRO_XPATH = (
        '//Text[contains(@text, "\u8def\u7ebf") '
        'and contains(@text, "\u4ecb\u7ecd") and @clickable="true"]'
    )
    PLAY_MODE_LOCATION_BUTTON_XPATH = '//*[@id="map_my_location"]'
    PLAY_MODE_LOCATION_BUTTON_CENTER = (1710, 2325)
    PLAY_MODE_LOCATION_BUTTON_BOUNDS = (1650, 2240, 1790, 2390)
    PLAY_MODE_BOTTOM_DRAWER_XPATH = '//*[@id="map_bottom_tab_comp"]'
    # The day cards/bubbles are rendered inside the map XComponent and are not
    # exposed as UI nodes, so this click uses the observed stable map position.
    PLAY_MODE_DAY_1_BUBBLE_CENTER = (980, 560)
    PLAY_MODE_DAY_1_BUBBLE_BOUNDS = (810, 450, 1145, 665)
    PLAY_MODE_DAY_2_BUBBLE_BOUNDS = (1410, 1890, 1745, 2105)
    PLAY_MODE_DAY_ROUTE_AREA_BOUNDS = (520, 410, 1780, 1510)
    PLAY_MODE_POI_2_NAME = "\u65fa\u89d2"
    PLAY_MODE_POI_3_NAME = "\u4fe1\u548c\u4e2d\u5fc3"
    PLAY_MODE_POI_2_BUBBLE_CANDIDATES = (
        (1070, 430),
        (970, 405),
        (920, 450),
        (1115, 455),
        (1010, 380),
    )
    PLAY_MODE_POI_2_BUBBLE_BOUNDS = (875, 350, 1255, 535)
    PLAY_MODE_AXIS_POI_3_CENTER = (830, 2420)
    PLAY_MODE_AXIS_POI_3_BOUNDS = (690, 2310, 970, 2520)
    POI_DETAIL_ANY_HEADER_XPATH = (
        '//*[@id="map_bottom_panel"]//Column[./Text[1] and ./Text[2]]'
    )
    POI_DETAIL_GENERIC_INTRO_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[@clickable="true" '
        'and contains(@text, "\u8be6\u60c5")]'
    )
    SURROUNDING_CATEGORY_XPATH_TEMPLATE = (
        '//*[@id="map_panel_poidetail"]//Row[@clickable="true" '
        'and ./Text[@text="{category_name}"]]'
    )
    SURROUNDING_CATEGORY_GROUP_XPATH = (
        '//*[@id="map_panel_poidetail"]//Column'
        '[.//Text[@text="\u5468\u8fb9\u63a8\u8350"] '
        'and .//Text[@text="\u666f\u70b9"] '
        'and .//Text[@text="\u9152\u5e97"] '
        'and .//Text[@text="\u7f8e\u98df"]]'
    )
    SURROUNDING_POI_CARD_XPATH = (
        '//*[@id="map_panel_poidetail"]//*[@clickable="true" '
        'and .//Text[starts-with(@text, "\u8bc4\u5206 ")]]'
    )
    SURROUNDING_POI_DISTANCE_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[contains(@text, "km") '
        'or contains(@text, "\u8ddd\u79bb")]'
    )

    @classmethod
    def title_xpath(cls, route_name: str) -> str:
        return cls.TITLE_XPATH_TEMPLATE.format(route_name=route_name)

    @classmethod
    def overview_title_xpath(cls, route_name: str) -> str:
        return cls.OVERVIEW_TITLE_XPATH_TEMPLATE.format(route_name=route_name)

    @classmethod
    def surrounding_category_xpath(cls, category_name: str) -> str:
        return cls.SURROUNDING_CATEGORY_XPATH_TEMPLATE.format(
            category_name=category_name
        )

    @classmethod
    def play_mode_poi_title_xpath(cls, poi_name: str) -> str:
        return f'//*[@id="map_bottom_panel"]//Text[@text="{poi_name}"]'

    @classmethod
    def play_mode_axis_poi_xpath(cls, poi_name: str) -> str:
        return f'//*[@id="map_bottom_tab_comp"]//Text[@text="{poi_name}"]'

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

    def swipe_poi_detail(self, direction: str = "UP") -> None:
        """Swipe inside the POI detail scroll area."""
        detail = self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI detail scroll card")
        self.driver.swipe(direction, distance=60, area=detail, swipe_time=0.55)
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

    def scroll_poi_detail_until_xpath_visible(
        self,
        xpath: str,
        name: str,
        *,
        max_swipes: int = 5,
        timeout: float = 8,
        directions: tuple[str, ...] = ("UP", "DOWN"),
    ) -> None:
        """Scroll the POI detail card until target content becomes visible."""
        if self.find_xpath(xpath) is not None:
            self.wait_xpath(xpath, name, timeout=timeout)
            return

        for direction in directions:
            for _ in range(max_swipes):
                self.swipe_poi_detail(direction)
                if self.find_xpath(xpath) is not None:
                    self.wait_xpath(xpath, name, timeout=timeout)
                    return

        raise RuntimeError(
            f"[{self.PAGE_NAME}] {name} was not found in POI detail after scrolling"
        )

    def wait_day_1_itinerary(self, *, timeout: float = 8) -> None:
        """Verify the day 1 tab is selected and the day map is rendered."""
        self.wait_xpath(self.MAP_VIEW_XPATH, "day 1 map background", timeout=timeout)
        self.wait_xpath(self.DAY_1_SELECTED_TAB_XPATH, "selected day 1 tab", timeout=timeout)

    def wait_day_1_route_list(self, *, timeout: float = 8) -> None:
        """Verify the day 1 POI list and its travel-distance row are visible."""
        self.wait_day_1_itinerary(timeout=timeout)
        self.wait_xpath(self.DAY_1_FIRST_POI_CARD_XPATH, "day 1 first POI card", timeout=timeout)
        self.wait_xpath(
            self.DAY_1_DISTANCE_TO_SECOND_XPATH,
            "day 1 first travel distance",
            timeout=timeout,
        )
        self.wait_xpath(self.DAY_1_SECOND_SPOT_XPATH, "day 1 second POI", timeout=timeout)

    def tap_day_1_first_poi(self, *, timeout: float = 8) -> None:
        """Tap the first POI in day 1 route list and wait for its detail card."""
        self.tap_xpath(self.DAY_1_FIRST_POI_CARD_XPATH, "day 1 first POI card", timeout=timeout)
        time.sleep(0.8)
        self.wait_day_1_poi_detail(timeout=timeout)

    def wait_day_1_poi_detail(self, *, timeout: float = 8) -> None:
        """Verify the day 1 POI detail card exposes the key modules."""
        self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI detail scroll card", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_HEADER_XPATH, "POI detail title and English name", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_TAG_XPATH, "POI detail tag", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_RATING_XPATH, "POI detail rating", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_GALLERY_XPATH, "POI detail gallery", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_INTRO_XPATH, "POI detail introduction", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_INLINE_ADD_XPATH, "POI detail add-to-trip entry", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_TIPS_XPATH, "POI detail tips", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_SURROUNDING_XPATH, "POI detail surrounding recommendations", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_FAVORITE_BUTTON_XPATH, "POI detail favorite button", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_SERVICE_XPATH, "POI detail linked service", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_NAVIGATION_XPATH, "POI detail navigation entry", timeout=timeout)

    def wait_surrounding_categories(self, *, timeout: float = 8) -> None:
        """Verify the surrounding recommendation category tabs are visible."""
        self.scroll_poi_detail_until_xpath_visible(
            self.POI_DETAIL_SURROUNDING_XPATH,
            "POI surrounding recommendations title",
            timeout=timeout,
        )
        self.scroll_poi_detail_until_xpath_visible(
            self.SURROUNDING_CATEGORY_GROUP_XPATH,
            "POI surrounding recommendation categories",
            timeout=timeout,
        )

    def wait_surrounding_poi_list(self, *, timeout: float = 8) -> None:
        """Verify the surrounding POI list exposes card information and distance."""
        self.scroll_poi_detail_until_xpath_visible(
            self.SURROUNDING_POI_CARD_XPATH,
            "surrounding POI card",
            timeout=timeout,
        )
        self.wait_xpath(
            self.SURROUNDING_POI_DISTANCE_XPATH,
            "surrounding POI distance",
            timeout=timeout,
        )

    def tap_surrounding_category(self, category_name: str, *, timeout: float = 8) -> None:
        """Tap a surrounding recommendation category tab."""
        xpath = self.surrounding_category_xpath(category_name)
        self.scroll_poi_detail_until_xpath_visible(
            xpath,
            f"surrounding category {category_name}",
            timeout=timeout,
        )
        self.tap_xpath(xpath, f"surrounding category {category_name}", timeout=timeout)
        time.sleep(0.8)

    def tap_surrounding_first_poi(self, *, timeout: float = 8) -> None:
        """Tap the first visible surrounding POI card and wait for its detail card."""
        self.scroll_poi_detail_until_xpath_visible(
            self.SURROUNDING_POI_CARD_XPATH,
            "surrounding POI card",
            timeout=timeout,
        )
        self.tap_xpath(
            self.SURROUNDING_POI_CARD_XPATH,
            "surrounding POI card",
            timeout=timeout,
        )
        time.sleep(0.8)
        self.wait_generic_poi_detail(timeout=timeout)

    def wait_generic_poi_detail(self, *, timeout: float = 8) -> None:
        """Verify a POI detail card without depending on a fixed POI name."""
        self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI detail scroll card", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_ANY_HEADER_XPATH, "POI detail title and English name", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_TAG_XPATH, "POI detail tag", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_RATING_XPATH, "POI detail rating", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_GALLERY_XPATH, "POI detail gallery", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_GENERIC_INTRO_XPATH, "POI detail introduction", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_INLINE_ADD_XPATH, "POI detail add-to-trip entry", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_SURROUNDING_XPATH, "POI detail surrounding recommendations", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_FAVORITE_BUTTON_XPATH, "POI detail favorite button", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_NAVIGATION_XPATH, "POI detail navigation entry", timeout=timeout)

    def close_day_1_poi_detail(self, *, timeout: float = 8) -> None:
        """Close the POI detail card and return to the day 1 route list."""
        self.tap_xpath(self.POI_DETAIL_CLOSE_XPATH, "POI detail close button", timeout=timeout)
        time.sleep(0.8)
        self.wait_day_1_route_list(timeout=timeout)

    def wait_day_2_itinerary(self, *, timeout: float = 8) -> None:
        """Verify the day 2 tab is selected and the day map is rendered."""
        self.wait_xpath(self.MAP_VIEW_XPATH, "day 2 map background", timeout=timeout)
        self.wait_xpath(self.DAY_2_SELECTED_TAB_XPATH, "selected day 2 tab", timeout=timeout)

    def tap_back_button(self) -> None:
        """Tap the route detail in-page back button."""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "route detail back button")

    def tap_join_trip(self, *, timeout: float = 8) -> None:
        """Tap the route detail bottom button to create this route as a trip."""
        self.tap_xpath(
            self.ROUTE_JOIN_TRIP_BUTTON_XPATH,
            "route detail join trip button",
            timeout=timeout,
        )

    def tap_one_click_play(self, *, timeout: float = 8) -> None:
        """Tap the route detail bottom button to enter play mode."""
        self.tap_xpath(
            self.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH,
            "route detail one-click play button",
            timeout=timeout,
        )
        time.sleep(1.2)
        self.wait_play_mode_overview(timeout=timeout)

    def wait_play_mode_overview(self, *, timeout: float = 8) -> None:
        """Verify play mode renders the overview map and core controls."""
        self.wait_xpath(self.PLAY_MODE_EXIT_TITLE_XPATH, "play mode exit title", timeout=timeout)
        self.wait_xpath(self.MAP_VIEW_XPATH, "play mode map background", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_TAB_BAR_XPATH, "play mode day tab bar", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_OVERVIEW_TAB_XPATH, "play mode overview tab", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_DAY_1_TAB_XPATH, "play mode day 1 tab", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_DAY_2_TAB_XPATH, "play mode day 2 tab", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_LEFT_SIDEBAR_XPATH, "play mode left sidebar", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_EDIT_ROUTE_XPATH, "play mode edit route entry", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_ROUTE_INTRO_XPATH, "play mode route intro entry", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_LOCATION_BUTTON_XPATH, "play mode location button", timeout=timeout)

    def wait_play_mode_map_and_drawer(self, *, timeout: float = 8) -> None:
        """Verify play mode map and bottom route drawer are visible."""
        self.wait_xpath(self.MAP_VIEW_XPATH, "play mode map background", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_TAB_BAR_XPATH, "play mode day tab bar", timeout=timeout)
        self.wait_xpath(self.PLAY_MODE_BOTTOM_DRAWER_XPATH, "play mode bottom drawer", timeout=timeout)

    def tap_play_mode_left_sidebar_content(self, *, timeout: float = 8) -> None:
        """Tap the first content item in the play-mode left sidebar."""
        sidebar = self.wait_xpath(
            self.PLAY_MODE_LEFT_SIDEBAR_XPATH,
            "play mode left sidebar",
            timeout=timeout,
        )
        bounds = sidebar.getBounds()
        x = (int(bounds.left) + int(bounds.right)) // 2
        y = int(bounds.top) + int((int(bounds.bottom) - int(bounds.top)) * 0.22)
        self.driver.click((x, y))
        time.sleep(1.2)

    def tap_play_mode_day_1_tab(self, *, timeout: float = 8) -> None:
        """Switch play mode to day 1."""
        self.tap_xpath(self.PLAY_MODE_DAY_1_TAB_XPATH, "play mode day 1 tab", timeout=timeout)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_day_2_tab(self, *, timeout: float = 8) -> None:
        """Switch play mode to day 2."""
        self.tap_xpath(self.PLAY_MODE_DAY_2_TAB_XPATH, "play mode day 2 tab", timeout=timeout)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_overview_tab(self, *, timeout: float = 8) -> None:
        """Switch play mode back to overview."""
        self.tap_xpath(self.PLAY_MODE_OVERVIEW_TAB_XPATH, "play mode overview tab", timeout=timeout)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_day_1_bubble(self, *, timeout: float = 8) -> None:
        """Tap the day 1 bubble rendered on the map and wait for day 1 view."""
        self.driver.click(self.PLAY_MODE_DAY_1_BUBBLE_CENTER)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_location_button(self, *, timeout: float = 8) -> None:
        """Tap the play-mode location button and wait for the map to settle."""
        button = self.find_xpath(self.PLAY_MODE_LOCATION_BUTTON_XPATH)
        if button is not None:
            button.click()
        else:
            self.driver.click(self.PLAY_MODE_LOCATION_BUTTON_CENTER)
        time.sleep(1.5)
        self.wait_xpath(self.MAP_VIEW_XPATH, "play mode map background", timeout=timeout)

    def wait_play_mode_poi_detail(self, poi_name: str, *, timeout: float = 8) -> None:
        """Verify a play-mode POI detail card is open for the expected POI."""
        self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "play mode POI detail card", timeout=timeout)
        self.wait_xpath(
            self.play_mode_poi_title_xpath(poi_name),
            f"play mode POI detail title {poi_name}",
            timeout=timeout,
        )
        self.wait_xpath(self.POI_DETAIL_TAG_XPATH, "play mode POI detail tag", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_RATING_XPATH, "play mode POI detail rating", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_GALLERY_XPATH, "play mode POI detail gallery", timeout=timeout)

    def _is_play_mode_poi_detail_open_for(self, poi_name: str) -> bool:
        return (
            self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is not None
            and self.find_xpath(self.play_mode_poi_title_xpath(poi_name)) is not None
        )

    def close_play_mode_poi_detail(self, *, timeout: float = 8) -> None:
        """Close a play-mode POI detail card and return to the full-screen map."""
        self.tap_xpath(self.POI_DETAIL_CLOSE_XPATH, "play mode POI detail close button", timeout=timeout)
        time.sleep(1)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_poi_2_bubble(self, *, timeout: float = 8) -> None:
        """Tap the No.2 map bubble and wait for its POI detail card."""
        for point in self.PLAY_MODE_POI_2_BUBBLE_CANDIDATES:
            self.driver.click(point)
            time.sleep(1.2)
            if self._is_play_mode_poi_detail_open_for(self.PLAY_MODE_POI_2_NAME):
                self.wait_play_mode_poi_detail(self.PLAY_MODE_POI_2_NAME, timeout=timeout)
                return
            if self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is not None:
                self.close_play_mode_poi_detail(timeout=timeout)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] failed to open No.2 POI bubble detail "
            f"for {self.PLAY_MODE_POI_2_NAME}"
        )

    def tap_play_mode_axis_poi_3(self, *, timeout: float = 8) -> None:
        """Tap the No.3 POI in the bottom itinerary axis."""
        poi_axis = self.find_xpath(self.play_mode_axis_poi_xpath(self.PLAY_MODE_POI_3_NAME))
        if poi_axis is not None:
            poi_axis.click()
        else:
            self.driver.click(self.PLAY_MODE_AXIS_POI_3_CENTER)
        time.sleep(1.2)
        self.wait_play_mode_poi_detail(self.PLAY_MODE_POI_3_NAME, timeout=timeout)

    def exit_play_mode(self, route_name: str, *, timeout: float = 8) -> None:
        """Exit play mode and wait until the route half-modal card is restored."""
        self.tap_xpath(
            self.PLAY_MODE_EXIT_BUTTON_XPATH,
            "play mode exit button",
            timeout=timeout,
        )
        time.sleep(1)
        self.wait_xpath(self.overview_title_xpath(route_name), "route overview card", timeout=timeout)
        self.wait_xpath(self.BOTTOM_PANEL_XPATH, "route half modal bottom panel", timeout=timeout)
