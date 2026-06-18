import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


ROUTE_NAME = "\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38"


@allure.feature("\u9996\u9875\u70ed\u95e8\u8def\u7ebf")
@allure.story("\u6e38\u73a9\u6a21\u5f0f\u5b9a\u4f4d\u6309\u94ae")
def test_home_hot_route_play_mode_location_toggle(driver) -> None:
    """\u9a8c\u8bc1\u6e38\u73a9\u6a21\u5f0f\u4e0b\u5b9a\u4f4d\u6309\u94ae\u53ef\u89e6\u53d1\uff0c\u518d\u6b21\u70b9\u51fb\u53ef\u56de\u5230\u8def\u7ebf\u5c55\u793a\u3002"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("\u524d\u7f6e\u6761\u4ef6\uff1a\u666e\u901a\u7528\u6237\u8fdb\u5165\u201c\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u201d\u6e38\u73a9\u6a21\u5f0f\u7b2c1\u5929\u8def\u7ebf\u5c55\u793a"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH),
            "\u4e00\u952e\u8ddf\u73a9\u6309\u94ae",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_one_click_play(timeout=12)
        route_detail.tap_play_mode_day_1_tab(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_LOCATION_BUTTON_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5b9a\u4f4d\u6309\u94ae",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "\u5b9a\u4f4d\u524d\u7684\u7b2c1\u5929\u5e95\u90e8\u884c\u7a0b\u62bd\u5c49",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "\u5b9a\u4f4d\u524d\u7684\u7b2c1\u5929\u8def\u7ebf\u5c55\u793a\u533a\u57df",
        )

    with allure.step("\u6b65\u9aa41\uff1a\u70b9\u51fb\u5730\u56fe\u53f3\u4fa7\u5b9a\u4f4d\u6309\u94ae"):
        route_detail.tap_play_mode_location_button(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "\u9996\u6b21\u70b9\u51fb\u5b9a\u4f4d\u540e\u7684\u5730\u56fe\u533a\u57df",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_LOCATION_BUTTON_BOUNDS,
            "\u9996\u6b21\u70b9\u51fb\u540e\u53f3\u4e0b\u89d2\u5b9a\u4f4d\u6309\u94ae\u533a\u57df",
        )

    with allure.step("\u6b65\u9aa42\uff1a\u518d\u6b21\u70b9\u51fb\u5b9a\u4f4d\u6309\u94ae\uff0c\u56de\u5230\u8def\u7ebf\u5c55\u793a"):
        route_detail.tap_play_mode_location_button(timeout=10)
        route_detail.wait_play_mode_map_and_drawer(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "\u518d\u6b21\u70b9\u51fb\u5b9a\u4f4d\u540e\u7684\u5e95\u90e8\u884c\u7a0b\u62bd\u5c49",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "\u518d\u6b21\u70b9\u51fb\u5b9a\u4f4d\u540e\u56de\u5230\u8def\u7ebf\u5c55\u793a\u533a\u57df",
        )
