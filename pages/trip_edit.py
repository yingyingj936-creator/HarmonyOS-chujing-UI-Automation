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
    PENDING_TAB_XPATH = '//*[@id="tabBarList"]//Text[@text="待规划" and @clickable="true"]'
    ADD_TEXT_XPATH = (
        '//*[@id="tabBarList"]//Text[contains(@text, "新增") or contains(@text, "添加")]'
    )
    ADD_ICON_XPATH = '//*[@id="tabBarList"]//*[@clickable="true" and not(.//Text)]'
    OVERVIEW_LIST_XPATH = '//*[@id="route_editor_overview"]'
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

    def wait_loaded(self, *, timeout: float = 10) -> None:
        """等待编辑行程页核心区域加载完成。"""
        self.wait_xpath(self.TITLE_XPATH, "编辑行程页标题", timeout=timeout)
        self.wait_xpath(self.MAP_VIEW_XPATH, "编辑行程页顶部地图", timeout=timeout)
        self.wait_xpath(self.BOTTOM_PANEL_XPATH, "编辑行程页半卡片区域", timeout=timeout)
        self.wait_xpath(self.TAB_BAR_XPATH, "编辑行程页半卡片Tab区域", timeout=timeout)
        self.wait_xpath(self.OVERVIEW_TAB_XPATH, "编辑行程页全览Tab", timeout=timeout)
        self.wait_xpath(self.OVERVIEW_LIST_XPATH, "编辑行程页全览路线列表", timeout=timeout)

    def wait_tabs_loaded(self, *, timeout: float = 8) -> None:
        """等待全览、Day1、DayN、待规划等Tab展示。"""
        self.wait_xpath(self.OVERVIEW_TAB_XPATH, "编辑行程页全览Tab", timeout=timeout)
        self.wait_xpath(self.DAY_1_TAB_XPATH, "编辑行程页Day1 Tab", timeout=timeout)
        self.wait_xpath(self.DAY_N_TAB_XPATH, "编辑行程页DayN Tab", timeout=timeout)
        self.wait_xpath(self.PENDING_TAB_XPATH, "编辑行程页待规划Tab", timeout=timeout)

    def wait_route_overview_loaded(self, *, timeout: float = 8) -> None:
        """等待全览下按天展示的路线列表加载完成。"""
        self.wait_xpath(self.OVERVIEW_LIST_XPATH, "编辑行程页全览路线列表", timeout=timeout)
        self.wait_xpath(self.DAY_1_SECTION_XPATH, "编辑行程页Day1路线分组", timeout=timeout)
        self.wait_xpath(self.DAY_2_SECTION_XPATH, "编辑行程页DayN路线分组", timeout=timeout)
        self.wait_xpath(self.DAY_NUMBER_1_XPATH, "编辑行程页POI顺序1", timeout=timeout)
        self.wait_xpath(self.DAY_NUMBER_2_XPATH, "编辑行程页POI顺序2", timeout=timeout)
        self.wait_xpath(self.FIRST_DAY_POI_XPATH, "编辑行程页Day1首个POI", timeout=timeout)
        self.wait_xpath(self.SECOND_DAY_POI_XPATH, "编辑行程页Day1第二个POI", timeout=timeout)
        self.wait_xpath(self.DAY_N_POI_XPATH, "编辑行程页DayN POI", timeout=timeout)

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
