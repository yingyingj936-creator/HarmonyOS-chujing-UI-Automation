import time

from hypium import BY
from hypium.model.basic_data_type import KeyCode

from pages.base_page import BasePage


class MinePage(BasePage):
    """出境服务“我的”页面对象。"""

    PAGE_NAME = "MinePage"
    LOADING_XPATH = '//Text[@text="加载中..."]'
    PROFILE_TITLE_XPATH = '//Text[@text="小星星的旅程"]'
    RECENT_SERVICES_TITLE_XPATH = '//Text[@text="最近使用"]'
    RECENT_SERVICES_GRID_XPATH = (
        '//ListItem[.//Text[@text="最近使用"]]//Grid[@scrollable="true"]'
    )
    RECENT_SERVICE_TEXT_XPATH = (
        '//ListItem[.//Text[@text="最近使用"]]//Grid[@scrollable="true"]//Text'
    )
    FAVORITES_TITLE_XPATH = '//Text[@text="收藏"]'
    FAVORITE_SEARCH_XPATH = (
        '//TextInput[@hint="搜索收藏的地点、帖子"]'
    )
    FAVORITE_CLEAR_SEARCH_XPATH = (
        '//TextInput[@hint="搜索收藏的地点、帖子"]/Stack[@clickable="true"]'
    )
    FAVORITE_PLACES_TAB_XPATH = (
        '//Row[./Text[contains(@text, "地点")]]'
    )
    FAVORITE_POSTS_TAB_XPATH = (
        '//Row[./Text[contains(@text, "帖子")]]'
    )
    FAVORITE_POSTS_TEXT_XPATH = '//Text[contains(@text, "帖子")]'
    CONTENT_STATE_TEXT_XPATH = (
        '//Text[@text="加载中..." or @text="小星星的旅程" or @text="收藏" '
        'or contains(@text, "帖子")]'
    )
    PAGE_SCROLL_XPATH = '//List[@scrollable="true"]'
    MINE_ENTRY_NAMES = (
        "我的订单",
        "优惠券",
        "联系人",
        "人工客服",
        "意见反馈",
        "更多",
    )
    MINE_ENTRY_XPATH_TEMPLATE = (
        '//Column[@clickable="true" and ./Text[@text={entry_name}]]'
    )
    ENTRY_PAGE_MARKER_XPATHS = {
        "我的订单": '//*[@text="所有" or @text="等待支付" or contains(@text, "订单")]',
        "优惠券": '//*[@text="目前可用" or contains(@text, "优惠券")]',
        "联系人": '//*[@text="出行人" or @text="联系人"]',
        "人工客服": '//*[@text="客服" or contains(@text, "机器人-小C")]',
        "更多": '//*[@text="Alipay+设置" or @text="清除缓存" or @text="关于我们"]',
    }
    FEEDBACK_TITLE_XPATH = '//*[@text="帮助与反馈"]'
    FEEDBACK_INITIAL_CATEGORY_XPATH = '//*[@text="桌面卡片"]'
    FEEDBACK_TAB_LIST_XPATH = '//*[@type="tabList"]'
    FEEDBACK_PROBLEM_BUTTON_XPATH = '//*[@text="问题反馈"]'
    FEEDBACK_DISTRICT_QUESTION_XPATH = '//*[contains(@text, "为什么定位不准确")]'
    FEEDBACK_UNINSTALL_QUESTION_XPATH = '//*[contains(@text, "如何卸载出境服务")]'
    FEEDBACK_UNINSTALL_ANSWER_XPATH = '//*[contains(@text, "移除元服务")]'
    PROBLEM_FEEDBACK_SERVICE_XPATH = '//*[@text="选择服务（必选）"]'
    PROBLEM_FEEDBACK_DESC_XPATH = '//*[@text="问题描述（必选）"]'
    FAVORITE_RESULT_IGNORED_TEXTS = {
        "收藏",
        "首页",
        "行程",
        "附近",
        "我的",
        "地点",
        "帖子",
        "景点",
        "酒店",
        "美食",
        "攻略",
        "路线",
        "服务",
    }

    @staticmethod
    def _as_list(components):
        if components is None:
            return []
        if isinstance(components, list):
            return components
        return [components]

    @staticmethod
    def _is_visible(component) -> bool:
        bounds = component.getBounds()
        return int(bounds.right) > int(bounds.left) and int(bounds.bottom) > int(bounds.top)

    @staticmethod
    def _bounds_tuple(component) -> tuple[int, int, int, int]:
        bounds = component.getBounds()
        return (
            int(bounds.left),
            int(bounds.top),
            int(bounds.right),
            int(bounds.bottom),
        )

    @staticmethod
    def favorite_place_xpath(place_name: str) -> str:
        return f'//Text[@text="{place_name}"]'

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

    @classmethod
    def any_text_xpath(cls, text: str) -> str:
        """匹配任意可访问节点文本，兼容 ArkWeb 暴露的 tab/button 节点。"""
        return f'//*[@text={cls._xpath_literal(text)}]'

    @classmethod
    def contains_any_text_xpath(cls, text: str) -> str:
        """按文本片段匹配任意可访问节点。"""
        return f'//*[contains(@text, {cls._xpath_literal(text)})]'

    @classmethod
    def mine_entry_xpath(cls, entry_name: str) -> str:
        return cls.MINE_ENTRY_XPATH_TEMPLATE.format(
            entry_name=cls._xpath_literal(entry_name)
        )

    @classmethod
    def favorite_post_xpath(cls, post_title: str) -> str:
        title_prefix = post_title.strip()[:18]
        return (
            f'//Text[starts-with(@text, {cls._xpath_literal(title_prefix)})]'
        )

    @classmethod
    def recent_service_xpath(cls, service_name: str) -> str:
        return (
            f'//ListItem[.//Text[@text="最近使用"]]//Grid[@scrollable="true"]//Column'
            f'[./Text[@text={cls._xpath_literal(service_name)}]]'
        )

    @classmethod
    def entry_page_marker_xpath(cls, entry_name: str) -> str:
        try:
            return cls.ENTRY_PAGE_MARKER_XPATHS[entry_name]
        except KeyError as exc:
            raise ValueError(f"未配置“{entry_name}”入口的页面标识") from exc

    def wait_content_loaded(self, *, timeout: float = 25) -> None:
        """等待“我的”页从 loading 态切到真实内容，避免过早查找收藏标签。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            components = self.driver.find_all_components(
                BY.xpath(self.CONTENT_STATE_TEXT_XPATH)
            )
            texts = {
                (component.getText() or "").strip()
                for component in self._as_list(components)
            }
            has_content = (
                "小星星的旅程" in texts
                or "收藏" in texts
                or any("帖子" in text for text in texts)
            )
            if "加载中..." not in texts and has_content:
                return
            time.sleep(0.5)

        raise RuntimeError(f"[{self.PAGE_NAME}] 我的页内容加载超时")

    def wait_layout_loaded(self, *, timeout: float = 15) -> None:
        """校验“我的”页关键布局已渲染。"""
        self.wait_content_loaded(timeout=timeout)
        self.wait_xpath(self.PROFILE_TITLE_XPATH, "我的页昵称", timeout=timeout)
        for entry_name in self.MINE_ENTRY_NAMES:
            self.wait_xpath(
                self.mine_entry_xpath(entry_name),
                f"我的页入口“{entry_name}”",
                timeout=timeout,
            )
        self.wait_xpath(self.RECENT_SERVICES_TITLE_XPATH, "最近使用标题", timeout=timeout)
        self.wait_xpath(self.FAVORITES_TITLE_XPATH, "收藏标题", timeout=timeout)

    def ensure_entry_area_visible(self, *, max_swipes: int = 5) -> None:
        """回到“我的”页顶部入口区域，避免前序收藏区域滚动影响入口点击。"""
        self.wait_content_loaded()
        for swipe_count in range(max_swipes + 1):
            if self.find_xpath(self.mine_entry_xpath("我的订单")) is not None:
                return
            if swipe_count == max_swipes:
                break
            page_scroll = self.wait_xpath(self.PAGE_SCROLL_XPATH, "我的页面滚动列表")
            self.driver.swipe(
                "DOWN",
                distance=55,
                area=page_scroll,
            )
            time.sleep(0.5)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未回到我的页入口区域")

    def tap_entry(self, entry_name: str, *, timeout: float = 8) -> None:
        """点击“我的”页顶部功能入口。"""
        self.ensure_entry_area_visible()
        self.tap_xpath(
            self.mine_entry_xpath(entry_name),
            f"我的页入口“{entry_name}”",
            timeout=timeout,
        )

    def wait_entry_page_loaded(self, entry_name: str, *, timeout: float = 12):
        """等待功能入口跳转后的目标页面标识出现。"""
        return self.wait_xpath(
            self.entry_page_marker_xpath(entry_name),
            f"{entry_name}页面标识",
            timeout=timeout,
        )

    def wait_feedback_loaded(self, *, timeout: float = 12) -> None:
        """等待帮助与反馈页加载完成。"""
        self.wait_xpath(self.FEEDBACK_TITLE_XPATH, "帮助与反馈标题", timeout=timeout)
        self.wait_xpath(
            self.FEEDBACK_INITIAL_CATEGORY_XPATH,
            "帮助与反馈默认分类",
            timeout=timeout,
        )
        self.wait_xpath(
            self.FEEDBACK_PROBLEM_BUTTON_XPATH,
            "问题反馈入口",
            timeout=timeout,
        )

    def tap_feedback_category(
        self,
        category_name: str,
        *,
        aliases: tuple[str, ...] = (),
        timeout: float = 8,
        max_swipes: int = 5,
    ) -> None:
        """点击帮助与反馈分类；分类横向隐藏时先滑动 tabList。"""
        self.wait_xpath(self.FEEDBACK_TITLE_XPATH, "帮助与反馈标题", timeout=timeout)
        candidate_names = (category_name, *aliases)
        deadline = time.monotonic() + timeout
        for swipe_count in range(max_swipes + 1):
            for candidate_name in candidate_names:
                component = self.find_xpath(self.any_text_xpath(candidate_name))
                if component is not None:
                    component.click()
                    time.sleep(1.2)
                    return
            if swipe_count == max_swipes or time.monotonic() >= deadline:
                break
            tab_list = self.find_xpath(self.FEEDBACK_TAB_LIST_XPATH)
            if tab_list is not None:
                self.driver.swipe(
                    "LEFT",
                    distance=75,
                    area=tab_list,
                    swipe_time=0.4,
                )
            else:
                self.driver.swipe("LEFT", distance=75, swipe_time=0.4)
            time.sleep(0.8)

        names = "、".join(candidate_names)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到帮助与反馈分类：{names}")

    def wait_problem_feedback_loaded(self, *, timeout: float = 12) -> None:
        """等待问题反馈表单加载完成。"""
        self.wait_xpath(
            self.PROBLEM_FEEDBACK_SERVICE_XPATH,
            "问题反馈-选择服务",
            timeout=timeout,
        )
        self.wait_xpath(
            self.PROBLEM_FEEDBACK_DESC_XPATH,
            "问题反馈-问题描述",
            timeout=timeout,
        )

    def wait_recent_services_visible(self, *, timeout: float = 10) -> tuple[str, ...]:
        """等待最近使用区域展示，并返回当前可见服务名称。"""
        self.wait_content_loaded()
        self.wait_xpath(self.RECENT_SERVICES_TITLE_XPATH, "最近使用标题", timeout=timeout)
        self.wait_xpath(self.RECENT_SERVICES_GRID_XPATH, "最近使用服务列表", timeout=timeout)

        deadline = time.monotonic() + timeout
        last_names: tuple[str, ...] = ()
        while time.monotonic() < deadline:
            names = self.visible_recent_service_names()
            if names:
                return names
            last_names = names
            time.sleep(0.4)

        raise RuntimeError(f"[{self.PAGE_NAME}] 最近使用服务列表为空：{last_names}")

    def visible_recent_service_names(self) -> tuple[str, ...]:
        """读取最近使用区域当前可见服务名，按屏幕从左到右排序。"""
        components = self.driver.find_all_components(
            BY.xpath(self.RECENT_SERVICE_TEXT_XPATH)
        )
        items: list[tuple[int, int, str]] = []
        for component in self._as_list(components):
            if not self._is_visible(component):
                continue
            text = component.getText().strip()
            if not text:
                continue
            bounds = component.getBounds()
            items.append((int(bounds.left), int(bounds.top), text))

        items.sort(key=lambda item: (item[0], item[1]))
        names: list[str] = []
        for _, _, text in items:
            if text not in names:
                names.append(text)
        return tuple(names)

    def recent_service_component(self, service_name: str, *, timeout: float = 8):
        """返回最近使用区域中指定服务的可见卡片。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            components = self.driver.find_all_components(
                BY.xpath(self.recent_service_xpath(service_name))
            )
            visible_components = [
                component
                for component in self._as_list(components)
                if self._is_visible(component)
            ]
            if visible_components:
                visible_components.sort(key=lambda component: int(component.getBounds().left))
                return visible_components[0]
            time.sleep(0.3)

        raise RuntimeError(f"[{self.PAGE_NAME}] 最近使用区域未找到服务“{service_name}”")

    def swipe_recent_services_to_tail(self, *, max_swipes: int = 8) -> str:
        """横向滑动最近使用列表到末尾，并返回当前末尾服务名。"""
        grid = self.wait_xpath(self.RECENT_SERVICES_GRID_XPATH, "最近使用服务列表")
        names = self.wait_recent_services_visible()
        stable_count = 0

        for _ in range(max_swipes):
            before_names = names
            self.driver.swipe("LEFT", distance=70, area=grid, swipe_time=0.55)
            time.sleep(0.8)
            names = self.visible_recent_service_names()
            if not names:
                names = before_names
            if names == before_names:
                stable_count += 1
                if stable_count >= 2:
                    break
            else:
                stable_count = 0

        if not names:
            raise RuntimeError(f"[{self.PAGE_NAME}] 最近使用列表未读取到服务")
        return names[-1]

    def swipe_recent_services_to_head(self, *, max_swipes: int = 8) -> tuple[str, ...]:
        """横向滑动最近使用列表到开头，并返回当前可见服务名。"""
        grid = self.wait_xpath(self.RECENT_SERVICES_GRID_XPATH, "最近使用服务列表")
        names = self.wait_recent_services_visible()
        stable_count = 0

        for _ in range(max_swipes):
            before_names = names
            self.driver.swipe("RIGHT", distance=70, area=grid, swipe_time=0.55)
            time.sleep(0.8)
            names = self.visible_recent_service_names()
            if not names:
                names = before_names
            if names == before_names:
                stable_count += 1
                if stable_count >= 2:
                    break
            else:
                stable_count = 0

        if not names:
            raise RuntimeError(f"[{self.PAGE_NAME}] 最近使用列表未读取到服务")
        return names

    def tap_recent_service(self, service_name: str, *, timeout: float = 8) -> None:
        """点击最近使用区域的指定服务。"""
        component = self.recent_service_component(service_name, timeout=timeout)
        component.click()

    def wait_recent_service_first(
        self,
        service_name: str,
        *,
        timeout: float = 12,
    ) -> tuple[str, ...]:
        """等待指定服务移动到最近使用第一位。"""
        deadline = time.monotonic() + timeout
        last_names: tuple[str, ...] = ()
        while time.monotonic() < deadline:
            names = self.swipe_recent_services_to_head(max_swipes=4)
            last_names = names
            if names and names[0] == service_name:
                return names
            time.sleep(0.8)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 服务“{service_name}”未移动到最近使用第一位，"
            f"当前顺序：{last_names}"
        )

    def scroll_favorites_area_into_view(self, *, max_swipes: int = 6) -> None:
        """滚动“我的”页面，直到收藏区域进入可见区域。"""
        self.wait_content_loaded()
        for swipe_count in range(max_swipes + 1):
            if self.driver.wait_for_component(
                BY.xpath(self.FAVORITES_TITLE_XPATH),
                timeout=1,
            ) is not None:
                return
            if swipe_count == max_swipes:
                break
            page_scroll = self.wait_xpath(
                self.PAGE_SCROLL_XPATH,
                "我的页面滚动列表",
            )
            self.driver.swipe(
                "UP",
                distance=45,
                area=page_scroll,
            )
            time.sleep(0.5)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到收藏区域")

    def tap_favorite_places_tab(self) -> None:
        """点击收藏区域的“地点”页签。"""
        self.scroll_favorites_area_into_view()
        self.tap_xpath(
            self.FAVORITE_PLACES_TAB_XPATH,
            "收藏地点页签",
        )

    def tap_favorite_posts_tab(self) -> None:
        """点击收藏区域的“帖子”页签。"""
        self.wait_content_loaded()
        self.scroll_favorites_area_into_view()
        page_scroll = self.wait_xpath(
            self.PAGE_SCROLL_XPATH,
            "我的页面滚动列表",
        )
        for _ in range(8):
            tab = self.find_xpath(self.FAVORITE_POSTS_TAB_XPATH)
            if tab is not None:
                tab.click()
                return

            tab_text = self.find_xpath(self.FAVORITE_POSTS_TEXT_XPATH)
            if tab_text is not None:
                tab_text.click()
                return

            self.driver.swipe(
                "UP",
                distance=30,
                area=page_scroll,
            )
            time.sleep(0.4)

        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到收藏帖子页签")

    @classmethod
    def _is_favorite_result_text(cls, text: str) -> bool:
        normalized = text.strip()
        if not normalized:
            return False
        if normalized in cls.FAVORITE_RESULT_IGNORED_TEXTS:
            return False
        if normalized.startswith(("地点·", "帖子·", "评分 ", "搜索收藏")):
            return False
        if normalized in {
            "暂无收藏",
            "暂无搜索结果",
            "没找到相关内容，换个搜索词试试?",
        }:
            return False
        if normalized.replace(",", "").replace(".", "").isdigit():
            return False
        return True

    def visible_favorite_result_items(self) -> list[tuple[str, object]]:
        """
        读取收藏搜索框下方当前可见的收藏内容。

        收藏地点和帖子列表没有稳定业务 id，这里用搜索框的空间位置作为上边界，
        排除底部导航和标签文案后，返回真实收藏内容文本。
        """
        search_input = self.wait_xpath(
            self.FAVORITE_SEARCH_XPATH,
            "收藏搜索框",
        )
        _, _, _, search_bottom = self._bounds_tuple(search_input)
        try:
            components = self.driver.find_all_components(BY.xpath("//Text"))
        except Exception:
            return []
        text_components = self._as_list(components)
        if not text_components:
            return []

        page_scroll = self.find_xpath(self.PAGE_SCROLL_XPATH)
        if page_scroll is not None:
            bottom_limit = self._bounds_tuple(page_scroll)[3] - 20
        else:
            visible_bounds = [
                self._bounds_tuple(component)
                for component in text_components
                if self._is_visible(component)
            ]
            if not visible_bounds:
                return []
            bottom_limit = max(bounds[3] for bounds in visible_bounds)

        nav_tops = []
        for component in text_components:
            text = component.getText().strip()
            if text not in {"首页", "行程", "附近", "我的"}:
                continue
            if not self._is_visible(component):
                continue
            _, top, _, _ = self._bounds_tuple(component)
            if top > search_bottom:
                nav_tops.append(top)
        if nav_tops:
            bottom_limit = min(bottom_limit, min(nav_tops) - 20)

        candidates: list[tuple[int, int, str, object]] = []
        seen_texts: set[str] = set()
        for component in text_components:
            if not self._is_visible(component):
                continue
            text = component.getText().strip()
            if text in seen_texts or not self._is_favorite_result_text(text):
                continue
            left, top, right, bottom = self._bounds_tuple(component)
            if right <= left or bottom <= top:
                continue
            if top <= search_bottom + 20:
                continue
            if top >= bottom_limit:
                continue
            candidates.append((top, left, text, component))
            seen_texts.add(text)

        candidates.sort(key=lambda item: (item[0], item[1]))
        return [(text, component) for _, _, text, component in candidates]

    @classmethod
    def favorite_item_container_xpaths(cls, item_name: str) -> tuple[str, ...]:
        literal = cls._xpath_literal(item_name)
        return (
            f'//Column[@clickable="true" and .//Text[@text={literal}]]',
            f'//Row[@clickable="true" and .//Text[@text={literal}]]',
            f'//Stack[@clickable="true" and .//Text[@text={literal}]]',
            f'//ListItem[@clickable="true" and .//Text[@text={literal}]]',
        )

    def tap_favorite_item(
        self,
        item_name: str,
        fallback_component,
    ) -> None:
        """优先点击收藏内容所在的可点击卡片，避免直接点击 Text 不触发跳转。"""
        text_left, text_top, text_right, text_bottom = self._bounds_tuple(
            fallback_component
        )
        candidates = []
        for xpath in self.favorite_item_container_xpaths(item_name):
            try:
                components = self.driver.find_all_components(BY.xpath(xpath))
            except Exception:
                components = []
            for component in self._as_list(components):
                if not self._is_visible(component):
                    continue
                left, top, right, bottom = self._bounds_tuple(component)
                if (
                    left <= text_left
                    and top <= text_top
                    and right >= text_right
                    and bottom >= text_bottom
                ):
                    area = (right - left) * (bottom - top)
                    candidates.append((area, top, left, component))

        if candidates:
            candidates.sort(key=lambda item: (item[0], item[1], item[2]))
            candidates[0][3].click()
            return

        fallback_component.click()

    def wait_first_visible_favorite_item(
        self,
        item_type: str,
        *,
        timeout: float = 8,
    ) -> tuple[str, object]:
        """等待并返回当前收藏 Tab 下第一条可见收藏内容。"""
        deadline = time.monotonic() + timeout
        last_items: list[tuple[str, object]] = []
        while time.monotonic() < deadline:
            items = self.visible_favorite_result_items()
            if items:
                return items[0]
            last_items = items
            time.sleep(0.4)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏{item_type}列表没有可见内容：{last_items}"
        )

    def wait_favorite_search_result(
        self,
        keyword: str,
        *,
        timeout: float = 8,
    ) -> tuple[str, object]:
        """等待收藏搜索结果中出现包含关键词的内容。"""
        deadline = time.monotonic() + timeout
        visible_texts: tuple[str, ...] = ()
        while time.monotonic() < deadline:
            items = self.visible_favorite_result_items()
            visible_texts = tuple(text for text, _ in items)
            for text, component in items:
                if keyword in text:
                    return text, component
            time.sleep(0.4)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏搜索未出现关键词“{keyword}”相关结果，"
            f"当前可见内容：{visible_texts}"
        )

    def input_favorite_search(self, keyword: str) -> None:
        """在收藏搜索框输入关键词，页面会刷新收藏搜索结果。"""
        self.clear_favorite_search()
        search_input = self.wait_xpath(
            self.FAVORITE_SEARCH_XPATH,
            "收藏搜索框",
        )
        search_input.click()
        time.sleep(0.4)
        search_input.inputText(keyword)
        time.sleep(0.4)
        self.driver.press_key(KeyCode.ENTER)
        time.sleep(1)
        if hasattr(search_input, "isFocused") and search_input.isFocused():
            self.driver.press_back()
            time.sleep(0.5)

    def clear_favorite_search(self) -> None:
        """清空收藏搜索框，避免上一次搜索词污染地点/帖子列表。"""
        self.scroll_favorites_area_into_view()
        search_input = self.wait_xpath(
            self.FAVORITE_SEARCH_XPATH,
            "收藏搜索框",
        )
        if not search_input.getText().strip():
            return
        search_input.click()
        time.sleep(0.4)
        if hasattr(search_input, "clearText"):
            try:
                search_input.clearText()
                time.sleep(0.2)
            except Exception:
                pass

        if search_input.getText().strip():
            clear_button = self.find_xpath(self.FAVORITE_CLEAR_SEARCH_XPATH)
            if clear_button is not None:
                clear_button.click()
                time.sleep(0.5)

        if hasattr(search_input, "isFocused") and search_input.isFocused():
            self.driver.press_back()
            time.sleep(0.5)

        deadline = time.monotonic() + 5
        while time.monotonic() < deadline:
            current_input = self.find_xpath(self.FAVORITE_SEARCH_XPATH)
            if current_input is not None and not current_input.getText().strip():
                return
            time.sleep(0.3)

        raise RuntimeError(f"[{self.PAGE_NAME}] 收藏搜索框未能清空")

    def restore_favorites_default_state(self) -> None:
        """恢复收藏默认地点页并回到“我的”页顶部，避免污染后续用例。"""
        self.wait_content_loaded(timeout=12)
        self.scroll_favorites_area_into_view(max_swipes=8)
        self.clear_favorite_search()
        self.tap_favorite_places_tab()
        time.sleep(0.5)
        self.ensure_entry_area_visible(max_swipes=10)

    def scroll_favorite_place_into_view(
        self,
        place_name: str,
        *,
        max_swipes: int = 5,
    ) -> None:
        """滚动“我的”页面，直到收藏地点进入可见区域。"""
        selector = BY.xpath(self.favorite_place_xpath(place_name))
        page_scroll = self.wait_xpath(
            self.PAGE_SCROLL_XPATH,
            "我的页面滚动列表",
        )

        for _ in range(max_swipes + 1):
            if self.driver.wait_for_component(selector, timeout=1) is not None:
                return
            self.driver.swipe(
                "UP",
                distance=35,
                area=page_scroll,
            )
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏地点列表未找到“{place_name}”"
        )

    def favorite_place_exists(
        self,
        place_name: str,
        *,
        max_swipes: int = 5,
    ) -> bool:
        """查找收藏地点是否存在，找不到时返回 False。"""
        try:
            self.scroll_favorite_place_into_view(
                place_name,
                max_swipes=max_swipes,
            )
        except RuntimeError:
            return False
        return True

    def wait_favorite_place_absent(
        self,
        place_name: str,
        *,
        timeout: float = 8,
        max_swipes: int = 5,
    ) -> bool:
        """等待收藏地点从列表中移除。"""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if not self.favorite_place_exists(
                place_name,
                max_swipes=max_swipes,
            ):
                return True
            time.sleep(0.8)
        return False

    def scroll_favorite_post_into_view(
        self,
        post_title: str,
        *,
        max_swipes: int = 8,
    ) -> None:
        """滚动“我的”页面，直到收藏帖子进入可见区域。"""
        selector = BY.xpath(self.favorite_post_xpath(post_title))
        page_scroll = self.wait_xpath(
            self.PAGE_SCROLL_XPATH,
            "我的页面滚动列表",
        )

        for _ in range(max_swipes + 1):
            if self.driver.wait_for_component(selector, timeout=1) is not None:
                return
            self.driver.swipe(
                "UP",
                distance=35,
                area=page_scroll,
            )
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏帖子列表未找到“{post_title}”"
        )

