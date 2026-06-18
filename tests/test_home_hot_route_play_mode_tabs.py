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
@allure.story("\u591a\u65e5\u8def\u7ebf\u6e38\u73a9\u6a21\u5f0f tab \u5207\u6362")
def test_home_hot_route_play_mode_tabs_and_day_bubble(driver) -> None:
    """\u9a8c\u8bc1\u6e38\u73a9\u6a21\u5f0f\u4e0b\u5168\u89c8\u3001Day1\u3001Day2 \u5207\u6362\u548c\u5730\u56fe\u6c14\u6ce1\u70b9\u51fb\u3002"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("\u524d\u7f6e\u6761\u4ef6\uff1a\u666e\u901a\u7528\u6237\u5df2\u8fdb\u5165\u201c\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u201d\u8def\u7ebf\u8be6\u60c5\u9875"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.overview_title_xpath(ROUTE_NAME)),
            "\u8def\u7ebf\u8be6\u60c5\u9875\u6982\u89c8\u5361\u7247",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa41\uff1a\u8fdb\u5165\u6e38\u73a9\u6a21\u5f0f\uff0c\u9a8c\u8bc1\u534a\u7a97\u5df2\u6536\u8d77\u5e76\u5c55\u793a\u5168\u89c8\u5730\u56fe"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH),
            "\u8def\u7ebf\u8be6\u60c5\u9875\u4e00\u952e\u8ddf\u73a9\u6309\u94ae",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_one_click_play(timeout=12)
        route_detail.wait_play_mode_overview(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_TAB_BAR_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5168\u89c8 tab \u533a",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_1_BUBBLE_BOUNDS,
            "\u5168\u89c8\u5730\u56fe\u7b2c1\u5929\u8def\u7ebf\u5361\u7247",
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_2_BUBBLE_BOUNDS,
            "\u5168\u89c8\u5730\u56fe\u7b2c2\u5929\u8def\u7ebf\u5361\u7247",
        )

    with allure.step("\u6b65\u9aa42\uff1a\u70b9\u51fb\u201c\u7b2c1\u5929\u201dTab\uff0c\u9a8c\u8bc1 Day1 \u8def\u7ebf\u548c\u5e95\u90e8\u884c\u7a0b\u62bd\u5c49\u540c\u6b65\u5c55\u793a"):
        route_detail.tap_play_mode_day_1_tab(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_DAY_1_TAB_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u7b2c1\u5929 tab",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "\u7b2c1\u5929\u5e95\u90e8\u884c\u7a0b\u62bd\u5c49",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "\u7b2c1\u5929 POI \u6c14\u6ce1\u548c\u8def\u7ebf\u533a\u57df",
        )

    with allure.step("\u6b65\u9aa43\uff1a\u70b9\u51fb\u201c\u7b2c2\u5929\u201dTab\uff0c\u9a8c\u8bc1 Day2 \u8def\u7ebf\u548c\u5e95\u90e8\u884c\u7a0b\u62bd\u5c49\u540c\u6b65\u5c55\u793a"):
        route_detail.tap_play_mode_day_2_tab(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_DAY_2_TAB_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u7b2c2\u5929 tab",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "\u7b2c2\u5929\u5e95\u90e8\u884c\u7a0b\u62bd\u5c49",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "\u7b2c2\u5929 POI \u6c14\u6ce1\u548c\u8def\u7ebf\u533a\u57df",
        )

    with allure.step("\u6b65\u9aa44\uff1a\u70b9\u51fb\u201c\u5168\u89c8\u201dTab\uff0c\u9a8c\u8bc1\u6062\u590d\u5168\u90e8\u5929\u6570\u8def\u7ebf\u548c\u5929\u6570\u5361\u7247"):
        route_detail.tap_play_mode_overview_tab(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_OVERVIEW_TAB_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5168\u89c8 tab",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_1_BUBBLE_BOUNDS,
            "\u5168\u89c8\u4e0b\u7b2c1\u5929\u8def\u7ebf\u5361\u7247",
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_2_BUBBLE_BOUNDS,
            "\u5168\u89c8\u4e0b\u7b2c2\u5929\u8def\u7ebf\u5361\u7247",
        )

    with allure.step("\u6b65\u9aa45\uff1a\u5168\u89c8 tab \u4e0b\u70b9\u51fb\u7b2c1\u5929\u6c14\u6ce1\uff0c\u9a8c\u8bc1\u5c55\u793a Day1 \u6570\u636e"):
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_1_BUBBLE_BOUNDS,
            "\u70b9\u51fb\u524d\u7684\u7b2c1\u5929\u6c14\u6ce1",
        )
        route_detail.tap_play_mode_day_1_bubble(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_DAY_1_TAB_XPATH),
            "\u70b9\u51fb\u7b2c1\u5929\u6c14\u6ce1\u540e\u7684 Day1 tab",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "\u70b9\u51fb\u7b2c1\u5929\u6c14\u6ce1\u540e\u7684\u5e95\u90e8\u884c\u7a0b\u62bd\u5c49",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "\u70b9\u51fb\u7b2c1\u5929\u6c14\u6ce1\u540e\u7684 Day1 \u8def\u7ebf\u533a\u57df",
        )
