from hypium import BY

from pages.base_page import BasePage


class TripDetailPage(BasePage):
    PAGE_NAME = "TripDetailPage"
    ROOT_XPATH = '//*[@id="planPageRoot"]'
    BACK_BUTTON_XPATH = '//*[@id="planPageRoot"]/Column[1]/Row[1]/Row[1]'
    FIRST_UNPLANNED_POI_XPATH_TEMPLATE = (
        '//*[@id="firstUnplannedPoi"]//Text[@text="{poi_name}"]'
    )
    ROUTE_POI_XPATH_TEMPLATE = (
        '//*[@id="planPageRoot"]//Text[@text="{poi_name}" '
        'or contains(@text, "{poi_name}")]'
    )
    SECOND_UNPLANNED_POI_XPATH_TEMPLATE = (
        '//*[@id="unplannedPoi_1"]//Text[@text="{poi_name}"]'
    )
    ROUTE_DAY_1_XPATH = (
        '//*[@id="planPageRoot"]//Text[@text="第 1 天" or @text="第1天" or @text="Day1"]'
    )
    ROUTE_DAY_2_XPATH = (
        '//*[@id="planPageRoot"]//Text[@text="第 2 天" or @text="第2天" or @text="Day2"]'
    )
    ROUTE_FIRST_POI_XPATH = '//*[@id="planPageRoot"]//Text[@text="通菜街"]'
    ROUTE_POI_COUNT_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "14") '
        'and (contains(@text, "地点") or contains(@text, "个"))]'
    )
    ANY_ROUTE_DAY_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "第") '
        'and contains(@text, "天")]'
    )
    ANY_ROUTE_POI_COUNT_XPATH = (
        '//*[@id="planPageRoot"]//Text[contains(@text, "地点") '
        'or contains(@text, "个")]'
    )
    ROOT_TEXT_XPATH = '//*[@id="planPageRoot"]//Text'

    @staticmethod
    def _display_name_xpath_condition(trip_name: str) -> str:
        names = []
        for name in (trip_name, trip_name.replace("-", "")):
            if name and name not in names:
                names.append(name)

        conditions = []
        for name in names:
            conditions.append(f'@text="{name}"')
            conditions.append(f'contains(@text, "{name}")')
            conditions.append(
                f'(string-length(@text) > 4 and contains("{name}", @text))'
            )
        return " or ".join(conditions)

    @classmethod
    def route_trip_title_xpath(cls, trip_name: str) -> str:
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'
    @classmethod
    def title_xpath(cls, trip_name: str) -> str:
        return (
            f'//*[@id="routeName"]/Text'
            f'[{cls._display_name_xpath_condition(trip_name)}]'
        )

    @classmethod
    def first_unplanned_poi_xpath(cls, poi_name: str) -> str:
        return cls.FIRST_UNPLANNED_POI_XPATH_TEMPLATE.format(poi_name=poi_name)

    @classmethod
    def route_poi_xpath(cls, poi_name: str) -> str:
        return cls.ROUTE_POI_XPATH_TEMPLATE.format(poi_name=poi_name)

    @classmethod
    def second_unplanned_poi_xpath(cls, poi_name: str) -> str:
        return cls.SECOND_UNPLANNED_POI_XPATH_TEMPLATE.format(poi_name=poi_name)

    def tap_back_button(self) -> None:
        """点击行程详情页顶部栏的页面内返回按钮。"""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "页面内返回按钮")

    def wait_route_trip_detail(self, trip_name: str, *, timeout: float = 8) -> None:
        """Verify a route-created trip detail page exposes title and route data."""
        self.wait_xpath(self.route_trip_title_xpath(trip_name), "route trip detail title", timeout=timeout)
        self.wait_xpath(self.ROUTE_DAY_1_XPATH, "route trip day 1", timeout=timeout)
        self.wait_xpath(self.ROUTE_DAY_2_XPATH, "route trip day 2", timeout=timeout)
        self.wait_xpath(self.ROUTE_FIRST_POI_XPATH, "route trip first day POI", timeout=timeout)

    def wait_generic_route_trip_detail(
        self,
        trip_name: str,
        *,
        poi_name: str | None = None,
        timeout: float = 8,
    ) -> None:
        """等待任意路线创建的行程详情页展示标题和路线地点数据。"""
        self.wait_xpath(
            self.ROOT_XPATH,
            "行程详情根节点",
            timeout=timeout,
        )
        self.wait_xpath(
            self.route_trip_title_xpath(trip_name),
            "行程详情标题",
            timeout=timeout,
        )
        if poi_name is not None:
            self.wait_xpath(
                self.route_poi_xpath(poi_name),
                f"行程详情路线POI{poi_name}",
                timeout=timeout,
            )

    def visible_texts(self) -> list[str]:
        """读取当前行程详情页暴露出的文本，用于诊断和报告附件。"""
        components = self.driver.find_all_components(BY.xpath(self.ROOT_TEXT_XPATH))
        if not components:
            return []

        texts: list[str] = []
        for component in components:
            properties = component.getAllProperties().to_dict()
            text = properties.get("text")
            if text and text not in texts:
                texts.append(text)
        return texts
