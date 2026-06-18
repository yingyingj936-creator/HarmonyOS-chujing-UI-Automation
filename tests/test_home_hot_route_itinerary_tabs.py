import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38"


@allure.feature("\u9996\u9875\u70ed\u95e8\u8def\u7ebf")
@allure.story("\u591a\u65e5\u8def\u7ebf\u884c\u7a0b\u89c4\u5212\u5207\u6362")
def test_home_hot_route_itinerary_tabs(driver) -> None:
    """\u9a8c\u8bc1\u591a\u65e5\u8def\u7ebf\u8be6\u60c5\u9875\u884c\u7a0b\u89c4\u5212 tab \u5207\u6362\u3002"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("\u524d\u7f6e\u6761\u4ef6\uff1a\u666e\u901a\u7528\u6237\u8fdb\u5165\u201c\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u201d\u8be6\u60c5\u9875"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)

    with allure.step("\u6b65\u9aa41\uff1a\u67e5\u770b\u884c\u7a0b\u89c4\u5212\u6a21\u5757\uff0c\u9ed8\u8ba4\u5c55\u793a\u5168\u89c8\u8def\u7ebf\u5217\u8868"):
        route_detail.wait_itinerary_tabs(timeout=10)
        route_detail.wait_overview_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "\u5168\u89c8\u8def\u7ebf\u5730\u56fe\u80cc\u666f",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa42\uff1a\u4f9d\u6b21\u70b9\u51fb\u201c\u7b2c1\u5929\u201d\u548c\u201c\u7b2c2\u5929\u201d\uff0c\u6821\u9a8c\u5bf9\u5e94\u5929\u6570\u5217\u8868\u548c\u5730\u56fe\u80cc\u666f"):
        route_detail.tap_day_1_tab(timeout=10)
        route_detail.wait_day_1_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_SELECTED_TAB_XPATH),
            "\u7b2c1\u5929 tab \u5df2\u9009\u4e2d\uff0c\u5730\u56fe\u80cc\u666f\u5df2\u6e32\u67d3",
            timeout=8,
            attach_crop=False,
        )

        route_detail.tap_day_2_tab(timeout=10)
        route_detail.wait_day_2_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_2_SELECTED_TAB_XPATH),
            "\u7b2c2\u5929 tab \u5df2\u9009\u4e2d\uff0c\u5730\u56fe\u80cc\u666f\u5df2\u6e32\u67d3",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa43\uff1a\u5207\u56de\u5168\u89c8\uff0c\u6821\u9a8c\u6062\u590d\u5c55\u793a\u5168\u89c8\u8def\u7ebf\u5217\u8868"):
        route_detail.tap_overview_tab(timeout=10)
        route_detail.wait_overview_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_TITLE_XPATH),
            "\u5207\u56de\u5168\u89c8\u540e\u7684\u7b2c1\u5929\u8def\u7ebf",
            timeout=8,
            attach_crop=False,
        )
