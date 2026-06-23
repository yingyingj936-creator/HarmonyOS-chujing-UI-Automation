import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


@allure.feature("行程管理")
@allure.story("我的行程长按编辑菜单")
def test_trip_card_long_press_edit_menu_close(driver) -> None:
    """验证我的行程卡片长按后展示编辑菜单，关闭后列表保持不变。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)

    with allure.step("前置条件：普通用户已登录，进入行程页并查看我的行程列表"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        trip_manager.scroll_to_trip_card_with_required_fields(max_swipes=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.TRIP_CARD_WITH_REQUIRED_FIELDS_XPATH),
            "我的行程列表-长按前行程卡片",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：长按任一行程卡片，校验弹出“编辑行程”操作菜单"):
        trip_manager.long_press_required_trip_card(press_time=2.0)
        trip_manager.wait_edit_trip_menu_loaded(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.EDIT_TRIP_MENU_TITLE_XPATH),
            "编辑行程底部菜单-标题",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看底部操作菜单，校验包含置顶和删除操作"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.PIN_TRIP_ACTION_XPATH),
            "编辑行程底部菜单-置顶该行程",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.DELETE_TRIP_ACTION_XPATH),
            "编辑行程底部菜单-删除该行程",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击关闭按钮，校验菜单消失且行程列表不发生变化"):
        attach_highlighted_bounds(
            driver,
            trip_manager.edit_menu_close_bounds(timeout=8),
            "编辑行程底部菜单-关闭按钮",
        )
        trip_manager.tap_edit_menu_close(timeout=8)
        trip_manager.wait_edit_menu_closed(timeout=5)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.TRIP_CARD_WITH_REQUIRED_FIELDS_XPATH),
            "我的行程列表-关闭菜单后行程卡片仍展示",
            timeout=8,
            attach_crop=False,
        )
