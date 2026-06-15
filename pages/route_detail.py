from pages.base_page import BasePage


class RouteDetailPage(BasePage):
    """搜索结果中的路线详情页。"""

    PAGE_NAME = "RouteDetailPage"
    OVERVIEW_TITLE_XPATH_TEMPLATE = '//Text[@text="{route_name}·概览"]'
    BACK_BUTTON_XPATH = (
        '//*[@id="mapPageRoot"]//Row[@clickable="true" and ./Image]'
    )

    @classmethod
    def overview_title_xpath(cls, route_name: str) -> str:
        return cls.OVERVIEW_TITLE_XPATH_TEMPLATE.format(
            route_name=route_name,
        )

    def tap_back_button(self) -> None:
        """点击路线详情页左上角页面内返回按钮。"""
        self.tap_xpath(self.BACK_BUTTON_XPATH, "路线详情页返回按钮")
