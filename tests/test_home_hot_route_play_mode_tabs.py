import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


ROUTE_NAME = "香港逛吃两日游"


@allure.feature("首页热门路线")
@allure.story("多日路线游玩模式标签切换")
def test_home_hot_route_play_mode_tabs_and_day_bubble(driver) -> None:
    """验证游玩模式下全览、第1天、第2天切换和地图气泡点击。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户已进入“香港逛吃两日游”路线详情页"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.overview_title_xpath(ROUTE_NAME)),
            "路线详情页概览卡片",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：进入游玩模式，验证半窗已收起并展示全览地图"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_ONE_CLICK_PLAY_BUTTON_XPATH),
            "路线详情页一键跟玩按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_one_click_play(timeout=12)
        route_detail.wait_play_mode_overview(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_TAB_BAR_XPATH),
            "游玩模式全览标签区",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_1_BUBBLE_BOUNDS,
            "全览地图第1天路线卡片",
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_2_BUBBLE_BOUNDS,
            "全览地图第2天路线卡片",
        )

    with allure.step("步骤2：点击“第1天”标签，验证第1天路线和底部行程抽屉同步展示"):
        route_detail.tap_play_mode_day_1_tab(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_DAY_1_TAB_XPATH),
            "游玩模式第1天标签",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "第1天底部行程抽屉",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "第1天地点气泡和路线区域",
        )

    with allure.step("步骤3：点击“第2天”标签，验证第2天路线和底部行程抽屉同步展示"):
        route_detail.tap_play_mode_day_2_tab(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_DAY_2_TAB_XPATH),
            "游玩模式第2天标签",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "第2天底部行程抽屉",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "第2天地点气泡和路线区域",
        )

    with allure.step("步骤4：点击“全览”标签，验证恢复全部天数路线和天数卡片"):
        route_detail.tap_play_mode_overview_tab(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_OVERVIEW_TAB_XPATH),
            "游玩模式全览标签",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_1_BUBBLE_BOUNDS,
            "全览下第1天路线卡片",
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_2_BUBBLE_BOUNDS,
            "全览下第2天路线卡片",
        )

    with allure.step("步骤5：全览标签下点击第1天气泡，验证展示第1天数据"):
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_1_BUBBLE_BOUNDS,
            "点击前的第1天气泡",
        )
        route_detail.tap_play_mode_day_1_bubble(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_DAY_1_TAB_XPATH),
            "点击第1天气泡后的第1天标签",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "点击第1天气泡后的底部行程抽屉",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "点击第1天气泡后的第1天路线区域",
        )



