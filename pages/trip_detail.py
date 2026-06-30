import time

from hypium import BY

from pages.base_page import BasePage


class TripDetailPage(BasePage):
    PAGE_NAME = "TripDetailPage"
    ROOT_XPATH = '//*[@id="planPageRoot"]'
    BACK_BUTTON_XPATH = '//*[@id="planPageRoot"]//Row[@clickable="true" and ./Image]'
    TITLE_CONTAINER_XPATH = '//*[@id="routeName"]'
    RENAME_BUTTON_XPATH = (
        '//*[@id="routeName"]//*[@clickable="true" or @type="Image"]'
    )
    RENAME_TEXT_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "重命名")]'
    )
    RENAME_DIALOG_XPATH = '//Dialog[.//TextInput]'
    RENAME_INPUT_XPATH = '//Dialog//TextInput'
    RENAME_CONFIRM_BUTTON_XPATH = (
        '//Dialog//Text[@text="确定" or @text="保存" or @text="完成" or @text="确认"]'
    )
    RENAME_CANCEL_BUTTON_XPATH = (
        '//Dialog//Text[@text="取消" or @text="关闭"]'
    )
    DETAIL_SCROLL_XPATH = '//*[@id="planPageRoot"]//*[@scrollable="true"]'
    MAP_THUMBNAIL_XPATH = (
        '//*[@id="planPageRoot"]//*[@id="mapview" or @id="mapView" '
        'or @id="map_thumb" or @key="mapview" or @key="mapView" '
        'or @key="map_thumb"]'
    )
    VIEW_MAP_BUTTON_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "查看地图")]'
    )
    DAY_1_XPATH = (
        '//*[@id="planPageRoot"]//Text[@text="第 1 天" or @text="第1天" '
        'or @text="Day1" or contains(@text, "第 1 天") '
        'or contains(@text, "第1天")]'
    )
    DAY_2_XPATH = (
        '//*[@id="planPageRoot"]//Text[@text="第 2 天" or @text="第2天" '
        'or @text="Day2" or contains(@text, "第 2 天") '
        'or contains(@text, "第2天")]'
    )
    ROUTE_POI_ICON_XPATH = (
        '//*[@id="planPageRoot"]//*[contains(@id, "poi") or contains(@key, "poi") '
        'or @type="SymbolGlyph" or @type="Image"]'
    )
    ROUTE_DISTANCE_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "距离") '
        'or contains(@text, "km") or contains(@text, "分钟")]'
    )
    EDIT_TRIP_BUTTON_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "编辑行程")]'
    )
    FIRST_UNPLANNED_POI_XPATH_TEMPLATE = (
        '//*[@id="firstUnplannedPoi"]//Text[@text="{poi_name}"]'
    )
    ROUTE_POI_XPATH_TEMPLATE = (
        '//*[@id="planPageRoot"]//Text[@text="{poi_name}" '
        'or contains(@text, "{poi_name}")]'
    )
    SECOND_UNPLANNED_POI_XPATH_TEMPLATE = (
        '//*[@id="unplannedPoi_1"]//Text[@text="{poi_name}"]'
    )
    ROUTE_DAY_1_XPATH = (
        '//*[@id="planPageRoot"]//Text[@text="第 1 天" or @text="第1天" or @text="Day1"]'
    )
    ROUTE_DAY_2_XPATH = (
        '//*[@id="planPageRoot"]//Text[@text="第 2 天" or @text="第2天" or @text="Day2"]'
    )
    ROUTE_FIRST_POI_XPATH = '//*[@id="planPageRoot"]//Text[@text="通菜街"]'
    ROUTE_POI_COUNT_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "14") '
        'and (contains(@text, "地点") or contains(@text, "个"))]'
    )
    ANY_ROUTE_DAY_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "第") '
        'and contains(@text, "天")]'
    )
    ANY_ROUTE_POI_COUNT_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "地点") '
        'or contains(@text, "个")]'
    )
    ROOT_TEXT_XPATH = '//*[@id="planPageRoot"]//Text'
    POI_DETAIL_ROOT_XPATH = '//*[@id="map_panel_poidetail"]'
    POI_DETAIL_ENGLISH_NAME_XPATH_TEMPLATE = '//Text[@text="{english_name}"]'
    POI_DETAIL_TAG_XPATH = '//*[@id="map_panel_poidetail"]//Text[@text="景点"]'
    POI_DETAIL_RATING_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[starts-with(@text, "评分 ")]'
    )
    POI_DETAIL_GALLERY_XPATH = (
        '//*[@id="map_panel_poidetail"]//ListItem/__Common__[@clickable="true"]'
    )
    POI_DETAIL_INTRO_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[contains(@text, "详情")]'
    )
    POI_DETAIL_TIPS_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text'
        '[contains(@text, "游玩") '
        'or contains(@text, "提示") '
        'or contains(@text, "贴士") '
        'or contains(@text, "建议") '
        'or contains(@text, "注意") '
        'or contains(@text, "交通") '
        'or contains(@text, "开放") '
        'or contains(@text, "营业") '
        'or contains(@text, "tips") '
        'or contains(@text, "Tips")]'
    )
    POI_DETAIL_RECOMMEND_TITLE_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[@text="相关推荐"]'
    )
    POI_DETAIL_RECOMMEND_LIST_XPATH = '//*[@id="discovery_list_poidetail"]'

    @staticmethod
    def _display_name_xpath_condition(trip_name: str) -> str:
        names = []
        for name in (trip_name, trip_name.replace("-", "")):
            if name and name not in names:
                names.append(name)

        conditions = []
        for name in names:
            conditions.append(f'@text="{name}"')
            conditions.append(f'contains(@text, "{name}")')
            conditions.append(
                f'(string-length(@text) > 4 and contains("{name}", @text))'
            )
        return " or ".join(conditions)

    @classmethod
    def route_trip_title_xpath(cls, trip_name: str) -> str:
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'

    @classmethod
    def title_xpath(cls, trip_name: str) -> str:
        return (
            f'//*[@id="routeName"]/Text'
            f'[{cls._display_name_xpath_condition(trip_name)}]'
        )

    @classmethod
    def first_unplanned_poi_xpath(cls, poi_name: str) -> str:
        return cls.FIRST_UNPLANNED_POI_XPATH_TEMPLATE.format(poi_name=poi_name)

    @classmethod
    def route_poi_xpath(cls, poi_name: str) -> str:
        return cls.ROUTE_POI_XPATH_TEMPLATE.format(poi_name=poi_name)

    @classmethod
    def second_unplanned_poi_xpath(cls, poi_name: str) -> str:
        return cls.SECOND_UNPLANNED_POI_XPATH_TEMPLATE.format(poi_name=poi_name)

    def tap_back_button(self) -> None:
        """点击行程详情页顶部栏的页面内返回按钮。"""
        components = self.driver.find_all_components(BY.xpath(self.BACK_BUTTON_XPATH))
        if components is not None:
            if not isinstance(components, list):
                components = [components]
            candidates = []
            for component in components:
                bounds = component.getBounds()
                if int(bounds.right) <= int(bounds.left) or int(bounds.bottom) <= int(bounds.top):
                    continue
                candidates.append((int(bounds.top), int(bounds.left), component))
            if candidates:
                candidates.sort(key=lambda item: (item[0], item[1]))
                candidates[0][2].click()
                return

        self.tap_xpath(self.BACK_BUTTON_XPATH, "页面内返回按钮")

    def tap_view_map(self, *, timeout: float = 8) -> None:
        """点击行程详情页地图缩略图上的查看地图按钮，进入游玩模式。"""
        self.tap_xpath(
            self.VIEW_MAP_BUTTON_XPATH,
            "行程详情查看地图按钮",
            timeout=timeout,
        )
        time.sleep(1.2)

    def tap_edit_trip(self, *, timeout: float = 8) -> None:
        """点击行程详情页底部“编辑行程”按钮。"""
        edit_button = self.scroll_until_xpath_visible(
            self.EDIT_TRIP_BUTTON_XPATH,
            "编辑行程按钮",
            max_swipes=8,
            timeout=timeout,
        )
        edit_button.click()
        time.sleep(1.2)

    def wait_loaded(self, trip_name: str, *, timeout: float = 10) -> None:
        """等待我的行程详情页加载完成。"""
        self.wait_xpath(self.ROOT_XPATH, "行程详情页根节点", timeout=timeout)
        self.wait_xpath(
            self.route_trip_title_xpath(trip_name),
            f"行程详情页标题{trip_name}",
            timeout=timeout,
        )

    def wait_returned_from_play_mode(
        self,
        trip_name: str,
        *,
        timeout: float = 10,
    ) -> None:
        """等待从查看地图游玩模式退出后恢复到我的行程详情页。"""
        self.wait_loaded(trip_name, timeout=timeout)
        self.wait_xpath(
            self.VIEW_MAP_BUTTON_XPATH,
            "行程详情查看地图按钮",
            timeout=timeout,
        )

    def wait_any_xpath(
        self,
        xpaths: tuple[str, ...],
        name: str,
        *,
        timeout: float = 8,
    ):
        """等待任一 XPath 出现，用于兼容不同版本的同一控件。"""
        deadline = time.time() + timeout
        last_error: Exception | None = None
        while time.time() < deadline:
            for xpath in xpaths:
                try:
                    component = self.find_xpath(xpath)
                except Exception as exc:
                    last_error = exc
                    continue
                if component is not None:
                    return component
            time.sleep(0.4)
        if last_error is not None:
            raise RuntimeError(f"[{self.PAGE_NAME}] 查找{name}时 XPath 异常：{last_error}")
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到{name}，timeout={timeout}s")

    def wait_rename_button(self, *, timeout: float = 8):
        """等待顶部重命名入口展示。"""
        return self.wait_any_xpath(
            (
                self.RENAME_BUTTON_XPATH,
                self.RENAME_TEXT_XPATH,
                self.TITLE_CONTAINER_XPATH,
            ),
            "行程详情顶部重命名入口",
            timeout=timeout,
        )

    @staticmethod
    def rename_input_value_xpath(trip_name: str) -> str:
        return f'//Dialog//TextInput[@text="{trip_name}"]'

    def tap_rename_entry(self, *, timeout: float = 8) -> None:
        """点击行程详情页顶部编辑/重命名入口。"""
        component = self.wait_any_xpath(
            (
                self.RENAME_BUTTON_XPATH,
                self.RENAME_TEXT_XPATH,
                self.TITLE_CONTAINER_XPATH,
            ),
            "行程详情顶部重命名入口",
            timeout=timeout,
        )
        component.click()

    def wait_rename_dialog_loaded(self, *, timeout: float = 8):
        """等待重命名弹窗展示。"""
        self.wait_xpath(
            self.RENAME_DIALOG_XPATH,
            "行程重命名弹窗",
            timeout=timeout,
        )
        return self.wait_xpath(
            self.RENAME_INPUT_XPATH,
            "行程重命名输入框",
            timeout=timeout,
        )

    def clear_and_input_rename(self, trip_name: str, *, timeout: float = 8) -> None:
        """清空重命名输入框并输入新名称。"""
        component = self.wait_xpath(
            self.RENAME_INPUT_XPATH,
            "行程重命名输入框",
            timeout=timeout,
        )
        component.clearText()
        component.inputText(trip_name)

    def tap_rename_confirm(self, *, timeout: float = 8) -> None:
        """点击重命名弹窗确认按钮。"""
        self.tap_xpath(
            self.RENAME_CONFIRM_BUTTON_XPATH,
            "行程重命名确认按钮",
            timeout=timeout,
        )

    def close_rename_dialog_if_present(self) -> None:
        """清理时如果重命名弹窗仍展示，优先点击取消，否则按返回关闭。"""
        if self.find_xpath(self.RENAME_CANCEL_BUTTON_XPATH) is not None:
            self.tap_xpath(
                self.RENAME_CANCEL_BUTTON_XPATH,
                "行程重命名取消按钮",
                timeout=1,
            )
            return
        if self.find_xpath(self.RENAME_INPUT_XPATH) is not None:
            self.driver.press_back()

    def _detail_scroll_area(self):
        return self.find_xpath(self.DETAIL_SCROLL_XPATH) or self.find_xpath(self.ROOT_XPATH)

    def swipe_detail_up(self) -> None:
        """在行程详情页向下浏览内容。"""
        area = self._detail_scroll_area()
        if area is not None:
            self.driver.swipe("UP", distance=55, area=area, swipe_time=0.55)
        else:
            self.driver.swipe("UP", distance=55, start_point=(0.5, 0.82), swipe_time=0.55)
        time.sleep(0.8)

    def scroll_until_xpath_visible(
        self,
        xpath: str,
        name: str,
        *,
        max_swipes: int = 5,
        timeout: float = 8,
    ):
        """滚动行程详情页直到目标内容可见。"""
        for swipe_count in range(max_swipes + 1):
            component = self.find_xpath(xpath)
            if component is not None:
                return component
            if swipe_count == max_swipes:
                break
            self.swipe_detail_up()
        return self.wait_xpath(xpath, name, timeout=timeout)

    @classmethod
    def route_day_poi_xpath(cls, poi_name: str) -> str:
        return (
            f'//*[@id="planPageRoot"]//Text[@text="{poi_name}" '
            f'or contains(@text, "{poi_name}")]'
        )

    @classmethod
    def route_poi_with_icon_xpath(cls, poi_name: str) -> str:
        return (
            f'//*[@id="planPageRoot"]//*[@clickable="true" '
            f'and .//Text[@text="{poi_name}" or contains(@text, "{poi_name}")] '
            'and (.//Image or .//SymbolGlyph)]'
        )

    @classmethod
    def poi_detail_english_name_xpath(cls, english_name: str) -> str:
        return cls.POI_DETAIL_ENGLISH_NAME_XPATH_TEMPLATE.format(
            english_name=english_name
        )

    @staticmethod
    def _as_list(components) -> list:
        if components is None:
            return []
        if isinstance(components, list):
            return components
        return [components]

    @staticmethod
    def _bounds_tuple(component) -> tuple[int, int, int, int]:
        bounds = component.getBounds()
        return int(bounds.left), int(bounds.top), int(bounds.right), int(bounds.bottom)

    @staticmethod
    def _component_type(component) -> str:
        try:
            return component.getAllProperties().to_dict().get("type", "")
        except Exception:
            return ""

    def tap_route_day_poi(
        self,
        poi_name: str,
        *,
        max_swipes: int = 8,
        timeout: float = 8,
    ) -> None:
        """点击行程详情里的指定 POI。"""
        poi = self.scroll_until_xpath_visible(
            self.route_day_poi_xpath(poi_name),
            f"行程详情POI{poi_name}",
            max_swipes=max_swipes,
            timeout=timeout,
        )
        poi.click()
        time.sleep(1)

    def wait_poi_detail_loaded(
        self,
        *,
        english_name: str | None = None,
        timeout: float = 8,
    ) -> None:
        """等待行程详情内 POI 详情卡片展示首屏核心内容。"""
        self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI详情卡片", timeout=timeout)
        if english_name is not None:
            self.wait_xpath(
                self.poi_detail_english_name_xpath(english_name),
                f"POI英文名{english_name}",
                timeout=timeout,
            )
        self.wait_xpath(self.POI_DETAIL_TAG_XPATH, "POI详情标签", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_RATING_XPATH, "POI详情评分", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_GALLERY_XPATH, "POI详情图集", timeout=timeout)
        self.wait_xpath(self.POI_DETAIL_INTRO_XPATH, "POI详情简介", timeout=timeout)

    def swipe_poi_detail_up(self) -> None:
        """在 POI 详情半卡片内向下浏览。"""
        detail = self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI详情卡片")
        self.driver.swipe("UP", distance=60, area=detail, swipe_time=0.55)
        time.sleep(0.8)

    def scroll_poi_detail_until_xpath_visible(
        self,
        xpath: str,
        name: str,
        *,
        max_swipes: int = 5,
        timeout: float = 8,
    ):
        """滚动 POI 详情卡片直到目标内容可见。"""
        for swipe_count in range(max_swipes + 1):
            component = self.find_xpath(xpath)
            if component is not None:
                return component
            if swipe_count == max_swipes:
                break
            self.swipe_poi_detail_up()
        return self.wait_xpath(xpath, name, timeout=timeout)

    def _screen_bounds(self) -> tuple[int, int, int, int]:
        root = self.find_xpath(self.ROOT_XPATH) or self.find_xpath(
            self.POI_DETAIL_ROOT_XPATH
        )
        if root is None:
            return 0, 0, 0, 0
        return self._bounds_tuple(root)

    def _find_clickable_by_bounds(
        self,
        predicate,
        name: str,
        *,
        timeout: float = 8,
    ):
        deadline = time.time() + timeout
        while time.time() < deadline:
            components = self._as_list(
                self.driver.find_all_components(BY.xpath('//*[@clickable="true"]'))
            )
            candidates = []
            for component in components:
                try:
                    bounds = self._bounds_tuple(component)
                except Exception:
                    continue
                if bounds[2] <= bounds[0] or bounds[3] <= bounds[1]:
                    continue
                if predicate(component, bounds):
                    candidates.append((bounds[1], bounds[0], component))
            if candidates:
                candidates.sort(key=lambda item: (item[0], item[1]))
                return candidates[0][2]
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到{name}，timeout={timeout}s")

    def poi_detail_light_button(self, *, timeout: float = 8):
        """定位 POI 详情左下角点亮按钮。"""
        detail_bounds = self._bounds_tuple(
            self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI详情卡片", timeout=timeout)
        )
        screen_bounds = self._screen_bounds()
        screen_width = max(1, screen_bounds[2] - screen_bounds[0])

        def is_light_button(component, bounds: tuple[int, int, int, int]) -> bool:
            return (
                self._component_type(component) == "Image"
                and bounds[0] <= screen_bounds[0] + screen_width * 0.15
                and bounds[1] >= detail_bounds[3]
                and bounds[3] > bounds[1]
            )

        return self._find_clickable_by_bounds(
            is_light_button,
            "POI详情左下角点亮按钮",
            timeout=timeout,
        )

    def tap_poi_detail_light_button(self, *, timeout: float = 8):
        """点击 POI 详情左下角点亮按钮并返回点击后的按钮控件。"""
        button = self.poi_detail_light_button(timeout=timeout)
        button.click()
        time.sleep(1)
        return self.poi_detail_light_button(timeout=timeout)

    def poi_detail_close_button(self, *, timeout: float = 8):
        """定位 POI 详情右上角关闭按钮，避开元服务右上角系统关闭按钮。"""
        detail_bounds = self._bounds_tuple(
            self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI详情卡片", timeout=timeout)
        )
        screen_bounds = self._screen_bounds()
        screen_width = max(1, screen_bounds[2] - screen_bounds[0])
        detail_height = max(1, detail_bounds[3] - detail_bounds[1])

        def is_close_button(component, bounds: tuple[int, int, int, int]) -> bool:
            return (
                self._component_type(component) == "Image"
                and bounds[0] >= screen_bounds[0] + screen_width * 0.85
                and bounds[1] >= detail_bounds[1] - detail_height * 0.35
                and bounds[3] <= detail_bounds[1] + detail_height * 0.08
            )

        return self._find_clickable_by_bounds(
            is_close_button,
            "POI详情右上角关闭按钮",
            timeout=timeout,
        )

    def close_poi_detail(self, trip_name: str, *, timeout: float = 8) -> None:
        """关闭 POI 详情并等待回到行程详情页。"""
        close_button = self.poi_detail_close_button(timeout=timeout)
        close_button.click()
        time.sleep(0.8)
        self.wait_poi_detail_closed(timeout=timeout)
        self.wait_loaded(trip_name, timeout=timeout)

    def gesture_back_from_poi_detail(
        self,
        trip_name: str,
        *,
        timeout: float = 8,
    ) -> None:
        """通过系统侧滑关闭 POI 详情并返回行程详情页。"""
        self.driver.swipe_to_back(side="RIGHT")
        time.sleep(0.8)
        self.wait_poi_detail_closed(timeout=timeout)
        self.wait_loaded(trip_name, timeout=timeout)

    def wait_poi_detail_closed(self, *, timeout: float = 5) -> None:
        """等待 POI 详情卡片消失。"""
        self.driver.wait_for_component_disappear(
            BY.xpath(self.POI_DETAIL_ROOT_XPATH),
            timeout=timeout,
        )
        if (
            self.driver.wait_for_component(
                BY.xpath(self.POI_DETAIL_ROOT_XPATH),
                timeout=0.5,
            )
            is not None
        ):
            raise RuntimeError(f"[{self.PAGE_NAME}] POI详情关闭后仍然展示")

    def wait_route_trip_detail(self, trip_name: str, *, timeout: float = 8) -> None:
        """Verify a route-created trip detail page exposes title and route data."""
        self.wait_xpath(self.route_trip_title_xpath(trip_name), "route trip detail title", timeout=timeout)
        self.wait_xpath(self.ROUTE_DAY_1_XPATH, "route trip day 1", timeout=timeout)
        self.wait_xpath(self.ROUTE_DAY_2_XPATH, "route trip day 2", timeout=timeout)
        self.wait_xpath(self.ROUTE_FIRST_POI_XPATH, "route trip first day POI", timeout=timeout)

    def wait_generic_route_trip_detail(
        self,
        trip_name: str,
        *,
        poi_name: str | None = None,
        timeout: float = 8,
    ) -> None:
        """等待任意路线创建的行程详情页展示标题和路线地点数据。"""
        self.wait_xpath(
            self.ROOT_XPATH,
            "行程详情根节点",
            timeout=timeout,
        )
        self.wait_xpath(
            self.route_trip_title_xpath(trip_name),
            "行程详情标题",
            timeout=timeout,
        )
        if poi_name is not None:
            self.wait_xpath(
                self.route_poi_xpath(poi_name),
                f"行程详情路线POI{poi_name}",
                timeout=timeout,
            )

    def visible_texts(self) -> list[str]:
        """读取当前行程详情页暴露出的文本，用于诊断和报告附件。"""
        components = self.driver.find_all_components(BY.xpath(self.ROOT_TEXT_XPATH))
        if not components:
            return []

        texts: list[str] = []
        for component in components:
            properties = component.getAllProperties().to_dict()
            text = properties.get("text")
            if text and text not in texts:
                texts.append(text)
        return texts
