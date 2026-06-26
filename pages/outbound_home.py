import time
from dataclasses import dataclass
from typing import Any

from hypium import BY

from pages.base_page import BasePage
from utils.allure_visual import component_has_red_highlight


@dataclass(frozen=True)
class HomeGuideCard:
    """首页攻略瀑布流卡片的关键展示字段。"""

    post_id: str
    title: str
    author: str
    destination: str
    likes: str


class OutboundHomePage(BasePage):
    """出境服务卡片首页对象。"""

    PAGE_NAME = "OutboundHomePage"
    REGION_DROPDOWN_XPATH_TEMPLATE = (
        '//*[@id="TabHomeCompRoot"]//Row[.//Text[@text="{region_text}"]]'
    )
    REGION_DROPDOWN_XPATH = REGION_DROPDOWN_XPATH_TEMPLATE.format(
        region_text="中国香港"
    )
    REGION_SELECTOR_XPATH = (
        '//*[@id="TabHomeCompRoot"]//Row[@clickable="true" and .//Text['
        'contains(@text, "中国") or contains(@text, "香港") '
        'or contains(@text, "澳门") or @text="温哥华" or @text="泰国"]]'
    )
    LEGACY_REGION_SELECTOR_XPATH = (
        '//*[@id="TabHomeCompRoot"]/Column[1]/Column[1]/Column[1]/Row[1]'
    )
    HOME_ROOT_XPATH = '//*[@id="TabHomeCompRoot"]'
    SEARCH_BAR_TEXT = "搜索服务、地图、帖子"
    SEARCH_BAR_XPATH = (
        '//*[@id="TabHomeCompRoot"]//*['
        '@text="搜索服务、地图、帖子" '
        'or @hint="搜索服务、地图、帖子" '
        'or contains(@text, "搜索服务") '
        'or contains(@hint, "搜索服务")]'
    )
    HOME_RECOMMENDS_SECTION_XPATH = '//*[@id="home_recommends_section"]'
    # 金刚区使用业务容器定位，避免依赖首屏 Stack 层级。
    KINGKONG_PROXY_XPATH = HOME_RECOMMENDS_SECTION_XPATH
    SERVICE_TAB_ROW_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}//Row'
        '[./Column/Text[@text="首页"]]'
        '[./Column/Text[@text="酒店"]]'
        '[./Column/Text[@text="火车"]]'
    )
    KINGKONG_ENTRY_GRID_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}//Grid'
    )
    TAXI_ENTRY_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}'
        '//Text[@text="打车"]'
    )
    SCENIC_TICKET_ENTRY_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}'
        '//Text[@text="景区门票" or @text="景区游玩"]'
    )
    YOUTUBE_ENTRY_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}'
        '//Text[@text="YouTube"]'
    )
    LOCAL_SERVICE_ENTRY_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}'
        '//GridItem[@clickable="true" '
        'and ./Column/Text[@text="本地服务"]]'
    )
    HOTEL_QUERY_BUTTON_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}'
        '//Text[@text="查询酒店" and @clickable="true"]'
    )
    TRAIN_DESTINATION_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}'
        '//Text[@text="目的地" and @clickable="true"]'
    )
    TRAIN_QUERY_BUTTON_XPATH = (
        f'{HOME_RECOMMENDS_SECTION_XPATH}'
        '//Text[@text="查询火车票" and @clickable="true"]'
    )
    HOTEL_RESULTS_FILTER_XPATH = '//*[@text="价格/等级"]'
    TRAIN_DESTINATION_PAGE_TITLE_XPATH = '//heading[@text="目的地"]'
    HOT_ROUTES_SECTION_XPATH = '//*[@id="home_hot_routes_section"]'
    HOT_ROUTE_CARD_XPATH_TEMPLATE = (
        f'{HOT_ROUTES_SECTION_XPATH}'
        '//Stack[@clickable="true" and .//Text[@text="{route_name}"]]'
    )
    HOT_ROUTE_TEXT_XPATH_TEMPLATE = (
        f'{HOT_ROUTES_SECTION_XPATH}//Text[@text="{{route_name}}"]'
    )
    WATERFALL_SECTION_XPATH = '//*[@id="home_discovery_section"]'
    CATEGORY_LIST_XPATH = (
        '//*[@id="TabHomeCompRoot"]//ListItemGroup/'
        'List[@scrollable="true"]'
    )
    WATERFALL_LIST_XPATH = (
        f'{WATERFALL_SECTION_XPATH}//WaterFlow'
    )
    WATERFALL_COVER_XPATH = (
        f'{WATERFALL_LIST_XPATH}/Column/__Common__'
    )
    BOTTOM_NAV_ROOT_XPATH = '//*[@id="HwAuthDialog_rootId"]'
    BOTTOM_HOME_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="首页"]'
    BOTTOM_TRIP_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="行程"]'
    BOTTOM_NEARBY_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="附近"]'
    BOTTOM_MINE_TAB_XPATH = '//*[@id="HwAuthDialog_rootId"]//Text[@text="我的"]'

    def _wait_by_text(self, text: str, timeout: float) -> bool:
        return (
            self.driver.wait_for_component(BY.text(text), timeout=timeout)
            is not None
        )

    def _wait_by_xpath(self, xpath: str, timeout: float) -> bool:
        return (
            self.driver.wait_for_component(BY.xpath(xpath), timeout=timeout)
            is not None
        )

    @classmethod
    def region_dropdown_xpath(cls, region_text: str) -> str:
        """生成首页左上角目的地入口 XPath。"""
        return cls.REGION_DROPDOWN_XPATH_TEMPLATE.format(region_text=region_text)

    def wait_first_screen_loaded(
        self,
        timeout: float = 5,
        destination: str = "中国香港",
    ) -> bool:
        """
        首页首屏加载判定（总超时）。
        用于“超过 5 秒为空白”的冒烟断言。
        """
        deadline = time.time() + timeout

        def remaining() -> float:
            return max(0.1, deadline - time.time())

        if not self._wait_by_xpath(self.HOME_ROOT_XPATH, remaining()):
            return False
        if not self._wait_by_text(destination, remaining()):
            return False
        if not self._wait_by_xpath(self.SEARCH_BAR_XPATH, remaining()):
            return False
        return True

    def is_home_tab_active(self, timeout: float = 3) -> bool:
        """
        首页高亮判定（代理断言）。
        说明：UI 树中未提供 selected=true，可通过“首页专属容器+首屏模块可见”推断当前为首页激活态。
        """
        return (
            self._wait_by_xpath(self.HOME_ROOT_XPATH, timeout)
            and self._wait_by_xpath(self.BOTTOM_HOME_TAB_XPATH, timeout)
            and self._wait_by_xpath(self.HOT_ROUTES_SECTION_XPATH, timeout)
        )

    def tap_region_selector(self, region_text: str | None = None) -> None:
        """点击首页地区切换下拉按钮。"""
        name = "地区切换下拉按钮"
        candidate_xpaths = []
        if region_text:
            name += f"（当前地区：{region_text}）"
            candidate_xpaths.append(self.region_dropdown_xpath(region_text))
        candidate_xpaths.extend(
            (
                self.REGION_SELECTOR_XPATH,
                self.REGION_DROPDOWN_XPATH,
                self.LEGACY_REGION_SELECTOR_XPATH,
            )
        )
        self.wait_any_xpath(tuple(candidate_xpaths), name).click()

    @classmethod
    def service_tab_xpath(cls, tab_name: str) -> str:
        """生成首页金刚区指定服务标签的 XPath。"""
        return (
            f'{cls.HOME_RECOMMENDS_SECTION_XPATH}'
            f'//Column[@clickable="true" and ./Text[@text="{tab_name}"]]'
        )

    def tap_service_tab(self, tab_name: str) -> None:
        """切换首页金刚区的首页、酒店或火车标签。"""
        self.tap_xpath(
            self.service_tab_xpath(tab_name),
            f"首页金刚区“{tab_name}”标签",
        )

    def tap_hotel_query(self) -> None:
        """点击酒店标签中的“查询酒店”。"""
        self.tap_xpath(self.HOTEL_QUERY_BUTTON_XPATH, "查询酒店")

    def tap_taxi_entry(self) -> None:
        """点击首页金刚区“打车”入口。"""
        self.tap_xpath(self.TAXI_ENTRY_XPATH, "首页金刚区“打车”入口")

    def tap_scenic_ticket_entry(self) -> None:
        """点击首页金刚区“景区门票”入口。"""
        self.tap_xpath(
            self.SCENIC_TICKET_ENTRY_XPATH,
            "首页金刚区“景区门票”入口",
        )

    def ensure_kingkong_first_page(self) -> None:
        """将金刚区恢复到包含“景区门票”的默认第一屏。"""
        self.restore_top(max_swipes=18)
        home_tab = self._restore_service_tab_row()
        if home_tab is not None:
            home_tab.click()
            time.sleep(0.8)
        if self.driver.wait_for_component(
            BY.xpath(self.SCENIC_TICKET_ENTRY_XPATH),
            timeout=1,
        ) is not None:
            return

        grid = self.wait_xpath(
            self.KINGKONG_ENTRY_GRID_XPATH,
            "首页金刚区服务列表",
            timeout=8,
        )
        for _ in range(3):
            self.driver.swipe("RIGHT", distance=60, area=grid)
            if self.driver.wait_for_component(
                BY.xpath(self.SCENIC_TICKET_ENTRY_XPATH),
                timeout=1.5,
            ) is not None:
                return

        self.wait_xpath(
            self.SCENIC_TICKET_ENTRY_XPATH,
            "金刚区默认第一屏“景区门票/景区游玩”入口",
            timeout=3,
        )

    def _restore_service_tab_row(self, *, max_swipes: int = 12):
        """回到金刚区服务标签行，用于需要操作服务入口的用例。"""
        home_tab_selector = self.service_tab_xpath("首页")
        for _ in range(max_swipes + 1):
            home_tab = self.find_xpath(home_tab_selector)
            if home_tab is not None:
                return home_tab
            self.driver.swipe(
                "DOWN",
                distance=80,
                start_point=(0.5, 0.25),
                swipe_time=0.5,
            )
            time.sleep(0.4)
        return None

    def swipe_kingkong_to_second_page(self) -> None:
        """在金刚区横向左滑到包含 YouTube 的第二屏。"""
        grid = self.wait_xpath(
            self.KINGKONG_ENTRY_GRID_XPATH,
            "首页金刚区服务列表",
        )
        self.driver.swipe("LEFT", distance=60, area=grid)
        self.wait_xpath(
            self.YOUTUBE_ENTRY_XPATH,
            "金刚区第二屏 YouTube 入口",
            timeout=8,
        )

    def tap_youtube_entry(self) -> None:
        """点击金刚区第二屏的 YouTube 入口。"""
        self.tap_xpath(self.YOUTUBE_ENTRY_XPATH, "YouTube 入口")

    def tap_local_service_entry(self) -> None:
        """点击首页金刚区“本地服务”入口。"""
        self.tap_xpath(
            self.LOCAL_SERVICE_ENTRY_XPATH,
            "首页金刚区“本地服务”入口",
        )

    @classmethod
    def hot_route_card_xpath(cls, route_name: str) -> str:
        """生成首页热门路线卡片 XPath。"""
        return cls.HOT_ROUTE_CARD_XPATH_TEMPLATE.format(route_name=route_name)

    @classmethod
    def hot_route_text_xpath(cls, route_name: str) -> str:
        """生成首页热门路线标题 XPath。"""
        return cls.HOT_ROUTE_TEXT_XPATH_TEMPLATE.format(route_name=route_name)

    def _find_hot_route_text(self, route_name: str, *, timeout: float = 0.8):
        """查找当前可视区域内的热门路线标题，兼容 section id 短时缺失。"""
        selectors = (
            BY.xpath(self.hot_route_text_xpath(route_name)),
            BY.text(route_name),
        )
        for selector in selectors:
            component = self.driver.wait_for_component(
                selector,
                timeout=timeout,
            )
            if component is not None:
                return component
        return None

    def ensure_hot_route_visible(
        self,
        route_name: str,
        *,
        max_swipes: int = 8,
    ):
        """回到首页顶部附近后，向下查找指定热门路线直到其进入可视区域。"""
        component = self._find_hot_route_text(route_name, timeout=0.5)
        if component is not None:
            return component

        try:
            self.restore_top(max_swipes=max(18, max_swipes))
        except RuntimeError:
            # 如果当前停在瀑布流吸顶区域，继续上拉会离热门路线更远。
            # 先向下回退几次，再进入常规“从顶部向下找热门路线”的流程。
            for _ in range(max(6, max_swipes)):
                component = self._find_hot_route_text(route_name, timeout=0.5)
                if component is not None:
                    return component
                self._swipe_home_down()

        for swipe_count in range(max_swipes + 1):
            component = self._find_hot_route_text(route_name, timeout=0.8)
            if component is not None:
                return component
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=75,
                start_point=(0.5, 0.78),
                swipe_time=0.5,
            )
            time.sleep(0.7)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 滚动查找后仍未找到首页热门路线“{route_name}”"
        )

    def tap_hot_route_card(self, route_name: str) -> None:
        """点击首页热门路线中的指定卡片。"""
        component = self.ensure_hot_route_visible(route_name)
        bounds = component.getBounds()
        self.driver.click(
            (
                (int(bounds.left) + int(bounds.right)) // 2,
                (int(bounds.top) + int(bounds.bottom)) // 2,
            )
        )

    def tap_train_destination(self) -> None:
        """点击火车标签中的“目的地”。"""
        self.tap_xpath(self.TRAIN_DESTINATION_XPATH, "火车目的地")

    @classmethod
    def category_tab_xpath(cls, tab_name: str) -> str:
        return (
            f'{cls.CATEGORY_LIST_XPATH}'
            f'//Row[@clickable="true" and .//Text[@text="{tab_name}"]]'
        )

    @classmethod
    def category_tab_text_xpath(cls, tab_name: str) -> str:
        return (
            f'{cls.category_tab_xpath(tab_name)}'
            f'//Text[@text="{tab_name}"]'
        )

    def ensure_category_tab_visible(
        self,
        tab_name: str,
        *,
        max_swipes: int = 8,
    ) -> None:
        """横向滚动攻略分类栏，直到目标标签完整可见。"""
        category_list = self.wait_xpath(
            self.CATEGORY_LIST_XPATH,
            "首页攻略分类栏",
        )
        selector = BY.xpath(self.category_tab_xpath(tab_name))
        direction = "RIGHT" if tab_name in {"发现", "入境"} else "LEFT"

        for _ in range(max_swipes + 1):
            tab = self.driver.wait_for_component(selector, timeout=0.5)
            if tab is not None:
                list_bounds = category_list.getBounds()
                tab_bounds = tab.getBounds()
                if (
                    tab_bounds.left >= list_bounds.left
                    and tab_bounds.right <= list_bounds.right
                ):
                    return
            self.driver.swipe(
                direction,
                distance=55,
                area=category_list,
                swipe_time=0.5,
            )
            time.sleep(0.4)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 横向浏览分类栏后仍未看到“{tab_name}”"
        )

    def switch_guide_category(
        self,
        tab_name: str,
        previous_post_ids: tuple[str, ...],
        *,
        timeout: float = 10,
    ) -> tuple[str, ...]:
        """Click a guide category and wait until the waterfall has visible content."""
        previous_ids = set(previous_post_ids)
        last_ids: tuple[str, ...] = ()

        for attempt in range(2):
            self.ensure_category_tab_visible(tab_name)
            self.tap_xpath(
                self.category_tab_text_xpath(tab_name),
                f"guide category {tab_name}",
            )

            deadline = time.monotonic() + (timeout / 2)
            while time.monotonic() < deadline:
                current_ids = self.visible_guide_post_ids()
                if current_ids:
                    last_ids = current_ids
                    if set(current_ids) != previous_ids:
                        return current_ids
                time.sleep(0.4)

            if attempt == 0:
                time.sleep(0.6)

        if last_ids:
            return last_ids
        raise RuntimeError(
            f"[{self.PAGE_NAME}] guide category {tab_name} has no visible waterfall content"
        )
    def select_guide_category(
        self,
        tab_name: str,
        *,
        timeout: float = 8,
    ) -> tuple[str, ...]:
        """Select a guide category and return currently visible waterfall IDs."""
        self.ensure_category_tab_visible(tab_name)
        self.tap_xpath(
            self.category_tab_text_xpath(tab_name),
            f"guide category {tab_name}",
        )

        deadline = time.monotonic() + timeout
        time.sleep(0.8)
        while time.monotonic() < deadline:
            current_ids = self.visible_guide_post_ids()
            if current_ids:
                return current_ids
            time.sleep(0.4)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] guide category {tab_name} has no visible waterfall content"
        )
    @classmethod
    def guide_card_xpath(cls, post_id: str) -> str:
        return (
            f'{cls.WATERFALL_LIST_XPATH}/Column'
            f'[./__Common__[@id="{post_id}"]]'
        )

    @classmethod
    def guide_cover_xpath(cls, post_id: str) -> str:
        return f'{cls.guide_card_xpath(post_id)}/__Common__[@id="{post_id}"]'

    @classmethod
    def guide_title_xpath(cls, post_id: str) -> str:
        return f'{cls.guide_card_xpath(post_id)}/Text[1]'

    @classmethod
    def guide_author_xpath(cls, post_id: str) -> str:
        return f'{cls.guide_card_xpath(post_id)}/Row[1]/Text[1]'

    @classmethod
    def guide_destination_xpath(cls, post_id: str) -> str:
        return f'{cls.guide_card_xpath(post_id)}/Row[2]/Row[1]/Text[1]'

    @classmethod
    def guide_likes_xpath(cls, post_id: str) -> str:
        return f'{cls.guide_like_row_xpath(post_id)}/Text[1]'

    @classmethod
    def guide_like_row_xpath(cls, post_id: str) -> str:
        digit_condition = " or ".join(
            f'contains(@text, "{digit}")' for digit in "0123456789"
        )
        return (
            f'{cls.guide_card_xpath(post_id)}//Row'
            f'[./Image and ./Text[{digit_condition}]]'
        )

    @classmethod
    def guide_like_icon_xpath(cls, post_id: str) -> str:
        return f'{cls.guide_like_row_xpath(post_id)}/Image'

    @staticmethod
    def _component_id(component: Any) -> str:
        properties = component.getAllProperties().to_dict()
        return str(properties.get("id") or properties.get("key") or "").strip()

    @staticmethod
    def _is_safe_log_text(text: str) -> bool:
        return all(
            ord(character) <= 0xFFFF and not 0xD800 <= ord(character) <= 0xDFFF
            for character in text
        )

    def visible_guide_post_ids(self) -> tuple[str, ...]:
        """读取当前已渲染攻略卡片的唯一帖子 ID。"""
        components = self.driver.find_all_components(
            BY.xpath(self.WATERFALL_COVER_XPATH)
        )
        if components is None:
            return ()
        if not isinstance(components, list):
            components = [components]

        post_ids = []
        for component in components:
            post_id = self._component_id(component)
            if post_id:
                post_ids.append(post_id)
        if len(post_ids) != len(set(post_ids)):
            raise RuntimeError(f"[{self.PAGE_NAME}] 当前瀑布流出现重复帖子 ID")
        return tuple(post_ids)

    def visible_full_guide_post_ids(self) -> tuple[str, ...]:
        """一次性读取当前屏幕内完整可见的攻略帖子 ID，减少 UI dump 次数。"""
        components = self.driver.find_all_components(
            BY.xpath(self.WATERFALL_COVER_XPATH)
        )
        categories = self.find_xpath(self.CATEGORY_LIST_XPATH)
        navigation = self.find_xpath(self.BOTTOM_NAV_ROOT_XPATH)
        if components is None or categories is None or navigation is None:
            return ()
        if not isinstance(components, list):
            components = [components]

        top_limit = int(categories.getBounds().bottom)
        bottom_limit = int(navigation.getBounds().top)
        post_ids = []
        for component in components:
            post_id = self._component_id(component)
            if not post_id:
                continue
            bounds = component.getBounds()
            if (
                int(bounds.top) >= top_limit
                and int(bounds.bottom) <= bottom_limit
                and int(bounds.right) > int(bounds.left)
                and int(bounds.bottom) - int(bounds.top) >= 100
            ):
                post_ids.append(post_id)
        if len(post_ids) != len(set(post_ids)):
            raise RuntimeError(f"[{self.PAGE_NAME}] 当前可见瀑布流出现重复帖子 ID")
        return tuple(post_ids)

    def scroll_to_waterfall(self) -> tuple[str, ...]:
        """实际上拉进入攻略瀑布流区域，并返回当前卡片 ID。"""
        self.wait_xpath(self.WATERFALL_LIST_XPATH, "首页攻略瀑布流")
        for _ in range(5):
            post_ids = self.visible_guide_post_ids()
            if post_ids:
                return post_ids
            self.driver.swipe(
                "UP",
                distance=75,
                start_point=(0.5, 0.82),
                swipe_time=0.6,
            )
            time.sleep(0.8)

        raise RuntimeError(f"[{self.PAGE_NAME}] 上拉后没有可见攻略卡片")

    def load_more_guides(
        self,
        initial_post_ids: tuple[str, ...],
        *,
        minimum_unique_cards: int = 50,
        max_swipes: int = 24,
    ) -> tuple[str, int, int]:
        """
        连续上拉并累计帖子 ID，以新增唯一 ID 作为分页成功代理判断。

        首页使用虚拟瀑布流，滚出屏幕的旧卡片会从 UI 树移除，因此不能通过
        DOM 数量判断“追加”。累计不同帖子 ID 可以避免把卡片复用误判为分页。
        """
        initial_ids = set(initial_post_ids)
        seen_ids = set(initial_ids)
        previous_ids = initial_post_ids

        for swipe_count in range(1, max_swipes + 1):
            self.driver.swipe(
                "UP",
                distance=70,
                start_point=(0.5, 0.84),
                swipe_time=0.6,
            )
            time.sleep(1)

            current_ids = self.visible_guide_post_ids()
            if not current_ids:
                raise RuntimeError(
                    f"[{self.PAGE_NAME}] 第 {swipe_count} 次上拉后"
                    "没有可见攻略卡片"
                )

            seen_ids.update(current_ids)
            new_ids = tuple(post_id for post_id in current_ids if post_id not in initial_ids)
            safe_new_ids = tuple(
                post_id for post_id in new_ids
                if self.is_guide_card_above_bottom_navigation(post_id)
            )
            if len(seen_ids) >= minimum_unique_cards and safe_new_ids:
                return safe_new_ids[0], len(seen_ids), swipe_count

            previous_ids = current_ids

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 连续上拉 {max_swipes} 次后仅累计"
            f" {len(seen_ids)} 张不同攻略卡片，分页加载未达到"
            f" {minimum_unique_cards} 张；最后可见={previous_ids}"
        )

    def is_guide_card_above_bottom_navigation(self, post_id: str) -> bool:
        """判断攻略卡片是否完整位于底部导航上方。"""
        card = self.find_xpath(self.guide_card_xpath(post_id))
        navigation = self.find_xpath(self.BOTTOM_NAV_ROOT_XPATH)
        if card is None or navigation is None:
            return False
        return int(card.getBounds().bottom) <= int(navigation.getBounds().top)

    @staticmethod
    def _is_component_center_visible(component, *, bottom_limit: int) -> bool:
        bounds = component.getBounds()
        center_y = (int(bounds.top) + int(bounds.bottom)) // 2
        return (
            int(bounds.right) > int(bounds.left)
            and int(bounds.bottom) > int(bounds.top)
            and 0 <= center_y <= bottom_limit
        )

    def guide_card_fields(self, post_id: str) -> HomeGuideCard:
        """读取指定攻略卡片的标题、作者、目的地和点赞数。"""
        self.wait_xpath(self.guide_cover_xpath(post_id), "攻略封面")
        try:
            title = self.wait_xpath(
                self.guide_title_xpath(post_id),
                "攻略标题",
            ).getText().strip()
            author = self.wait_xpath(
                self.guide_author_xpath(post_id),
                "攻略作者",
            ).getText().strip()
            destination = self.wait_xpath(
                self.guide_destination_xpath(post_id),
                "攻略目的地",
            ).getText().strip()
            likes = self.wait_xpath(
                self.guide_likes_xpath(post_id),
                "攻略点赞数",
            ).getText().strip()
        except RuntimeError:
            texts = self._guide_card_texts(post_id)
            if len(texts) < 4:
                raise RuntimeError(
                    f"[{self.PAGE_NAME}] 攻略卡片 {post_id} 文案字段不足：{texts}"
                )

            likes_index = next(
                (
                    index
                    for index in range(len(texts) - 1, -1, -1)
                    if texts[index].replace(",", "").isdigit()
                ),
                -1,
            )
            if likes_index <= 1:
                raise RuntimeError(
                    f"[{self.PAGE_NAME}] 攻略卡片 {post_id} 未找到点赞数字段：{texts}"
                )
            title = texts[0]
            author = texts[1]
            destination = texts[likes_index - 1]
            likes = texts[likes_index]
        return HomeGuideCard(
            post_id=post_id,
            title=title,
            author=author,
            destination=destination,
            likes=likes,
        )

    def _guide_card_texts(self, post_id: str) -> tuple[str, ...]:
        """按可视位置读取卡片内全部文本，作为结构 XPath 变化时的兜底。"""
        components = self.driver.find_all_components(
            BY.xpath(f'{self.guide_card_xpath(post_id)}//Text')
        )
        if components is None:
            return ()
        if not isinstance(components, list):
            components = [components]

        entries = []
        for component in components:
            text = component.getText().strip()
            if not text:
                continue
            bounds = component.getBounds()
            if int(bounds.right) <= int(bounds.left) or int(bounds.bottom) <= int(bounds.top):
                continue
            entries.append((int(bounds.top), int(bounds.left), text))
        entries.sort(key=lambda item: (item[0], item[1]))
        return tuple(item[2] for item in entries)

    @staticmethod
    def _normalize_destination_text(value: str) -> str:
        return value.replace("中国", "").strip()

    def find_visible_guide_for_destination(
        self,
        destination: str,
        *,
        max_swipes: int = 10,
    ) -> HomeGuideCard:
        """在当前首页瀑布流中找一张目的地匹配的攻略卡片，避免依赖后端固定帖子 ID。"""
        expected = self._normalize_destination_text(destination)
        self.scroll_to_waterfall()

        for swipe_count in range(max_swipes + 1):
            for post_id in self.visible_guide_post_ids():
                if not self.is_guide_card_above_bottom_navigation(post_id):
                    continue
                try:
                    card = self.guide_card_fields(post_id)
                except RuntimeError:
                    continue
                actual = self._normalize_destination_text(card.destination)
                if expected and (expected in actual or actual in expected):
                    return card

            if swipe_count == max_swipes:
                break
            self.scroll_guide_feed_once()

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 浏览 {max_swipes} 屏后未找到目的地为“{destination}”的首页攻略卡片"
        )

    @staticmethod
    def parse_like_count(value: str) -> int:
        normalized = value.replace(",", "").strip()
        if not normalized.isdigit():
            raise RuntimeError(f"点赞数格式异常：{value!r}")
        return int(normalized)

    def guide_like_count(self, post_id: str) -> int:
        text = self.wait_xpath(
            self.guide_likes_xpath(post_id),
            "攻略点赞数",
        ).getText()
        return self.parse_like_count(text)

    def is_guide_liked(self, post_id: str) -> bool:
        icon = self.wait_xpath(
            self.guide_like_icon_xpath(post_id),
            "攻略点赞爱心",
        )
        return component_has_red_highlight(self.driver, icon)

    def tap_guide_like(self, post_id: str) -> None:
        self.tap_xpath(
            self.guide_like_row_xpath(post_id),
            "攻略点赞按钮",
        )

    def tap_guide_card(self, post_id: str) -> None:
        navigation = self.find_xpath(self.BOTTOM_NAV_ROOT_XPATH)
        bottom_limit = (
            int(navigation.getBounds().top)
            if navigation is not None
            else 10_000
        )
        for xpath in (self.guide_cover_xpath(post_id), self.guide_title_xpath(post_id)):
            component = self.find_xpath(xpath)
            if component is not None and self._is_component_center_visible(
                component,
                bottom_limit=bottom_limit,
            ):
                component.click()
                return
        self.tap_xpath(self.guide_card_xpath(post_id), "攻略卡片")

    def wait_guide_like_count(
        self,
        post_id: str,
        expected: int,
        *,
        timeout: float = 10,
    ) -> int:
        deadline = time.monotonic() + timeout
        last_count: int | None = None
        while time.monotonic() < deadline:
            try:
                last_count = self.guide_like_count(post_id)
            except RuntimeError:
                time.sleep(0.4)
                continue
            if last_count == expected:
                return last_count
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 攻略 {post_id} 点赞数未变为 {expected}，"
            f"最后读取={last_count}"
        )

    def is_guide_like_control_visible(self, post_id: str) -> bool:
        like_row = self.find_xpath(self.guide_like_row_xpath(post_id))
        navigation = self.find_xpath(self.BOTTOM_NAV_ROOT_XPATH)
        if like_row is None or navigation is None:
            return False
        bounds = like_row.getBounds()
        return (
            int(bounds.top) >= 0
            and int(bounds.bottom) <= int(navigation.getBounds().top)
        )

    def is_guide_card_fully_visible(self, post_id: str) -> bool:
        """判断卡片封面和信息区均处于分类栏与底部导航之间。"""
        card = self.find_xpath(self.guide_card_xpath(post_id))
        cover = self.find_xpath(self.guide_cover_xpath(post_id))
        categories = self.find_xpath(self.CATEGORY_LIST_XPATH)
        navigation = self.find_xpath(self.BOTTOM_NAV_ROOT_XPATH)
        if any(
            component is None
            for component in (card, cover, categories, navigation)
        ):
            return False

        card_bounds = card.getBounds()
        cover_bounds = cover.getBounds()
        return (
            int(card_bounds.top) >= int(categories.getBounds().bottom)
            and int(card_bounds.bottom) <= int(navigation.getBounds().top)
            and int(cover_bounds.right) > int(cover_bounds.left)
            and int(cover_bounds.bottom) - int(cover_bounds.top) >= 100
        )

    def is_guide_card_safely_clickable(self, post_id: str) -> bool:
        """判断攻略卡片当前有可点击区域未被底部导航遮挡。"""
        navigation = self.find_xpath(self.BOTTOM_NAV_ROOT_XPATH)
        if navigation is None:
            return False
        bottom_limit = int(navigation.getBounds().top)
        for xpath in (self.guide_cover_xpath(post_id), self.guide_title_xpath(post_id)):
            component = self.find_xpath(xpath)
            if component is not None and self._is_component_center_visible(
                component,
                bottom_limit=bottom_limit,
            ):
                return True
        return False

    def find_visible_guide(self, *, max_swipes: int = 12) -> HomeGuideCard:
        """返回发现流中首个完整可见、可安全点击的攻略卡片。"""
        self.select_guide_category("发现")
        self.scroll_to_waterfall()

        for swipe_count in range(max_swipes + 1):
            for post_id in self.visible_guide_post_ids():
                if not self.is_guide_card_fully_visible(post_id):
                    continue
                card = self.guide_card_fields(post_id)
                if self._is_safe_log_text(card.title):
                    return card

            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=55,
                start_point=(0.5, 0.82),
                swipe_time=0.55,
            )
            time.sleep(0.7)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 浏览 {max_swipes} 屏后仍未找到完整可见的攻略卡片"
        )

    def visible_fully_visible_guides(
        self,
        excluded_post_ids: set[str] | None = None,
    ) -> tuple[HomeGuideCard, ...]:
        """读取当前屏幕内完整可见且尚未检查的攻略卡片。"""
        excluded = excluded_post_ids or set()
        cards = []
        for post_id in self.visible_full_guide_post_ids():
            if post_id in excluded:
                continue
            card = self.guide_card_fields(post_id)
            if self._is_safe_log_text(card.title):
                cards.append(card)
        return tuple(cards)

    def scroll_guide_feed_once(self) -> None:
        self.driver.swipe(
            "UP",
            distance=60,
            start_point=(0.5, 0.82),
            swipe_time=0.55,
        )
        time.sleep(0.7)

    def guide_card_bounds(self, post_id: str) -> tuple[int, int, int, int]:
        card = self.wait_xpath(
            self.guide_card_xpath(post_id),
            f"攻略卡片 {post_id}",
        )
        bounds = card.getBounds()
        return (
            int(bounds.left),
            int(bounds.top),
            int(bounds.right),
            int(bounds.bottom),
        )

    def find_unliked_guide(
        self,
        *,
        max_swipes: int = 16,
    ) -> HomeGuideCard:
        """浏览发现瀑布流并返回首个完整可见的未点赞帖子。"""
        self.select_guide_category("发现")
        self.scroll_to_waterfall()

        for swipe_count in range(max_swipes + 1):
            for post_id in self.visible_guide_post_ids():
                if not self.is_guide_card_safely_clickable(post_id):
                    continue
                if not self.is_guide_like_control_visible(post_id):
                    continue
                if not self.is_guide_liked(post_id):
                    return self.guide_card_fields(post_id)

            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=65,
                start_point=(0.5, 0.82),
                swipe_time=0.6,
            )
            time.sleep(0.8)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 浏览 {max_swipes} 屏后仍未找到未点赞攻略"
        )

    def find_guide_in_feed(
        self,
        post_id: str,
        *,
        max_swipes: int = 18,
    ) -> None:
        """重进首页后按帖子 ID 找回目标攻略，并确保点赞区域未被导航遮挡。"""
        if (
            self.find_xpath(self.guide_card_xpath(post_id)) is not None
            and self.is_guide_like_control_visible(post_id)
        ):
            return

        self.select_guide_category("发现")
        self.scroll_to_waterfall()

        for swipe_count in range(max_swipes + 1):
            if (
                self.find_xpath(self.guide_card_xpath(post_id)) is not None
                and self.is_guide_like_control_visible(post_id)
            ):
                return

            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=65,
                start_point=(0.5, 0.82),
                swipe_time=0.6,
            )
            time.sleep(0.8)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 重进后未在发现流找到攻略 {post_id}"
        )

    def restore_top(self, *, max_swipes: int = 12) -> None:
        """测试结束后将首页恢复到顶部，避免污染后续用例。"""
        # 搜索框和攻略分类栏会吸顶，不能作为“已回到顶部”的依据。
        top_module_xpaths = (
            self.SERVICE_TAB_ROW_XPATH,
            self.KINGKONG_ENTRY_GRID_XPATH,
            self.SCENIC_TICKET_ENTRY_XPATH,
        )
        for _ in range(max_swipes + 1):
            if (
                self.find_xpath(self.HOME_ROOT_XPATH) is not None
                and self._is_any_xpath_visibly_rendered(top_module_xpaths)
            ):
                return
            self._swipe_home_down()
        raise RuntimeError(f"[{self.PAGE_NAME}] 无法将首页恢复到顶部")

    def _swipe_home_down(self) -> None:
        """向首页顶部方向滑动，避开底部导航和吸顶分类栏。"""
        self.driver.swipe(
            "DOWN",
            distance=90,
            start_point=(0.5, 0.55),
            swipe_time=0.5,
        )
        time.sleep(0.4)

    def _is_any_xpath_visibly_rendered(self, xpaths: tuple[str, ...]) -> bool:
        """判断任一真实顶部业务模块可见，过滤零尺寸/反向 bounds 的节点。"""
        for xpath in xpaths:
            component = self.driver.wait_for_component(
                BY.xpath(xpath),
                timeout=0.3,
            )
            if component is None:
                continue
            bounds = component.getBounds()
            if int(bounds.right) > int(bounds.left) and int(bounds.bottom) > int(bounds.top):
                return True
        return False

    def wait_loaded(self, timeout: float = 8) -> bool:
        """等待首页标识元素出现。"""
        return self._wait_by_xpath(self.BOTTOM_HOME_TAB_XPATH, timeout=timeout)

    def is_at_home(self) -> bool:
        """
        判断当前是否在首页。
        逻辑：判断首页特有的、唯一的组件是否存在。
        """
        try:
            return self.find_xpath(self.SEARCH_BAR_XPATH) is not None
        except Exception:
            return False


