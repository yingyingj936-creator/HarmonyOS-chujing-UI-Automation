import time

from hypium import BY

from pages.base_page import BasePage


class FoodOrderingPage(BasePage):
    """掌上美食点餐列表页面对象。"""

    PAGE_NAME = "FoodOrderingPage"
    PAGE_TITLE_XPATH = '//Text[@text="点餐 · 中国香港"]'
    SEARCH_INPUT_XPATH = '//TextInput[@hint="搜索服务"]'
    CLEAR_SEARCH_XPATH = (
        '//TextInput[@hint="搜索服务"]/Stack[@clickable="true"]'
    )
    SEARCH_RESULT_ROW_XPATH_TEMPLATE = (
        '//Stack/Stack/List/ListItem/Row'
        '[@clickable="true" and ./Column/Text[@text="{service_name}"]]'
    )
    DEFAULT_FIRST_ROW_XPATH = (
        '//Tabs//Row[@clickable="true" '
        'and ./Column/Text[@text="蜀小魚 (深水埗)"]]'
    )
    ORDER_CONTENT_XPATH = '//Tabs'
    ORDER_TEXT_XPATH = (
        '//Tabs//ListItem//Row[@clickable="true"]/Column/Text'
    )
    SELECTED_BACKGROUND = "#E6000000"
    LIGE_ROW_XPATH = (
        '//Tabs//Row[@clickable="true" and ./Column/Text[@text="立哥"]]'
    )

    @classmethod
    def category_xpath(cls, category_name: str) -> str:
        return (
            '//ListItem[@clickable="true"]'
            f'/Text[@text="{category_name}"]'
        )

    @classmethod
    def category_item_xpath(cls, category_name: str) -> str:
        return (
            '//ListItem[@clickable="true" '
            f'and ./Text[@text="{category_name}"]]'
        )

    def tap_category(self, category_name: str) -> None:
        """点击点餐页顶部分类。"""
        self.tap_xpath(
            self.category_item_xpath(category_name),
            f"点餐分类“{category_name}”",
        )

    def is_category_highlighted(self, category_name: str) -> bool:
        """通过分类文字背景色判断是否选中。"""
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
        """等待指定点餐分类高亮。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.is_category_highlighted(category_name):
                return
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 分类“{category_name}”未切换为高亮状态"
        )

    def visible_order_texts(self) -> tuple[str, ...]:
        """读取当前分类已渲染的商户名称和说明。"""
        components = self.driver.find_all_components(
            BY.xpath(self.ORDER_TEXT_XPATH)
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

    def wait_order_content(
        self,
        *,
        previous_texts: tuple[str, ...] | None = None,
        timeout: float = 8,
    ) -> tuple[str, ...]:
        """等待商户列表出现，并可校验相对上一分类已经刷新。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            current_texts = self.visible_order_texts()
            if current_texts and (
                previous_texts is None
                or set(current_texts) != set(previous_texts)
            ):
                return current_texts
            time.sleep(0.4)

        if previous_texts is None:
            reason = "未展示商户"
        else:
            reason = "商户列表未相对上一分类刷新"
        raise RuntimeError(f"[{self.PAGE_NAME}] {reason}")

    def tap_lige(self) -> None:
        """点击快餐分类中的“立哥”商户。"""
        self.tap_xpath(self.LIGE_ROW_XPATH, "快餐商户“立哥”")

    @classmethod
    def search_result_row_xpath(cls, service_name: str) -> str:
        return cls.SEARCH_RESULT_ROW_XPATH_TEMPLATE.format(
            service_name=service_name,
        )

    def input_search_keyword(self, keyword: str) -> None:
        """在点餐页搜索框输入关键词，页面会自动筛选结果。"""
        self.input_xpath(
            self.SEARCH_INPUT_XPATH,
            keyword,
            "点餐搜索框",
        )

    def tap_search_result(self, service_name: str) -> None:
        """点击搜索结果层中的指定服务。"""
        result_xpath = self.search_result_row_xpath(service_name)
        # 输入后键盘仍处于焦点状态，先收起键盘，避免首次点击仅关闭输入法。
        self.driver.press_back()
        self.wait_xpath(
            result_xpath,
            f"收起键盘后的搜索结果“{service_name}”",
            timeout=5,
        )
        self.tap_xpath(
            result_xpath,
            f"搜索结果“{service_name}”",
        )

    def tap_clear_search(self) -> None:
        """点击点餐搜索框内的清除按钮。"""
        self.tap_xpath(
            self.CLEAR_SEARCH_XPATH,
            "点餐搜索框清除按钮",
        )

    def wait_search_cleared(self, *, timeout: float = 8) -> None:
        """等待搜索词清空且默认分类列表恢复。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            search_input = self.find_xpath(self.SEARCH_INPUT_XPATH)
            default_row = self.find_xpath(self.DEFAULT_FIRST_ROW_XPATH)
            if (
                search_input is not None
                and not search_input.getText().strip()
                and default_row is not None
            ):
                return
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 搜索内容未清空或默认点餐列表未恢复"
        )

    def system_gesture_back(self) -> None:
        """从屏幕右边缘向左侧滑，执行 HarmonyOS 系统返回手势。"""
        self.driver.swipe_to_back(side="RIGHT")
