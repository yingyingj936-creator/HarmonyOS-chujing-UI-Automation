import re
import time
from dataclasses import dataclass
from typing import Any

from hypium import BY

from pages.base_page import BasePage


@dataclass(frozen=True)
class NearbyPoiRecord:
    """附近页 POI 卡片中用于排序断言的字段。"""

    name: str
    rating: float
    distance_meters: float


class NearbyPage(BasePage):
    """附近页页面对象。"""

    PAGE_NAME = "NearbyPage"

    ROOT_XPATH = '//*[@id="NearRootId"]'
    MAP_XPATH = '//*[@id="NearRootId"]//*[@id="mapview"]'
    MAP_LOCATION_BUTTON_XPATH = '//*[@id="map_my_location"]'
    SORT_PANEL_XPATH = '//*[@id="nearby_map_bottom_panel"]'
    POI_LIST_XPATH = '//*[@id="nearby_poiList"]'
    POI_LIST_TEXT_XPATH = '//*[@id="nearby_poiList"]//Text'
    BOTTOM_NAV_ROOT_XPATH = '//*[@id="HwAuthDialog_rootId"]'
    EXPLORE_NEARBY_XPATH = '//*[@id="NearRootId"]//Text[@text="探索附近"]'
    FOOD_CATEGORY_XPATH = '//*[@id="NearRootId"]//Text[@text="找美食"]'
    READY_XPATH = (
        '//*[@id="NearRootId" '
        'and .//*[@id="mapview"] '
        'and .//*[@id="nearby_map_bottom_panel"] '
        'and .//*[@id="nearby_poiList"] '
        'and .//Text[@text="探索附近"] '
        'and .//Text[@text="找美食"]]'
    )
    REGION_ENTRY_XPATH_TEMPLATE = (
        '//*[@id="NearRootId"]//*[@clickable="true" and .//Text[@text="{region_text}"]]'
    )
    CATEGORY_TEXT_XPATH_TEMPLATE = '//*[@id="NearRootId"]//Text[@text="{category_name}"]'
    CATEGORY_ENTRY_XPATH_TEMPLATE = (
        '//*[@id="NearRootId"]//*[@clickable="true" and ./Text[@text="{category_name}"]]'
    )
    SORT_CONTROL_XPATH_TEMPLATE = (
        '//*[@id="nearby_map_bottom_panel"]//*[@clickable="true" '
        'and ./Text[@text="{sort_name}"]]'
    )
    SORT_TEXT_XPATH_TEMPLATE = (
        '//*[@id="nearby_map_bottom_panel"]//Text[@text="{sort_name}"]'
    )
    SORT_OPTION_XPATH_TEMPLATE = (
        '//Text[@text="{sort_name}" and @clickable="true"]'
    )
    SEARCH_ENTRY_XPATH = (
        '//*[@id="nearby_map_bottom_panel"]//*[@clickable="true" '
        'and .//Text[@text="搜索"]]'
    )
    SEARCH_CURRENT_SELECTION_XPATH = '//Text[@text="当前选择："]'
    SEARCH_RELOCATE_XPATH = '//Text[@text="重新定位"]'
    SEARCH_RECOMMEND_TITLE_XPATH = '//Text[@text="推荐地点"]'
    SEARCH_INPUT_XPATH = '//TextInput'
    SEARCH_RESULT_RATING_XPATH = '//Text[starts-with(@text, "评分 ")]'
    RECOMMENDED_POI_TEXT_XPATH_TEMPLATE = '//Text[@text="{poi_name}"]'
    SELECTED_POI_LABEL_XPATH_TEMPLATE = (
        '//*[@id="NearRootId"]//Text[contains(@text, "{poi_keyword}")]'
    )
    POI_TEXT_XPATH_TEMPLATE = '//*[@id="nearby_poiList"]//Text[@text="{poi_name}"]'
    SEARCH_RESULT_TEXT_XPATH_TEMPLATE = '//Text[@text="{text}"]'

    _DISTANCE_PATTERN = re.compile(r"^(\d+(?:\.\d+)?)(m|km)$", re.IGNORECASE)
    _RATING_PATTERN = re.compile(r"^评分\s*(\d+(?:\.\d+)?)$")

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

    @classmethod
    def region_xpath(cls, region_text: str) -> str:
        return f'{cls.ROOT_XPATH}//Text[@text="{region_text}"]'

    @classmethod
    def region_entry_xpath(cls, region_text: str) -> str:
        return cls.REGION_ENTRY_XPATH_TEMPLATE.format(region_text=region_text)

    @classmethod
    def category_text_xpath(cls, category_name: str) -> str:
        return cls.CATEGORY_TEXT_XPATH_TEMPLATE.format(category_name=category_name)

    @classmethod
    def category_entry_xpath(cls, category_name: str) -> str:
        return cls.CATEGORY_ENTRY_XPATH_TEMPLATE.format(category_name=category_name)

    @classmethod
    def sort_control_xpath(cls, sort_name: str) -> str:
        return cls.SORT_CONTROL_XPATH_TEMPLATE.format(sort_name=sort_name)

    @classmethod
    def sort_text_xpath(cls, sort_name: str) -> str:
        return cls.SORT_TEXT_XPATH_TEMPLATE.format(sort_name=sort_name)

    @classmethod
    def sort_option_xpath(cls, sort_name: str) -> str:
        return cls.SORT_OPTION_XPATH_TEMPLATE.format(sort_name=sort_name)

    @classmethod
    def recommended_poi_text_xpath(cls, poi_name: str) -> str:
        return cls.RECOMMENDED_POI_TEXT_XPATH_TEMPLATE.format(poi_name=poi_name)

    @classmethod
    def selected_poi_label_xpath(cls, poi_name: str) -> str:
        keyword = poi_name.split("（", 1)[0].split("(", 1)[0]
        return cls.SELECTED_POI_LABEL_XPATH_TEMPLATE.format(poi_keyword=keyword)

    @classmethod
    def poi_text_xpath(cls, poi_name: str) -> str:
        return cls.POI_TEXT_XPATH_TEMPLATE.format(poi_name=poi_name)

    @classmethod
    def search_result_text_xpath(cls, text: str) -> str:
        return cls.SEARCH_RESULT_TEXT_XPATH_TEMPLATE.format(text=text)

    def wait_loaded(self, *, timeout: float = 10) -> None:
        """等待附近页关键区域加载完成。"""
        self.wait_xpath(self.READY_XPATH, "附近页完整结构", timeout=timeout)
        self.wait_poi_names_loaded(timeout=timeout)

    def current_region_text(self, *, timeout: float = 8) -> str:
        """读取附近页左上角当前地区，避免固定写死目的地。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            root = self.cached_xpath(self.ROOT_XPATH, max_age_seconds=30)
            if root is None:
                time.sleep(0.3)
                continue

            root_bounds = root.getBounds()
            root_left = int(root_bounds.left)
            root_top = int(root_bounds.top)
            root_width = int(root_bounds.right) - root_left
            root_height = int(root_bounds.bottom) - root_top
            max_left = root_left + int(root_width * 0.32)
            max_top = root_top + int(root_height * 0.12)

            components = self.driver.find_all_components(
                BY.xpath(f"{self.ROOT_XPATH}//Text")
            )
            for component in self._as_list(components):
                if not self._is_visible(component):
                    continue
                text = component.getText().strip()
                if not text:
                    continue
                bounds = component.getBounds()
                if int(bounds.left) <= max_left and int(bounds.top) <= max_top:
                    return text
            time.sleep(0.3)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未读取到附近页左上角当前地区")

    def tap_region_selector(self, *, timeout: float = 8) -> str:
        """点击附近页左上角地区入口，并返回点击前的地区名称。"""
        current_region = self.current_region_text(timeout=timeout)
        self.tap_xpath(
            self.region_entry_xpath(current_region),
            f"附近页左上角地区入口“{current_region}”",
            timeout=timeout,
        )
        return current_region

    def wait_region_refreshed(
        self,
        region_text: str,
        *,
        previous_poi_names: tuple[str, ...] | None = None,
        timeout: float = 12,
    ) -> tuple[str, ...]:
        """等待附近页地区和 POI 列表刷新到指定目的地。"""
        deadline = time.time() + timeout
        previous_set = set(previous_poi_names or ())
        self.wait_xpath(
            self.region_xpath(region_text),
            f"附近页左上角地区-{region_text}",
            timeout=timeout,
        )

        while time.time() < deadline:
            names = self.visible_poi_names()
            if names and (not previous_set or set(names) != previous_set):
                return names
            time.sleep(0.5)

        raise RuntimeError(f"[{self.PAGE_NAME}] 附近页切换到“{region_text}”后POI列表未刷新")

    def tap_category_and_wait_refresh(
        self,
        category_name: str,
        *,
        previous_poi_names: tuple[str, ...],
        expected_keywords: tuple[str, ...] = (),
        timeout: float = 10,
    ) -> tuple[str, ...]:
        """点击左侧分类，并等待右侧 POI 列表刷新。"""
        self.tap_category(category_name, timeout=timeout)
        return self.wait_poi_list_refreshed_or_matched(
            previous_poi_names,
            refresh_name=f"附近页分类“{category_name}”",
            expected_keywords=expected_keywords,
            timeout=timeout,
        )

    def tap_category(self, category_name: str, *, timeout: float = 8) -> None:
        """点击左侧当前可见分类，避免命中隐藏节点或被底部导航遮挡的旧节点。"""
        deadline = time.time() + timeout
        last_visible_categories: tuple[str, ...] = ()

        while time.time() < deadline:
            category_text = self.visible_left_category_text(category_name)
            if category_text is not None:
                self._click_component_center(category_text)
                time.sleep(0.8)
                return

            last_visible_categories = self.visible_left_category_names()
            self._swipe_left_category_rail_up()
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到可点击的附近页左侧分类“{category_name}”，"
            f"当前可见分类：{last_visible_categories}"
        )

    def visible_left_category_text(self, category_name: str) -> Any | None:
        """返回左侧分类栏内当前可见且未被底部导航遮挡的指定文字节点。"""
        components = self.driver.find_all_components(
            BY.xpath(self.category_text_xpath(category_name))
        )
        candidates = self._visible_left_rail_components(components)
        if not candidates:
            return None
        return sorted(candidates, key=lambda item: (item[0], item[1]))[0][2]

    def visible_left_category_names(self) -> tuple[str, ...]:
        """读取当前屏幕左侧分类栏内可见分类名，用于报告和失败诊断。"""
        components = self.driver.find_all_components(BY.xpath(f"{self.ROOT_XPATH}//Text"))
        candidates = self._visible_left_rail_components(components)
        names: list[str] = []
        for _, _, component in sorted(candidates, key=lambda item: (item[0], item[1])):
            text = component.getText().strip()
            if text and text not in names:
                names.append(text)
        return tuple(names)

    def _visible_left_rail_components(
        self,
        components: Any,
    ) -> list[tuple[int, int, Any]]:
        """筛选附近页左侧分类栏内可点击区域，排除右侧列表、地图和底部导航。"""
        root = self.cached_xpath(self.ROOT_XPATH, max_age_seconds=30)
        if root is None:
            return []

        root_bounds = root.getBounds()
        root_left = int(root_bounds.left)
        root_top = int(root_bounds.top)
        root_right = int(root_bounds.right)
        root_bottom = int(root_bounds.bottom)
        root_width = root_right - root_left
        left_rail_right = root_left + int(root_width * 0.35)
        bottom_limit = min(root_bottom, self._bottom_navigation_top() - 8)

        candidates: list[tuple[int, int, Any]] = []
        for component in self._as_list(components):
            if not self._is_visible(component):
                continue

            bounds = component.getBounds()
            left = int(bounds.left)
            top = int(bounds.top)
            right = int(bounds.right)
            bottom = int(bounds.bottom)
            center_y = (top + bottom) // 2

            if left < root_left or right > left_rail_right:
                continue
            if top < root_top or center_y >= bottom_limit:
                continue

            candidates.append((top, left, component))
        return candidates

    def _bottom_navigation_top(self) -> int:
        """读取底部导航顶部坐标，避免点击被导航栏遮挡的分类文本。"""
        bottom_nav = self.cached_xpath(
            self.BOTTOM_NAV_ROOT_XPATH,
            max_age_seconds=30,
        )
        if bottom_nav is None or not self._is_visible(bottom_nav):
            return 10**9
        return int(bottom_nav.getBounds().top)

    def _click_component_center(self, component: Any) -> None:
        bounds = component.getBounds()
        x = (int(bounds.left) + int(bounds.right)) // 2
        y = (int(bounds.top) + int(bounds.bottom)) // 2
        self.driver.click((x, y))

    def _swipe_left_category_rail_up(self) -> None:
        """在左侧分类栏区域上滑，让较低的分类进入可见可点区域。"""
        root = self.cached_xpath(self.ROOT_XPATH, max_age_seconds=30)
        if root is None or not self._is_visible(root):
            self.driver.swipe("UP", distance=45, start_point=(0.18, 0.75), swipe_time=0.45)
            return

        bounds = root.getBounds()
        left = int(bounds.left)
        top = int(bounds.top)
        right = int(bounds.right)
        bottom = int(bounds.bottom)
        width = right - left
        height = bottom - top
        x_ratio = (left + int(width * 0.18)) / max(right, 1)
        y_ratio = (top + int(height * 0.72)) / max(bottom, 1)
        self.driver.swipe("UP", distance=45, start_point=(x_ratio, y_ratio), swipe_time=0.45)

    def wait_poi_list_refreshed_or_matched(
        self,
        previous_poi_names: tuple[str, ...],
        *,
        refresh_name: str,
        expected_keywords: tuple[str, ...] = (),
        timeout: float = 10,
    ) -> tuple[str, ...]:
        """等待 POI 列表刷新，或当前内容已符合目标分类特征。"""
        deadline = time.time() + timeout
        previous_set = set(previous_poi_names)
        while time.time() < deadline:
            names = self.visible_poi_names()
            if not names:
                time.sleep(0.5)
                continue
            if expected_keywords and self.names_match_keywords(names, expected_keywords):
                return names
            if not expected_keywords and set(names) != previous_set:
                return names
            time.sleep(0.5)
        raise RuntimeError(f"[{self.PAGE_NAME}] {refresh_name}切换后POI列表未刷新或不符合目标分类")

    def visible_poi_text_component(self, poi_name: str) -> Any | None:
        """返回附近 POI 列表中当前可见的指定 POI 文本节点。"""
        components = self.driver.find_all_components(BY.xpath(self.poi_text_xpath(poi_name)))
        candidates: list[tuple[int, int, Any]] = []
        bottom_limit = self._bottom_navigation_top() - 8
        for component in self._as_list(components):
            if not self._is_visible(component):
                continue
            bounds = component.getBounds()
            center_y = (int(bounds.top) + int(bounds.bottom)) // 2
            if center_y >= bottom_limit:
                continue
            candidates.append((int(bounds.top), int(bounds.left), component))
        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], item[1]))
        return candidates[0][2]

    def first_visible_poi_text_component(
        self,
        *,
        timeout: float = 8,
    ) -> tuple[str, Any]:
        """返回附近 POI 列表当前第一位可见 POI 的名称和文本节点。"""
        deadline = time.time() + timeout
        last_names: tuple[str, ...] = ()
        while time.time() < deadline:
            components = self.driver.find_all_components(BY.xpath(self.POI_LIST_TEXT_XPATH))
            candidates: list[tuple[int, int, str, Any]] = []
            bottom_limit = self._bottom_navigation_top() - 8
            for component in self._as_list(components):
                if not self._is_visible(component):
                    continue
                text = component.getText().strip()
                if not self._is_poi_name(text):
                    continue
                bounds = component.getBounds()
                center_y = (int(bounds.top) + int(bounds.bottom)) // 2
                if center_y >= bottom_limit:
                    continue
                candidates.append((int(bounds.top), int(bounds.left), text, component))

            if candidates:
                candidates.sort(key=lambda item: (item[0], item[1]))
                _, _, name, component = candidates[0]
                return name, component

            last_names = self.visible_poi_names()
            time.sleep(0.4)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未读取到附近 POI 列表第一位地点，"
            f"最后可见POI：{last_names}"
        )

    def scroll_poi_into_view(
        self,
        poi_name: str,
        *,
        max_swipes: int = 10,
    ) -> Any:
        """滚动附近 POI 列表，直到指定 POI 进入可见区域。"""
        visible_names: tuple[str, ...] = ()
        for swipe_index in range(max_swipes + 1):
            component = self.visible_poi_text_component(poi_name)
            if component is not None:
                return component
            visible_names = self.visible_poi_names()
            if swipe_index == max_swipes:
                break

            poi_list = self.find_xpath(self.POI_LIST_XPATH)
            if poi_list is not None and self._is_visible(poi_list):
                self.driver.swipe("UP", distance=65, area=poi_list, swipe_time=0.55)
            else:
                self.driver.swipe(
                    "UP",
                    distance=65,
                    start_point=(0.55, 0.82),
                    swipe_time=0.55,
                )
            time.sleep(0.8)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 附近 POI 列表未找到“{poi_name}”，"
            f"当前可见POI：{visible_names}"
        )

    def tap_poi_in_list(self, poi_name: str, *, max_swipes: int = 10) -> None:
        """点击附近 POI 列表中的指定地点。"""
        component = self.scroll_poi_into_view(poi_name, max_swipes=max_swipes)
        self._click_component_center(component)
        time.sleep(1.2)

    def open_search_layer(self, *, timeout: float = 8) -> None:
        """点击附近页底部抽屉搜索框，打开搜索弹层。"""
        self.tap_xpath(self.SEARCH_ENTRY_XPATH, "附近页底部抽屉搜索框", timeout=timeout)
        self.wait_search_layer_opened(timeout=timeout)

    def wait_search_layer_opened(self, *, timeout: float = 8) -> None:
        """等待附近页搜索弹层展示当前选择、重新定位和推荐地点。"""
        self.wait_xpath(
            self.SEARCH_CURRENT_SELECTION_XPATH,
            "附近页搜索弹层-当前选择",
            timeout=timeout,
        )
        self.wait_xpath(
            self.SEARCH_RELOCATE_XPATH,
            "附近页搜索弹层-重新定位",
            timeout=timeout,
        )
        self.wait_xpath(
            self.SEARCH_RECOMMEND_TITLE_XPATH,
            "附近页搜索弹层-推荐地点",
            timeout=timeout,
        )

    def input_search_keyword(self, keyword: str, *, timeout: float = 8) -> None:
        """在附近页搜索弹层输入关键词，等待结果列表刷新。"""
        self.input_xpath(self.SEARCH_INPUT_XPATH, keyword, "附近页搜索输入框", timeout=timeout)

    def wait_search_result_loaded(
        self,
        poi_name: str,
        *,
        poi_type: str = "景点",
        timeout: float = 8,
    ) -> None:
        """等待附近页搜索结果展示名称、类型、评分、详情和看附近。"""
        ready_xpath = (
            f'//*[.//Text[@text="{poi_name}"] '
            f'and .//Text[@text="{poi_type}"] '
            'and .//Text[starts-with(@text, "评分 ")]]'
        )
        self.wait_xpath(ready_xpath, f"附近页搜索结果-{poi_name}", timeout=timeout)
        self.search_result_action_component(poi_name, "详情", timeout=timeout)
        self.search_result_action_component(poi_name, "看附近", timeout=timeout)

    def search_result_action_component(
        self,
        poi_name: str,
        action_text: str,
        *,
        timeout: float = 8,
    ) -> Any:
        """
        返回指定搜索结果卡片中的动作文本。

        搜索结果可能有多条，同名按钮会重复出现；通过 POI 名称和按钮的空间距离
        绑定同一张卡片，避免点击到其它结果。
        """
        deadline = time.time() + timeout
        last_candidates: list[tuple[int, int, str]] = []
        while time.time() < deadline:
            poi_component = self.find_xpath(self.search_result_text_xpath(poi_name))
            action_components = self.driver.find_all_components(
                BY.xpath(self.search_result_text_xpath(action_text))
            )
            action_components = self._as_list(action_components)
            if poi_component is not None:
                poi_bounds = poi_component.getBounds()
                poi_top = int(poi_bounds.top)
                poi_left = int(poi_bounds.left)
                poi_bottom = int(poi_bounds.bottom)

                candidates: list[tuple[int, int, Any]] = []
                last_candidates = []
                for component in action_components:
                    if not self._is_visible(component):
                        continue
                    bounds = component.getBounds()
                    top = int(bounds.top)
                    left = int(bounds.left)
                    bottom = int(bounds.bottom)
                    if top < poi_top - 120 or top > poi_bottom + 360:
                        continue
                    candidates.append((abs(top - poi_top), abs(left - poi_left), component))
                    last_candidates.append((top, left, component.getText().strip()))

                if candidates:
                    candidates.sort(key=lambda item: (item[0], item[1]))
                    return candidates[0][2]
            time.sleep(0.3)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 搜索结果“{poi_name}”未找到动作“{action_text}”，"
            f"候选={last_candidates}"
        )

    def tap_search_result_action(
        self,
        poi_name: str,
        action_text: str,
        *,
        timeout: float = 8,
    ) -> None:
        """点击指定搜索结果卡片中的详情/看附近等动作。"""
        component = self.search_result_action_component(
            poi_name,
            action_text,
            timeout=timeout,
        )
        self._click_component_center(component)
        time.sleep(1.2)

    def tap_recommended_poi(self, poi_name: str, *, timeout: float = 8) -> None:
        """
        点击推荐地点文本节点。

        推荐地点外层可点击容器在部分设备会匹配到整页根节点，因此这里固定点击
        文本节点中心点，避免误点。
        """
        component = self.wait_xpath(
            self.recommended_poi_text_xpath(poi_name),
            f"附近页推荐地点-{poi_name}",
            timeout=timeout,
        )
        self._click_component_center(component)
        time.sleep(1.2)

    def wait_selected_poi_surrounding_loaded(
        self,
        poi_name: str,
        *,
        timeout: float = 10,
    ) -> tuple[str, ...]:
        """等待地图选中指定 POI，并刷新出周边 POI 列表。"""
        self.wait_xpath(
            self.selected_poi_label_xpath(poi_name),
            f"附近页地图选中地点-{poi_name}",
            timeout=timeout,
        )
        return self.wait_poi_names_loaded(minimum=2, timeout=timeout)

    def tap_map_location_and_wait_loaded(
        self,
        *,
        previous_poi_names: tuple[str, ...] = (),
        timeout: float = 12,
    ) -> tuple[str, ...]:
        """
        点击附近页地图定位按钮，并等待地图与 POI 列表恢复到可验证状态。

        地图坐标本身由 mapview 渲染，UI 树通常不暴露坐标文本；这里用稳定的
        map_my_location id 触发定位，并通过 POI 列表加载完成确认页面未空白。
        """
        self.tap_xpath(
            self.MAP_LOCATION_BUTTON_XPATH,
            "附近页地图定位按钮",
            timeout=timeout,
        )

        clicked_at = time.time()
        deadline = clicked_at + timeout
        previous_set = set(previous_poi_names)
        last_names: tuple[str, ...] = ()
        while time.time() < deadline:
            self.wait_xpath(self.MAP_XPATH, "附近页地图", timeout=2)
            names = self.visible_poi_names()
            if len(names) >= 2:
                last_names = names
                if not previous_set or set(names) != previous_set:
                    return names
                # 定位前可能已经在当前位置；给地图刷新留出时间后接受稳定列表。
                if time.time() - clicked_at >= 3:
                    return names
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 点击地图定位后 POI 列表未恢复加载，"
            f"最后可见POI：{last_names}"
        )

    def open_sort_dropdown(self, current_sort_name: str, *, timeout: float = 8) -> None:
        """点击附近页排序入口，打开排序下拉层。"""
        self.tap_xpath(
            self.sort_control_xpath(current_sort_name),
            f"附近页排序入口“{current_sort_name}”",
            timeout=timeout,
        )
        time.sleep(0.5)

    def tap_sort_option(self, sort_name: str, *, timeout: float = 8) -> None:
        """点击排序下拉层中的选项。"""
        self.tap_xpath(
            self.sort_option_xpath(sort_name),
            f"附近页排序选项“{sort_name}”",
            timeout=timeout,
        )
        time.sleep(1)

    def visible_poi_records(self) -> tuple[NearbyPoiRecord, ...]:
        """读取当前可见 POI 卡片的名称、评分和距离。"""
        components = self.driver.find_all_components(BY.xpath(self.POI_LIST_TEXT_XPATH))
        text_nodes: list[tuple[int, int, str]] = []
        for component in self._as_list(components):
            if not self._is_visible(component):
                continue
            text = component.getText().strip()
            if not text:
                continue
            bounds = component.getBounds()
            text_nodes.append((int(bounds.top), int(bounds.left), text))

        text_nodes.sort(key=lambda item: (item[0], item[1]))
        name_nodes = [
            (top, left, text)
            for top, left, text in text_nodes
            if self._is_poi_name(text)
        ]

        records: list[NearbyPoiRecord] = []
        for index, (name_top, _, name) in enumerate(name_nodes):
            next_name_top = (
                name_nodes[index + 1][0]
                if index + 1 < len(name_nodes)
                else 10**9
            )
            group_texts = [
                text
                for top, _, text in text_nodes
                if name_top <= top < next_name_top
            ]
            rating = self._first_rating(group_texts)
            distance = self._first_distance(group_texts)
            if rating is None or distance is None:
                continue
            records.append(
                NearbyPoiRecord(
                    name=name,
                    rating=rating,
                    distance_meters=distance,
                )
            )
        return tuple(records)

    def wait_poi_records_sorted_by_rating(
        self,
        *,
        minimum: int = 3,
        timeout: float = 10,
    ) -> tuple[NearbyPoiRecord, ...]:
        """等待当前可见 POI 按评分从高到低排列。"""
        return self._wait_poi_records_sorted(
            sort_name="评分优先",
            predicate=self.records_sorted_by_rating_desc,
            minimum=minimum,
            timeout=timeout,
        )

    def wait_poi_records_sorted_by_distance(
        self,
        *,
        minimum: int = 3,
        timeout: float = 10,
    ) -> tuple[NearbyPoiRecord, ...]:
        """等待当前可见 POI 按距离从近到远排列。"""
        return self._wait_poi_records_sorted(
            sort_name="距离优先",
            predicate=self.records_sorted_by_distance_asc,
            minimum=minimum,
            timeout=timeout,
        )

    def _wait_poi_records_sorted(
        self,
        *,
        sort_name: str,
        predicate: Any,
        minimum: int,
        timeout: float,
    ) -> tuple[NearbyPoiRecord, ...]:
        deadline = time.time() + timeout
        last_records: tuple[NearbyPoiRecord, ...] = ()
        self.wait_xpath(self.sort_text_xpath(sort_name), f"附近页当前排序“{sort_name}”", timeout=timeout)

        while time.time() < deadline:
            records = self.visible_poi_records()
            if records:
                last_records = records
            if len(records) >= minimum and predicate(records):
                return records
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 当前可见 POI 未按“{sort_name}”排序："
            f"{self.format_poi_records(last_records)}"
        )

    @staticmethod
    def records_sorted_by_rating_desc(records: tuple[NearbyPoiRecord, ...]) -> bool:
        ratings = [record.rating for record in records]
        return all(ratings[index] >= ratings[index + 1] for index in range(len(ratings) - 1))

    @staticmethod
    def records_sorted_by_distance_asc(records: tuple[NearbyPoiRecord, ...]) -> bool:
        distances = [record.distance_meters for record in records]
        return all(
            distances[index] <= distances[index + 1]
            for index in range(len(distances) - 1)
        )

    @staticmethod
    def format_poi_records(records: tuple[NearbyPoiRecord, ...]) -> str:
        if not records:
            return "未读取到完整 POI 记录"
        return "\n".join(
            f"{index}. {record.name}｜评分 {record.rating:g}｜距离 {record.distance_meters:g}m"
            for index, record in enumerate(records, start=1)
        )

    @classmethod
    def _first_rating(cls, texts: list[str]) -> float | None:
        for text in texts:
            match = cls._RATING_PATTERN.match(text)
            if match:
                return float(match.group(1))
        return None

    @classmethod
    def _first_distance(cls, texts: list[str]) -> float | None:
        for text in texts:
            value = cls.parse_distance_to_meters(text)
            if value is not None:
                return value
        return None

    @classmethod
    def parse_distance_to_meters(cls, text: str) -> float | None:
        match = cls._DISTANCE_PATTERN.match(text)
        if not match:
            return None
        value = float(match.group(1))
        unit = match.group(2).lower()
        return value * 1000 if unit == "km" else value

    @staticmethod
    def names_match_keywords(
        names: tuple[str, ...],
        expected_keywords: tuple[str, ...],
    ) -> bool:
        """只要求当前可见 POI 中至少一个命中目标分类关键词。"""
        normalized_names = tuple(name.casefold() for name in names)
        normalized_keywords = tuple(keyword.casefold() for keyword in expected_keywords)
        return any(
            keyword in name
            for name in normalized_names
            for keyword in normalized_keywords
        )

    def visible_poi_names(self) -> tuple[str, ...]:
        """读取当前可见的附近 POI 名称。"""
        components = self.driver.find_all_components(BY.xpath(self.POI_LIST_TEXT_XPATH))
        names: list[str] = []
        for component in self._as_list(components):
            if not self._is_visible(component):
                continue
            text = component.getText().strip()
            if self._is_poi_name(text) and text not in names:
                names.append(text)
        return tuple(names)

    def wait_poi_names_loaded(
        self,
        *,
        minimum: int = 3,
        timeout: float = 8,
    ) -> tuple[str, ...]:
        """等待附近 POI 列表至少展示指定数量的地点名称。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            names = self.visible_poi_names()
            if len(names) >= minimum:
                return names
            time.sleep(0.4)
        raise RuntimeError(f"[{self.PAGE_NAME}] 附近页POI列表加载不足 {minimum} 项")

    def swipe_poi_list_until_more(
        self,
        before_names: tuple[str, ...],
        *,
        max_swipes: int = 5,
    ) -> tuple[tuple[str, ...], str]:
        """上滑附近卡片或 POI 列表，直到卡片拉起或出现更多地点。"""
        before_set = set(before_names)
        before_top = self.poi_list_top()

        for _ in range(max_swipes):
            # 附近页底部是半卡片，优先从屏幕下方上滑拉起卡片。
            self.driver.swipe(
                "UP",
                distance=80,
                start_point=(0.55, 0.84),
                swipe_time=0.65,
            )
            time.sleep(1)
            current_names = self.visible_poi_names()
            if current_names and set(current_names) != before_set:
                return current_names, "上滑后出现新的可见POI"
            if len(current_names) > len(before_names):
                return current_names, "上滑后可见POI数量增加"

            current_top = self.poi_list_top()
            if (
                current_names
                and before_top is not None
                and current_top is not None
                and current_top < before_top - 120
            ):
                return current_names, "附近卡片已拉起到顶部"

        for _ in range(max_swipes):
            # 卡片已展开后，再尝试直接滚动 POI 列表。
            poi_list = self.wait_xpath(self.POI_LIST_XPATH, "附近页POI列表", timeout=8)
            self.driver.swipe("UP", distance=70, area=poi_list, swipe_time=0.6)
            time.sleep(1)
            current_names = self.visible_poi_names()
            if current_names and set(current_names) != before_set:
                return current_names, "列表滚动后出现新的可见POI"
            if len(current_names) > len(before_names):
                return current_names, "列表滚动后可见POI数量增加"

        raise RuntimeError(f"[{self.PAGE_NAME}] 上滑附近卡片或POI列表后未出现可验证的变化")

    def poi_list_top(self) -> int | None:
        """读取 POI 列表顶部坐标，用于判断附近半卡片是否被拉起。"""
        component = self.find_xpath(self.POI_LIST_XPATH)
        if component is None or not self._is_visible(component):
            return None
        return int(component.getBounds().top)

    def _is_poi_name(self, text: str) -> bool:
        if not text:
            return False
        if self._DISTANCE_PATTERN.match(text):
            return False
        if text.startswith("评分") or text.endswith("人去过"):
            return False
        return True
