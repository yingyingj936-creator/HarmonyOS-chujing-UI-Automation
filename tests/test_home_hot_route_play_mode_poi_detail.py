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
@allure.story("\u6e38\u73a9\u6a21\u5f0f\u5355\u5929 POI \u6c14\u6ce1\u548c\u884c\u7a0b\u8f74\u8be6\u60c5")
def test_home_hot_route_play_mode_day_poi_detail(driver) -> None:
    """\u9a8c\u8bc1\u6e38\u73a9\u6a21\u5f0f\u5355\u5929 tab \u4e0b\u5730\u56fe\u6c14\u6ce1\u548c\u5e95\u90e8\u884c\u7a0b\u8f74\u53ef\u6253\u5f00 POI \u8be6\u60c5\u3002"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("\u524d\u7f6e\u6761\u4ef6\uff1a\u8fdb\u5165\u201c\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u201d\u6e38\u73a9\u6a21\u5f0f\u7b2c1\u5929 tab"):
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
            BY.xpath(route_detail.PLAY_MODE_DAY_1_TAB_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u7b2c1\u5929 tab",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "\u7b2c1\u5929\u5e95\u90e8\u884c\u7a0b\u8f74",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa41\uff1a\u70b9\u51fb\u5730\u56fe\u4e0a\u7f16\u53f7\u4e3a2\u7684 POI \u6c14\u6ce1"):
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_POI_2_BUBBLE_BOUNDS,
            "\u70b9\u51fb\u524d\u7684\u5730\u56fe2\u53f7 POI \u6c14\u6ce1\u533a\u57df",
        )
        route_detail.tap_play_mode_poi_2_bubble(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.play_mode_poi_title_xpath(route_detail.PLAY_MODE_POI_2_NAME)),
            "\u5730\u56fe2\u53f7 POI \u8be6\u60c5\u6807\u9898",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_ROOT_XPATH),
            "\u5730\u56fe2\u53f7 POI \u5e95\u90e8\u8be6\u60c5\u5361\u7247",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa42\uff1a\u70b9\u51fb POI \u8be6\u60c5\u53c9\u53f7\uff0c\u56de\u5230\u6e38\u73a9\u6a21\u5f0f\u5168\u5c4f"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_CLOSE_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f POI \u8be6\u60c5\u5173\u95ed\u6309\u94ae",
            timeout=8,
            attach_crop=False,
        )
        route_detail.close_play_mode_poi_detail(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "\u5173\u95ed POI \u8be6\u60c5\u540e\u7684\u6e38\u73a9\u6a21\u5f0f\u5730\u56fe",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "\u5173\u95ed POI \u8be6\u60c5\u540e\u7684\u5e95\u90e8\u884c\u7a0b\u8f74",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_POI_2_BUBBLE_BOUNDS,
            "\u5173\u95ed\u540e2\u53f7 POI \u9ad8\u4eae\u53d6\u6d88\u533a\u57df",
        )

    with allure.step("\u6b65\u9aa43\uff1a\u70b9\u51fb\u5e95\u90e8\u884c\u7a0b\u8f74\u7f16\u53f7\u4e3a3\u7684\u5730\u70b9"):
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_AXIS_POI_3_BOUNDS,
            "\u70b9\u51fb\u524d\u7684\u5e95\u90e8\u884c\u7a0b\u8f743\u53f7\u5730\u70b9",
        )
        route_detail.tap_play_mode_axis_poi_3(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.play_mode_poi_title_xpath(route_detail.PLAY_MODE_POI_3_NAME)),
            "\u5e95\u90e8\u884c\u7a0b\u8f743\u53f7 POI \u8be6\u60c5\u6807\u9898",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_ROOT_XPATH),
            "\u5e95\u90e8\u884c\u7a0b\u8f743\u53f7 POI \u8be6\u60c5\u5361\u7247",
            timeout=8,
            attach_crop=False,
        )
