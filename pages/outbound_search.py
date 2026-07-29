import time
from typing import Any

from hypium import BY

from pages.base_page import BasePage
from pages.outbound_home import OutboundHomePage


class OutboundSearchPage(BasePage):
    """出境服务搜索页面对象"""

    PAGE_NAME = "OutboundSearchPage"
    HOME_SEARCH_BAR_XPATH = OutboundHomePage.SEARCH_BAR_XPATH
    SEARCH_INPUT_XPATH = '//TextInput'
    SEARCH_START_INPUT_XPATH = (
        '//TextInput['
        'contains(@hint, "搜索") '
        'or contains(@text, "搜索") '
        'or string-length(@hint) > 0 '
        'or string-length(@text) > 0 '
        'or ./Stack[@clickable="true"]]'
    )
    SEARCH_BUTTON_XPATH = (
        '//Text[@text="搜索" and @clickable="true"]'
        ' | //Stack[@clickable="true" and .//Text[@text="搜索"]]'
        ' | //Button[@clickable="true" and .//Text[@text="搜索"]]'
    )
    BACK_BUTTON_XPATH = '//Row[./Text[@text="搜索"]]/Row[./Image]'
    SEARCH_HISTORY_TITLE_XPATH = '//Text[@text="搜索历史"]'
    CLEAR_HISTORY_BUTTON_XPATH = (
        '//Row[./Text[@text="搜索历史"]]/Row[@clickable="true" and ./Image]'
    )
    KEYBOARD_PANEL_XPATH = (
        '//*[@id="inputMethodPanel" or @key="inputMethodPanel"]'
    )
    EVERYONE_SEARCHING_TITLE_XPATH = '//Text[@text="大家都在搜"]'
    EVERYONE_SEARCHING_KEYWORD_TEXT_XPATH = (
        '//ListItemGroup[./Text[@text="大家都在搜"]]//Grid//Text'
    )
    PLAY_RANKING_TITLE_XPATH = '//Text[@text="必玩榜"]'
    RANKING_GRID_XPATH = '//Grid[@scrollable="true"]'
    CLEAR_INPUT_BUTTON_XPATH = (
        '//TextInput/Stack[@clickable="true"]'
        ' | //Stack[./TextInput]/Stack[@clickable="true" and ./Image]'
        ' | //Row[.//TextInput]//Stack[@clickable="true" and ./Image]'
    )
    RESULT_ROOT_XPATH = '//*[@id="GlobalSearchResultComp"]'
    RESULT_LIST_XPATH = (
        '//*[@id="GlobalSearchResultComp"]/List[@scrollable="true"]'
    )
    AI_SUMMARY_CARD_XPATH_TEMPLATE = (
        '//*[@id="GlobalSearchResultComp"]/List/ListItem'
        '[.//Text[@text="查看详情"] and .//Text[contains(@text, {keyword})]]'
    )
    AI_SUMMARY_DETAIL_BUTTON_XPATH = (
        '//*[@id="GlobalSearchResultComp"]/List/ListItem[1]'
        '//Text[@text="查看详情"]'
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

    @classmethod
    def search_start_input_xpath(cls, destination: str | None = None) -> str:
        """
        生成搜索启动页输入框 XPath。

        搜索框接入 AI 推荐词后，输入框内可能展示推荐词，而不再只展示
        “在xx中搜索”这类 placeholder。这里兼容两种形态，用例只验证搜索
        输入区可用，具体推荐词文案不作为稳定断言。
        """
        if not destination:
            return cls.SEARCH_START_INPUT_XPATH
        return (
            f'//TextInput[@hint="在{destination}中搜索"]'
            f' | {cls.SEARCH_START_INPUT_XPATH}'
        )

    @staticmethod
    def history_keyword_xpath(keyword: str) -> str:
        """生成搜索历史词对应的可点击标签 XPath。"""
        return f'//Column[@clickable="true" and ./Text[@text="{keyword}"]]'

    @classmethod
    def everyone_searching_keyword_row_xpath(cls, keyword: str) -> str:
        """生成“大家都在搜”指定热词所在可点击行 XPath。"""
        return (
            '//ListItemGroup[./Text[@text="大家都在搜"]]'
            '//Row[@clickable="true" '
            f'and ./Text[@text={cls._xpath_literal(keyword)}]]'
        )

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
        return f'//TextInput[@text={OutboundSearchPage._xpath_literal(keyword)}]'

    @classmethod
    def result_input_value_xpath(cls, keyword: str) -> str:
        """生成搜索结果页顶部已填充指定关键词的搜索框 XPath。"""
        return (
            f'{cls.RESULT_ROOT_XPATH}//TextInput'
            f'[@text={cls._xpath_literal(keyword)}]'
            f' | //TextInput[@text={cls._xpath_literal(keyword)}]'
        )

    @staticmethod
    def result_group_title_xpath(group_name: str) -> str:
        """生成搜索结果分组标题 XPath。"""
        return f'//Text[@text="{group_name}"]'

    @classmethod
    def ai_summary_card_xpath(cls, keyword: str) -> str:
        """生成搜索结果页顶部 AI 总结卡片 XPath。"""
        return cls.AI_SUMMARY_CARD_XPATH_TEMPLATE.format(
            keyword=cls._xpath_literal(keyword)
        )

    @classmethod
    def result_ready_with_ai_summary_xpath(
        cls,
        keyword: str,
        group_names: tuple[str, ...],
    ) -> str:
        """生成搜索结果页关键模块一次性就绪 XPath。"""
        group_conditions = " ".join(
            f'and .//Text[@text={cls._xpath_literal(group_name)}]'
            for group_name in group_names
        )
        return (
            f'{cls.RESULT_ROOT_XPATH}'
            f'[.//ListItem[.//Text[@text="查看详情"] '
            f'and .//Text[contains(@text, {cls._xpath_literal(keyword)})]] '
            f'{group_conditions}]'
        )

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

    def wait_search_start_loaded(
        self,
        *,
        destination: str | None = None,
        timeout: float = 8,
    ) -> Any:
        """等待搜索启动页可操作，兼容目的地 placeholder 和 AI 推荐词。"""
        return self.wait_xpath(
            self.search_start_input_xpath(destination),
            "搜索启动页输入框",
            timeout=timeout,
        )

    @staticmethod
    def _component_text(component: Any | None) -> str:
        if component is None:
            return ""
        try:
            return (component.getText() or "").strip()
        except Exception:
            return ""

    @staticmethod
    def _component_hint(component: Any | None) -> str:
        if component is None:
            return ""
        try:
            properties = component.getAllProperties().to_dict()
        except Exception:
            return ""
        return str(properties.get("hint") or "").strip()

    @staticmethod
    def _is_ai_recommend_keyword(value: str) -> bool:
        normalized = value.strip()
        if not normalized:
            return False
        fixed_placeholders = {"搜索", "搜索服务、地图、帖子"}
        if normalized in fixed_placeholders:
            return False
        if normalized.startswith("在") and normalized.endswith("中搜索"):
            return False
        return True

    def current_ai_recommend_keyword(
        self,
        *,
        timeout: float = 8,
    ) -> tuple[str, Any]:
        """读取搜索启动页当前展示的 AI 推荐词，不写死服务端配置值。"""
        deadline = time.monotonic() + timeout
        last_values: tuple[str, ...] = ()

        while time.monotonic() < deadline:
            component = self.driver.wait_for_component(
                BY.xpath(self.SEARCH_START_INPUT_XPATH),
                timeout=0.8,
            )
            if component is None:
                time.sleep(0.2)
                continue

            values = tuple(
                value
                for value in (
                    self._component_text(component),
                    self._component_hint(component),
                )
                if value
            )
            last_values = values
            for value in values:
                if self._is_ai_recommend_keyword(value):
                    return value, component
            time.sleep(0.3)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 搜索框未展示 AI 推荐词，"
            f"最后读取={last_values or '<空>'}"
        )

    def first_everyone_searching_keyword(
        self,
        *,
        timeout: float = 8,
    ) -> tuple[str, Any]:
        """读取“大家都在搜”模块中当前可见的第一个 AI 推荐词。"""
        self.wait_xpath(
            self.EVERYONE_SEARCHING_TITLE_XPATH,
            "大家都在搜模块",
            timeout=timeout,
        )
        deadline = time.monotonic() + timeout
        last_values: tuple[str, ...] = ()

        while time.monotonic() < deadline:
            components = self.driver.find_all_components(
                BY.xpath(self.EVERYONE_SEARCHING_KEYWORD_TEXT_XPATH)
            )
            if components is None:
                components = []
            elif not isinstance(components, list):
                components = [components]

            values: list[str] = []
            for component in components:
                value = self._component_text(component)
                if not value:
                    continue
                values.append(value)
                if self._is_ai_recommend_keyword(value):
                    return value, component
            last_values = tuple(values)
            time.sleep(0.3)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] “大家都在搜”未展示可用 AI 推荐词，"
            f"最后读取={last_values or '<空>'}"
        )

    def clear_input_if_needed(self, *, timeout: float = 1) -> None:
        """如果搜索框已有真实输入值，先点清除，避免 AI 推荐词或旧词拼接。"""
        search_input = self.driver.wait_for_component(
            BY.xpath(self.SEARCH_INPUT_XPATH),
            timeout=timeout,
        )
        if not self._component_text(search_input):
            return

        clear_button = self.driver.wait_for_component(
            BY.xpath(self.CLEAR_INPUT_BUTTON_XPATH),
            timeout=timeout,
        )
        if clear_button is None:
            return

        clear_button.click()
        deadline = time.monotonic() + max(timeout, 1)
        while time.monotonic() < deadline:
            refreshed_input = self.driver.wait_for_component(
                BY.xpath(self.SEARCH_INPUT_XPATH),
                timeout=0.3,
            )
            if not self._component_text(refreshed_input):
                return
            time.sleep(0.2)

    def input_keyword(self, keyword: str) -> None:
        """在搜索框中输入关键词。"""
        self.clear_input_if_needed(timeout=1)
        self.input_xpath(self.SEARCH_INPUT_XPATH, keyword, "搜索输入框")

    def tap_search_button(self) -> None:
        """点击搜索框右侧的页面内“搜索”按钮。"""
        self.tap_xpath(self.SEARCH_BUTTON_XPATH, "搜索按钮")

    def tap_everyone_searching_keyword(self, keyword: str) -> None:
        """点击“大家都在搜”模块中的指定 AI 推荐词。"""
        self.tap_xpath(
            self.everyone_searching_keyword_row_xpath(keyword),
            f"大家都在搜 AI 推荐词“{keyword}”",
        )

    def wait_result_keyword_filled(
        self,
        keyword: str,
        *,
        timeout: float = 8,
    ) -> Any:
        """等待搜索结果页顶部搜索框填充为指定关键词。"""
        return self.wait_xpath(
            self.result_input_value_xpath(keyword),
            f"搜索结果页顶部搜索框-{keyword}",
            timeout=timeout,
        )

    def wait_result_has_visible_content(self, *, timeout: float = 8) -> Any:
        """等待搜索结果页出现可见结果内容，排除空状态和加载失败。"""
        return self.wait_any_xpath(
            (
                f'{self.RESULT_ROOT_XPATH}//ListItem[.//Text]',
                f'{self.RESULT_ROOT_XPATH}//GridItem[.//Text]',
                f'{self.RESULT_ROOT_XPATH}//Column[.//Text]',
                f'{self.RESULT_ROOT_XPATH}//WaterFlow//Text',
            ),
            "搜索结果内容",
            timeout=timeout,
        )

    def wait_result_ready_with_ai_summary(
        self,
        keyword: str,
        group_names: tuple[str, ...],
        *,
        timeout: float = 12,
    ) -> Any:
        """等待搜索结果页 AI 总结和结果分组均展示。"""
        return self.wait_xpath(
            self.result_ready_with_ai_summary_xpath(keyword, group_names),
            "搜索结果页AI总结和结果分组",
            timeout=timeout,
        )

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
