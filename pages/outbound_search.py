import time

from hypium import BY

from pages.base_page import BasePage
from pages.outbound_home import OutboundHomePage


class OutboundSearchPage(BasePage):
    """出境服务搜索页面对象"""

    PAGE_NAME = "OutboundSearchPage"
    HOME_SEARCH_BAR_XPATH = OutboundHomePage.SEARCH_BAR_XPATH
    SEARCH_INPUT_XPATH = '//TextInput'
    SEARCH_BUTTON_XPATH = '//Text[@text="搜索" and @clickable="true"]'
    BACK_BUTTON_XPATH = '//Row[./Text[@text="搜索"]]/Row[./Image]'
    SEARCH_HISTORY_TITLE_XPATH = '//Text[@text="搜索历史"]'
    CLEAR_HISTORY_BUTTON_XPATH = (
        '//Row[./Text[@text="搜索历史"]]/Row[@clickable="true" and ./Image]'
    )
    PLAY_RANKING_TITLE_XPATH = '//Text[@text="必玩榜"]'
    RANKING_GRID_XPATH = '//Grid[@scrollable="true"]'
    CLEAR_INPUT_BUTTON_XPATH = '//TextInput/Stack[@clickable="true"]'
    RESULT_ROOT_XPATH = '//*[@id="GlobalSearchResultComp"]'
    RESULT_LIST_XPATH = (
        '//*[@id="GlobalSearchResultComp"]/List[@scrollable="true"]'
    )
    LATEST_GUIDES_LIST_XPATH = (
        '//*[@id="GlobalSearchResultComp"]//WaterFlow[@scrollable="true"]'
    )
    LATEST_GUIDE_TITLE_XPATH = (
        f'{LATEST_GUIDES_LIST_XPATH}//Text'
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

    @staticmethod
    def placeholder_xpath(destination: str) -> str:
        """生成指定目的地对应的搜索框 placeholder XPath。"""
        return f'//TextInput[@hint="在{destination}中搜索"]'

    @staticmethod
    def history_keyword_xpath(keyword: str) -> str:
        """生成搜索历史词对应的可点击标签 XPath。"""
        return f'//Column[@clickable="true" and ./Text[@text="{keyword}"]]'

    @staticmethod
    def ranking_poi_xpath(poi_name: str) -> str:
        """
        生成榜单 POI 文本 XPath。

        HarmonyOS XPath 对 ``Row[.//Text]`` 后代条件支持不稳定，可能错误返回
        榜单第一行，因此直接点击唯一的 POI 文本节点。
        """
        return f'//Text[@text="{poi_name}"]'

    @staticmethod
    def input_value_xpath(keyword: str) -> str:
        """生成已填充指定关键词的搜索框 XPath。"""
        return f'//TextInput[@text="{keyword}"]'

    @staticmethod
    def result_group_title_xpath(group_name: str) -> str:
        """生成搜索结果分组标题 XPath。"""
        return f'//Text[@text="{group_name}"]'

    @staticmethod
    def result_item_xpath(item_name: str) -> str:
        """生成搜索结果目标条目的文本 XPath。"""
        return f'//Text[@text="{item_name}"]'

    @classmethod
    def result_group_list_xpath(cls, group_index: int) -> str:
        """生成搜索结果指定分组的横向列表 XPath。"""
        return (
            f'{cls.RESULT_ROOT_XPATH}/List/'
            f'ListItemGroup[{group_index}]/ListItem/'
            'List[@scrollable="true"]'
        )

    @classmethod
    def latest_guide_card_xpath(cls, index: int) -> str:
        """生成“最新攻略”瀑布流中当前渲染卡片的 XPath。"""
        return f'{cls.LATEST_GUIDES_LIST_XPATH}/Column[{index}]'

    @classmethod
    def latest_guide_title_xpath(cls, title: str) -> str:
        """生成当前可见攻略标题的 XPath。"""
        return (
            f'{cls.LATEST_GUIDES_LIST_XPATH}//Text'
            f'[@text={cls._xpath_literal(title)}]'
        )

    def tap_home_search(self) -> None:
        """步骤：从首页点击搜索框进入搜索页"""
        self.tap_xpath(self.HOME_SEARCH_BAR_XPATH, "首页搜索框")

    def input_keyword(self, keyword: str) -> None:
        """在搜索框中输入关键词。"""
        self.input_xpath(self.SEARCH_INPUT_XPATH, keyword, "搜索输入框")

    def tap_search_button(self) -> None:
        """点击搜索框右侧的页面内“搜索”按钮。"""
        self.tap_xpath(self.SEARCH_BUTTON_XPATH, "搜索按钮")

    def input_and_tap_search(self, keyword: str) -> None:
        """输入关键词并点击页面内搜索按钮。"""
        self.input_keyword(keyword)
        self.tap_search_button()

    def tap_back_button(self) -> None:
        """点击搜索页左上角页面内返回按钮。"""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "搜索页页面内返回按钮")

    def tap_ranking_poi(self, poi_name: str) -> None:
        """点击搜索启动页榜单中的指定 POI。"""
        self.tap_xpath(
            self.ranking_poi_xpath(poi_name),
            f"搜索榜单 POI“{poi_name}”",
        )

    def tap_result_item(self, item_name: str) -> None:
        """点击搜索结果分组中的指定条目。"""
        self.tap_xpath(
            self.result_item_xpath(item_name),
            f"搜索结果“{item_name}”",
        )

    def wait_result_loaded(self, *, timeout: float = 8) -> None:
        """等待搜索结果页重新展示。"""
        self.wait_xpath(
            self.RESULT_ROOT_XPATH,
            "搜索结果页",
            timeout=timeout,
        )

    def wait_result_hidden(self, *, timeout: float = 8) -> bool:
        """等待搜索结果页退出，防止详情页断言误命中旧页面。"""
        deadline = time.monotonic() + timeout
        selector = BY.xpath(self.RESULT_ROOT_XPATH)
        while time.monotonic() < deadline:
            if self.driver.wait_for_component(selector, timeout=0.5) is None:
                return True
            time.sleep(0.3)
        return False

    def scroll_result_text_into_view(
        self,
        text: str,
        *,
        max_swipes: int = 6,
    ) -> None:
        """滚动搜索结果主列表，直到指定分组标题或条目重新渲染。"""
        selector = BY.xpath(f'//Text[@text="{text}"]')
        result_list = self.wait_xpath(
            self.RESULT_LIST_XPATH,
            "搜索结果主列表",
        )

        for _ in range(max_swipes + 1):
            if self.driver.wait_for_component(selector, timeout=1) is not None:
                return
            self.driver.swipe(
                "UP",
                distance=50,
                area=result_list,
            )
            time.sleep(0.6)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 滚动搜索结果后仍未找到“{text}”"
        )

    def browse_result_group_to_right_until_visible(
        self,
        group_index: int,
        item_name: str,
        *,
        max_swipes: int = 8,
    ) -> None:
        """向左滑动横向结果分组，浏览右侧内容直到目标条目完整可见。"""
        group_list = self.wait_xpath(
            self.result_group_list_xpath(group_index),
            f"搜索结果第 {group_index} 个横向分组",
        )
        item_selector = BY.xpath(self.result_item_xpath(item_name))
        list_bounds = group_list.getBounds()

        for swipe_index in range(max_swipes + 1):
            item = self.driver.wait_for_component(item_selector, timeout=1)
            if item is not None:
                item_bounds = item.getBounds()
                if (
                    item_bounds.left >= list_bounds.left
                    and item_bounds.right <= list_bounds.right
                ):
                    return

            if swipe_index == max_swipes:
                break

            self.driver.swipe(
                "LEFT",
                distance=60,
                area=group_list,
            )
            time.sleep(0.6)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 浏览第 {group_index} 个结果分组后"
            f"仍未看到“{item_name}”"
        )

    def browse_latest_guides(
        self,
        *,
        minimum_browsed_cards: int = 25,
        max_swipes: int = 18,
    ) -> tuple[str, int, int]:
        """
        实际滑动“最新攻略”并累计不同的可见帖子标题。

        不再根据滑动调用次数推算浏览数量。每次滑动后必须出现新的帖子
        标题，累计至少浏览指定数量后才返回当前可点击的帖子标题。
        """
        self.wait_xpath(
            self.LATEST_GUIDES_LIST_XPATH,
            "最新攻略瀑布流",
        )
        visible_titles = ()
        for pre_swipe_count in range(4):
            visible_titles = self._visible_latest_guide_titles()
            if visible_titles:
                break
            if pre_swipe_count == 3:
                break
            self.driver.swipe(
                "UP",
                distance=45,
                start_point=(0.5, 0.84),
                swipe_time=0.5,
            )
            time.sleep(0.8)
        if not visible_titles:
            raise RuntimeError(
                f"[{self.PAGE_NAME}] 最新攻略首屏没有可识别的帖子标题"
            )

        browsed_titles = set(visible_titles)
        previous_titles = visible_titles

        for swipe_count in range(1, max_swipes + 1):
            # 起点位于屏幕底部攻略卡片内，取消 area 限制以获得足够滑动距离。
            self.driver.swipe(
                "UP",
                distance=55,
                start_point=(0.5, 0.88),
                swipe_time=0.6,
            )
            time.sleep(1)

            current_titles = self._visible_latest_guide_titles()
            if not current_titles:
                raise RuntimeError(
                    f"[{self.PAGE_NAME}] 第 {swipe_count} 次滑动后"
                    "没有可识别的攻略标题"
                )
            if current_titles == previous_titles:
                raise RuntimeError(
                    f"[{self.PAGE_NAME}] 第 {swipe_count} 次滑动后"
                    "可见帖子没有变化，攻略列表未实际滑动"
                )

            browsed_titles.update(current_titles)
            if len(browsed_titles) >= minimum_browsed_cards:
                target_title = current_titles[-1]
                return (
                    self.latest_guide_title_xpath(target_title),
                    len(browsed_titles),
                    swipe_count,
                )

            previous_titles = current_titles

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 实际滑动 {max_swipes} 次后仅浏览到"
            f" {len(browsed_titles)} 个不同帖子标题，未达到"
            f" {minimum_browsed_cards} 个"
        )

    def _visible_latest_guide_titles(self) -> tuple[str, ...]:
        """读取当前屏幕内最新攻略卡片的标题。"""
        components = self.driver.find_all_components(
            BY.xpath(self.LATEST_GUIDE_TITLE_XPATH)
        )
        if components is None:
            return ()
        if not isinstance(components, list):
            components = [components]

        titles = []
        excluded_texts = {
            "服务",
            "路线",
            "地点",
            "最新攻略",
            "搜索",
            "综合",
            "攻略",
        }
        for component in components:
            text = component.getText().strip()
            normalized = text.replace(",", "")
            if (
                len(text) >= 2
                and not normalized.isdigit()
                and text not in excluded_texts
                and text not in titles
            ):
                titles.append(text)
        return tuple(titles)

    def tap_latest_guide(self, title_xpath: str) -> None:
        """点击深分页中当前可见的最新攻略帖子。"""
        self.tap_xpath(title_xpath, "最新攻略帖子")

    def dismiss_keyboard(self) -> None:
        """仅在搜索输入框聚焦时按返回键收起软键盘。"""
        search_input = self.find_xpath(self.SEARCH_INPUT_XPATH)
        if search_input is not None and search_input.isFocused():
            self.driver.press_back()
            time.sleep(0.5)

    def scroll_ranking_poi_into_view(
        self,
        poi_name: str,
        *,
        max_swipes: int = 4,
    ) -> None:
        """向上滚动榜单，直到指定 POI 文字进入可见区域。"""
        selector = BY.xpath(self.ranking_poi_xpath(poi_name))
        for _ in range(max_swipes + 1):
            if self.driver.wait_for_component(selector, timeout=1) is not None:
                return
            self.driver.swipe(
                "UP",
                distance=30,
                start_point=(0.5, 0.65),
            )
            time.sleep(0.5)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 滚动榜单后仍未找到 POI“{poi_name}”"
        )

    def swipe_ranking_right_until_visible(
        self,
        poi_name: str,
        *,
        max_swipes: int = 4,
    ) -> None:
        """在横向榜单中向右滑动，直到指定 POI 完整进入可见区域。"""
        ranking_grid = self.wait_xpath(
            self.RANKING_GRID_XPATH,
            "搜索页横向榜单",
        )
        poi_selector = BY.xpath(self.ranking_poi_xpath(poi_name))

        for _ in range(max_swipes):
            self.driver.swipe(
                "RIGHT",
                distance=55,
                area=ranking_grid,
            )
            time.sleep(0.6)

            poi = self.driver.wait_for_component(poi_selector, timeout=1)
            if poi is None:
                continue

            grid_bounds = ranking_grid.getBounds()
            poi_bounds = poi.getBounds()
            if (
                poi_bounds.left >= grid_bounds.left
                and poi_bounds.right <= grid_bounds.right
            ):
                return

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 向右浏览榜单后仍未看到 POI“{poi_name}”"
        )

    def browse_ranking_to_right_until_visible(
        self,
        poi_name: str,
        *,
        max_swipes: int = 8,
    ) -> None:
        """手指向左滑动横向榜单，浏览右侧内容直到目标 POI 完整可见。"""
        ranking_grid = self.wait_xpath(
            self.RANKING_GRID_XPATH,
            "搜索页横向榜单",
        )
        poi_selector = BY.xpath(self.ranking_poi_xpath(poi_name))

        for _ in range(max_swipes):
            self.driver.swipe(
                "LEFT",
                distance=55,
                area=ranking_grid,
            )
            time.sleep(0.6)

            poi = self.driver.wait_for_component(poi_selector, timeout=1)
            if poi is None:
                continue

            grid_bounds = ranking_grid.getBounds()
            poi_bounds = poi.getBounds()
            if (
                poi_bounds.left >= grid_bounds.left
                and poi_bounds.right <= grid_bounds.right
            ):
                return

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 浏览右侧榜单后仍未看到 POI“{poi_name}”"
        )

    def tap_history_keyword(self, keyword: str) -> None:
        """点击搜索启动页中的指定历史搜索词。"""
        self.tap_xpath(
            self.history_keyword_xpath(keyword),
            f"搜索历史词“{keyword}”",
        )

    def tap_clear_history(self) -> None:
        """点击搜索历史标题右侧的一键删除按钮。"""
        self.tap_xpath(
            self.CLEAR_HISTORY_BUTTON_XPATH,
            "搜索历史一键删除按钮",
        )

    def wait_history_hidden(self, *, timeout: float = 8) -> bool:
        """等待搜索历史模块从搜索启动页消失。"""
        deadline = time.monotonic() + timeout
        selector = BY.xpath(self.SEARCH_HISTORY_TITLE_XPATH)
        while time.monotonic() < deadline:
            if self.driver.wait_for_component(selector, timeout=0.5) is None:
                return True
            time.sleep(0.3)
        return False

    def tap_clear_input(self) -> None:
        """点击搜索框内的清除按钮。"""
        self.tap_xpath(self.CLEAR_INPUT_BUTTON_XPATH, "搜索框清除按钮")
