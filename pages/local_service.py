import time
from typing import Any

from hypium import BY

from pages.base_page import BasePage


class LocalServicePage(BasePage):
    """首页金刚区本地服务列表页面对象。"""

    PAGE_NAME = "LocalServicePage"
    PAGE_TITLE_XPATH = '//Text[@text="服务"]'
    SEARCH_INPUT_XPATH = '//TextInput[@hint="搜索服务"]'
    SEARCH_BUTTON_XPATH = '//Text[@text="搜索" and @clickable="true"]'
    CLEAR_SEARCH_XPATH = (
        '//TextInput[@hint="搜索服务"]/Stack[@clickable="true"]'
    )
    SEARCH_RESULT_NAME_XPATH = (
        '//ListItem//Row[@clickable="true"]//Column/Text[1]'
    )
    SEARCH_RESULT_ROW_XPATH_TEMPLATE = (
        '//ListItem[.//Row[@clickable="true"]//Column/Text[1]'
        '[@text="{service_name}"]]//Row[@clickable="true"]'
    )
    SERVICE_ROW_XPATH_TEMPLATE = (
        '//SideBarContainer//*[@clickable="true" '
        'and .//Text[@text="{service_name}"]]'
    )
    DEFAULT_FIRST_SERVICE_XPATH = (
        '//SideBarContainer//*[@clickable="true" and .//Text[@text="Xe"]]'
    )
    SERVICE_CONTAINER_XPATH = '//SideBarContainer'
    RIGHT_SERVICE_TEXT_XPATH = (
        '//SideBarContainer//*[@clickable="true"]//Text'
    )
    SELECTED_BACKGROUND = "#FFFFFFFF"
    BBC_NEWS_ROW_XPATH = (
        '//SideBarContainer//*[@clickable="true" and .//Text[@text="BBC News"]]'
    )
    FOOD_ORDERING_CARD_TEXT_XPATH = (
        '//SideBarContainer//Text[@text="掌上美食" or contains(@text, "掌上美食")]'
    )
    FOOD_ORDERING_CARD_XPATH = FOOD_ORDERING_CARD_TEXT_XPATH
    FOOD_ORDERING_IMAGE_CARD_XPATHS = (
        '//SideBarContainer//*[@clickable="true" and .//Image]',
        '//SideBarContainer//ListItem[@clickable="true" and .//Image]',
        '//SideBarContainer//Stack[@clickable="true" and .//Image]',
    )

    @classmethod
    def category_xpath(cls, category_name: str) -> str:
        return (
            '//SideBarContainer'
            f'//Column[@clickable="true" and .//Text[@text="{category_name}"]]'
        )

    @classmethod
    def category_text_xpath(cls, category_name: str) -> str:
        return (
            '//SideBarContainer'
            f'//Column[@clickable="true"]//Text[@text="{category_name}"]'
        )

    def tap_category(self, category_name: str) -> None:
        """点击左侧服务分类文字，触发所属分类容器切换。"""
        self.tap_xpath(
            self.category_text_xpath(category_name),
            f"服务分类“{category_name}”",
        )

    def is_category_highlighted(self, category_name: str) -> bool:
        """通过分类容器的白色背景判断当前分类是否高亮。"""
        component = self.find_xpath(self.category_xpath(category_name))
        if component is None:
            return False
        background = component.getAllProperties().to_dict().get(
            "backgroundColor",
            "",
        )
        return background.upper() == self.SELECTED_BACKGROUND

    def wait_category_highlighted(
        self,
        category_name: str,
        *,
        timeout: float = 5,
    ) -> None:
        """等待指定分类切换为高亮状态。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.is_category_highlighted(category_name):
                return
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 分类“{category_name}”未切换为高亮状态"
        )

    def visible_service_texts(self) -> tuple[str, ...]:
        """读取右侧当前已渲染的服务名称和说明文字。"""
        components = self.driver.find_all_components(
            BY.xpath(self.RIGHT_SERVICE_TEXT_XPATH)
        )
        if components is None:
            return ()
        if not isinstance(components, list):
            components = [components]

        texts = []
        for component in components:
            text = component.getText().strip()
            if text and text not in texts:
                texts.append(text)
        return tuple(texts)

    def wait_service_content(
        self,
        *,
        previous_texts: tuple[str, ...] | None = None,
        timeout: float = 8,
    ) -> tuple[str, ...]:
        """等待右侧服务内容出现，并可校验相对上一分类已经刷新。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            current_texts = self.visible_service_texts()
            if current_texts and (
                previous_texts is None
                or set(current_texts) != set(previous_texts)
            ):
                return current_texts
            time.sleep(0.4)

        if previous_texts is None:
            reason = "未展示任何服务项"
        else:
            reason = "服务项未相对上一分类刷新"
        raise RuntimeError(f"[{self.PAGE_NAME}] 右侧{reason}")

    def tap_bbc_news(self) -> None:
        """点击“其他”分类中的 BBC News 服务。"""
        self.tap_xpath(self.BBC_NEWS_ROW_XPATH, "BBC News 服务")

    @classmethod
    def service_row_xpath(cls, service_name: str) -> str:
        return cls.SERVICE_ROW_XPATH_TEMPLATE.format(
            service_name=service_name,
        )

    def tap_service(self, service_name: str) -> None:
        """点击默认服务列表中的指定服务。"""
        self.tap_xpath(
            self.service_row_xpath(service_name),
            f"本地服务“{service_name}”",
        )

    def tap_food_ordering_card(self) -> None:
        """点击“美食”分类中的掌上美食卡片。"""
        component = self.ensure_food_ordering_card_visible()
        component.click()

    def ensure_food_ordering_card_visible(
        self,
        *,
        timeout: float = 8,
        max_swipes: int = 6,
    ) -> object:
        """滚动右侧服务列表，直到掌上美食卡片进入可见区域。

        线上配置里“掌上美食”可能是图片卡片，UI 树没有文字节点。
        因此这里先按文字找，失败后按右侧内容区的图片大卡片兜底。
        """
        deadline = time.time() + timeout
        container = self.wait_xpath(
            self.SERVICE_CONTAINER_XPATH,
            "本地服务内容区",
            timeout=timeout,
        )
        for swipe_count in range(max_swipes + 1):
            component = self.find_food_ordering_card(container=container)
            if component is not None:
                return component
            if swipe_count == max_swipes or time.time() >= deadline:
                break
            self.driver.swipe(
                "UP",
                distance=55,
                area=container,
                swipe_time=0.5,
            )
            time.sleep(0.6)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到掌上美食卡片，timeout={timeout}s"
        )

    def find_food_ordering_card(self, *, container: Any | None = None) -> Any | None:
        """Find food ordering card by text first, then image-card fallback."""
        text_component = self.find_xpath(self.FOOD_ORDERING_CARD_TEXT_XPATH)
        if text_component is not None:
            return text_component

        if container is None:
            container = self.find_xpath(self.SERVICE_CONTAINER_XPATH)
        if container is None:
            return None

        candidates = []
        for xpath in self.FOOD_ORDERING_IMAGE_CARD_XPATHS:
            for component in self._find_all_xpath(xpath):
                if not self._is_right_service_card(component, container):
                    continue
                left, top, right, bottom = self._component_bounds(component)
                area = (right - left) * (bottom - top)
                is_banner = self._is_food_ordering_banner(component)
                candidates.append((not is_banner, top, left, -area, component))

        if not candidates:
            return None
        return sorted(candidates, key=lambda item: item[:4])[0][4]

    def _find_all_xpath(self, xpath: str) -> list[Any]:
        components = self.driver.find_all_components(BY.xpath(xpath))
        if components is None:
            return []
        if isinstance(components, list):
            return components
        return [components]

    @staticmethod
    def _component_bounds(component: Any) -> tuple[int, int, int, int]:
        bounds = component.getBounds()
        return (
            int(bounds.left),
            int(bounds.top),
            int(bounds.right),
            int(bounds.bottom),
        )

    def _is_right_service_card(self, component: Any, container: Any) -> bool:
        left, top, right, bottom = self._component_bounds(component)
        c_left, c_top, c_right, c_bottom = self._component_bounds(container)
        width = right - left
        height = bottom - top
        if width < 180 or height < 80:
            return False
        if right <= c_left or left >= c_right or bottom <= c_top or top >= c_bottom:
            return False

        # Ignore the left category rail; food ordering is a large card in right content.
        right_content_left = c_left + int((c_right - c_left) * 0.28)
        return left >= right_content_left

    def _is_food_ordering_banner(self, component: Any) -> bool:
        left, top, right, bottom = self._component_bounds(component)
        width = right - left
        height = bottom - top
        if width <= 0 or height <= 0:
            return False
        properties = component.getAllProperties().to_dict()
        # The "掌上美食" entry is configured as a wide image banner, while
        # third-party service rows such as foodpanda/Keeta are shorter rows.
        return (
            properties.get("type") == "__Common__"
            or height / width >= 0.32
        )

    def scroll_service_content_until_xpath_visible(
        self,
        xpath: str,
        name: str,
        *,
        timeout: float = 8,
        max_swipes: int = 6,
    ) -> object:
        """在本地服务右侧内容区向下滚动查找目标服务入口。"""
        deadline = time.time() + timeout
        container = self.wait_xpath(
            self.SERVICE_CONTAINER_XPATH,
            "本地服务内容区",
            timeout=timeout,
        )
        for swipe_count in range(max_swipes + 1):
            component = self.find_xpath(xpath)
            if component is not None:
                return component
            if swipe_count == max_swipes or time.time() >= deadline:
                break
            self.driver.swipe(
                "UP",
                distance=55,
                area=container,
                swipe_time=0.5,
            )
            time.sleep(0.6)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到{name}，timeout={timeout}s"
        )

    @classmethod
    def search_result_row_xpath(cls, service_name: str) -> str:
        return cls.SEARCH_RESULT_ROW_XPATH_TEMPLATE.format(
            service_name=service_name,
        )

    def tap_search_input(self) -> None:
        """点击服务列表搜索框并拉起键盘。"""
        self.tap_xpath(self.SEARCH_INPUT_XPATH, "服务列表搜索框")

    def input_search_keyword(self, keyword: str) -> None:
        """在服务列表搜索框输入关键词。"""
        self.input_xpath(
            self.SEARCH_INPUT_XPATH,
            keyword,
            "服务列表搜索框",
        )

    def tap_search_button(self) -> None:
        """点击搜索框右侧的页面内搜索按钮。"""
        self.tap_xpath(self.SEARCH_BUTTON_XPATH, "服务搜索按钮")

    def visible_search_result_names(self) -> tuple[str, ...]:
        """读取独立搜索结果层中当前展示的服务名称。"""
        components = self.driver.find_all_components(
            BY.xpath(self.SEARCH_RESULT_NAME_XPATH)
        )
        if components is None:
            return ()
        if not isinstance(components, list):
            components = [components]

        names = []
        for component in components:
            name = component.getText().strip()
            if name and name not in names:
                names.append(name)
        return tuple(names)

    def wait_search_results_match(
        self,
        keyword: str,
        *,
        timeout: float = 8,
    ) -> tuple[str, ...]:
        """等待搜索结果出现，并确认至少一个业务结果命中关键词。"""
        deadline = time.time() + timeout
        normalized_keyword = keyword.casefold()
        while time.time() < deadline:
            names = self.visible_search_result_names()
            if names and any(
                normalized_keyword in name.casefold() for name in names
            ):
                return names
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 搜索结果未匹配关键词“{keyword}”"
        )

    def tap_search_result(self, service_name: str) -> None:
        """点击搜索结果层中的指定服务。"""
        self.tap_xpath(
            self.search_result_row_xpath(service_name),
            f"服务搜索结果“{service_name}”",
        )

    def tap_clear_search(self) -> None:
        """点击服务搜索框内的清除按钮。"""
        self.tap_xpath(self.CLEAR_SEARCH_XPATH, "服务搜索框清除按钮")

    def wait_search_cleared(self, *, timeout: float = 8) -> None:
        """等待搜索词清空、结果层消失且默认服务列表恢复。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            search_input = self.find_xpath(self.SEARCH_INPUT_XPATH)
            result_row = self.find_xpath(
                self.search_result_row_xpath("Dufry")
            )
            default_service = self.find_xpath(
                self.DEFAULT_FIRST_SERVICE_XPATH
            )
            if (
                search_input is not None
                and not search_input.getText().strip()
                and result_row is None
                and default_service is not None
            ):
                return
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 搜索内容未清空或默认服务列表未恢复"
        )

    def system_gesture_back(self) -> None:
        """执行 HarmonyOS 右侧边缘返回手势。"""
        self.driver.swipe_to_back(side="RIGHT")
