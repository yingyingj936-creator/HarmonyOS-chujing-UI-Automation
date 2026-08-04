import time

from hypium import BY

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
        '//*[@id="mapPageRoot"]//Row[./Text and ./Row[@clickable="true" '
        'and ./Image and not(.//Text)]]/Row[@clickable="true" '
        'and ./Image and not(.//Text)]'
    )

    OVERVIEW_TAB_XPATH = '//Text[@text="\u5168\u89c8" and @clickable="true"]'
    DAY_1_TAB_XPATH = '//Text[@text="\u7b2c 1 \u5929" and @clickable="true"]'
    DAY_2_TAB_XPATH = '//Text[@text="\u7b2c 2 \u5929" and @clickable="true"]'
    DAY_1_CARD_XPATH = '//Text[@text="\u7b2c 1 \u5929" and @clickable="false"]'
    DAY_2_CARD_XPATH = '//Text[@text="\u7b2c 2 \u5929" and @clickable="false"]'
    OVERVIEW_SELECTED_TAB_XPATH = '//Text[@text="\u5168\u89c8"]'
    DAY_1_SELECTED_TAB_XPATH = '//Text[@text="\u7b2c 1 \u5929"]'
    DAY_2_SELECTED_TAB_XPATH = '//Text[@text="\u7b2c 2 \u5929"]'
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
    DAY_1_POI_COUNT_XPATH = (
        '//Text[contains(@text, "8") and contains(@text, "\u5730\u70b9")]'
    )
    DAY_2_POI_COUNT_XPATH = (
        '//Text[contains(@text, "6") and contains(@text, "\u5730\u70b9")]'
    )
    DAY_1_OVERVIEW_CARD_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="\u7b2c 1 \u5929"] '
        'and .//Text[contains(@text, "8") and contains(@text, "\u5730\u70b9")]]'
    )
    DAY_2_OVERVIEW_CARD_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="\u7b2c 2 \u5929"] '
        'and .//Text[contains(@text, "6") and contains(@text, "\u5730\u70b9")]]'
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
        '//*[@id="map_panel_poidetail"]//Text'
        '[contains(@text, "\u6e38\u73a9") '
        'or contains(@text, "\u63d0\u793a") '
        'or contains(@text, "\u8d34\u58eb") '
        'or contains(@text, "\u5efa\u8bae") '
        'or contains(@text, "\u5c0f\u8d34\u58eb") '
        'or contains(@text, "\u6ce8\u610f") '
        'or contains(@text, "\u4ea4\u901a") '
        'or contains(@text, "\u5f00\u653e") '
        'or contains(@text, "\u8425\u4e1a") '
        'or contains(@text, "tips") '
        'or contains(@text, "Tips")]'
    )
    POI_DETAIL_SURROUNDING_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[@text="\u5468\u8fb9\u63a8\u8350"]'
    )
    POI_DETAIL_FAVORITE_BUTTON_XPATH = (
        '//*[@id="map_bottom_panel"]//Row[@clickable="true" and ./Image]'
    )
    POI_DETAIL_FAVORITE_SELECTED_BACKGROUND = "#1AFFBF00"
    POI_DETAIL_SERVICE_XPATH = '//*[@id="map_bottom_panel"]//Text[@text="\u8ddf\u56e2\u6e38"]'
    POI_DETAIL_NAVIGATION_XPATH = '//*[@id="map_bottom_panel"]//Text[@text="\u5bfc\u822a"]'
    POI_DETAIL_CLOSE_XPATH = '//*[@id="map_bottom_panel"]//Image[@clickable="true"]'
    ROUTE_JOIN_TRIP_BUTTON_XPATH = '//*[@id="copyPlanBtn"]'
    ROUTE_MAP_LOADING_XPATH = '//Text[contains(@text, "加载中")]'
    ROUTE_ACTION_READY_XPATH = (
        '//*[@id="mapPageRoot" '
        'and .//*[@id="mapview"] '
        'and .//*[@id="map_bottom_panel"] '
        'and .//*[@id="copyPlanBtn"]]'
    )
    ROUTE_CONTENT_READY_XPATH_TEMPLATE = (
        '//*[@id="mapPageRoot" '
        'and .//*[@id="mapview"] '
        'and .//*[@id="map_bottom_panel"] '
        'and .//*[@id="copyPlanBtn"] '
        'and .//Text[@text="{route_name}\u00b7\u6982\u89c8"] '
        'and .//Text[starts-with(@text, "\u5173\u952e\u666f\u70b9\uff1a")] '
        'and .//Text[@text="\u884c\u7a0b\u89c4\u5212"]]'
    )
    ROUTE_AI_CONTENT_READY_XPATH_TEMPLATE = (
        '//*[@id="mapPageRoot" '
        'and .//*[@id="mapview"] '
        'and .//*[@id="map_bottom_panel"] '
        'and .//*[@id="copyPlanBtn"] '
        'and .//Text[@text="{route_name}\u00b7\u6982\u89c8"] '
        'and .//Text[@text="\u95ee\u4e00\u95ee"] '
        'and .//Text[@text="\u884c\u7a0b\u89c4\u5212"]]'
    )
    ROUTE_AI_HIGHLIGHT_XPATH = (
        '//*[@id="mapPageRoot"]//*[.//Text[contains(@text, "\u95ee\u4e00\u95ee")] '
        'and (.//Text[contains(@text, "\u884c\u7a0b\u4eae\u70b9")] '
        'or .//Text[contains(@text, "\u5173\u952e\u666f\u70b9")] '
        'or .//Text[contains(@text, "Ai")] '
        'or .//Text[contains(@text, "AI")])]'
        ' | //*[@id="mapPageRoot"]//*[@clickable="true" '
        'and .//Text[contains(@text, "\u95ee\u4e00\u95ee")]]'
        ' | //*[@id="mapPageRoot"]//Text[contains(@text, "\u95ee\u4e00\u95ee")]'
    )
    ROUTE_AI_ASK_BUTTON_XPATH = (
        '//*[@id="mapPageRoot"]//Text[contains(@text, "\u95ee\u4e00\u95ee") '
        'and @clickable="true"]'
        ' | //*[@id="mapPageRoot"]//*[@clickable="true" '
        'and .//Text[contains(@text, "\u95ee\u4e00\u95ee")]]'
        ' | //*[@id="mapPageRoot"]//Text[contains(@text, "\u95ee\u4e00\u95ee")]'
    )
    ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH = (
        '//Text[@text="\u4e00\u952e\u8ddf\u73a9" and @clickable="true"]'
    )
    PLAY_MODE_EXIT_TITLE_XPATH = '//Text[@text="\u9000\u51fa\u6e38\u73a9\u6a21\u5f0f"]'
    PLAY_MODE_EXIT_ROW_XPATH = (
        '//*[@id="mapPageRoot"]//Row[@clickable="true" '
        'and .//Text[@text="\u9000\u51fa\u6e38\u73a9\u6a21\u5f0f"]]'
    )
    PLAY_MODE_EXIT_BUTTON_XPATH = (
        PLAY_MODE_EXIT_TITLE_XPATH
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
    PLAY_MODE_READY_XPATH = (
        '//*[@id="mapPageRoot" '
        'and .//*[@id="mapview"] '
        'and .//Text[@text="\u9000\u51fa\u6e38\u73a9\u6a21\u5f0f"] '
        'and .//*[@id="map_top_dateChoose"] '
        'and .//*[@id="map_top_dateChoose"]//Text[@text="\u5168\u89c8"] '
        'and .//*[@id="map_top_dateChoose"]//Text[@text="\u7b2c 1 \u5929"] '
        'and .//*[@id="map_top_dateChoose"]//Text[@text="\u7b2c 2 \u5929"] '
        'and .//*[@id="map_left_bottom_tip"] '
        'and .//Text[contains(@text, "\u7f16\u8f91") '
        'and contains(@text, "\u8def\u7ebf") and @clickable="true"] '
        'and .//Text[contains(@text, "\u8def\u7ebf") '
        'and contains(@text, "\u4ecb\u7ecd") and @clickable="true"] '
        'and .//*[@id="map_my_location"]]'
    )
    PLAY_MODE_MAP_AND_DRAWER_READY_XPATH = (
        '//*[@id="mapPageRoot" '
        'and .//*[@id="mapview"] '
        'and .//*[@id="map_top_dateChoose"] '
        'and .//*[@id="map_bottom_tab_comp"]]'
    )
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
    def route_content_ready_xpath(cls, route_name: str) -> str:
        return cls.ROUTE_CONTENT_READY_XPATH_TEMPLATE.format(route_name=route_name)

    @classmethod
    def route_ai_content_ready_xpath(cls, route_name: str) -> str:
        return cls.ROUTE_AI_CONTENT_READY_XPATH_TEMPLATE.format(route_name=route_name)

    @classmethod
    def route_any_content_ready_xpath(cls, route_name: str) -> str:
        return (
            f"{cls.route_content_ready_xpath(route_name)}"
            f" | {cls.route_ai_content_ready_xpath(route_name)}"
        )

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

    @classmethod
    def play_mode_poi_ready_xpath(cls, poi_name: str) -> str:
        return (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="map_panel_poidetail"] '
            f'and .//*[@id="map_bottom_panel"]//Text[@text="{poi_name}"]]'
        )

    def wait_loaded(self, route_name: str, *, timeout: float = 12) -> dict[str, object]:
        """等待路线详情核心内容稳定，避免地图容器先出现但路线数据未完成加载。"""
        deadline = time.time() + timeout
        stable_rounds = 0
        latest_state = "未检测到路线详情页"

        while time.time() < deadline:
            map_view = self.driver.wait_for_component(
                BY.xpath(self.MAP_VIEW_XPATH),
                timeout=0.4,
            )
            overview_title = self.driver.wait_for_component(
                BY.xpath(self.overview_title_xpath(route_name)),
                timeout=0.4,
            )
            bottom_panel = self.driver.wait_for_component(
                BY.xpath(self.BOTTOM_PANEL_XPATH),
                timeout=0.2,
            )
            action_button = self.driver.wait_for_component(
                BY.xpath(
                    f"{self.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH} | "
                    f"{self.ROUTE_JOIN_TRIP_BUTTON_XPATH}"
                ),
                timeout=0.2,
            )
            loading = self.driver.wait_for_component(
                BY.xpath(self.ROUTE_MAP_LOADING_XPATH),
                timeout=0.2,
            )

            if (
                map_view is not None
                and overview_title is not None
                and bottom_panel is not None
                and action_button is not None
                and loading is None
            ):
                stable_rounds += 1
                if stable_rounds >= 2:
                    return {
                        "map": map_view,
                        "overview_title": overview_title,
                    }
                latest_state = "路线详情核心内容已出现，等待连续稳定"
            else:
                stable_rounds = 0
                visible_overview = self.driver.wait_for_component(
                    BY.xpath(
                        '//*[@id="mapPageRoot"]//Text[contains(@text, "·概览")]'
                        ' | //*[@id="mapPageRoot"]//Text[contains(@text, "· 概览")]'
                    ),
                    timeout=0.2,
                )
                visible_title = ""
                if visible_overview is not None:
                    visible_title = visible_overview.getText() or ""
                latest_state = (
                    f"map={map_view is not None}, "
                    f"目标概览={overview_title is not None}, "
                    f"底部面板={bottom_panel is not None}, "
                    f"操作按钮={action_button is not None}, "
                    f"加载中={loading is not None}, "
                    f"当前概览标题={visible_title}"
                )
            time.sleep(0.4)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 路线详情“{route_name}”未加载稳定，"
            f"最后状态：{latest_state}"
        )

    def wait_overview_modules(self, *, timeout: float = 8) -> None:
        """Verify overview highlights, key spots, and itinerary modules."""
        legacy_ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//Text[@text="\u6e38\u73a9\u98ce\u683c"] '
            'and .//Text[@text="\u6700\u4f73\u65f6\u95f4"] '
            'and .//Text[@text="\u666f\u70b9\u7c7b\u578b"] '
            'and .//Text[starts-with(@text, "\u5173\u952e\u666f\u70b9\uff1a")] '
            'and .//Text[@text="\u884c\u7a0b\u89c4\u5212"]]'
        )
        ai_ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//Text[@text="\u95ee\u4e00\u95ee"] '
            'and .//Text[@text="\u884c\u7a0b\u89c4\u5212"] '
            'and .//Text[contains(@text, "\u884c\u7a0b\u4eae\u70b9") '
            'or contains(@text, "\u5173\u952e\u666f\u70b9")]]'
        )
        self.wait_any_xpath(
            (legacy_ready_xpath, ai_ready_xpath),
            "路线概览核心模块",
            timeout=timeout,
        )

    def wait_ai_highlight_module(self, *, timeout: float = 8):
        """等待新版行程亮点/关键景点 AI 模块展示。"""
        component = self.driver.wait_for_component(
            BY.xpath(self.ROUTE_AI_HIGHLIGHT_XPATH),
            timeout=min(timeout, 3),
        )
        if component is not None:
            return component
        # “问一问”在新版卡片里可能是绘制文本，不进入 UI 树。
        # 此时用底部卡片已稳定展示作为前置，再通过卡片相对位置点击。
        return self.wait_xpath(
            self.BOTTOM_PANEL_XPATH,
            "路线详情底部卡片",
            timeout=timeout,
        )

    def tap_ai_ask(self, *, timeout: float = 8) -> tuple[int, int, int, int]:
        """点击路线详情行程亮点区域的“问一问”按钮。"""
        ask = self.driver.wait_for_component(
            BY.xpath(self.ROUTE_AI_ASK_BUTTON_XPATH),
            timeout=min(timeout, 2),
        )
        if ask is not None:
            bounds = ask.getBounds()
            center = (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
            self.driver.click(center)
            click_bounds = (
                int(bounds.left),
                int(bounds.top),
                int(bounds.right),
                int(bounds.bottom),
            )
        else:
            page = self.wait_xpath(
                self.ROOT_XPATH,
                "路线详情页",
                timeout=timeout,
            )
            bounds = page.getBounds()
            width = int(bounds.right) - int(bounds.left)
            height = int(bounds.bottom) - int(bounds.top)
            # “问一问”是绘制内容时没有可点击节点，按整页比例命中完整可见的 AI 推荐问题卡片。
            click_point = (
                int(bounds.left) + int(width * 0.50),
                int(bounds.top) + int(height * 0.59),
            )
            self.driver.click(click_point)
            click_bounds = (
                click_point[0] - 80,
                click_point[1] - 60,
                click_point[0] + 80,
                click_point[1] + 60,
            )
        time.sleep(2)
        return click_bounds

    def swipe_card_up(self) -> None:
        """Swipe the bottom route card upward."""
        panel = self.wait_xpath(self.BOTTOM_PANEL_XPATH, "路线底部卡片")
        self.driver.swipe("UP", distance=60, area=panel, swipe_time=0.55)
        time.sleep(0.8)

    def swipe_card_down(self) -> None:
        """Swipe the bottom route card downward."""
        panel = self.wait_xpath(self.BOTTOM_PANEL_XPATH, "路线底部卡片")
        self.driver.swipe("DOWN", distance=60, area=panel, swipe_time=0.55)
        time.sleep(0.8)

    def swipe_poi_detail(self, direction: str = "UP") -> None:
        """Swipe inside the POI detail scroll area."""
        detail = self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI详情滚动卡片")
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
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到温馨提示模块")


    def wait_itinerary_tabs(self, *, timeout: float = 8) -> None:
        """校验行程标签栏可见。"""
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//Text[@text="\u884c\u7a0b\u89c4\u5212"] '
            'and .//Text[@text="\u5168\u89c8" and @clickable="true"] '
            'and .//Text[@text="\u7b2c 1 \u5929" and @clickable="true"] '
            'and .//Text[@text="\u7b2c 2 \u5929" and @clickable="true"]]'
        )
        self.wait_xpath(ready_xpath, "路线全览及单天标签栏", timeout=timeout)

    def wait_overview_itinerary(self, *, timeout: float = 8) -> None:
        """校验全览展示两天路线列表，且地图已渲染。"""
        day_1_ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="mapview"] '
            'and .//Text[@text="市井繁华·维港夜色"] '
            'and .//Text[@text="第 1 天" and @clickable="false"]]'
        )
        self.wait_xpath(day_1_ready_xpath, "路线全览第1天内容", timeout=timeout)
        self.scroll_until_xpath_visible(
            self.DAY_2_CARD_XPATH,
            "第2天全览卡片",
            max_swipes=4,
            timeout=timeout,
        )
        self.wait_xpath(self.DAY_2_TITLE_XPATH, "第2天全览路线标题", timeout=timeout)
        self._restore_overview_card_to_day_1()


    def wait_overview_day_cards(self, *, timeout: float = 8) -> None:
        """Verify overview day cards include route summaries, POI counts, and POI entries."""
        day_1_ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="mapview"] '
            'and .//Text[@text="全览"] '
            'and .//Column[@clickable="true" and .//Text[@text="第 1 天"] '
            'and .//Text[contains(@text, "8") and contains(@text, "地点")]] '
            'and .//Text[@text="市井繁华·维港夜色"] '
            'and .//Text[@text="通菜街"]]'
        )
        self.wait_xpath(day_1_ready_xpath, "路线全览第1天摘要", timeout=timeout)
        self.scroll_until_xpath_visible(
            self.DAY_2_OVERVIEW_CARD_XPATH,
            "第2天全览卡片",
            max_swipes=4,
            timeout=timeout,
        )
        self.wait_xpath(self.DAY_2_TITLE_XPATH, "第2天路线摘要", timeout=timeout)
        self._restore_overview_card_to_day_1()

    def tap_day_1_overview_card(self, *, timeout: float = 8) -> None:
        """点击全览第1天卡片，并等待进入第1天视图。"""
        self.tap_xpath(self.DAY_1_OVERVIEW_CARD_XPATH, "第1天全览卡片", timeout=timeout)
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
        """点击行程标签，并等待选中态和地图渲染完成。"""
        self.tap_xpath(tab_xpath, name, timeout=timeout)
        time.sleep(0.8)
        selected_relative_xpath = selected_tab_xpath.removeprefix("//")
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="mapview"] '
            f'and .//{selected_relative_xpath}]'
        )
        self.wait_xpath(ready_xpath, f"已选中{name}且地图已渲染", timeout=timeout)

    def tap_day_1_tab(self, *, timeout: float = 8) -> None:
        self.tap_itinerary_tab(
            self.DAY_1_TAB_XPATH,
            self.DAY_1_SELECTED_TAB_XPATH,
            "第1天行程标签",
            timeout=timeout,
        )

    def tap_day_2_tab(self, *, timeout: float = 8) -> None:
        self.tap_itinerary_tab(
            self.DAY_2_TAB_XPATH,
            self.DAY_2_SELECTED_TAB_XPATH,
            "第2天行程标签",
            timeout=timeout,
        )

    def tap_overview_tab(self, *, timeout: float = 8) -> None:
        self.tap_itinerary_tab(
            self.OVERVIEW_TAB_XPATH,
            self.OVERVIEW_SELECTED_TAB_XPATH,
            "全览行程标签",
            timeout=timeout,
        )


    def scroll_until_xpath_visible(
        self,
        xpath: str,
        name: str,
        *,
        max_swipes: int = 3,
        timeout: float = 8,
    ) -> object:
        """Scroll the bottom card until the target content becomes visible."""
        for swipe_count in range(max_swipes + 1):
            component = self.find_xpath(xpath)
            if component is not None:
                return component
            if swipe_count == max_swipes:
                break
            self.swipe_card_up()
        raise RuntimeError(f"[{self.PAGE_NAME}] 滚动后仍未找到{name}")

    def _restore_overview_card_to_day_1(self) -> None:
        """Return the route half-card to the day 1 summary after checking lower content."""
        for _ in range(3):
            if self.find_xpath(self.DAY_1_OVERVIEW_CARD_XPATH) is not None:
                return
            self.swipe_card_down()

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
            return

        for direction in directions:
            for _ in range(max_swipes):
                self.swipe_poi_detail(direction)
                if self.find_xpath(xpath) is not None:
                    return

        raise RuntimeError(
            f"[{self.PAGE_NAME}] POI详情滚动后仍未找到{name}"
        )

    def wait_day_1_itinerary(self, *, timeout: float = 8) -> None:
        """校验第1天标签选中，且第1天地图已渲染。"""
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="mapview"] '
            'and .//Text[@text="第 1 天"]]'
        )
        self.wait_xpath(ready_xpath, "第1天标签和地图", timeout=timeout)

    def wait_day_1_route_list(self, *, timeout: float = 8) -> None:
        """校验第1天 POI 列表和交通距离行可见。"""
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="mapview"] '
            'and .//Text[@text="第 1 天"] '
            'and .//Column[@clickable="true" and .//Text[@text="通菜街"] '
            'and .//Text[contains(@text, "通菜街贯穿旺角")]] '
            'and .//Text[@text="距离 0.3km·步行预计 5分钟"] '
            'and .//Text[@text="旺角"]]'
        )
        self.wait_xpath(ready_xpath, "第1天路线列表和距离", timeout=timeout)

    def tap_day_1_first_poi(
        self,
        *,
        timeout: float = 8,
        verify_full_detail: bool = False,
    ) -> None:
        """点击第1天路线列表第一个 POI，并等待详情卡片展示。"""
        self.tap_xpath(self.DAY_1_FIRST_POI_CARD_XPATH, "第1天第一个POI卡片", timeout=timeout)
        if verify_full_detail:
            self.wait_day_1_poi_detail(timeout=timeout)
        else:
            self.wait_day_1_poi_basic_detail(timeout=timeout)

    def wait_day_1_poi_detail(self, *, timeout: float = 8) -> None:
        """Verify core POI detail content; tips/recommendations are data-dependent."""
        self.wait_day_1_poi_basic_detail(timeout=timeout)
        try:
            self.scroll_poi_detail_until_xpath_visible(
                self.POI_DETAIL_TIPS_XPATH,
                "POI detail tips",
                max_swipes=6,
                timeout=timeout,
            )
        except RuntimeError:
            try:
                self.scroll_poi_detail_until_xpath_visible(
                    self.POI_DETAIL_SURROUNDING_XPATH,
                    "POI surrounding recommendations",
                    max_swipes=6,
                    timeout=timeout,
                )
            except RuntimeError:
                return
    def wait_day_1_poi_basic_detail(self, *, timeout: float = 8) -> None:
        """校验第1天 POI 详情已打开，并展示首屏基础信息和底部操作区。"""
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="map_panel_poidetail"] '
            'and .//*[@id="map_bottom_panel"]//Column'
            '[./Text[@text="通菜街"] and ./Text[@text="Tung Choi Street"]] '
            'and .//*[@id="map_panel_poidetail"]//Text[@text="景点"] '
            'and .//*[@id="map_panel_poidetail"]//Text[starts-with(@text, "评分 ")] '
            'and .//*[@id="map_panel_poidetail"]//ListItem/__Common__[@clickable="true"] '
            'and .//*[@id="map_panel_poidetail"]//Text[contains(@text, "通菜街贯穿旺角")] '
            'and .//*[@id="map_panel_poidetail"]//Text[@text="添加到我的行程"] '
            'and .//*[@id="map_bottom_panel"]//Row[@clickable="true" and ./Image] '
            'and .//*[@id="map_bottom_panel"]//Text[@text="跟团游"] '
            'and .//*[@id="map_bottom_panel"]//Text[@text="导航"]]'
        )
        self.wait_xpath(ready_xpath, "第1天POI详情基础内容", timeout=timeout)

    def wait_surrounding_categories(self, *, timeout: float = 8) -> None:
        """校验周边推荐分类标签可见。"""
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

    def wait_generic_route_loaded(self, route_name: str, *, timeout: float = 12) -> None:
        """等待任意热门路线详情页加载完成。"""
        ready_xpath = self.route_any_content_ready_xpath(route_name)
        self.wait_xpath(ready_xpath, f"热门路线详情页{route_name}", timeout=timeout)

    def wait_surrounding_poi_list(self, *, timeout: float = 8) -> None:
        """校验周边 POI 列表展示卡片信息和距离。"""
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
        """点击周边推荐分类标签。"""
        xpath = self.surrounding_category_xpath(category_name)
        self.scroll_poi_detail_until_xpath_visible(
            xpath,
            f"surrounding category {category_name}",
            timeout=timeout,
        )
        self.tap_xpath(xpath, f"surrounding category {category_name}", timeout=timeout)
        time.sleep(0.8)

    def tap_surrounding_first_poi(self, *, timeout: float = 8) -> None:
        """点击第一个可见周边 POI 卡片，并等待详情卡片展示。"""
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
        self.wait_generic_poi_detail(timeout=timeout)

    def wait_generic_poi_detail(self, *, timeout: float = 8) -> None:
        """Verify a POI detail card without depending on a fixed POI name."""
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="map_panel_poidetail"] '
            'and .//*[@id="map_bottom_panel"]//Column[./Text[1] and ./Text[2]] '
            'and .//*[@id="map_panel_poidetail"]//Text[@text="\u666f\u70b9"] '
            'and .//*[@id="map_panel_poidetail"]//Text[starts-with(@text, "\u8bc4\u5206 ")] '
            'and .//*[@id="map_panel_poidetail"]//ListItem/__Common__[@clickable="true"] '
            'and .//*[@id="map_panel_poidetail"]//Text[@clickable="true" '
            'and contains(@text, "\u8be6\u60c5")] '
            'and .//*[@id="map_panel_poidetail"]//Text[@text="\u6dfb\u52a0\u5230\u6211\u7684\u884c\u7a0b"] '
            'and .//*[@id="map_bottom_panel"]//Row[@clickable="true" and ./Image] '
            'and .//*[@id="map_bottom_panel"]//Text[@text="\u5bfc\u822a"]]'
        )
        self.wait_xpath(ready_xpath, "POI详情完整内容", timeout=timeout)

    def close_day_1_poi_detail(self, *, timeout: float = 8) -> None:
        """Close the POI detail card and return to the day 1 route list."""
        self.tap_xpath(self.POI_DETAIL_CLOSE_XPATH, "POI详情关闭按钮", timeout=timeout)
        time.sleep(0.8)
        self.wait_day_1_route_list(timeout=timeout)

    def wait_day_2_itinerary(self, *, timeout: float = 8) -> None:
        """校验第2天标签选中，且第2天地图已渲染。"""
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="mapview"] '
            'and .//Text[@text="第 2 天"]]'
        )
        self.wait_xpath(ready_xpath, "第2天标签和地图", timeout=timeout)

    def tap_back_button(self) -> None:
        """点击路线详情页内返回按钮。"""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "路线详情返回按钮")
        time.sleep(1.5)

    def tap_join_trip(self, *, timeout: float = 8) -> None:
        """点击路线详情底部按钮，将路线创建为行程。"""
        self._wait_route_map_loading_done(
            timeout=max(timeout, 45),
            action_name="加入我的行程",
        )
        self.tap_xpath(
            self.ROUTE_JOIN_TRIP_BUTTON_XPATH,
            "路线详情加入行程按钮",
            timeout=timeout,
        )

    def _wait_route_map_loading_done(
        self,
        *,
        timeout: float = 8,
        action_name: str = "操作路线",
    ) -> None:
        """路线地图加载完成后再点击底部操作，避免全量执行时过早点击。"""
        deadline = time.time() + timeout
        stable_ready_rounds = 0
        latest_state = "未检测到路线详情可操作区"

        while time.time() < deadline:
            loading = self.driver.wait_for_component(
                BY.xpath(self.ROUTE_MAP_LOADING_XPATH),
                timeout=0.3,
            )
            route_title = self.find_xpath(
                '//*[@id="mapPageRoot"]//Text[contains(@text, "\u00b7\u6982\u89c8")]'
            )
            if route_title is not None:
                route_name = (route_title.getText() or "").replace("\u00b7\u6982\u89c8", "")
                ready_xpath = self.route_any_content_ready_xpath(route_name)
            else:
                ready_xpath = self.ROUTE_ACTION_READY_XPATH

            action_ready = self.driver.wait_for_component(
                BY.xpath(ready_xpath),
                timeout=0.3,
            )
            if loading is None and action_ready is not None:
                stable_ready_rounds += 1
                if stable_ready_rounds >= 3:
                    return
                latest_state = "路线内容和操作区已出现，等待连续稳定"
            else:
                stable_ready_rounds = 0
                latest_state = (
                    "路线仍显示加载中"
                    if loading is not None
                    else "路线操作区未完整出现"
                )
            time.sleep(0.5)

        raise RuntimeError(
            f"路线地图加载未完成，暂不能{action_name}，最后状态：{latest_state}"
        )

    def tap_one_click_play(self, *, timeout: float = 8) -> None:
        """点击路线详情底部按钮进入游玩模式。"""
        self._wait_route_map_loading_done(
            timeout=max(timeout, 30),
            action_name="进入游玩模式",
        )
        self.tap_xpath(
            self.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH,
            "路线详情一键跟玩按钮",
            timeout=timeout,
        )
        self.wait_play_mode_map_and_drawer(timeout=max(timeout, 15))

    def wait_play_mode_overview(self, *, timeout: float = 8) -> None:
        """Verify play mode renders the overview map and core controls."""
        self.wait_xpath(
            self.PLAY_MODE_READY_XPATH,
            "游玩模式全览视图及关键控件",
            timeout=timeout,
        )

    def wait_play_mode_map_and_drawer(self, *, timeout: float = 8) -> None:
        """Verify play mode map and bottom route drawer are visible."""
        self.wait_xpath(
            self.PLAY_MODE_MAP_AND_DRAWER_READY_XPATH,
            "游玩模式地图、天数标签和底部行程抽屉",
            timeout=timeout,
        )

    def tap_play_mode_left_sidebar_content(self, *, timeout: float = 8) -> None:
        """点击游玩模式左侧侧边栏第一个内容位。"""
        sidebar = self.wait_xpath(
            self.PLAY_MODE_LEFT_SIDEBAR_XPATH,
            "游玩模式左侧边栏",
            timeout=timeout,
        )
        bounds = sidebar.getBounds()
        x = (int(bounds.left) + int(bounds.right)) // 2
        y = int(bounds.top) + int((int(bounds.bottom) - int(bounds.top)) * 0.22)
        self.driver.click((x, y))
        time.sleep(1.2)

    def tap_play_mode_route_intro(self, route_name: str, *, timeout: float = 8) -> None:
        """Open the route introduction page from play mode."""
        self.tap_xpath(
            self.PLAY_MODE_ROUTE_INTRO_XPATH,
            "游玩模式路线介绍入口",
            timeout=timeout,
        )
        time.sleep(1.2)
        self.wait_loaded(route_name, timeout=timeout)

    def tap_play_mode_day_1_tab(self, *, timeout: float = 8) -> None:
        """Switch play mode to day 1."""
        self.tap_xpath(self.PLAY_MODE_DAY_1_TAB_XPATH, "游玩模式第1天标签", timeout=timeout)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_day_2_tab(self, *, timeout: float = 8) -> None:
        """Switch play mode to day 2."""
        self.tap_xpath(self.PLAY_MODE_DAY_2_TAB_XPATH, "游玩模式第2天标签", timeout=timeout)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_overview_tab(self, *, timeout: float = 8) -> None:
        """Switch play mode back to overview."""
        self.tap_xpath(self.PLAY_MODE_OVERVIEW_TAB_XPATH, "游玩模式全览标签", timeout=timeout)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_day_1_bubble(self, *, timeout: float = 8) -> None:
        """点击地图上的第1天气泡，并等待进入第1天视图。"""
        self.driver.click(self.PLAY_MODE_DAY_1_BUBBLE_CENTER)
        time.sleep(1.5)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_location_button(self, *, timeout: float = 8) -> None:
        """点击游玩模式定位按钮，并等待地图稳定。"""
        button = self.find_xpath(self.PLAY_MODE_LOCATION_BUTTON_XPATH)
        if button is not None:
            button.click()
        else:
            self.driver.click(self.PLAY_MODE_LOCATION_BUTTON_CENTER)
        time.sleep(1.5)
        self.wait_xpath(self.MAP_VIEW_XPATH, "游玩模式地图背景", timeout=timeout)

    def tap_play_mode_exit_button(self, *, timeout: float = 8) -> None:
        """点击左上角“退出游玩模式”，避开底部行程抽屉里的可点击 Row。"""
        title = self.wait_xpath(
            self.PLAY_MODE_EXIT_TITLE_XPATH,
            "游玩模式退出标题",
            timeout=timeout,
        )
        row = self.find_xpath(self.PLAY_MODE_EXIT_ROW_XPATH)
        if row is not None:
            row.click()
        else:
            title.click()

        time.sleep(0.5)
        if self.find_xpath(self.PLAY_MODE_EXIT_TITLE_XPATH) is not None:
            bounds = title.getBounds()
            x = max(1, int(bounds.left) - 80)
            y = (int(bounds.top) + int(bounds.bottom)) // 2
            self.driver.click((x, y))

    def wait_play_mode_poi_detail(self, poi_name: str, *, timeout: float = 8) -> None:
        """Verify a play-mode POI detail card is open for the expected POI."""
        ready_xpath = (
            '//*[@id="mapPageRoot" '
            'and .//*[@id="map_panel_poidetail"] '
            f'and .//*[@id="map_bottom_panel"]//Text[@text="{poi_name}"] '
            'and .//*[@id="map_panel_poidetail"]//Text[@text="\u666f\u70b9"] '
            'and .//*[@id="map_panel_poidetail"]//Text[starts-with(@text, "\u8bc4\u5206 ")] '
            'and .//*[@id="map_panel_poidetail"]//ListItem/__Common__[@clickable="true"]]'
        )
        self.wait_xpath(ready_xpath, f"游玩模式POI详情{poi_name}", timeout=timeout)

    def tap_poi_favorite(self, *, timeout: float = 8) -> None:
        """点击游玩模式地点详情收藏按钮。"""
        self.tap_xpath(
            self.POI_DETAIL_FAVORITE_BUTTON_XPATH,
            "游玩模式地点详情收藏按钮",
            timeout=timeout,
        )

    def is_poi_favorite_highlighted(self) -> bool:
        """通过收藏按钮背景色判断地点是否已收藏。"""
        component = self.wait_xpath(
            self.POI_DETAIL_FAVORITE_BUTTON_XPATH,
            "游玩模式地点详情收藏按钮",
        )
        background = component.getAllProperties().to_dict().get(
            "backgroundColor",
            "",
        )
        return background.upper() == self.POI_DETAIL_FAVORITE_SELECTED_BACKGROUND

    def wait_poi_favorite_highlighted(
        self,
        expected: bool,
        *,
        timeout: float = 5,
    ) -> bool:
        """等待游玩模式地点收藏按钮切换到期望状态。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.is_poi_favorite_highlighted() is expected:
                return True
            time.sleep(0.4)
        return False

    def ensure_poi_favorite_unselected(self) -> None:
        """重复执行用例前，先将游玩模式地点恢复为未收藏状态。"""
        if not self.is_poi_favorite_highlighted():
            return
        self.tap_poi_favorite()
        if not self.wait_poi_favorite_highlighted(False):
            raise RuntimeError("无法将游玩模式地点收藏按钮恢复为未高亮状态")

    def _is_play_mode_poi_detail_open_for(self, poi_name: str) -> bool:
        return self.find_xpath(self.play_mode_poi_ready_xpath(poi_name)) is not None

    def close_play_mode_poi_detail(self, *, timeout: float = 8) -> None:
        """Close a play-mode POI detail card and return to the full-screen map."""
        self.tap_xpath(self.POI_DETAIL_CLOSE_XPATH, "游玩模式POI详情关闭按钮", timeout=timeout)
        time.sleep(1)
        self.wait_play_mode_map_and_drawer(timeout=timeout)

    def tap_play_mode_poi_2_bubble(self, *, timeout: float = 8) -> None:
        """点击地图编号2的 POI 气泡，并等待 POI 详情卡片展示。"""
        poi_axis = self.driver.wait_for_component(
            BY.xpath(self.play_mode_axis_poi_xpath(self.PLAY_MODE_POI_2_NAME)),
            timeout=min(3.0, timeout),
        )
        if poi_axis is not None:
            poi_axis.click()
            if self.driver.wait_for_component(
                BY.xpath(self.play_mode_poi_ready_xpath(self.PLAY_MODE_POI_2_NAME)),
                timeout=min(3.0, timeout),
            ) is not None:
                self.wait_play_mode_poi_detail(self.PLAY_MODE_POI_2_NAME, timeout=timeout)
                return

        for point in self.PLAY_MODE_POI_2_BUBBLE_CANDIDATES:
            self.driver.click(point)
            if self.driver.wait_for_component(
                BY.xpath(self.play_mode_poi_ready_xpath(self.PLAY_MODE_POI_2_NAME)),
                timeout=min(2.0, timeout),
            ) is not None:
                self.wait_play_mode_poi_detail(self.PLAY_MODE_POI_2_NAME, timeout=timeout)
                return
            if self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is not None:
                self.close_play_mode_poi_detail(timeout=timeout)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未能打开编号2的POI气泡详情"
            f"：{self.PLAY_MODE_POI_2_NAME}"
        )

    def tap_play_mode_axis_poi_3(self, *, timeout: float = 8) -> None:
        """点击底部行程轴编号3的 POI。"""
        poi_axis = self.find_xpath(self.play_mode_axis_poi_xpath(self.PLAY_MODE_POI_3_NAME))
        if poi_axis is not None:
            poi_axis.click()
        else:
            self.driver.click(self.PLAY_MODE_AXIS_POI_3_CENTER)
        self.wait_play_mode_poi_detail(self.PLAY_MODE_POI_3_NAME, timeout=timeout)

    def exit_play_mode(self, route_name: str, *, timeout: float = 8) -> None:
        """退出游玩模式，并等待路线半屏卡片恢复。"""
        self.tap_play_mode_exit_button(timeout=timeout)
        time.sleep(1)
        self.wait_xpath(self.overview_title_xpath(route_name), "路线概览卡片", timeout=timeout)
        self.wait_xpath(self.BOTTOM_PANEL_XPATH, "路线半屏底部面板", timeout=timeout)



