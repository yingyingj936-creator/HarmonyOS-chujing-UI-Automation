import time

from hypium import BY

from pages.base_page import BasePage


class TripManagerPage(BasePage):
    PAGE_NAME = "TripManagerPage"
    TRIP_LIST_XPATH = '//*[@scrollable="true"]'
    CREATE_TRIP_TITLE_XPATH = '//Text[@text="创建行程"]'
    HOT_ROUTE_REFERENCE_XPATH = (
        '//Text[contains(@text, "参考热门路线") and contains(@text, "修改")]'
    )
    MY_TRIPS_TITLE_XPATH = '//Text[@text="我的行程"]'
    VIDEO_TUTORIAL_XPATH = '//Text[contains(@text, "查看视频教程")]'
    TRIP_CARD_WITH_REQUIRED_FIELDS_XPATH = (
        '//*[@scrollable="true"]//*[@clickable="true" '
        'and .//Text[contains(@text, "天") and contains(@text, "地点")] '
        'and .//Text[contains(@text, "待规划")]]'
    )
    EDIT_TRIP_MENU_TITLE_XPATH = '//Text[@text="编辑行程"]'
    PIN_TRIP_ACTION_XPATH = '//Text[@text="置顶该行程"]'
    DELETE_TRIP_ACTION_XPATH = '//Text[@text="删除该行程"]'
    DELETE_CONFIRM_DIALOG_XPATH = '//Dialog[.//Text[@text="删除"]]'
    DELETE_CONFIRM_BUTTON_XPATH = '//Dialog//Text[@text="删除"]'
    DELETE_CANCEL_BUTTON_XPATH = '//Dialog//Text[@text="取消"]'
    SCREEN_ROOT_XPATH = '//*[@id="HwAuthDialog_rootId"]'
    BOTTOM_TRIP_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="行程"]'
    PAGE_READY_TEXT_XPATH = (
        '//Text[@text="创建行程" or @text="我的行程" or @text="行程" '
        'or (contains(@text, "参考热门路线") and contains(@text, "修改")) '
        'or contains(@text, "查看视频教程")]'
    )
    MY_TRIPS_AREA_MARKER_XPATH = (
        '//Text[@text="我的行程" or contains(@text, "查看视频教程")]'
    )
    TOP_AREA_MARKER_XPATH = (
        '//Text[@text="创建行程" '
        'or (contains(@text, "参考热门路线") and contains(@text, "修改"))]'
    )

    @staticmethod
    def _xpath(xpath: str):
        return BY.xpath(xpath)

    @staticmethod
    def _bounds_tuple(component) -> tuple[int, int, int, int]:
        bounds = component.getBounds()
        return int(bounds.left), int(bounds.top), int(bounds.right), int(bounds.bottom)

    @staticmethod
    def _contains(
        parent: tuple[int, int, int, int],
        child: tuple[int, int, int, int],
    ) -> bool:
        return (
            child[0] >= parent[0]
            and child[1] >= parent[1]
            and child[2] <= parent[2]
            and child[3] <= parent[3]
        )

    @staticmethod
    def _as_list(components) -> list:
        if components is None:
            return []
        if isinstance(components, list):
            return components
        return [components]

    def _visible_xpath(self, xpath: str):
        """返回有有效可见区域的组件，过滤列表保留的离屏节点。"""
        component = self.find_xpath(xpath)
        if component is None:
            return None
        left, top, right, bottom = self._bounds_tuple(component)
        if right <= left or bottom <= top or bottom <= 0:
            return None
        return component

    def _has_visible_xpath(self, xpath: str) -> bool:
        """一次查询全部候选，判断是否至少有一个节点真实可见。"""
        components = self.driver.find_all_components(BY.xpath(xpath))
        for component in self._as_list(components):
            left, top, right, bottom = self._bounds_tuple(component)
            if right > left and bottom > top and bottom > 0:
                return True
        return False

    def _visible_trip_card(self, xpath: str):
        """返回未被底部导航遮挡的完整行程卡片。"""
        component = self._visible_xpath(xpath)
        if component is None:
            return None
        navigation = self.find_xpath(self.SCREEN_ROOT_XPATH)
        if navigation is None:
            return component
        _, _, _, card_bottom = self._bounds_tuple(component)
        _, navigation_top, _, _ = self._bounds_tuple(navigation)
        if card_bottom > navigation_top - 10:
            return None
        return component

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
    def trip_card_xpath(cls, trip_name: str) -> str:
        """返回“我的行程”列表中包含摘要字段的可点击卡片。"""
        return cls.trip_card_with_summary_xpath(trip_name)

    @classmethod
    def trip_list_title_xpath(cls, trip_name: str) -> str:
        return f'//*[@scrollable="true"]//Text[{cls._display_name_xpath_condition(trip_name)}]'

    @classmethod
    def route_trip_card_title_xpath(cls, trip_name: str) -> str:
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'

    @classmethod
    def route_trip_card_summary_xpath(cls, trip_name: str) -> str:
        return (
            f'//*[@scrollable="true"]//*[.//Text[{cls._display_name_xpath_condition(trip_name)}] '
            'and .//Text[contains(@text, "2") and contains(@text, "天")] '
            'and .//Text[contains(@text, "14")]]'
        )

    @classmethod
    def trip_card_with_summary_xpath(cls, trip_name: str) -> str:
        return (
            f'//*[@scrollable="true"]//*[@clickable="true" '
            f'and .//Text[{cls._display_name_xpath_condition(trip_name)}] '
            'and .//Text[contains(@text, "天") and contains(@text, "地点")]]'
        )

    def tap_trip(self, trip_name: str, *, timeout: float = 8) -> None:
        """点击我的行程列表中的指定行程。"""
        target_xpath = self.trip_card_with_summary_xpath(trip_name)
        trip_card = self._visible_trip_card(target_xpath)
        if trip_card is None:
            trip_card = self.scroll_trip_into_view(
                trip_name,
                max_swipes=max(8, int(timeout)),
            )
        bounds = trip_card.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )

    def tap_hot_route_reference(self, *, timeout: float = 8) -> None:
        """点击“参考热门路线修改”入口。"""
        self.scroll_to_create_area(max_swipes=12)
        self.tap_xpath(
            self.HOT_ROUTE_REFERENCE_XPATH,
            "参考热门路线修改入口",
            timeout=timeout,
        )

    def tap_video_tutorial(self, *, timeout: float = 8) -> None:
        """点击“查看视频教程”入口。"""
        self.tap_xpath(
            self.VIDEO_TUTORIAL_XPATH,
            "查看视频教程入口",
            timeout=timeout,
        )

    def wait_loaded(self, *, timeout: float = 8) -> None:
        """等待行程页核心区域加载完成。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            components = self.driver.find_all_components(
                BY.xpath(self.PAGE_READY_TEXT_XPATH)
            )
            texts = {
                (component.getText() or "").strip()
                for component in self._as_list(components)
            }
            has_hot_route = any(
                "参考热门路线" in text and "修改" in text for text in texts
            )
            has_create = "创建行程" in texts
            has_my_trips = "我的行程" in texts
            has_video = any("查看视频教程" in text for text in texts)
            has_trip_tab = "行程" in texts
            if (
                has_hot_route and (has_my_trips or has_create)
            ) or (
                has_trip_tab and (has_create or has_my_trips or has_video)
            ):
                return
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到行程页核心区域，timeout={timeout}s"
        )

    def scroll_to_create_area(
        self,
        *,
        max_swipes: int = 12,
        trip_list=None,
    ) -> None:
        """恢复到行程页顶部创建区域，兼容页面保留上次滚动位置。"""
        if trip_list is None:
            trip_list = self.wait_xpath(
                self.TRIP_LIST_XPATH,
                "行程页滚动列表",
            )
        for swipe_count in range(max_swipes + 1):
            if self._has_visible_xpath(self.TOP_AREA_MARKER_XPATH):
                return
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "DOWN",
                distance=70,
                area=trip_list,
            )
            time.sleep(0.35)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未回到行程页创建区域")

    def scroll_to_my_trips_area(self, *, max_swipes: int = 6) -> None:
        """滚动到我的行程区域。"""
        trip_list = self.wait_xpath(
            self.TRIP_LIST_XPATH,
            "行程页滚动列表",
        )
        for swipe_count in range(max_swipes + 1):
            if self.find_xpath(self.MY_TRIPS_AREA_MARKER_XPATH) is not None:
                return
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=45,
                area=trip_list,
            )
            time.sleep(0.5)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到我的行程区域")

    def scroll_to_trip_card_with_required_fields(
        self,
        *,
        max_swipes: int = 8,
    ) -> None:
        """滚动查找包含名称、天数、地点数、待规划数和封面的行程卡片。"""
        self.wait_trip_card_with_required_fields(max_swipes=max_swipes)

    def wait_trip_card_with_required_fields(
        self,
        *,
        max_swipes: int = 8,
    ) -> object:
        """返回可见的字段完整行程卡片。"""
        self.scroll_to_my_trips_area(max_swipes=max_swipes)
        trip_list = self.wait_xpath(
            self.TRIP_LIST_XPATH,
            "行程页滚动列表",
        )
        for swipe_count in range(max_swipes + 1):
            trip_card = self.find_xpath(self.TRIP_CARD_WITH_REQUIRED_FIELDS_XPATH)
            if trip_card is not None:
                return trip_card
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=35,
                area=trip_list,
            )
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 我的行程列表未找到字段完整的行程卡片"
        )

    def visible_trip_cards_with_titles(self, *, max_swipes: int = 8) -> list[tuple]:
        """返回当前我的行程可见区域内的行程卡片及标题，按从上到下排序。"""
        self.scroll_to_trip_card_with_required_fields(max_swipes=max_swipes)
        return self.current_visible_trip_cards_with_titles()

    def current_visible_trip_cards_with_titles(self) -> list[tuple]:
        """读取当前屏幕内已展示的行程卡片及标题，不额外滚动。"""
        cards = self._as_list(
            self.driver.find_all_components(
                self._xpath(self.TRIP_CARD_WITH_REQUIRED_FIELDS_XPATH)
            )
        )
        text_components = self._as_list(
            self.driver.find_all_components(
                self._xpath('//*[@scrollable="true"]//Text')
            )
        )

        card_infos = []
        for card in cards:
            title = self._trip_card_title(card, text_components)
            if title:
                card_infos.append((card, title))

        card_infos.sort(key=lambda item: self._bounds_tuple(item[0])[1])
        return card_infos

    def _trip_card_title(self, card, text_components: list) -> str:
        card_bounds = self._bounds_tuple(card)
        title_candidates = []
        for text_component in text_components:
            text = text_component.getText().strip()
            if (
                not text
                or ("天" in text and "地点" in text)
                or "待规划" in text
                or text in ("我的行程", "查看视频教程", "暂无更多数据")
            ):
                continue

            text_bounds = self._bounds_tuple(text_component)
            if self._contains(card_bounds, text_bounds):
                title_candidates.append((text_bounds[1], text))

        if not title_candidates:
            return ""
        title_candidates.sort(key=lambda item: item[0])
        return title_candidates[0][1]

    def long_press_required_trip_card(self, *, press_time: float = 2.0):
        """长按当前可见的字段完整行程卡片。"""
        trip_card = self.wait_trip_card_with_required_fields(max_swipes=8)
        self.driver.long_click(trip_card, press_time=press_time)
        return trip_card

    def long_press_trip_card(self, trip_card, *, press_time: float = 2.0) -> None:
        """长按指定行程卡片。"""
        self.driver.long_click(trip_card, press_time=press_time)

    def wait_edit_trip_menu_loaded(self, *, timeout: float = 8) -> None:
        """等待行程长按后的编辑菜单展示完整。"""
        self.wait_xpath(
            self.EDIT_TRIP_MENU_TITLE_XPATH,
            "编辑行程菜单标题",
            timeout=timeout,
        )
        self.wait_xpath(
            self.PIN_TRIP_ACTION_XPATH,
            "置顶该行程操作",
            timeout=timeout,
        )
        self.wait_xpath(
            self.DELETE_TRIP_ACTION_XPATH,
            "删除该行程操作",
            timeout=timeout,
        )

    def tap_edit_menu_close(self, *, timeout: float = 8) -> None:
        """点击编辑行程底部菜单关闭按钮。"""
        left, top, right, bottom = self.edit_menu_close_bounds(timeout=timeout)
        self.driver.click(((left + right) // 2, (top + bottom) // 2))

    def tap_pin_trip_action(self, *, timeout: float = 8) -> None:
        """点击编辑菜单中的“置顶该行程”。"""
        self.tap_xpath(
            self.PIN_TRIP_ACTION_XPATH,
            "置顶该行程操作",
            timeout=timeout,
        )

    def tap_delete_trip_action(self, *, timeout: float = 8) -> None:
        """点击编辑菜单中的“删除该行程”。"""
        self.tap_xpath(
            self.DELETE_TRIP_ACTION_XPATH,
            "删除该行程操作",
            timeout=timeout,
        )

    def wait_delete_confirm_loaded(self, *, timeout: float = 8) -> None:
        """等待删除行程二次确认弹窗展示。"""
        self.wait_xpath(
            self.DELETE_CONFIRM_DIALOG_XPATH,
            "删除行程二次确认弹窗",
            timeout=timeout,
        )
        self.wait_xpath(
            self.DELETE_CONFIRM_BUTTON_XPATH,
            "删除行程二次确认按钮",
            timeout=timeout,
        )

    def tap_confirm_delete_trip(self, *, timeout: float = 8) -> None:
        """在二次确认弹窗中点击“删除”。"""
        self.tap_xpath(
            self.DELETE_CONFIRM_BUTTON_XPATH,
            "删除行程二次确认按钮",
            timeout=timeout,
        )

    def wait_delete_confirm_closed(self, *, timeout: float = 5) -> None:
        """等待删除行程二次确认弹窗消失。"""
        self.driver.wait_for_component_disappear(
            self._xpath(self.DELETE_CONFIRM_BUTTON_XPATH),
            timeout=timeout,
        )
        if self.driver.wait_for_component(
            self._xpath(self.DELETE_CONFIRM_BUTTON_XPATH),
            timeout=0.5,
        ) is not None:
            raise RuntimeError(f"[{self.PAGE_NAME}] 删除确认弹窗关闭后仍然展示")

    def wait_trip_title_absent(
        self,
        trip_name: str,
        *,
        timeout: float = 10,
    ) -> None:
        """等待当前行程列表可见区域内不再展示指定行程标题。"""
        target_xpath = self.trip_list_title_xpath(trip_name)
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.find_xpath(target_xpath) is None:
                return
            time.sleep(0.5)

        visible_titles = [
            title
            for _, title in self.current_visible_trip_cards_with_titles()
        ]
        raise AssertionError(
            f"删除后行程“{trip_name}”仍然展示，当前可见行程={visible_titles}"
        )

    def wait_first_trip_title(
        self,
        expected_title: str,
        *,
        timeout: float = 10,
    ) -> None:
        """等待目标行程展示在我的行程列表第一位。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            card_infos = self.visible_trip_cards_with_titles(max_swipes=2)
            if card_infos and card_infos[0][1] == expected_title:
                return
            time.sleep(0.5)

        visible_titles = [
            title
            for _, title in self.visible_trip_cards_with_titles(max_swipes=2)
        ]
        raise AssertionError(
            f"目标行程未移动到列表首位，期望首位={expected_title!r}，"
            f"当前可见顺序={visible_titles}"
        )

    def edit_menu_close_bounds(self, *, timeout: float = 8) -> tuple[int, int, int, int]:
        """返回编辑行程菜单右上角关闭按钮的可点击区域。"""
        title = self.wait_xpath(
            self.EDIT_TRIP_MENU_TITLE_XPATH,
            "编辑行程菜单标题",
            timeout=timeout,
        )
        root = self.wait_xpath(
            self.SCREEN_ROOT_XPATH,
            "出境服务页面根节点",
            timeout=timeout,
        )

        title_bounds = title.getBounds()
        root_bounds = root.getBounds()
        screen_width = int(root_bounds.right - root_bounds.left)
        button_size = max(80, int(screen_width * 0.11))
        right_margin = max(32, int(screen_width * 0.045))
        center_x = int(root_bounds.right - right_margin - button_size / 2)
        center_y = int((title_bounds.top + title_bounds.bottom) / 2)
        half = button_size // 2
        return (
            center_x - half,
            center_y - half,
            center_x + half,
            center_y + half,
        )

    def wait_edit_menu_closed(self, *, timeout: float = 5) -> None:
        """等待编辑行程菜单消失。"""
        self.driver.wait_for_component_disappear(
            self._xpath(self.EDIT_TRIP_MENU_TITLE_XPATH),
            timeout=timeout,
        )
        if self.driver.wait_for_component(
            self._xpath(self.EDIT_TRIP_MENU_TITLE_XPATH),
            timeout=0.5,
        ) is not None:
            raise RuntimeError(f"[{self.PAGE_NAME}] 编辑行程菜单关闭后仍然展示")

    def scroll_trip_into_view(
        self,
        trip_name: str,
        *,
        max_swipes: int = 8,
    ):
        """从行程列表顶部向下查找指定行程，兼容列表位置被前序用例保留。"""
        trip_list = self.wait_xpath(
            self.TRIP_LIST_XPATH,
            "行程页滚动列表",
        )
        target_xpath = self.trip_card_with_summary_xpath(trip_name)

        visible_target = self._visible_trip_card(target_xpath)
        if visible_target is not None:
            return visible_target

        # 行程页会保留上次滚动位置。先回到页面顶部，再从“我的行程”区域向下扫描，
        # 避免从列表底部继续上拉而漏掉被新增行程挤到中间的目标卡片。
        self.scroll_to_create_area(
            max_swipes=max(max_swipes, 12),
            trip_list=trip_list,
        )

        self.scroll_to_my_trips_area(max_swipes=max(max_swipes, 10))
        scan_swipes = max(max_swipes, 24)
        for swipe_count in range(scan_swipes + 1):
            visible_target = self._visible_trip_card(target_xpath)
            if visible_target is not None:
                return visible_target
            if swipe_count == scan_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=50,
                area=trip_list,
            )
            time.sleep(0.4)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 从列表顶部向下扫描 {scan_swipes} 次后"
            f"仍未找到“{trip_name}”"
        )

    def pull_to_refresh(self) -> None:
        """在我的行程列表内执行下拉刷新。"""
        trip_list = self.wait_xpath(
            self.TRIP_LIST_XPATH,
            "我的行程列表",
        )
        self.driver.swipe(
            "DOWN",
            distance=45,
            area=trip_list,
            start_point=(0.5, 0.3),
        )
        time.sleep(2)

