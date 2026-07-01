import allure
import pytest
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_detail import TripDetailPage
from pages.trip_edit import TripEditPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


TRIP_NAME = "香港逛吃两日游"


@allure.feature("行程管理")
@allure.story("行程详情进入编辑行程页")
def test_trip_detail_edit_page_layout_and_back(driver) -> None:
    """验证从我的行程详情页进入编辑行程页后，编辑页核心布局展示完整，并可返回详情页。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：普通用户已登录，进入“香港逛吃两日游”行程详情页"):
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
            f"行程详情页标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击底部“编辑行程”按钮，校验进入编辑行程页成功"):
        edit_button = trip_detail.scroll_until_xpath_visible(
            trip_detail.EDIT_TRIP_BUTTON_XPATH,
            "编辑行程按钮",
            max_swipes=8,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            edit_button.getBounds(),
            "行程详情页底部编辑行程按钮",
        )
        edit_button.click()
        trip_edit.wait_ready(timeout=12)
        title = trip_edit.wait_xpath(
            trip_edit.TITLE_XPATH,
            "编辑行程页标题",
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            title.getBounds(),
            "编辑行程页标题",
        )

    with allure.step("步骤2：查看编辑页顶部地图、半卡片Tab、待规划、新增入口和全览路线列表"):
        tab_bar = trip_edit.wait_tabs_ready(timeout=8)
        trip_edit.wait_add_entry(timeout=8)
        trip_edit.wait_route_overview_ready(timeout=10)
        attach_highlighted_bounds(
            driver,
            tab_bar.getBounds(),
            "编辑行程页Tab及全览路线区域",
        )

    with allure.step("步骤3：点击返回键，校验返回“香港逛吃两日游”行程详情页"):
        back_button = trip_edit.back_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            back_button.getBounds(),
            "编辑行程页返回键",
        )
        back_button.click()
        returned_trip = trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            returned_trip["title"],
            f"返回后的行程详情页标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
