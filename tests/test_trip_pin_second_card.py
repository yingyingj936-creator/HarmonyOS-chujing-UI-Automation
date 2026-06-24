import allure
import pytest
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.outbound_home import OutboundHomePage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


@allure.feature("行程管理")
@allure.story("我的行程置顶并保持排序")
def test_pin_second_trip_card_and_keep_order_after_reenter(driver) -> None:
    """验证长按第二条行程置顶后，该行程移动到列表首位且重新进入后排序保持。"""
    navigation = BottomNavigation(driver)
    home = OutboundHomePage(driver)
    trip_manager = TripManagerPage(driver)

    with allure.step("前置条件：普通用户已登录，进入行程页并确认我的行程列表至少有 2 条行程"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        card_infos = trip_manager.visible_trip_cards_with_titles(max_swipes=8)
        if len(card_infos) < 2:
            pytest.skip(
                f"前置条件不满足：我的行程列表当前仅识别到 {len(card_infos)} 条行程，"
                "需要至少 2 条"
            )

        first_title = card_infos[0][1]
        target_card, target_title = card_infos[1]
        if first_title == target_title:
            pytest.skip(
                f"前置条件不满足：前两条行程标题相同，无法可靠判断置顶排序：{target_title}"
            )

        attach_highlighted_bounds(
            driver,
            target_card.getBounds(),
            f"置顶前第二条行程-{target_title}",
        )
        allure.attach(
            f"置顶前首位：{first_title}\n待置顶第二条：{target_title}",
            "置顶前行程顺序",
            allure.attachment_type.TEXT,
        )

    with allure.step("步骤1：长按第二条行程卡片，校验弹出“编辑行程”菜单"):
        trip_manager.long_press_trip_card(target_card, press_time=2.0)
        trip_manager.wait_edit_trip_menu_loaded(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.EDIT_TRIP_MENU_TITLE_XPATH),
            "编辑行程菜单-标题",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击“置顶该行程”，校验目标行程移动到列表首位"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.PIN_TRIP_ACTION_XPATH),
            "编辑行程菜单-置顶该行程",
            timeout=8,
            attach_crop=False,
        )
        trip_manager.tap_pin_trip_action(timeout=8)
        trip_manager.wait_edit_menu_closed(timeout=5)
        trip_manager.wait_first_trip_title(target_title, timeout=10)

        after_pin_infos = trip_manager.visible_trip_cards_with_titles(max_swipes=2)
        attach_highlighted_bounds(
            driver,
            after_pin_infos[0][0].getBounds(),
            f"置顶后首位行程-{target_title}",
        )

    with allure.step("步骤3：退出并重新进入行程页，校验置顶排序保持"):
        navigation.tap_home(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.HOME_ROOT_XPATH),
            "退出行程页后-首页",
            timeout=8,
            attach_crop=False,
        )
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        trip_manager.wait_first_trip_title(target_title, timeout=10)

        reenter_infos = trip_manager.visible_trip_cards_with_titles(max_swipes=2)
        attach_highlighted_bounds(
            driver,
            reenter_infos[0][0].getBounds(),
            f"重新进入后首位行程-{target_title}",
        )
        allure.attach(
            "\n".join(title for _, title in reenter_infos),
            "重新进入后可见行程顺序",
            allure.attachment_type.TEXT,
        )
