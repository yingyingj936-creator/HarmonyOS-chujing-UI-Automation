import time

import allure
import pytest
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.route_detail import RouteDetailPage
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


TRIP_NAME = "香港逛吃两日游"


@allure.feature("行程管理")
@allure.story("我的行程详情查看地图进入游玩模式")
def test_trip_detail_view_map_play_mode_tabs_and_exit(driver) -> None:
    """验证从我的行程详情点击查看地图后，可进入游玩模式、切换天数标签并退出回详情页。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户已登录，进入我的行程详情页"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        try:
            trip_manager.scroll_trip_into_view(TRIP_NAME, max_swipes=10)
        except RuntimeError as exc:
            visible_titles = [
                title
                for _, title in trip_manager.current_visible_trip_cards_with_titles()
            ]
            pytest.fail(
                f"前置条件不满足：我的行程列表未找到“{TRIP_NAME}”。"
                f"当前可见行程={visible_titles}；原始错误={exc}"
            )

        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.trip_card_xpath(TRIP_NAME)),
            f"我的行程列表-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
        trip_manager.tap_trip(TRIP_NAME)
        trip_loaded = trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            trip_loaded["title"],
            f"我的行程详情页-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击“查看地图”，进入游玩模式并校验地图渲染"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.VIEW_MAP_BUTTON_XPATH),
            "行程详情查看地图按钮",
            timeout=8,
            attach_crop=False,
        )
        trip_detail.tap_view_map(timeout=10)
        route_detail.wait_xpath(
            route_detail.ROOT_XPATH,
            "游玩模式地图页根节点",
            timeout=15,
        )
        map_view = route_detail.wait_xpath(
            route_detail.MAP_VIEW_XPATH,
            "游玩模式地图背景",
            timeout=15,
        )
        tab_bar = route_detail.wait_xpath(
            route_detail.PLAY_MODE_TAB_BAR_XPATH,
            "游玩模式天数标签栏",
            timeout=15,
        )
        route_detail.wait_xpath(
            route_detail.PLAY_MODE_OVERVIEW_TAB_XPATH,
            "游玩模式全览标签",
            timeout=15,
        )
        route_detail.wait_xpath(
            route_detail.PLAY_MODE_DAY_1_TAB_XPATH,
            "游玩模式第1天标签",
            timeout=15,
        )
        route_detail.wait_xpath(
            route_detail.PLAY_MODE_DAY_2_TAB_XPATH,
            "游玩模式第2天标签",
            timeout=15,
        )
        attach_highlighted_bounds(
            driver,
            map_view.getBounds(),
            "游玩模式地图背景",
        )
        attach_highlighted_bounds(
            driver,
            tab_bar.getBounds(),
            "游玩模式全览和天数标签",
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_1_BUBBLE_BOUNDS,
            "游玩模式全览地图第1天路线气泡",
        )

    with allure.step("步骤2：点击切换 tab，校验对应地图和底部行程抽屉渲染成功"):
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
            "游玩模式第1天底部行程抽屉",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "游玩模式第1天地点气泡和路线区域",
        )

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
            "游玩模式第2天底部行程抽屉",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            route_detail.PLAY_MODE_DAY_ROUTE_AREA_BOUNDS,
            "游玩模式第2天地点气泡和路线区域",
        )

    with allure.step("步骤3：退出游玩模式，校验回到我的行程详情页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.PLAY_MODE_EXIT_BUTTON_XPATH),
            "游玩模式退出按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_play_mode_exit_button(timeout=8)
        # 详情页节点可能仍保留在页面栈中，等待退出动画完成后再校验返回状态。
        time.sleep(1.2)
        trip_detail.wait_returned_from_play_mode(TRIP_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(TRIP_NAME)),
            f"退出游玩模式后回到行程详情页-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.VIEW_MAP_BUTTON_XPATH),
            "回到详情页后的查看地图按钮",
            timeout=8,
            attach_crop=False,
        )
