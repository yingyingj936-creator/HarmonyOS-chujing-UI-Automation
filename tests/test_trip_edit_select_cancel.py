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
@allure.story("编辑路线 Day1 POI 勾选与取消")
def test_trip_edit_day1_poi_select_cancel(driver) -> None:
    """验证编辑路线 Day1 首个 POI 勾选后展示批量操作菜单，取消后列表恢复未选中。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：已进入“香港逛吃两日游”编辑路线 Day1"):
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
        trip_edit.tap_day_1_tab(timeout=8)
        trip_edit.wait_day_1_ready(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_1_TAB_XPATH),
            "编辑行程页Tab-Day1",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_1_CHILD_POI_XPATH),
            "编辑行程页Day1第一个POI-通菜街",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击第1个 POI 通菜街左侧勾选框，校验出现批量操作菜单"):
        before_texts = trip_edit.visible_child_list_texts()
        checkbox = trip_edit.first_poi_select_icon(timeout=8)
        attach_highlighted_bounds(
            driver,
            checkbox.getBounds(),
            "通菜街左侧勾选框-点击前",
        )
        trip_edit.tap_first_poi_select_icon(timeout=8)
        menu = trip_edit.wait_selection_action_menu_loaded(timeout=8)
        attach_highlighted_bounds(
            driver,
            menu.getBounds(),
            "POI选中后的批量操作菜单",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SELECTION_CANCEL_ACTION_XPATH),
            "选中菜单-取消",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SELECTION_DELETE_ACTION_XPATH),
            "选中菜单-删除",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SELECTION_MOVE_ACTION_XPATH),
            "选中菜单-移动到",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SELECTION_COPY_ACTION_XPATH),
            "选中菜单-复制到",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击取消，校验 POI 恢复未选中且行程列表不发生变化"):
        cancel_action = trip_edit.selection_cancel_action(timeout=8)
        attach_highlighted_bounds(
            driver,
            cancel_action.getBounds(),
            "选中菜单-取消按钮",
        )
        trip_edit.tap_selection_cancel(timeout=8)
        trip_edit.wait_selection_action_menu_closed(timeout=8)
        trip_edit.wait_day_1_ready(timeout=10)
        after_texts = trip_edit.visible_child_list_texts()
        assert after_texts == before_texts, (
            "点击取消后 Day1 行程列表发生变化，"
            f"取消前={before_texts}，取消后={after_texts}"
        )

        checkbox_after_cancel = trip_edit.first_poi_select_icon(timeout=8)
        attach_highlighted_bounds(
            driver,
            checkbox_after_cancel.getBounds(),
            "通菜街左侧勾选框-取消后",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.CHILD_LIST_XPATH),
            "取消后Day1行程列表",
            timeout=8,
            attach_crop=False,
        )
