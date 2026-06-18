import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38"


@allure.feature("\u9996\u9875\u70ed\u95e8\u8def\u7ebf")
@allure.story("\u5168\u89c8\u8def\u7ebf\u5361\u7247\u8fdb\u5165\u5355\u65e5\u89c6\u56fe")
def test_home_hot_route_overview_day_card_to_day_view(driver) -> None:
    """\u9a8c\u8bc1\u5168\u89c8 tab \u4e0b\u70b9\u51fb\u7b2c1\u5929\u5361\u7247\u540e\u8fdb\u5165\u7b2c1\u5929\u89c6\u56fe\u3002"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("\u524d\u7f6e\u6761\u4ef6\uff1a\u666e\u901a\u7528\u6237\u8fdb\u5165\u201c\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u201d\u8be6\u60c5\u9875"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)

    with allure.step("\u6b65\u9aa41\uff1a\u67e5\u770b\u201c\u5168\u89c8\u201dtab\u4e0b\u5730\u56fe\u80cc\u666f\uff0c\u6821\u9a8c\u5168\u89c8 tab \u5df2\u9ed8\u8ba4\u9009\u4e2d"):
        route_detail.wait_itinerary_tabs(timeout=10)
        route_detail.wait_xpath(
            route_detail.OVERVIEW_SELECTED_TAB_XPATH,
            "\u5168\u89c8 tab \u9009\u4e2d\u6001",
            timeout=10,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "\u5168\u89c8\u5730\u56fe\u80cc\u666f\uff0c\u5c55\u793a\u6240\u6709\u5929\u6570\u8def\u7ebf",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa42\uff1a\u67e5\u770b\u201c\u5168\u89c8\u201dtab\u4e0b\u5361\u7247\u9648\u5217\uff0c\u6821\u9a8c\u6bcf\u5929\u884c\u7a0b\u6458\u8981\u3001POI\u70b9\u6570\u548c POI \u6761\u76ee"):
        route_detail.wait_overview_day_cards(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_OVERVIEW_CARD_XPATH),
            "\u5168\u89c8\u4e0b\u7b2c1\u5929\u884c\u7a0b\u6458\u8981\u5361\u7247\uff0c\u5305\u542b POI \u70b9\u6570\u548c POI \u6761\u76ee",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa43\uff1a\u70b9\u51fb\u201c\u5168\u89c8\u201dtab\u4e0b\u7b2c1\u5929\u5361\u7247\uff0c\u6821\u9a8c\u7b2c1\u5929 tab \u540c\u6b65\u9ad8\u4eae\u5e76\u8fdb\u5165\u7b2c1\u5929\u89c6\u56fe"):
        route_detail.tap_day_1_overview_card(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_SELECTED_TAB_XPATH),
            "\u70b9\u51fb\u5168\u89c8\u7b2c1\u5929\u5361\u7247\u540e\uff0c\u7b2c1\u5929 tab \u5df2\u9ad8\u4eae",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "\u7b2c1\u5929\u89c6\u56fe\u5730\u56fe\u80cc\u666f",
            timeout=8,
            attach_crop=False,
        )
