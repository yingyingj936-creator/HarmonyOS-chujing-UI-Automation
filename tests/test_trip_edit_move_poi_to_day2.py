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
MOVE_POI = "星光大道"


def _assert_detail_route_after_move(
    driver,
    trip_detail: TripDetailPage,
    *,
    max_swipes: int = 10,
) -> None:
    """滚动详情页，校验星光大道不在 Day1 区段，且移动后出现在 Day2 区段。"""
    seen_texts: list[str] = []
    seen_day2 = False
    seen_moved_poi_after_day2 = False

    for swipe_count in range(max_swipes + 1):
        current_texts = trip_detail.visible_texts()
        seen_texts.extend(text for text in current_texts if text not in seen_texts)

        if any(
            text in ("第 2 天", "第2天", "Day2") or "第 2 天" in text or "第2天" in text
            for text in current_texts
        ):
            seen_day2 = True

        if any(MOVE_POI in text for text in current_texts):
            if not seen_day2:
                pytest.fail(
                    f"移动后详情页在 Day2 之前仍展示“{MOVE_POI}”，疑似 Day1 未移除。"
                    f"当前可见文本={current_texts}"
                )
            seen_moved_poi_after_day2 = True
            poi = driver.wait_for_component(
                BY.xpath(trip_detail.route_day_poi_xpath(MOVE_POI)),
                timeout=1,
            )
            if poi is not None:
                attach_highlighted_bounds(
                    driver,
                    poi.getBounds(),
                    f"详情页Day2新增POI-{MOVE_POI}",
                )
            break

        if swipe_count < max_swipes:
            trip_detail.swipe_detail_up()

    allure.attach(
        "\n".join(seen_texts) or "未读取到可见文本",
        "移动后行程详情页滚动检查文本",
        allure.attachment_type.TEXT,
    )
    assert seen_day2, "移动后行程详情页未看到 Day2 行程轴"
    assert seen_moved_poi_after_day2, f"移动后行程详情页 Day2 未看到“{MOVE_POI}”"


@allure.feature("行程管理")
@allure.story("编辑路线移动 Day1 POI 到 Day2")
def test_trip_edit_move_day1_poi_to_day2(driver) -> None:
    """验证编辑路线中将 Day1 的星光大道移动到 Day2 后，编辑页和详情页路线同步刷新。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：已进入“香港逛吃两日游”编辑路线 Day1，且 Day1 存在星光大道"):
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
        target_poi = trip_edit.scroll_child_list_until_poi_visible(
            MOVE_POI,
            max_swipes=16,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            target_poi.getBounds(),
            f"编辑行程页Day1待移动POI-{MOVE_POI}",
        )

    with allure.step("步骤1：勾选 Day1 中的 POI 星光大道，校验星光大道进入选中态"):
        checkbox = trip_edit.child_poi_select_icon(MOVE_POI, timeout=8)
        attach_highlighted_bounds(
            driver,
            checkbox.getBounds(),
            f"{MOVE_POI}左侧勾选框-点击前",
        )
        trip_edit.tap_child_poi_select_icon(MOVE_POI, timeout=8)
        menu = trip_edit.wait_selection_action_menu_loaded(timeout=8)
        attach_highlighted_bounds(
            driver,
            menu.getBounds(),
            "星光大道选中后的批量操作菜单",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SELECTION_MOVE_ACTION_XPATH),
            "选中菜单-移动到",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击移动到并选择 Day2，校验 Day1 不显示星光大道且 Day2 新增星光大道"):
        move_action = trip_edit.selection_move_action(timeout=8)
        attach_highlighted_bounds(
            driver,
            move_action.getBounds(),
            "选中菜单-移动到按钮",
        )
        trip_edit.tap_selection_move(timeout=8)
        move_panel = trip_edit.wait_move_target_panel_loaded(timeout=8)
        attach_highlighted_bounds(
            driver,
            move_panel.getBounds(),
            "移动目标面板",
        )
        target_day2 = trip_edit.move_target_day_2(timeout=8)
        attach_highlighted_bounds(
            driver,
            target_day2.getBounds(),
            "移动目标-Day2",
        )
        trip_edit.tap_move_target_day_2(timeout=8)
        trip_edit.wait_move_target_panel_closed(timeout=6)


    with allure.step("步骤3：点击编辑完成，校验详情页 Day1/Day2 行程轴和路线距离刷新"):
        complete = trip_edit.edit_complete_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            complete.getBounds(),
            "编辑行程页编辑完成按钮",
        )
        trip_edit.tap_edit_complete(timeout=10)
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)

        distance = trip_detail.scroll_until_xpath_visible(
            trip_detail.ROUTE_DISTANCE_XPATH,
            "移动后行程详情页路线距离",
            max_swipes=4,
            timeout=8,
        )
        attach_highlighted_bounds(driver, distance.getBounds(), "移动后行程详情页路线距离")
        _assert_detail_route_after_move(driver, trip_detail, max_swipes=10)
