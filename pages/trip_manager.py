import time

from hypium import BY

from pages.base_page import BasePage


class TripManagerPage(BasePage):
    PAGE_NAME = "TripManagerPage"
    TRIP_LIST_XPATH = '//List[@scrollable="true"]'
    CREATE_TRIP_TITLE_XPATH = '//Text[@text="创建行程"]'
    HOT_ROUTE_REFERENCE_XPATH = (
        '//Text[contains(@text, "参考热门路线") and contains(@text, "修改")]'
    )
    MY_TRIPS_TITLE_XPATH = '//Text[@text="我的行程"]'
    VIDEO_TUTORIAL_XPATH = '//Text[contains(@text, "查看视频教程")]'
    TRIP_CARD_WITH_REQUIRED_FIELDS_XPATH = (
        '//List[@scrollable="true"]//*[@clickable="true" '
        'and .//Text[contains(@text, "天") and contains(@text, "地点")] '
        'and .//Text[contains(@text, "待规划")]]'
    )
    EDIT_TRIP_MENU_TITLE_XPATH = '//Text[@text="编辑行程"]'
    PIN_TRIP_ACTION_XPATH = '//Text[@text="置顶该行程"]'
    DELETE_TRIP_ACTION_XPATH = '//Text[@text="删除该行程"]'
    SCREEN_ROOT_XPATH = '//*[@id="HwAuthDialog_rootId"]'

    @staticmethod
    def _xpath(xpath: str):
        return BY.xpath(xpath)

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
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'

    @classmethod
    def route_trip_card_title_xpath(cls, trip_name: str) -> str:
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'

    @classmethod
    def route_trip_card_summary_xpath(cls, trip_name: str) -> str:
        return (
            f'//List[@scrollable="true"]//*[.//Text[{cls._display_name_xpath_condition(trip_name)}] '
            'and .//Text[contains(@text, "2") and contains(@text, "天")] '
            'and .//Text[contains(@text, "14")]]'
        )

    @classmethod
    def trip_card_with_summary_xpath(cls, trip_name: str) -> str:
        return (
            f'//List[@scrollable="true"]//*[@clickable="true" '
            f'and .//Text[{cls._display_name_xpath_condition(trip_name)}] '
            'and .//Text[contains(@text, "天") and contains(@text, "地点")]]'
        )

    def tap_trip(self, trip_name: str) -> None:
        """点击我的行程列表中的指定行程。"""
        self.tap_xpath(self.trip_card_xpath(trip_name), f"行程“{trip_name}”")

    def tap_hot_route_reference(self, *, timeout: float = 8) -> None:
        """点击“参考热门路线修改”入口。"""
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
        self.wait_xpath(
            self.CREATE_TRIP_TITLE_XPATH,
            "行程页创建行程区域",
            timeout=timeout,
        )
        self.wait_xpath(
            self.HOT_ROUTE_REFERENCE_XPATH,
            "参考热门路线修改入口",
            timeout=timeout,
        )

    def scroll_to_my_trips_area(self, *, max_swipes: int = 6) -> None:
        """滚动到我的行程区域。"""
        trip_list = self.wait_xpath(
            self.TRIP_LIST_XPATH,
            "行程页滚动列表",
        )
        for swipe_count in range(max_swipes + 1):
            if (
                self.find_xpath(self.MY_TRIPS_TITLE_XPATH) is not None
                or self.find_xpath(self.VIDEO_TUTORIAL_XPATH) is not None
            ):
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
    ):
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

    def long_press_required_trip_card(self, *, press_time: float = 2.0):
        """长按当前可见的字段完整行程卡片。"""
        trip_card = self.wait_trip_card_with_required_fields(max_swipes=8)
        self.driver.long_click(trip_card, press_time=press_time)
        return trip_card

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
    ) -> None:
        """滚动我的行程列表，直到指定行程进入可视区域。"""
        self.scroll_to_my_trips_area(max_swipes=max_swipes)
        trip_list = self.wait_xpath(
            self.TRIP_LIST_XPATH,
            "行程页滚动列表",
        )
        target_xpath = self.trip_card_with_summary_xpath(trip_name)
        for swipe_count in range(max_swipes + 1):
            if self.find_xpath(target_xpath) is not None:
                return
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=35,
                area=trip_list,
            )
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 我的行程列表未找到“{trip_name}”"
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

