import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"


@allure.feature("首页热门路线")
@allure.story("热门路线一键跟玩游玩模式")
def test_home_hot_route_one_click_play_mode(driver) -> None:
    """验证热门路线详情页可进入并退出游玩模式。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户已进入“香港逛吃两日游”路线详情页"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_loaded = route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            route_loaded["overview_title"],
            "香港逛吃两日游详情页",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击详情页“一键跟玩”按钮"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH),
            "一键跟玩按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_one_click_play(timeout=10)

    with allure.step("步骤2：查看游玩模式全览视图和关键控件"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "游玩模式地图全览",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击页面内叉号，退出游玩模式"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_EXIT_BUTTON_XPATH),
            "退出游玩模式叉号",
            timeout=8,
            attach_crop=False,
        )
        route_detail.exit_play_mode(ROUTE_NAME, timeout=10)

    with allure.step("步骤4：退出后恢复路线半模态卡片和当前路线抽屉"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.BOTTOM_PANEL_XPATH),
            "退出后的路线半模态卡片",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_OVERVIEW_CARD_XPATH),
            "退出后的当前路线 POI 抽屉",
            timeout=8,
            attach_crop=False,
        )

