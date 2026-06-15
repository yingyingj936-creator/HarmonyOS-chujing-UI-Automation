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
