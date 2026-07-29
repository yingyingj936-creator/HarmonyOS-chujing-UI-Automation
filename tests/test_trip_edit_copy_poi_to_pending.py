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
COPY_POI = "K11"


def _assert_detail_day1_and_pending_have_poi(
    driver,
    trip_detail: TripDetailPage,
    *,
    poi_name: str,
    max_swipes: int = 14,
) -> None:
    """滚动详情页，确认 Day1 保留 POI，且待规划栏新增同名 POI。"""
    seen_texts: list[str] = []
    seen_day1_poi = False
    seen_pending = False

    for swipe_count in range(max_swipes + 1):
        current_texts = trip_detail.visible_texts()
        seen_texts.extend(text for text in current_texts if text not in seen_texts)

        if not seen_pending and any(poi_name in text for text in current_texts):
            seen_day1_poi = True

        if any("待规划" in text for text in current_texts):
            seen_pending = True

        if seen_pending and any(poi_name in text for text in current_texts):
            poi = driver.wait_for_component(
                BY.xpath(trip_detail.route_day_poi_xpath(poi_name)),
                timeout=1,
            )
            if poi is not None:
                attach_highlighted_bounds(
                    driver,
                    poi.getBounds(),
                    f"行程详情页待规划POI-{poi_name}",
                )
            allure.attach(
                "\n".join(seen_texts) or "未读取到可见文本",
                "复制后行程详情页滚动检查文本",
                allure.attachment_type.TEXT,
            )
            assert seen_day1_poi, f"复制后 Day1 未保留 POI“{poi_name}”"
            return

        if swipe_count < max_swipes:
            trip_detail.swipe_detail_up()

    allure.attach(
        "\n".join(seen_texts) or "未读取到可见文本",
        "复制后行程详情页滚动检查文本",
        allure.attachment_type.TEXT,
    )
    pytest.fail(
        f"复制后详情页未在待规划栏看到 POI“{poi_name}”，"
        f"是否看到Day1保留={seen_day1_poi}，是否看到待规划栏={seen_pending}"
    )


@allure.feature("行程管理")
@allure.story("编辑路线复制 Day1 POI 到待规划")
def test_trip_edit_copy_day1_poi_to_pending(driver) -> None:
    """验证编辑路线中将 Day1 的 K11 复制到待规划后，详情页同步展示。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：已进入“香港逛吃两日游”编辑路线页 Day1，且 Day1 存在 K11"):
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
            COPY_POI,
            max_swipes=18,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            target_poi.getBounds(),
            f"编辑行程页Day1待复制POI-{COPY_POI}",
        )

    with allure.step("步骤1：勾选 Day1 中的 POI K11，校验 K11 呈选中态"):
        checkbox = trip_edit.child_poi_select_icon(COPY_POI, timeout=8)
        attach_highlighted_bounds(
            driver,
            checkbox.getBounds(),
            f"{COPY_POI}左侧勾选框-点击前",
        )
        trip_edit.tap_child_poi_select_icon(COPY_POI, timeout=8)
        menu = trip_edit.wait_selection_action_menu_loaded(timeout=8)
        attach_highlighted_bounds(
            driver,
            menu.getBounds(),
            f"{COPY_POI}选中后的批量操作菜单",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SELECTION_COPY_ACTION_XPATH),
            "选中菜单-复制到",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击复制到并选择待规划"):
        copy_action = trip_edit.selection_copy_action(timeout=8)
        attach_highlighted_bounds(
            driver,
            copy_action.getBounds(),
            "选中菜单-复制到按钮",
        )
        trip_edit.tap_selection_copy(timeout=8)
        copy_panel = trip_edit.wait_copy_target_panel_loaded(timeout=8)
        attach_highlighted_bounds(
            driver,
            copy_panel.getBounds(),
            "复制目标面板",
        )
        target_pending = trip_edit.copy_target_pending(timeout=8)
        attach_highlighted_bounds(
            driver,
            target_pending.getBounds(),
            "复制目标-待规划",
        )
        trip_edit.tap_copy_target_pending(timeout=8)
        trip_edit.wait_copy_target_panel_closed(timeout=6)

    with allure.step("步骤3：点击编辑完成，校验详情页 Day1 保留 K11 且待规划栏新增 K11"):
        complete = trip_edit.edit_complete_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            complete.getBounds(),
            "编辑行程页编辑完成按钮",
        )
        trip_edit.tap_edit_complete(timeout=10)
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        _assert_detail_day1_and_pending_have_poi(
            driver,
            trip_detail,
            poi_name=COPY_POI,
            max_swipes=14,
        )
