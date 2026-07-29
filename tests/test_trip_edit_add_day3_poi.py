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
SEARCH_KEYWORD = "太古"
TARGET_POI = "太古广场"
DETAIL_DAY_3_XPATH = (
    '//Text[@text="Day3" or @text="第3天" or @text="第 3 天" '
    'or contains(@text, "第3天") or contains(@text, "第 3 天")]'
)


@allure.feature("行程管理")
@allure.story("编辑路线新增 Day3 并添加 POI")
def test_trip_edit_add_day3_and_poi(driver) -> None:
    """验证编辑路线新增 Day3，并将太古广场添加到 Day3 后同步到行程详情页。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：普通用户进入“香港逛吃两日游”编辑路线页，当前行程为2天"):
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
        trip_edit.wait_tabs_ready(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_N_TAB_XPATH),
            "编辑行程页Tab-Day2",
            timeout=8,
            attach_crop=False,
        )
        if driver.wait_for_component(BY.xpath(trip_edit.DAY_3_TAB_XPATH), timeout=0.5):
            pytest.fail("前置条件不满足：当前行程已存在 Day3，不符合“当前行程为2天”")

    with allure.step("步骤1：点击 Tab 区域的“+”按钮，新增 Day3"):
        add_day_entry = trip_edit.wait_add_entry(timeout=8)
        attach_highlighted_bounds(
            driver,
            add_day_entry.getBounds(),
            "编辑行程页Tab区域新增Day按钮",
        )
        trip_edit.tap_add_day_entry(timeout=8)

    with allure.step("步骤2：查看新增 Day3 Tab，并确认展示添加地点/活动按钮"):
        day3_tab = trip_edit.wait_xpath(
            trip_edit.DAY_3_TAB_XPATH,
            "编辑行程页新增Day3 Tab",
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            day3_tab.getBounds(),
            "编辑行程页新增Day3 Tab",
        )
        add_place_entry = trip_edit.switch_to_day_3_empty(timeout=12)
        attach_highlighted_bounds(
            driver,
            add_place_entry.getBounds(),
            "Day3添加地点/活动按钮",
        )

    with allure.step("步骤3：点击添加地点/活动按钮，输入“太古”，展示相关搜索结果"):
        trip_edit.tap_day_3_add_place_entry(timeout=8)
        search_input = trip_edit.input_add_poi_keyword(SEARCH_KEYWORD, timeout=8)
        attach_highlighted_bounds(
            driver,
            search_input.getBounds(),
            f"添加地点搜索框-已输入{SEARCH_KEYWORD}",
        )
        result = trip_edit.add_poi_search_result(TARGET_POI, timeout=10)
        attach_highlighted_bounds(
            driver,
            result.getBounds(),
            f"添加地点搜索结果-{TARGET_POI}",
        )

    with allure.step("步骤4：点击“太古广场”，校验 Day3 新增该 POI 点"):
        added_poi = trip_edit.tap_add_poi_search_result_and_wait_added(
            TARGET_POI,
            timeout=10,
        )
        attach_highlighted_bounds(
            driver,
            added_poi.getBounds(),
            f"编辑行程页Day3新增POI-{TARGET_POI}",
        )

    with allure.step("步骤5：点击编辑完成，校验行程详情页新增 Day3 并展示太古广场"):
        complete = trip_edit.edit_complete_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            complete.getBounds(),
            "编辑行程页编辑完成按钮",
        )
        trip_edit.tap_edit_complete(timeout=10)
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)

        day3_detail = trip_detail.scroll_until_xpath_visible(
            DETAIL_DAY_3_XPATH,
            "行程详情页Day3",
            max_swipes=12,
            timeout=10,
        )
        attach_highlighted_bounds(
            driver,
            day3_detail.getBounds(),
            "行程详情页新增Day3",
        )
        poi_detail = trip_detail.scroll_until_xpath_visible(
            trip_detail.route_day_poi_xpath(TARGET_POI),
            f"行程详情页Day3 POI-{TARGET_POI}",
            max_swipes=6,
            timeout=10,
        )
        attach_highlighted_bounds(
            driver,
            poi_detail.getBounds(),
            f"行程详情页Day3新增POI-{TARGET_POI}",
        )
