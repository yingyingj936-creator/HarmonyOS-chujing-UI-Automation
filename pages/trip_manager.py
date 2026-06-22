import time

from pages.base_page import BasePage


class TripManagerPage(BasePage):
    PAGE_NAME = "TripManagerPage"
    TRIP_LIST_XPATH = '//List[@scrollable="true"]'

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
    def trip_card_xpath(cls, trip_name: str) -> str:
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'

    @classmethod
    def route_trip_card_title_xpath(cls, trip_name: str) -> str:
        return f'//Text[{cls._display_name_xpath_condition(trip_name)}]'

    @classmethod
    def route_trip_card_summary_xpath(cls, trip_name: str) -> str:
        return (
            f'//List[@scrollable="true"]//*[.//Text[{cls._display_name_xpath_condition(trip_name)}] '
            'and .//Text[contains(@text, "2") and contains(@text, "天")] '
            'and .//Text[contains(@text, "14")]]'
        )

    def tap_trip(self, trip_name: str) -> None:
        """点击我的行程列表中的指定行程。"""
        self.tap_xpath(self.trip_card_xpath(trip_name), f"行程“{trip_name}”")

    def pull_to_refresh(self) -> None:
        """在我的行程列表内执行下拉刷新。"""
        trip_list = self.wait_xpath(
            self.TRIP_LIST_XPATH,
            "我的行程列表",
        )
        self.driver.swipe(
            "DOWN",
            distance=45,
            area=trip_list,
            start_point=(0.5, 0.3),
        )
        time.sleep(2)

