import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38"


@allure.feature("\u9996\u9875\u70ed\u95e8\u8def\u7ebf")
@allure.story("\u70ed\u95e8\u8def\u7ebf\u4e00\u952e\u8ddf\u73a9\u6e38\u73a9\u6a21\u5f0f")
def test_home_hot_route_one_click_play_mode(driver) -> None:
    """\u9a8c\u8bc1\u70ed\u95e8\u8def\u7ebf\u8be6\u60c5\u9875\u53ef\u8fdb\u5165\u5e76\u9000\u51fa\u6e38\u73a9\u6a21\u5f0f\u3002"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("\u524d\u7f6e\u6761\u4ef6\uff1a\u666e\u901a\u7528\u6237\u5df2\u8fdb\u5165\u201c\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u201d\u8def\u7ebf\u8be6\u60c5\u9875"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.overview_title_xpath(ROUTE_NAME)),
            "\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u8be6\u60c5\u9875",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa41\uff1a\u70b9\u51fb\u8be6\u60c5\u9875\u201c\u4e00\u952e\u8ddf\u73a9\u201d\u6309\u94ae"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH),
            "\u4e00\u952e\u8ddf\u73a9\u6309\u94ae",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_one_click_play(timeout=10)

    with allure.step("\u6b65\u9aa42\uff1a\u67e5\u770b\u6e38\u73a9\u6a21\u5f0f\u5168\u89c8\u89c6\u56fe\u548c\u5173\u952e\u63a7\u4ef6"):
        route_detail.wait_play_mode_overview(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5730\u56fe\u5168\u89c8",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_TAB_BAR_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5168\u89c8-\u7b2c1\u5929-\u7b2c2\u5929 tab",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_LEFT_SIDEBAR_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5de6\u4e0b\u89d2\u4fa7\u8fb9\u680f",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_EDIT_ROUTE_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u7f16\u8f91\u8def\u7ebf\u5165\u53e3",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_ROUTE_INTRO_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u8def\u7ebf\u4ecb\u7ecd\u5165\u53e3",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_LOCATION_BUTTON_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5b9a\u4f4d\u6309\u94ae",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa43\uff1a\u70b9\u51fb\u9875\u9762\u5185\u53c9\u53f7\uff0c\u9000\u51fa\u6e38\u73a9\u6a21\u5f0f"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_EXIT_BUTTON_XPATH),
            "\u9000\u51fa\u6e38\u73a9\u6a21\u5f0f\u53c9\u53f7",
            timeout=8,
            attach_crop=False,
        )
        route_detail.exit_play_mode(ROUTE_NAME, timeout=10)

    with allure.step("\u6b65\u9aa44\uff1a\u9000\u51fa\u540e\u6062\u590d\u8def\u7ebf\u534a\u6a21\u6001\u5361\u7247\u548c\u5f53\u524d\u8def\u7ebf\u62bd\u5c49"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.BOTTOM_PANEL_XPATH),
            "\u9000\u51fa\u540e\u7684\u8def\u7ebf\u534a\u6a21\u6001\u5361\u7247",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_OVERVIEW_CARD_XPATH),
            "\u9000\u51fa\u540e\u7684\u5f53\u524d\u8def\u7ebf POI \u62bd\u5c49",
            timeout=8,
            attach_crop=False,
        )
