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
@allure.story("编辑行程页切换全览、Day和待规划Tab")
def test_trip_edit_page_tabs_switch_content(driver) -> None:
    """验证编辑行程页切换Day1、Day2、待规划、全览时，下方卡片内容同步刷新。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：已进入“香港逛吃两日游”编辑路线页，行程含多天和待规划"):
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
        tab_bar = trip_edit.wait_tabs_ready(timeout=8)
        attach_highlighted_bounds(
            driver,
            tab_bar.getBounds(),
            "编辑行程页Tab栏",
        )

    with allure.step("步骤1：点击“Day1”Tab，校验卡片展示第1天地点和相邻距离"):
        day_1_tab = trip_edit.tap_day_1_tab(timeout=8)
        trip_edit.wait_day_1_content_ready(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            day_1_tab,
            "编辑行程页Tab-Day1",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击“Day2”Tab，校验卡片展示第2天地点和相邻距离"):
        day_2_tab = trip_edit.tap_day_2_tab(timeout=8)
        trip_edit.wait_day_2_ready(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            day_2_tab,
            "编辑行程页Tab-Day2",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击“待规划”Tab，校验展示待规划栏"):
        pending_tab = trip_edit.tap_pending_tab(timeout=8)
        trip_edit.wait_pending_ready(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            pending_tab,
            "编辑行程页Tab-待规划",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击“全览”Tab，校验全览展示各天汇总路线"):
        overview_tab = trip_edit.tap_overview_tab(timeout=8)
        trip_edit.wait_route_overview_ready(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            overview_tab,
            "编辑行程页Tab-全览",
            timeout=8,
            attach_crop=False,
        )
