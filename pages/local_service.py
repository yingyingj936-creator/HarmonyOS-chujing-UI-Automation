import time

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
        '//Stack/Stack/List/ListItem/Column/'
        'Row[@clickable="true"]/Column/Text[1]'
    )
    SEARCH_RESULT_ROW_XPATH_TEMPLATE = (
        '//Stack/Stack/List/ListItem/Column/Row'
        '[@clickable="true" and ./Column/Text[@text="{service_name}"]]'
    )
    SERVICE_ROW_XPATH_TEMPLATE = (
        '//SideBarContainer//Row'
        '[@clickable="true" and ./Column/Text[@text="{service_name}"]]'
    )
    DEFAULT_FIRST_SERVICE_XPATH = (
        '//SideBarContainer//Row'
        '[@clickable="true" and ./Column/Text[@text="Xe"]]'
    )
    SERVICE_CONTAINER_XPATH = '//SideBarContainer'
    RIGHT_SERVICE_TEXT_XPATH = (
        '//SideBarContainer//ListItem'
        '//Row[@clickable="true"]/Column/Text'
    )
    SELECTED_BACKGROUND = "#FFFFFFFF"
    BBC_NEWS_ROW_XPATH = (
        '//Row[@clickable="true" and ./Column/Text[@text="BBC News"]]'
    )
    FOOD_ORDERING_CARD_XPATH = (
        '//ListItemGroup[./Text[@text="美食外卖"]]'
        '/List/ListItem[3]/*[@clickable="true" and ./Image]'
    )

    @classmethod
    def category_xpath(cls, category_name: str) -> str:
        return (
            '//SideBarContainer'
            f'//Column[@clickable="true" and ./Text[@text="{category_name}"]]'
        )

    @classmethod
    def category_text_xpath(cls, category_name: str) -> str:
        return (
            '//SideBarContainer'
            f'//Column[@clickable="true"]/Text[@text="{category_name}"]'
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
        self.tap_xpath(
            self.FOOD_ORDERING_CARD_XPATH,
            "掌上美食卡片",
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
        """等待结果出现，并校验所有服务名称均包含搜索关键词。"""
        deadline = time.time() + timeout
        normalized_keyword = keyword.casefold()
        while time.time() < deadline:
            names = self.visible_search_result_names()
            if names and all(
                normalized_keyword in name.casefold() for name in names
            ):
                return names
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 搜索结果未全部匹配关键词“{keyword}”"
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
