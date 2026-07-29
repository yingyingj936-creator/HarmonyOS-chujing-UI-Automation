import time
from typing import Any

from hypium import BY

from pages.base_page import BasePage


class TripEditPage(BasePage):
    """我的行程编辑页。"""

    PAGE_NAME = "TripEditPage"

    TITLE_XPATH = '//Text[@text="编辑行程"]'
    BACK_BUTTON_XPATH = '//Row[@clickable="true" and ./Image]'
    MAP_VIEW_XPATH = '//*[@id="mapview"]'
    BOTTOM_PANEL_XPATH = '//*[@id="map_bottom_panel"]'
    TAB_BAR_XPATH = '//*[@id="tabBarList"]'
    OVERVIEW_TAB_XPATH = '//*[@id="tabBarList"]//Text[@text="全览" and @clickable="true"]'
    DAY_1_TAB_XPATH = '//*[@id="tabBarList"]//Text[@text="Day1" and @clickable="true"]'
    DAY_N_TAB_XPATH = '//*[@id="tabBarList"]//Text[@text="Day2" and @clickable="true"]'
    DAY_3_TAB_XPATH = '//*[@id="tabBarList"]//Text[@text="Day3" and @clickable="true"]'
    DAY_3_TAB_CONTAINER_XPATH = (
        '//*[@id="tabBarList"]//*[@clickable="true" and .//Text[@text="Day3"]]'
    )
    PENDING_TAB_XPATH = '//*[@id="tabBarList"]//Text[@text="待规划" and @clickable="true"]'
    ADD_TEXT_XPATH = (
        '//*[@id="tabBarList"]//Text[contains(@text, "新增") or contains(@text, "添加")]'
    )
    ADD_ICON_XPATH = '//*[@id="tabBarList"]//*[@clickable="true" and not(.//Text)]'
    OVERVIEW_LIST_XPATH = '//*[@id="route_editor_overview"]'
    CHILD_LIST_XPATH = '//*[@id="route_editor_childs"]'
    CHILD_DAY_3_SECTION_XPATH = '//*[@id="route_editor_childs"]//Text[@text="Day3"]'
    CHILD_PENDING_SECTION_XPATH = '//*[@id="route_editor_childs"]//Text[@text="待规划"]'
    DAY_1_SECTION_XPATH = (
        '//*[@id="route_editor_overview"]//*[@clickable="true" '
        'and .//Text[@text="Day1"] and .//Text[@text="通菜街"]]'
    )
    DAY_2_SECTION_XPATH = (
        '//*[@id="route_editor_overview"]//*[@clickable="true" '
        'and .//Text[@text="Day2"] and .//Text[@text="铜锣湾"]]'
    )
    DAY_NUMBER_1_XPATH = '//*[@id="route_editor_overview"]//Text[@id="dayNumber" and @text="1"]'
    DAY_NUMBER_2_XPATH = '//*[@id="route_editor_overview"]//Text[@id="dayNumber" and @text="2"]'
    FIRST_DAY_POI_XPATH = '//*[@id="route_editor_overview"]//Text[@text="通菜街"]'
    SECOND_DAY_POI_XPATH = '//*[@id="route_editor_overview"]//Text[@text="旺角"]'
    DAY_N_POI_XPATH = (
        '//*[@id="route_editor_overview"]//Text[@text="铜锣湾" or @text="太平山顶"]'
    )
    DAY_1_CHILD_POI_XPATH = '//*[@id="route_editor_childs"]//Text[contains(@text, "通菜街")]'
    DAY_1_CHILD_SECOND_POI_XPATH = '//*[@id="route_editor_childs"]//Text[contains(@text, "旺角")]'
    DAY_1_CHILD_REORDERED_SECOND_POI_XPATH = (
        '//*[@id="route_editor_childs"]//Text[contains(@text, "2.") '
        'and contains(@text, "信和中心")]'
    )
    DAY_2_CHILD_POI_XPATH = '//*[@id="route_editor_childs"]//Text[contains(@text, "铜锣湾")]'
    DAY_2_CHILD_SECOND_POI_XPATH = '//*[@id="route_editor_childs"]//Text[contains(@text, "希慎广场")]'
    CHILD_DISTANCE_XPATH = '//*[@id="route_editor_childs"]//Text[contains(@text, "km")]'
    PENDING_ADD_ENTRY_XPATH = (
        '//*[@id="route_editor_childs"]//Text[@text="添加地点/活动" or contains(@text, "添加地点")]'
    )
    PENDING_POI_XPATH = (
        '//*[@id="route_editor_childs"]//Text[contains(@text, "坚尼地城") '
        'or contains(@text, "太平山顶")]'
    )
    FIRST_SELECT_ICON_XPATH = '//*[@id="firstSelectIcon"]'
    SELECTION_ACTION_MENU_XPATH = (
        '//Grid[.//Text[@text="取消"] and .//Text[@text="删除"] '
        'and .//Text[@text="移动到"] and .//Text[@text="复制到"]]'
    )
    SELECTION_CANCEL_ACTION_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="取消"]]'
    )
    SELECTION_DELETE_ACTION_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="删除"]]'
    )
    SELECTION_MOVE_ACTION_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="移动到"]]'
    )
    SELECTION_COPY_ACTION_XPATH = (
        '//Column[@clickable="true" and .//Text[@text="复制到"]]'
    )
    DELETE_CONFIRM_SHEET_XPATH = '//Text[@text="删除地点"]'
    DELETE_CONFIRM_BUTTON_XPATH = (
        '//Text[@text="删除" and @clickable="true"]'
    )
    DELETE_CONFIRM_CANCEL_XPATH = (
        '//Text[@text="取消" and @clickable="true"]'
    )
    EDIT_COMPLETE_XPATH = (
        '//Text'
        '[@text="编辑完成" or @text="完成" or @text="保存"]'
    )
    MOVE_TARGET_TITLE_XPATH = (
        '//Text[@text="移动到" or @text="移动至" or contains(@text, "移动到")]'
    )
    MOVE_TARGET_DAY_2_TEXT_XPATH = (
        '//Text[@text="Day2" or @text="第2天" or @text="第 2 天"]'
    )
    COPY_TARGET_TITLE_XPATH = (
        '//Text[@text="复制到" or @text="复制至" or contains(@text, "复制到")]'
    )
    COPY_TARGET_PENDING_TEXT_XPATH = (
        '//Text[@text="待规划" or contains(@text, "待规划")]'
    )
    ADD_POI_SEARCH_INPUT_XPATH = (
        '//TextInput[contains(@hint, "搜索") '
        'or contains(@hint, "地点") '
        'or contains(@hint, "活动") '
        'or contains(@hint, "请输入")]'
    )
    CHILD_LIST_TEXT_XPATH = '//*[@id="route_editor_childs"]//Text'

    @staticmethod
    def _as_list(components: Any) -> list[Any]:
        if components is None:
            return []
        if isinstance(components, list):
            return components
        return [components]

    @staticmethod
    def _is_visible(component: Any) -> bool:
        bounds = component.getBounds()
        return int(bounds.right) > int(bounds.left) and int(bounds.bottom) > int(bounds.top)

    def wait_loaded(self, *, timeout: float = 10) -> dict[str, Any]:
        """等待编辑行程页核心区域加载完成。"""
        return self.snapshot_xpaths(
            {
                "title": (self.TITLE_XPATH, "编辑行程页标题"),
                "map": (self.MAP_VIEW_XPATH, "编辑行程页顶部地图"),
                "panel": (self.BOTTOM_PANEL_XPATH, "编辑行程页半卡片区域"),
                "tab_bar": (self.TAB_BAR_XPATH, "编辑行程页半卡片Tab区域"),
                "overview_tab": (self.OVERVIEW_TAB_XPATH, "编辑行程页全览Tab"),
                "overview_list": (self.OVERVIEW_LIST_XPATH, "编辑行程页全览路线列表"),
            },
            timeout=timeout,
        )

    def wait_ready(self, *, timeout: float = 10) -> Any:
        """一次查询等待编辑行程页核心区域，供不需要返回组件的流程使用。"""
        ready_xpath = (
            '//*[@id="map_bottom_panel" '
            'and .//*[@id="tabBarList"] '
            'and .//*[@id="route_editor_overview"]]'
        )
        return self.wait_xpath(ready_xpath, "编辑行程页核心区域", timeout=timeout)

    def wait_tabs_loaded(self, *, timeout: float = 8) -> dict[str, Any]:
        """等待全览、Day1、DayN、待规划等Tab展示。"""
        return self.snapshot_xpaths(
            {
                "overview": (self.OVERVIEW_TAB_XPATH, "编辑行程页全览Tab"),
                "day_1": (self.DAY_1_TAB_XPATH, "编辑行程页Day1 Tab"),
                "day_n": (self.DAY_N_TAB_XPATH, "编辑行程页DayN Tab"),
                "pending": (self.PENDING_TAB_XPATH, "编辑行程页待规划Tab"),
            },
            timeout=timeout,
        )

    def wait_tabs_ready(self, *, timeout: float = 8) -> Any:
        """一次查询等待全览、Day1、Day2 和待规划 Tab。"""
        ready_xpath = (
            '//*[@id="tabBarList" '
            'and .//Text[@text="全览" and @clickable="true"] '
            'and .//Text[@text="Day1" and @clickable="true"] '
            'and .//Text[@text="Day2" and @clickable="true"] '
            'and .//Text[@text="待规划" and @clickable="true"]]'
        )
        return self.wait_xpath(ready_xpath, "编辑行程页完整Tab栏", timeout=timeout)

    def wait_route_overview_loaded(self, *, timeout: float = 8) -> dict[str, Any]:
        """等待全览下按天展示的路线列表加载完成。"""
        return self.snapshot_xpaths(
            {
                "list": (self.OVERVIEW_LIST_XPATH, "编辑行程页全览路线列表"),
                "day_1": (self.DAY_1_SECTION_XPATH, "编辑行程页Day1路线分组"),
                "day_2": (self.DAY_2_SECTION_XPATH, "编辑行程页DayN路线分组"),
                "number_1": (self.DAY_NUMBER_1_XPATH, "编辑行程页POI顺序1"),
                "number_2": (self.DAY_NUMBER_2_XPATH, "编辑行程页POI顺序2"),
                "first_poi": (self.FIRST_DAY_POI_XPATH, "编辑行程页Day1首个POI"),
                "second_poi": (self.SECOND_DAY_POI_XPATH, "编辑行程页Day1第二个POI"),
                "day_n_poi": (self.DAY_N_POI_XPATH, "编辑行程页DayN POI"),
            },
            timeout=timeout,
        )

    def wait_route_overview_ready(self, *, timeout: float = 8) -> Any:
        """一次查询等待全览下两天路线、顺序编号和关键地点。"""
        ready_xpath = (
            '//*[@id="route_editor_overview" '
            'and .//*[@clickable="true" and .//Text[@text="Day1"] '
            'and .//Text[@text="通菜街"]] '
            'and .//*[@clickable="true" and .//Text[@text="Day2"] '
            'and .//Text[@text="铜锣湾"]] '
            'and .//Text[@id="dayNumber" and @text="1"] '
            'and .//Text[@id="dayNumber" and @text="2"] '
            'and .//Text[@text="旺角"]]'
        )
        return self.wait_xpath(ready_xpath, "编辑行程页全览路线内容", timeout=timeout)

    def tap_overview_tab(self, *, timeout: float = 8) -> Any:
        """点击全览Tab。"""
        component = self.tap_xpath(
            self.OVERVIEW_TAB_XPATH,
            "编辑行程页全览Tab",
            timeout=timeout,
        )
        return component

    def tap_day_1_tab(self, *, timeout: float = 8) -> Any:
        """点击Day1 Tab。"""
        component = self.tap_xpath(
            self.DAY_1_TAB_XPATH,
            "编辑行程页Day1 Tab",
            timeout=timeout,
        )
        return component

    def tap_day_2_tab(self, *, timeout: float = 8) -> Any:
        """点击Day2 Tab。"""
        component = self.tap_xpath(
            self.DAY_N_TAB_XPATH,
            "编辑行程页Day2 Tab",
            timeout=timeout,
        )
        return component

    def tap_day_3_tab(self, *, timeout: float = 8) -> Any:
        """点击Day3 Tab。"""
        text_component = self.wait_xpath(
            self.DAY_3_TAB_XPATH,
            "编辑行程页Day3 Tab",
            timeout=timeout,
        )
        text_bounds = text_component.getBounds()
        text_center_x = (int(text_bounds.left) + int(text_bounds.right)) // 2
        text_center_y = (int(text_bounds.top) + int(text_bounds.bottom)) // 2

        candidates: list[tuple[int, Any]] = []
        for component in self._as_list(
            self.driver.find_all_components(BY.xpath(self.DAY_3_TAB_CONTAINER_XPATH))
        ):
            if not self._is_visible(component):
                continue
            bounds = component.getBounds()
            left = int(bounds.left)
            right = int(bounds.right)
            top = int(bounds.top)
            bottom = int(bounds.bottom)
            width = right - left
            height = bottom - top
            if (
                left <= text_center_x <= right
                and top <= text_center_y <= bottom
                and width <= 260
                and height <= 160
            ):
                candidates.append((width * height, component))

        component = text_component
        if candidates:
            candidates.sort(key=lambda item: item[0])
            component = candidates[0][1]

        bounds = component.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )
        return component

    def tap_pending_tab(self, *, timeout: float = 8) -> Any:
        """点击待规划Tab。"""
        component = self.tap_xpath(
            self.PENDING_TAB_XPATH,
            "编辑行程页待规划Tab",
            timeout=timeout,
        )
        return component

    def wait_day_1_loaded(self, *, timeout: float = 8) -> dict[str, Any]:
        """等待Day1路线卡片加载完成。"""
        return self.snapshot_xpaths(
            {
                "list": (self.CHILD_LIST_XPATH, "编辑行程页Day1列表"),
                "first_poi": (self.DAY_1_CHILD_POI_XPATH, "编辑行程页Day1地点"),
                "second_poi": (
                    self.DAY_1_CHILD_SECOND_POI_XPATH,
                    "编辑行程页Day1第二个地点",
                ),
                "distance": (self.CHILD_DISTANCE_XPATH, "编辑行程页Day1相邻距离"),
            },
            timeout=timeout,
        )

    def wait_day_1_ready(self, *, timeout: float = 8) -> Any:
        """一次查询等待 Day1 列表及首个通菜街地点。"""
        ready_xpath = (
            '//*[@id="route_editor_childs" '
            'and .//Text[contains(@text, "通菜街")]]'
        )
        return self.wait_xpath(ready_xpath, "编辑行程页Day1路线内容", timeout=timeout)

    def wait_day_1_content_ready(self, *, timeout: float = 8) -> Any:
        """一次查询等待 Day1 两个关键地点和相邻距离。"""
        ready_xpath = (
            '//*[@id="route_editor_childs" '
            'and .//Text[contains(@text, "通菜街")] '
            'and .//Text[contains(@text, "旺角")] '
            'and .//Text[contains(@text, "km")]]'
        )
        return self.wait_xpath(ready_xpath, "编辑行程页Day1完整路线", timeout=timeout)

    def wait_day_2_loaded(self, *, timeout: float = 8) -> dict[str, Any]:
        """等待Day2路线卡片加载完成。"""
        return self.snapshot_xpaths(
            {
                "list": (self.CHILD_LIST_XPATH, "编辑行程页Day2列表"),
                "first_poi": (self.DAY_2_CHILD_POI_XPATH, "编辑行程页Day2地点"),
                "second_poi": (
                    self.DAY_2_CHILD_SECOND_POI_XPATH,
                    "编辑行程页Day2第二个地点",
                ),
                "distance": (self.CHILD_DISTANCE_XPATH, "编辑行程页Day2相邻距离"),
            },
            timeout=timeout,
        )

    def wait_day_2_ready(self, *, timeout: float = 8) -> Any:
        """一次查询等待 Day2 两个关键地点和相邻距离。"""
        ready_xpath = (
            '//*[@id="route_editor_childs" '
            'and .//Text[contains(@text, "铜锣湾")] '
            'and .//Text[contains(@text, "希慎广场")] '
            'and .//Text[contains(@text, "km")]]'
        )
        return self.wait_xpath(ready_xpath, "编辑行程页Day2完整路线", timeout=timeout)

    def wait_pending_loaded(self, *, timeout: float = 8) -> dict[str, Any]:
        """等待待规划栏加载完成。"""
        return self.snapshot_xpaths(
            {
                "list": (self.CHILD_LIST_XPATH, "编辑行程页待规划列表"),
                "add": (self.PENDING_ADD_ENTRY_XPATH, "编辑行程页待规划添加入口"),
                "poi": (self.PENDING_POI_XPATH, "编辑行程页待规划地点"),
            },
            timeout=timeout,
        )

    def wait_pending_ready(self, *, timeout: float = 8) -> Any:
        """一次查询等待待规划栏、添加入口和已有地点。"""
        ready_xpath = (
            '//*[@id="route_editor_childs" '
            'and .//Text[@text="添加地点/活动" or contains(@text, "添加地点")] '
            'and .//Text[contains(@text, "坚尼地城") '
            'or contains(@text, "太平山顶")]]'
        )
        return self.wait_xpath(ready_xpath, "编辑行程页待规划内容", timeout=timeout)

    def wait_day_3_empty_loaded(self, *, timeout: float = 8) -> Any:
        """等待新增Day3分组展示，并返回Day3分组下的添加地点入口。"""
        return self.day_3_add_place_entry(timeout=timeout)

    def switch_to_day_3_empty(self, *, timeout: float = 12) -> Any:
        """切换或定位新增Day3，并返回Day3分组下的添加地点入口。"""
        deadline = time.time() + timeout
        last_error: Exception | None = None

        while time.time() < deadline:
            try:
                self.tap_day_3_tab(timeout=min(2, max(0.5, deadline - time.time())))
            except RuntimeError as error:
                last_error = error
            time.sleep(0.5)
            try:
                return self.day_3_add_place_entry(
                    timeout=min(2.5, max(0.8, deadline - time.time()))
                )
            except RuntimeError as error:
                last_error = error
                time.sleep(0.4)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到Day3分组下的添加地点入口：{last_error}")

    def first_poi_select_icon(self, *, timeout: float = 8) -> Any:
        """返回 Day1 第一个 POI 左侧勾选框图标。"""
        return self.wait_xpath(
            self.FIRST_SELECT_ICON_XPATH,
            "编辑行程页Day1第一个POI勾选框",
            timeout=timeout,
        )

    def tap_first_poi_select_icon(self, *, timeout: float = 8) -> Any:
        """点击 Day1 第一个 POI 左侧勾选框。"""
        icon = self.first_poi_select_icon(timeout=timeout)
        bounds = icon.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )
        return icon

    @classmethod
    def child_poi_text_xpath(cls, poi_name: str) -> str:
        """返回编辑页子列表内指定 POI 文本 XPath。"""
        return f'//*[@id="route_editor_childs"]//Text[contains(@text, "{poi_name}")]'

    @classmethod
    def child_poi_card_xpath(cls, poi_name: str) -> str:
        """返回编辑页子列表内包含指定 POI 的可点击卡片 XPath。"""
        return (
            f'//*[@id="route_editor_childs"]//*[@clickable="true" '
            f'and .//Text[contains(@text, "{poi_name}")]]'
        )

    def child_poi_card(
        self,
        poi_name: str,
        *,
        timeout: float = 8,
    ) -> Any:
        """返回 Day 子列表中指定 POI 的卡片。"""
        return self.wait_xpath(
            self.child_poi_card_xpath(poi_name),
            f"编辑行程页POI卡片-{poi_name}",
            timeout=timeout,
        )

    def _child_poi_actionable_limits(self) -> tuple[int, int] | None:
        """读取一次 Day 列表可操作区边界，供同一轮滑动复用。"""
        child_list = self.find_xpath(self.CHILD_LIST_XPATH)
        if child_list is None:
            return None

        list_bounds = child_list.getBounds()
        top_limit = int(list_bounds.top) + 8
        bottom_limit = int(list_bounds.bottom) - 8
        complete_button = self.find_xpath(self.EDIT_COMPLETE_XPATH)
        if complete_button is not None:
            complete_bounds = complete_button.getBounds()
            # XPath 命中的是按钮文字，真实蓝色按钮容器会比文字顶部更高。
            bottom_limit = min(bottom_limit, int(complete_bounds.top) - 60)
        return top_limit, bottom_limit

    def child_poi_select_icon(
        self,
        poi_name: str,
        *,
        timeout: float = 8,
    ) -> Any:
        """返回指定 POI 卡片左侧勾选框图标。"""
        deadline = time.time() + timeout
        last_card = None
        while time.time() < deadline:
            try:
                card = self.child_poi_card(poi_name, timeout=1)
            except RuntimeError:
                time.sleep(0.3)
                continue

            last_card = card
            icon = self._find_child_poi_select_icon_in_card(card)
            if icon is not None:
                return icon
            time.sleep(0.3)

        debug_bounds = None
        if last_card is not None:
            debug_bounds = last_card.getBounds()
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到POI“{poi_name}”左侧勾选框，"
            f"timeout={timeout}s，卡片bounds={debug_bounds}"
        )

    def _find_child_poi_select_icon_in_card(self, card: Any) -> Any | None:
        """从已定位的 POI 卡片中查找左侧勾选框，避免重复查询卡片。"""
        card_bounds = card.getBounds()
        card_left = int(card_bounds.left)
        card_top = int(card_bounds.top)
        card_right = int(card_bounds.right)
        card_bottom = int(card_bounds.bottom)

        images = self._as_list(
            self.driver.find_all_components(
                BY.xpath('//*[@id="route_editor_childs"]//Image')
            )
        )
        candidates = []
        for image in images:
            bounds = image.getBounds()
            left = int(bounds.left)
            top = int(bounds.top)
            right = int(bounds.right)
            bottom = int(bounds.bottom)
            width = right - left
            height = bottom - top
            if (
                card_left <= left
                and right <= min(card_right, card_left + 150)
                and card_top <= top
                and bottom <= card_bottom
                and 20 <= width <= 90
                and 20 <= height <= 90
            ):
                candidates.append((top, left, image))

        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], item[1]))
        return candidates[0][2]

    @staticmethod
    def _is_component_in_actionable_area(
        component: Any,
        limits: tuple[int, int] | None,
    ) -> bool:
        """判断组件是否完整位于 Day 列表可点击区域。"""
        if limits is None:
            return False
        bounds = component.getBounds()
        top_limit, bottom_limit = limits
        return int(bounds.top) >= top_limit and int(bounds.bottom) <= bottom_limit

    def tap_child_poi_select_icon(
        self,
        poi_name: str,
        *,
        timeout: float = 8,
    ) -> Any:
        """点击指定 POI 左侧勾选框。"""
        icon = self.child_poi_select_icon(poi_name, timeout=timeout)
        bounds = icon.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )
        return icon

    def wait_selection_action_menu_loaded(self, *, timeout: float = 8) -> Any:
        """等待选择 POI 后底部批量操作菜单展示完整。"""
        return self.wait_xpath(
            self.SELECTION_ACTION_MENU_XPATH,
            "编辑行程页POI选中后的批量操作菜单",
            timeout=timeout,
        )

    def selection_cancel_action(self, *, timeout: float = 8) -> Any:
        """返回选中菜单中的取消操作。"""
        return self.wait_xpath(
            self.SELECTION_CANCEL_ACTION_XPATH,
            "编辑行程页选中菜单-取消",
            timeout=timeout,
        )

    def tap_selection_cancel(self, *, timeout: float = 8) -> None:
        """点击选中菜单中的取消操作。"""
        self.selection_cancel_action(timeout=timeout).click()

    def selection_delete_action(self, *, timeout: float = 8) -> Any:
        """返回选中菜单中的删除操作。"""
        return self.wait_xpath(
            self.SELECTION_DELETE_ACTION_XPATH,
            "编辑行程页选中菜单-删除",
            timeout=timeout,
        )

    def tap_selection_delete(self, *, timeout: float = 8) -> None:
        """点击选中菜单中的删除操作。"""
        self.selection_delete_action(timeout=timeout).click()

    def selection_move_action(self, *, timeout: float = 8) -> Any:
        """返回选中菜单中的移动到操作。"""
        return self.wait_xpath(
            self.SELECTION_MOVE_ACTION_XPATH,
            "编辑行程页选中菜单-移动到",
            timeout=timeout,
        )

    def tap_selection_move(self, *, timeout: float = 8) -> None:
        """点击选中菜单中的移动到操作。"""
        self.selection_move_action(timeout=timeout).click()

    def selection_copy_action(self, *, timeout: float = 8) -> Any:
        """返回选中菜单中的复制到操作。"""
        return self.wait_xpath(
            self.SELECTION_COPY_ACTION_XPATH,
            "编辑行程页选中菜单-复制到",
            timeout=timeout,
        )

    def tap_selection_copy(self, *, timeout: float = 8) -> None:
        """点击选中菜单中的复制到操作。"""
        self.selection_copy_action(timeout=timeout).click()

    def wait_delete_confirm_loaded(self, *, timeout: float = 8) -> Any:
        """等待删除地点二次确认 Sheet 展示。"""
        return self.snapshot_xpaths(
            {
                "sheet": (self.DELETE_CONFIRM_SHEET_XPATH, "删除地点确认Sheet"),
                "cancel": (self.DELETE_CONFIRM_CANCEL_XPATH, "删除地点确认Sheet-取消"),
                "delete": (self.DELETE_CONFIRM_BUTTON_XPATH, "删除地点确认Sheet-删除"),
            },
            timeout=timeout,
        )["sheet"]

    def tap_confirm_delete_poi(self, *, timeout: float = 8) -> None:
        """在删除地点确认 Sheet 中点击删除。"""
        self.tap_xpath(
            self.DELETE_CONFIRM_BUTTON_XPATH,
            "删除地点确认Sheet-删除",
            timeout=timeout,
        )

    def wait_delete_confirm_closed(self, *, timeout: float = 5) -> None:
        """等待删除地点确认 Sheet 消失。"""
        self.driver.wait_for_component_disappear(
            BY.xpath(self.DELETE_CONFIRM_SHEET_XPATH),
            timeout=timeout,
        )
        if (
            self.driver.wait_for_component(
                BY.xpath(self.DELETE_CONFIRM_SHEET_XPATH),
                timeout=0.5,
            )
            is not None
        ):
            raise RuntimeError(f"[{self.PAGE_NAME}] 删除地点确认Sheet关闭后仍然展示")

    def wait_child_poi_absent(self, poi_name: str, *, timeout: float = 8) -> None:
        """等待编辑子列表内指定 POI 消失。"""
        deadline = time.time() + timeout
        xpath = self.child_poi_text_xpath(poi_name)
        while time.time() < deadline:
            if self.driver.wait_for_component(BY.xpath(xpath), timeout=0.5) is None:
                return
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 删除后仍找到POI“{poi_name}”，timeout={timeout}s"
        )

    def child_list(self, *, timeout: float = 8) -> Any:
        """返回当前 Day 子列表。"""
        return self.wait_xpath(self.CHILD_LIST_XPATH, "编辑行程页Day子列表", timeout=timeout)

    def swipe_child_list_up(self) -> None:
        """在当前 Day 子列表内向下浏览更多 POI。"""
        child_list = self.child_list(timeout=5)
        self.driver.swipe("UP", distance=65, area=child_list, swipe_time=0.55)
        time.sleep(0.8)

    def drag_child_poi_below(
        self,
        source_poi: str,
        target_poi: str,
        *,
        timeout: float = 8,
    ) -> tuple[Any, Any]:
        """长按拖拽当前 Day 列表中的 POI 到目标 POI 下方。"""
        source_card = self.child_poi_card(source_poi, timeout=timeout)
        target_card = self.child_poi_card(target_poi, timeout=timeout)
        source_bounds = source_card.getBounds()
        target_bounds = target_card.getBounds()
        start = (
            (int(source_bounds.left) + int(source_bounds.right)) // 2,
            (int(source_bounds.top) + int(source_bounds.bottom)) // 2,
        )
        end_y = int(target_bounds.bottom) + max(12, (int(target_bounds.bottom) - int(target_bounds.top)) // 4)
        end = (
            (int(target_bounds.left) + int(target_bounds.right)) // 2,
            end_y,
        )
        self.driver.drag(start, end, press_time=1.2, drag_time=1.1)
        time.sleep(1.5)
        return source_card, target_card

    def scroll_child_list_until_poi_visible(
        self,
        poi_name: str,
        *,
        max_swipes: int = 12,
        timeout: float = 8,
    ) -> Any:
        """滚动当前 Day 子列表，直到指定 POI 的勾选框处于可操作区。"""
        xpath = self.child_poi_text_xpath(poi_name)
        actionable_limits: tuple[int, int] | None = None
        for swipe_count in range(max_swipes + 1):
            component = self.driver.wait_for_component(BY.xpath(xpath), timeout=0.8)
            if component is not None:
                card = self.find_xpath(self.child_poi_card_xpath(poi_name))
                if card is not None:
                    actionable_limits = (
                        actionable_limits or self._child_poi_actionable_limits()
                    )
                    select_icon = self._find_child_poi_select_icon_in_card(card)
                    if select_icon is not None and self._is_component_in_actionable_area(
                        select_icon,
                        actionable_limits,
                    ):
                        return component
            if swipe_count == max_swipes:
                break
            self.swipe_child_list_up()
        component = self.wait_xpath(
            xpath,
            f"编辑行程页POI-{poi_name}",
            timeout=timeout,
        )
        card = self.child_poi_card(poi_name, timeout=timeout)
        select_icon = self._find_child_poi_select_icon_in_card(card)
        if select_icon is None or not self._is_component_in_actionable_area(
            select_icon,
            actionable_limits,
        ):
            raise RuntimeError(
                f"[{self.PAGE_NAME}] POI“{poi_name}”已出现但勾选框仍不可操作，"
                f"卡片bounds={card.getBounds()}，"
                f"勾选框bounds={select_icon.getBounds() if select_icon else None}"
            )
        return component

    def assert_child_poi_absent_while_scrolling(
        self,
        poi_name: str,
        *,
        max_swipes: int = 8,
    ) -> list[str]:
        """从当前列表位置向下扫描，确认指定 POI 不再展示。"""
        seen_texts: list[str] = []
        previous_snapshot: list[str] | None = None
        same_snapshot_count = 0
        for swipe_count in range(max_swipes + 1):
            current_texts = self.visible_child_list_texts()
            seen_texts.extend(text for text in current_texts if text not in seen_texts)
            if any(poi_name in text for text in current_texts):
                raise RuntimeError(
                    f"[{self.PAGE_NAME}] 当前Day列表仍展示POI“{poi_name}”，"
                    f"当前可见文本={current_texts}"
                )
            if current_texts == previous_snapshot:
                same_snapshot_count += 1
            else:
                same_snapshot_count = 0
            if same_snapshot_count >= 1:
                break
            if swipe_count < max_swipes:
                self.swipe_child_list_up()
            previous_snapshot = current_texts
        return seen_texts

    def _visible_component_candidates(self, xpath: str) -> list[tuple[int, int, int, Any]]:
        """返回可见组件候选，按纵坐标从上到下排序。"""
        candidates = []
        for component in self._as_list(self.driver.find_all_components(BY.xpath(xpath))):
            if not self._is_visible(component):
                continue
            bounds = component.getBounds()
            width = int(bounds.right) - int(bounds.left)
            height = int(bounds.bottom) - int(bounds.top)
            candidates.append((int(bounds.top), int(bounds.left), width * height, component))
        candidates.sort(key=lambda item: (item[0], item[1]))
        return candidates

    def _tab_bar_bottom(self) -> int:
        """返回编辑页 Tab 栏底部坐标，用于过滤顶部 Tab 候选。"""
        tab_bar = self.find_xpath(self.TAB_BAR_XPATH)
        if tab_bar is None:
            return 0
        bounds = tab_bar.getBounds()
        return int(bounds.bottom)

    def move_target_day_2(self, *, timeout: float = 8) -> Any:
        """返回移动目标里的 Day2 文本，避免点击大容器中心落到待规划。"""
        deadline = time.time() + timeout
        last_candidates: list[tuple[int, int, int, Any]] = []
        while time.time() < deadline:
            candidates = self._visible_component_candidates(
                self.MOVE_TARGET_DAY_2_TEXT_XPATH
            )
            last_candidates = candidates
            min_top = self._tab_bar_bottom() + 20
            panel_candidates = [
                (top, component)
                for top, _, _, component in candidates
                if top > min_top
            ]
            if panel_candidates:
                panel_candidates.sort(key=lambda item: item[0], reverse=True)
                return panel_candidates[0][1]
            time.sleep(0.3)
        candidate_bounds = []
        for _, _, _, component in last_candidates:
            bounds = component.getBounds()
            candidate_bounds.append(
                [int(bounds.left), int(bounds.top), int(bounds.right), int(bounds.bottom)]
            )
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到移动目标面板里的Day2，timeout={timeout}s，"
            f"当前Day2候选bounds={candidate_bounds}"
        )

    def wait_move_target_panel_loaded(self, *, timeout: float = 8) -> Any:
        """等待移动目标面板展示。"""
        return self.move_target_day_2(timeout=timeout)

    def tap_move_target_day_2(self, *, timeout: float = 8) -> None:
        """在移动目标面板里选择 Day2。"""
        target = self.move_target_day_2(timeout=timeout)
        bounds = target.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )

    def copy_target_pending(self, *, timeout: float = 8) -> Any:
        """返回复制目标里的待规划文本，避免点击顶部Tab。"""
        deadline = time.time() + timeout
        last_candidates: list[tuple[int, int, int, Any]] = []
        while time.time() < deadline:
            candidates = self._visible_component_candidates(
                self.COPY_TARGET_PENDING_TEXT_XPATH
            )
            last_candidates = candidates
            min_top = self._tab_bar_bottom() + 20
            panel_candidates = [
                (top, component)
                for top, _, _, component in candidates
                if top > min_top
            ]
            if panel_candidates:
                panel_candidates.sort(key=lambda item: item[0], reverse=True)
                return panel_candidates[0][1]
            time.sleep(0.3)
        candidate_bounds = []
        for _, _, _, component in last_candidates:
            bounds = component.getBounds()
            candidate_bounds.append(
                [int(bounds.left), int(bounds.top), int(bounds.right), int(bounds.bottom)]
            )
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到复制目标面板里的待规划，timeout={timeout}s，"
            f"当前待规划候选bounds={candidate_bounds}"
        )

    def wait_copy_target_panel_loaded(self, *, timeout: float = 8) -> Any:
        """等待复制目标面板展示。"""
        return self.copy_target_pending(timeout=timeout)

    def tap_copy_target_pending(self, *, timeout: float = 8) -> None:
        """在复制目标面板里选择待规划。"""
        target = self.copy_target_pending(timeout=timeout)
        bounds = target.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )

    def wait_copy_target_panel_closed(self, *, timeout: float = 5) -> None:
        """等待复制目标面板关闭，确认目标选择已被页面接受。"""
        self.driver.wait_for_component_disappear(
            BY.xpath(self.COPY_TARGET_TITLE_XPATH),
            timeout=timeout,
        )
        if (
            self.driver.wait_for_component(
                BY.xpath(self.COPY_TARGET_TITLE_XPATH),
                timeout=0.5,
            )
            is not None
        ):
            raise RuntimeError(f"[{self.PAGE_NAME}] 选择复制目标后复制面板仍未关闭")

    def wait_move_target_panel_closed(self, *, timeout: float = 5) -> None:
        """等待移动目标面板关闭，确认目标选择已被页面接受。"""
        self.driver.wait_for_component_disappear(
            BY.xpath(self.MOVE_TARGET_TITLE_XPATH),
            timeout=timeout,
        )
        if (
            self.driver.wait_for_component(
                BY.xpath(self.MOVE_TARGET_TITLE_XPATH),
                timeout=0.5,
            )
            is not None
        ):
            raise RuntimeError(f"[{self.PAGE_NAME}] 选择移动目标后移动面板仍未关闭")

    def wait_day_1_after_wangjiao_deleted(self, *, timeout: float = 8) -> None:
        """等待 Day1 删除旺角后列表重新排序并刷新距离。"""
        ready_xpath = (
            '//*[@id="route_editor_childs" '
            'and .//Text[contains(@text, "通菜街")] '
            'and .//Text[contains(@text, "2.") and contains(@text, "信和中心")] '
            'and .//Text[contains(@text, "km")]]'
        )
        self.wait_xpath(ready_xpath, "编辑行程页Day1删除旺角后的路线", timeout=timeout)
        self.wait_child_poi_absent("旺角", timeout=timeout)

    def wait_selection_action_menu_closed(self, *, timeout: float = 5) -> None:
        """等待选中菜单消失。"""
        self.driver.wait_for_component_disappear(
            BY.xpath(self.SELECTION_ACTION_MENU_XPATH),
            timeout=timeout,
        )
        if (
            self.driver.wait_for_component(
                BY.xpath(self.SELECTION_ACTION_MENU_XPATH),
                timeout=0.5,
            )
            is not None
        ):
            raise RuntimeError(f"[{self.PAGE_NAME}] POI选中菜单取消后仍然展示")

    def visible_child_list_texts(self) -> list[str]:
        """读取当前编辑行程子列表内可见文本，用于校验取消后列表未变化。"""
        components = self._as_list(
            self.driver.find_all_components(BY.xpath(self.CHILD_LIST_TEXT_XPATH))
        )
        texts: list[str] = []
        for component in components:
            if not self._is_visible(component):
                continue
            text = component.getText().strip()
            if text:
                texts.append(text)
        return texts

    def wait_add_entry(self, *, timeout: float = 8) -> Any:
        """等待新增入口展示；当前版本新增按钮是无文案图标，优先文案定位，失败后按Tab栏内小图标兜底。"""
        text_entry = self.driver.wait_for_component(BY.xpath(self.ADD_TEXT_XPATH), timeout=1)
        if text_entry is not None:
            return text_entry

        deadline = time.time() + timeout
        while time.time() < deadline:
            components = self._as_list(
                self.driver.find_all_components(BY.xpath(self.ADD_ICON_XPATH))
            )
            candidates = []
            for component in components:
                if not self._is_visible(component):
                    continue
                bounds = component.getBounds()
                width = int(bounds.right) - int(bounds.left)
                height = int(bounds.bottom) - int(bounds.top)
                if width <= 180 and height <= 180:
                    candidates.append((int(bounds.left), component))

            if candidates:
                candidates.sort(key=lambda item: item[0])
                return candidates[-1][1]
            time.sleep(0.3)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到编辑行程页新增入口，timeout={timeout}s")

    def tap_add_day_entry(self, *, timeout: float = 8) -> Any:
        """点击Tab区域的新增Day入口。"""
        entry = self.wait_add_entry(timeout=timeout)
        bounds = entry.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )
        return entry

    def child_add_place_entry(self, *, timeout: float = 8) -> Any:
        """返回当前Day列表里的添加地点/活动入口。"""
        return self.wait_xpath(
            self.PENDING_ADD_ENTRY_XPATH,
            "编辑行程页添加地点/活动入口",
            timeout=timeout,
        )

    def tap_child_add_place_entry(self, *, timeout: float = 8) -> None:
        """点击当前Day列表里的添加地点/活动入口。"""
        self.child_add_place_entry(timeout=timeout).click()

    def day_3_add_place_entry(self, *, timeout: float = 8) -> Any:
        """返回Day3分组下方、待规划分组上方的添加地点/活动入口。"""
        deadline = time.time() + timeout
        last_debug: str = ""

        while time.time() < deadline:
            candidates = self._day_3_add_place_candidates()
            if candidates:
                return candidates[0][1]

            day3_titles = self._visible_component_candidates(
                self.CHILD_DAY_3_SECTION_XPATH
            )
            pending_titles = self._visible_component_candidates(
                self.CHILD_PENDING_SECTION_XPATH
            )
            add_entries = self._visible_component_candidates(
                self.PENDING_ADD_ENTRY_XPATH
            )
            last_debug = (
                f"Day3标题={self._debug_candidate_bounds(day3_titles)}，"
                f"待规划标题={self._debug_candidate_bounds(pending_titles)}，"
                f"添加入口={self._debug_candidate_bounds(add_entries)}"
            )
            time.sleep(0.3)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到Day3分组下的添加地点/活动入口，timeout={timeout}s，{last_debug}"
        )

    def tap_day_3_add_place_entry(self, *, timeout: float = 8) -> Any:
        """点击Day3分组下方的添加地点/活动入口。"""
        entry = self.day_3_add_place_entry(timeout=timeout)
        bounds = entry.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )
        return entry

    def _day_3_add_place_candidates(self) -> list[tuple[int, Any]]:
        day3_titles = self._visible_component_candidates(self.CHILD_DAY_3_SECTION_XPATH)
        add_entries = self._visible_component_candidates(self.PENDING_ADD_ENTRY_XPATH)
        if not day3_titles or not add_entries:
            return []

        day3_bottom = max(int(component.getBounds().bottom) for _, _, _, component in day3_titles)
        pending_titles = self._visible_component_candidates(self.CHILD_PENDING_SECTION_XPATH)
        pending_top = min(
            (
                int(component.getBounds().top)
                for _, _, _, component in pending_titles
                if int(component.getBounds().top) > day3_bottom
            ),
            default=10**9,
        )

        candidates: list[tuple[int, Any]] = []
        for _, _, _, component in add_entries:
            bounds = component.getBounds()
            top = int(bounds.top)
            if day3_bottom <= top < pending_top:
                candidates.append((top, component))
        candidates.sort(key=lambda item: item[0])
        return candidates

    @staticmethod
    def _debug_candidate_bounds(candidates: list[tuple[int, int, int, Any]]) -> list[list[int]]:
        bounds_list: list[list[int]] = []
        for _, _, _, component in candidates:
            bounds = component.getBounds()
            bounds_list.append(
                [int(bounds.left), int(bounds.top), int(bounds.right), int(bounds.bottom)]
            )
        return bounds_list

    @classmethod
    def add_poi_result_text_xpath(cls, poi_name: str) -> str:
        """返回添加地点搜索结果里的指定POI文本 XPath。"""
        return f'//Text[@text="{poi_name}" or contains(@text, "{poi_name}")]'

    @classmethod
    def add_poi_result_clickable_xpath(cls, poi_name: str) -> str:
        """返回添加地点搜索结果里包含指定POI的可点击卡片 XPath。"""
        return (
            f'//*[@clickable="true" and .//Text'
            f'[@text="{poi_name}" or contains(@text, "{poi_name}")]]'
        )

    def input_add_poi_keyword(self, keyword: str, *, timeout: float = 8) -> Any:
        """在添加地点搜索框输入关键词。"""
        search_input = self.input_xpath(
            self.ADD_POI_SEARCH_INPUT_XPATH,
            keyword,
            "添加地点搜索框",
            timeout=timeout,
        )
        return search_input

    def add_poi_search_result(self, poi_name: str, *, timeout: float = 8) -> Any:
        """返回添加地点搜索结果里的指定POI。"""
        deadline = time.time() + timeout
        text_xpath = self.add_poi_result_text_xpath(poi_name)
        clickable_xpath = self.add_poi_result_clickable_xpath(poi_name)
        while time.time() < deadline:
            result = self.find_xpath(clickable_xpath)
            if result is not None:
                return result
            result = self.find_xpath(text_xpath)
            if result is not None:
                return result
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到添加地点搜索结果“{poi_name}”，timeout={timeout}s"
        )

    def tap_add_poi_search_result(self, poi_name: str, *, timeout: float = 8) -> Any:
        """点击添加地点搜索结果里的指定POI。"""
        result = self.add_poi_search_result(poi_name, timeout=timeout)
        bounds = result.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )
        return result

    def tap_add_poi_search_result_and_wait_added(
        self,
        poi_name: str,
        *,
        timeout: float = 12,
    ) -> Any:
        """点击添加地点搜索结果，并确认回到当前Day列表且POI已出现。"""
        deadline = time.time() + timeout
        last_error: Exception | None = None
        while time.time() < deadline:
            try:
                self.tap_add_poi_search_result(
                    poi_name,
                    timeout=min(3, max(0.5, deadline - time.time())),
                )
                break
            except RuntimeError as error:
                last_error = error
                time.sleep(0.4)
        else:
            raise RuntimeError(
                f"[{self.PAGE_NAME}] 未能点击添加地点搜索结果“{poi_name}”：{last_error}"
            )

        self.driver.wait_for_component_disappear(
            BY.xpath(self.ADD_POI_SEARCH_INPUT_XPATH),
            timeout=min(5, max(1, deadline - time.time())),
        )
        return self.scroll_child_list_until_poi_visible(
            poi_name,
            max_swipes=8,
            timeout=max(3, deadline - time.time()),
        )

    def back_button(self, *, timeout: float = 8) -> Any:
        """返回编辑页左上角页面内返回按钮。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            components = self._as_list(
                self.driver.find_all_components(BY.xpath(self.BACK_BUTTON_XPATH))
            )
            candidates = []
            for component in components:
                if not self._is_visible(component):
                    continue
                bounds = component.getBounds()
                if int(bounds.left) <= 320 and int(bounds.top) <= 360:
                    candidates.append((int(bounds.top), int(bounds.left), component))

            if candidates:
                candidates.sort(key=lambda item: (item[0], item[1]))
                return candidates[0][2]
            time.sleep(0.3)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到编辑行程页返回按钮，timeout={timeout}s")

    def tap_back_button(self, *, timeout: float = 8) -> None:
        """点击编辑行程页左上角返回按钮。"""
        self.back_button(timeout=timeout).click()

    def edit_complete_button(self, *, timeout: float = 8) -> Any:
        """返回编辑完成入口；必须真实存在，不再用返回键兜底。"""
        return self.wait_component(
            BY.xpath(self.EDIT_COMPLETE_XPATH),
            "编辑行程页编辑完成按钮",
            timeout=timeout,
        )

    def tap_edit_complete(self, *, timeout: float = 8) -> Any:
        """点击编辑完成入口，并确认已经离开编辑态。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            complete = self.edit_complete_button(
                timeout=min(2, max(0.5, deadline - time.time()))
            )
            bounds = complete.getBounds()
            self.driver.click(
                (
                    (int(bounds.left) + int(bounds.right)) // 2,
                    (int(bounds.top) + int(bounds.bottom)) // 2,
                )
            )
            time.sleep(0.8)
            if self.find_xpath(self.EDIT_COMPLETE_XPATH) is None:
                return complete

        raise RuntimeError(f"[{self.PAGE_NAME}] 点击编辑完成后仍停留在编辑页")
