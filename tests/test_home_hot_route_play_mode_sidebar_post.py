import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.post_detail import PostDetailPage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38"


@allure.feature("\u9996\u9875\u70ed\u95e8\u8def\u7ebf")
@allure.story("\u6e38\u73a9\u6a21\u5f0f\u5de6\u4fa7\u4fa7\u8fb9\u680f\u5e16\u5b50")
def test_home_hot_route_play_mode_sidebar_post_return(driver) -> None:
    """\u9a8c\u8bc1\u6e38\u73a9\u6a21\u5f0f\u5de6\u4fa7\u4fa7\u8fb9\u680f\u5185\u5bb9\u4f4d\u53ef\u6253\u5f00\u5e16\u5b50\u8be6\u60c5\u5e76\u8fd4\u56de\u6e38\u73a9\u6a21\u5f0f\u3002"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)
    post_detail = PostDetailPage(driver)

    with allure.step("\u524d\u7f6e\u6761\u4ef6\uff1a\u666e\u901a\u7528\u6237\u8fdb\u5165\u201c\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38\u201d\u6e38\u73a9\u6a21\u5f0f"):
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
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_LEFT_SIDEBAR_XPATH),
            "\u6e38\u73a9\u6a21\u5f0f\u5de6\u4fa7\u4fa7\u8fb9\u680f\u5185\u5bb9\u4f4d",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa41\uff1a\u70b9\u51fb\u5de6\u4fa7\u4fa7\u8fb9\u680f\u5185\u5bb9\u4f4d\uff0c\u62c9\u8d77\u5bf9\u5e94\u5e16\u5b50\u8be6\u60c5"):
        route_detail.tap_play_mode_left_sidebar_content(timeout=10)
        post_detail.wait_loaded(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(post_detail.ROOT_XPATH),
            "\u4fa7\u8fb9\u680f\u5bf9\u5e94\u5e16\u5b50\u8be6\u60c5",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            post_detail.back_button(timeout=8),
            "\u5e16\u5b50\u8be6\u60c5\u9875\u8fd4\u56de\u6309\u94ae",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("\u6b65\u9aa42\uff1a\u70b9\u51fb\u8fd4\u56de\uff0c\u56de\u5230\u6e38\u73a9\u6a21\u5f0f"):
        post_detail.tap_back_button()
        route_detail.wait_play_mode_overview(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "\u8fd4\u56de\u540e\u6e38\u73a9\u6a21\u5f0f\u5730\u56fe",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_LEFT_SIDEBAR_XPATH),
            "\u8fd4\u56de\u540e\u6e38\u73a9\u6a21\u5f0f\u5de6\u4fa7\u4fa7\u8fb9\u680f",
            timeout=8,
            attach_crop=False,
        )
