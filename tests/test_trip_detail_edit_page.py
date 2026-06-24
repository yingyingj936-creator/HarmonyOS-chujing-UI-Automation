import time

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
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(TRIP_NAME)),
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
        time.sleep(1.2)

        trip_edit.wait_loaded(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.TITLE_XPATH),
            "编辑行程页标题",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看编辑页顶部地图、半卡片Tab、待规划、新增入口和全览路线列表"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.MAP_VIEW_XPATH),
            "编辑行程页顶部地图路线区域",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.TAB_BAR_XPATH),
            "编辑行程页半卡片Tab区域",
            timeout=8,
            attach_crop=False,
        )
        trip_edit.wait_tabs_loaded(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.OVERVIEW_TAB_XPATH),
            "编辑行程页Tab-全览",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_1_TAB_XPATH),
            "编辑行程页Tab-Day1",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_N_TAB_XPATH),
            "编辑行程页Tab-DayN",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.PENDING_TAB_XPATH),
            "编辑行程页Tab-待规划",
            timeout=8,
            attach_crop=False,
        )
        add_entry = trip_edit.wait_add_entry(timeout=8)
        attach_highlighted_bounds(
            driver,
            add_entry.getBounds(),
            "编辑行程页新增入口",
        )

        trip_edit.wait_route_overview_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.OVERVIEW_LIST_XPATH),
            "编辑行程页全览按天路线列表",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_1_SECTION_XPATH),
            "编辑行程页Day1路线分组",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_2_SECTION_XPATH),
            "编辑行程页DayN路线分组",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_NUMBER_1_XPATH),
            "编辑行程页POI顺序编号1",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.FIRST_DAY_POI_XPATH),
            "编辑行程页单天POI-通菜街",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SECOND_DAY_POI_XPATH),
            "编辑行程页单天POI-旺角",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击返回键，校验返回“香港逛吃两日游”行程详情页"):
        back_button = trip_edit.back_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            back_button.getBounds(),
            "编辑行程页返回键",
        )
        back_button.click()
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(TRIP_NAME)),
            f"返回后的行程详情页标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
