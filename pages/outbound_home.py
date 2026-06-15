import time
from dataclasses import dataclass
from typing import Any

from hypium import BY

from pages.base_page import BasePage


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
        '//*[@id="TabHomeCompRoot"]//Row[./Text[@text="{region_text}"]]'
    )
    REGION_DROPDOWN_XPATH = REGION_DROPDOWN_XPATH_TEMPLATE.format(
        region_text="中国香港"
    )
    REGION_SELECTOR_XPATH = (
        '//*[@id="TabHomeCompRoot"]/Column[1]/Column[1]/Column[1]/Row[1]'
    )
    HOME_ROOT_XPATH = '//*[@id="TabHomeCompRoot"]'
    SEARCH_BAR_TEXT = "搜索服务、地图、帖子"
    SEARCH_BAR_XPATH = '//*[@text="搜索服务、地图、帖子"]'
    # 该节点在首页首屏中承载顶部视觉区（含金刚区渲染区域）。
    KINGKONG_PROXY_XPATH = '//*[@id="TabHomeCompRoot"]/Stack[1]'
    HOME_RECOMMENDS_SECTION_XPATH = '//*[@id="home_recommends_section"]'
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
        '//Text[@text="景区门票"]'
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
    WATERFALL_SECTION_XPATH = '//*[@id="home_discovery_section"]'
    CATEGORY_LIST_XPATH = (
        '//*[@id="TabHomeCompRoot"]//ListItemGroup/'
        'List[@scrollable="true"]'
    )
    WATERFALL_LIST_XPATH = (
        f'{WATERFALL_SECTION_XPATH}//WaterFlow[@scrollable="true"]'
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
        if not self._wait_by_text(self.SEARCH_BAR_TEXT, remaining()):
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
        if region_text:
            name += f"（当前地区：{region_text}）"
        self.tap_xpath(self.REGION_SELECTOR_XPATH, name)

    @classmethod
    def service_tab_xpath(cls, tab_name: str) -> str:
        """生成首页金刚区指定服务 Tab 的 XPath。"""
        return (
            f'{cls.HOME_RECOMMENDS_SECTION_XPATH}'
            f'//Column[@clickable="true" and ./Text[@text="{tab_name}"]]'
        )

    def tap_service_tab(self, tab_name: str) -> None:
        """切换首页金刚区的首页、酒店或火车 Tab。"""
        self.tap_xpath(
            self.service_tab_xpath(tab_name),
            f"首页金刚区“{tab_name}”Tab",
        )

    def tap_hotel_query(self) -> None:
        """点击酒店 Tab 中的“查询酒店”。"""
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
        if self.driver.wait_for_component(
            BY.xpath(self.SCENIC_TICKET_ENTRY_XPATH),
            timeout=1,
        ) is not None:
            return

        grid = self.wait_xpath(
            self.KINGKONG_ENTRY_GRID_XPATH,
            "首页金刚区服务列表",
        )
        self.driver.swipe("RIGHT", distance=60, area=grid)
        self.wait_xpath(
            self.SCENIC_TICKET_ENTRY_XPATH,
            "金刚区默认第一屏“景区门票”入口",
            timeout=8,
        )

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

    def tap_train_destination(self) -> None:
        """点击火车 Tab 中的“目的地”。"""
        self.tap_xpath(self.TRAIN_DESTINATION_XPATH, "火车目的地")

    @classmethod
    def category_tab_xpath(cls, tab_name: str) -> str:
        return (
            f'{cls.CATEGORY_LIST_XPATH}'
            f'//Row[@clickable="true" and ./Text[@text="{tab_name}"]]'
        )

    @classmethod
    def category_tab_text_xpath(cls, tab_name: str) -> str:
        return (
            f'{cls.category_tab_xpath(tab_name)}'
            f'/Text[@text="{tab_name}"]'
        )

    def ensure_category_tab_visible(
        self,
        tab_name: str,
        *,
        max_swipes: int = 8,
    ) -> None:
        """横向滚动攻略分类栏，直到目标 Tab 完整可见。"""
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
        """
        点击攻略分类并等待瀑布流内容变化。

        UI 树不暴露分类 selected 状态，使用“目标 Tab 可见且帖子 ID 集合变化”
        作为选中高亮和对应内容加载成功的代理断言。
        """
        previous_ids = set(previous_post_ids)
        attempt_timeout = timeout / 2

        for attempt in range(2):
            self.ensure_category_tab_visible(tab_name)
            self.tap_xpath(
                self.category_tab_text_xpath(tab_name),
                f"首页攻略分类“{tab_name}”文字",
            )

            deadline = time.monotonic() + attempt_timeout
            while time.monotonic() < deadline:
                current_ids = self.visible_guide_post_ids()
                if current_ids and set(current_ids) != previous_ids:
                    return current_ids
                time.sleep(0.4)

            if attempt == 0:
                time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 两次点击“{tab_name}”后瀑布流内容仍未变化"
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
        return f'{cls.guide_card_xpath(post_id)}/Row[2]/Row[2]/Text[1]'

    @staticmethod
    def _component_id(component: Any) -> str:
        properties = component.getAllProperties().to_dict()
        return str(properties.get("id") or properties.get("key") or "").strip()

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

    def scroll_to_waterfall(self) -> tuple[str, ...]:
        """实际上拉进入攻略瀑布流区域，并返回当前卡片 ID。"""
        waterfall = self.wait_xpath(
            self.WATERFALL_LIST_XPATH,
            "首页攻略瀑布流",
        )
        self.driver.swipe(
            "UP",
            distance=45,
            area=waterfall,
            swipe_time=0.5,
        )
        time.sleep(0.8)
        post_ids = self.visible_guide_post_ids()
        if not post_ids:
            raise RuntimeError(f"[{self.PAGE_NAME}] 上拉后没有可见攻略卡片")
        return post_ids

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

    def guide_card_fields(self, post_id: str) -> HomeGuideCard:
        """读取指定攻略卡片的标题、作者、目的地和点赞数。"""
        self.wait_xpath(self.guide_cover_xpath(post_id), "攻略封面")
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
        return HomeGuideCard(
            post_id=post_id,
            title=title,
            author=author,
            destination=destination,
            likes=likes,
        )

    def restore_top(self, *, max_swipes: int = 12) -> None:
        """测试结束后将首页恢复到顶部，避免污染后续用例。"""
        selector = BY.xpath(self.SEARCH_BAR_XPATH)
        for _ in range(max_swipes + 1):
            if self.driver.wait_for_component(selector, timeout=0.5) is not None:
                return
            self.driver.swipe(
                "DOWN",
                distance=80,
                start_point=(0.5, 0.25),
                swipe_time=0.5,
            )
            time.sleep(0.4)
        raise RuntimeError(f"[{self.PAGE_NAME}] 无法将首页恢复到顶部")

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
