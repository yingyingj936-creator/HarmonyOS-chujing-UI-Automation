import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"


@allure.feature("首页热门路线")
@allure.story("游玩模式路线介绍返回详情")
def test_home_hot_route_play_mode_route_intro_reenter(driver) -> None:
    """验证游玩模式路线介绍可回到路线详情，并能再次进入游玩模式。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户进入“香港逛吃两日游”游玩模式"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH),
            "一键跟玩按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_one_click_play(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_ROUTE_INTRO_XPATH),
            "游玩模式路线介绍按钮",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击右侧“路线介绍”按钮"):
        route_detail.tap_play_mode_route_intro(ROUTE_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.overview_title_xpath(ROUTE_NAME)),
            "路线详情介绍页-路线概览",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看路线介绍页核心内容"):
        route_detail.wait_overview_modules(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ITINERARY_PLANNING_XPATH),
            "路线详情-行程规划",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_JOIN_TRIP_BUTTON_XPATH),
            "路线详情-加入我的行程按钮",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH),
            "路线详情-一键跟玩按钮",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：再次点击“一键跟玩”，进入游玩模式"):
        route_detail.tap_one_click_play(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_TAB_BAR_XPATH),
            "再次进入游玩模式-天数标签",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_LEFT_SIDEBAR_XPATH),
            "再次进入游玩模式-当前路线数据",
            timeout=8,
            attach_crop=False,
        )

