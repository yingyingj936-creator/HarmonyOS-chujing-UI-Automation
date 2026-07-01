import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


ROUTE_NAME = "\u9999\u6e2f\u901b\u5403\u4e24\u65e5\u6e38"


@allure.feature("首页热门路线")
@allure.story("热门路线详情浏览")
def test_home_hot_route_detail_browsing(driver) -> None:
    """验证打开热门路线、滑动详情卡片并返回首页。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户已进入首页，且当前目的地下存在热门路线"):
        home.restore_top(max_swipes=12)
        hot_route = home.ensure_hot_route_visible(ROUTE_NAME)
        attach_highlighted_bounds(
            driver,
            hot_route.getBounds(),
            f"首页热门路线：{ROUTE_NAME}",
        )

    with allure.step("步骤1：点击首页热门路线“香港逛吃两日游”，校验详情页概览内容"):
        home.tap_hot_route_card(ROUTE_NAME)
        route_loaded = route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        route_detail.wait_overview_modules(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            route_loaded["map"],
            "路线详情页地图背景",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：向上向下拉动路线详情卡片，校验模块内容可滑动展示"):
        route_detail.scroll_to_warm_tips(max_swipes=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.WARM_TIPS_XPATH),
            "温馨提示模块",
            timeout=8,
            attach_crop=False,
        )
        route_detail.swipe_card_down()
        route_detail.wait_xpath(
            route_detail.BOTTOM_PANEL_XPATH,
            "下滑后的路线详情底部卡片",
            timeout=8,
        )

    with allure.step("步骤3：点击返回键，校验可以回到首页"):
        route_detail.tap_back_button()
        assert home.wait_first_screen_loaded(timeout=10), (
            "点击返回后未回到首页"
        )
        hot_route = home.ensure_hot_route_visible(ROUTE_NAME)
        attach_highlighted_bounds(
            driver,
            hot_route.getBounds(),
            f"返回首页后的热门路线：{ROUTE_NAME}",
        )
