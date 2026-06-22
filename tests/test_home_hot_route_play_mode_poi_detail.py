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
@allure.story("游玩模式单天地点气泡和行程轴详情")
def test_home_hot_route_play_mode_day_poi_detail(driver) -> None:
    """验证游玩模式单天标签下地图气泡和底部行程轴可打开地点详情。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：进入“香港逛吃两日游”游玩模式第1天标签"):
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
            "第1天底部行程轴",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击地图上编号为2的地点气泡"):
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_POI_2_BUBBLE_BOUNDS,
            "点击前的地图2号地点气泡区域",
        )
        route_detail.tap_play_mode_poi_2_bubble(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.play_mode_poi_title_xpath(route_detail.PLAY_MODE_POI_2_NAME)),
            "地图2号地点详情标题",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_ROOT_XPATH),
            "地图2号地点底部详情卡片",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击地点详情叉号，回到游玩模式全屏"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_CLOSE_XPATH),
            "游玩模式地点详情关闭按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.close_play_mode_poi_detail(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "关闭地点详情后的游玩模式地图",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_BOTTOM_DRAWER_XPATH),
            "关闭 POI 详情后的底部行程轴",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_POI_2_BUBBLE_BOUNDS,
            "关闭后2号 POI 高亮取消区域",
        )

    with allure.step("步骤3：点击底部行程轴编号为3的地点"):
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_AXIS_POI_3_BOUNDS,
            "点击前的底部行程轴3号地点",
        )
        route_detail.tap_play_mode_axis_poi_3(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.play_mode_poi_title_xpath(route_detail.PLAY_MODE_POI_3_NAME)),
            "底部行程轴3号 POI 详情标题",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_ROOT_XPATH),
            "底部行程轴3号 POI 详情卡片",
            timeout=8,
            attach_crop=False,
        )

