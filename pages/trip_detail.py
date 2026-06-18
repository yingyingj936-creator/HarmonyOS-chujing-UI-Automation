from pages.base_page import BasePage


class TripDetailPage(BasePage):
    PAGE_NAME = "TripDetailPage"
    BACK_BUTTON_XPATH = '//*[@id="planPageRoot"]/Column[1]/Row[1]/Row[1]'
    TITLE_XPATH_TEMPLATE = '//*[@id="routeName"]/Text[@text="{trip_name}"]'
    FIRST_UNPLANNED_POI_XPATH_TEMPLATE = (
        '//*[@id="firstUnplannedPoi"]//Text[@text="{poi_name}"]'
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

    @staticmethod
    def _display_name_xpath_condition(trip_name: str) -> str:
        displayed_name = trip_name.replace("-", "")
        if displayed_name == trip_name:
            return f'@text="{trip_name}"'
        return f'@text="{trip_name}" or @text="{displayed_name}"'

    @classmethod
    def route_trip_title_xpath(cls, trip_name: str) -> str:
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'
    @classmethod
    def title_xpath(cls, trip_name: str) -> str:
        return cls.TITLE_XPATH_TEMPLATE.format(trip_name=trip_name)

    @classmethod
    def first_unplanned_poi_xpath(cls, poi_name: str) -> str:
        return cls.FIRST_UNPLANNED_POI_XPATH_TEMPLATE.format(poi_name=poi_name)

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
