import allure
import pytest
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)

PROTECTED_TRIP_TITLES = ("香港逛吃两日游",)


def _select_delete_target(card_infos):
    for card, title in card_infos:
        if not any(protected in title for protected in PROTECTED_TRIP_TITLES):
            return card, title
    return card_infos[0]


@allure.feature("行程管理")
@allure.story("删除我的行程")
def test_delete_trip_card_after_confirm(driver) -> None:
    """验证长按行程卡片后删除行程，二次确认后列表不再展示该行程。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)

    with allure.step("前置条件：普通用户已登录，进入行程页并确认我的行程列表至少有 1 条行程"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        card_infos = trip_manager.visible_trip_cards_with_titles(max_swipes=8)
        if not card_infos:
            pytest.skip("前置条件不满足：我的行程列表当前没有可删除的行程")

        target_card, target_title = _select_delete_target(card_infos)
        attach_highlighted_bounds(
            driver,
            target_card.getBounds(),
            f"删除前目标行程-{target_title}",
        )
        allure.attach(
            target_title,
            "待删除行程名称",
            allure.attachment_type.TEXT,
        )

    with allure.step("步骤1：长按目标行程，校验弹出“编辑行程”卡片"):
        trip_manager.long_press_trip_card_until_menu(
            target_card,
            trip_name=target_title,
            press_time=2.0,
            attempts=3,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.EDIT_TRIP_MENU_TITLE_XPATH),
            "编辑行程卡片-标题",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击“删除该行程”，校验弹出二次删除确认弹窗"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.DELETE_TRIP_ACTION_XPATH),
            "编辑行程卡片-删除该行程",
            timeout=8,
            attach_crop=False,
        )
        trip_manager.tap_delete_trip_action(timeout=8)
        trip_manager.wait_delete_confirm_loaded(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.DELETE_CONFIRM_BUTTON_XPATH),
            "删除行程二次确认弹窗-删除按钮",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：在确认弹窗点击“删除”，校验我的行程列表没有该行程"):
        trip_manager.tap_confirm_delete_trip(timeout=8)
        trip_manager.wait_delete_confirm_closed(timeout=5)
        trip_manager.wait_trip_title_absent(target_title, timeout=12)

        trip_list = driver.wait_for_component(
            BY.xpath(trip_manager.TRIP_LIST_XPATH),
            timeout=3,
        )
        if trip_list is not None:
            attach_highlighted_bounds(
                driver,
                trip_list.getBounds(),
                "删除后行程列表区域",
            )
        else:
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(trip_manager.SCREEN_ROOT_XPATH),
                "删除后行程页区域",
                timeout=8,
                attach_crop=False,
            )
        remaining_titles = [
            title
            for _, title in trip_manager.current_visible_trip_cards_with_titles()
        ]
        allure.attach(
            "\n".join(remaining_titles) or "当前可见区域无行程卡片",
            "删除后可见行程列表",
            allure.attachment_type.TEXT,
        )
