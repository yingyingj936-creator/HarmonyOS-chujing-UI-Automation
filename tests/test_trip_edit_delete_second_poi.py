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
DELETE_POI = "旺角"
NEXT_POI_AFTER_DELETE = "信和中心"


def _fail_if_day1_route_still_has_poi(
    trip_detail: TripDetailPage,
    poi_name: str,
    *,
    max_swipes: int = 5,
) -> None:
    """在详情页 Day1 行程轴区域滚动检查指定 POI 是否仍残留。"""
    seen_texts: list[str] = []
    for swipe_index in range(max_swipes + 1):
        current_texts = trip_detail.visible_texts()
        seen_texts.extend(text for text in current_texts if text not in seen_texts)
        if any(poi_name in text for text in current_texts):
            pytest.fail(
                f"删除后行程详情页仍展示 POI“{poi_name}”。"
                f"当前可见文本={current_texts}"
            )
        if swipe_index < max_swipes:
            trip_detail.swipe_detail_up()

    allure.attach(
        "\n".join(seen_texts) or "未读取到可见文本",
        "删除后行程详情页滚动检查文本",
        allure.attachment_type.TEXT,
    )


@allure.feature("行程管理")
@allure.story("编辑路线 Day1 删除第二个 POI")
def test_trip_edit_day1_delete_second_poi(driver) -> None:
    """验证编辑路线 Day1 删除第二个 POI 后，编辑页与详情页行程轴同步刷新。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：已进入“香港逛吃两日游”编辑路线 Day1，且 Day1 存在旺角"):
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
        trip_edit.wait_loaded(timeout=12)
        trip_edit.tap_day_1_tab(timeout=8)
        trip_edit.wait_day_1_loaded(timeout=10)

        before_texts = trip_edit.visible_child_list_texts()
        if not any(DELETE_POI in text for text in before_texts):
            pytest.fail(
                f"前置条件不满足：Day1 中未找到待删除 POI“{DELETE_POI}”。"
                f"可能该用例已执行过；当前列表文本={before_texts}"
            )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.child_poi_text_xpath(DELETE_POI)),
            f"编辑行程页Day1待删除POI-{DELETE_POI}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：勾选 Day1 中第2个 POI 旺角，校验旺角进入选中态"):
        checkbox = trip_edit.child_poi_select_icon(DELETE_POI, timeout=8)
        attach_highlighted_bounds(
            driver,
            checkbox.getBounds(),
            f"{DELETE_POI}左侧勾选框-点击前",
        )
        trip_edit.tap_child_poi_select_icon(DELETE_POI, timeout=8)
        menu = trip_edit.wait_selection_action_menu_loaded(timeout=8)
        attach_highlighted_bounds(
            driver,
            menu.getBounds(),
            "旺角选中后的批量操作菜单",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.SELECTION_DELETE_ACTION_XPATH),
            "选中菜单-删除",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击删除并在确认 Sheet 点击删除，校验旺角消失且相邻 POI 重新排序"):
        delete_action = trip_edit.selection_delete_action(timeout=8)
        attach_highlighted_bounds(
            driver,
            delete_action.getBounds(),
            "选中菜单-删除按钮",
        )
        trip_edit.tap_selection_delete(timeout=8)
        delete_sheet = trip_edit.wait_delete_confirm_loaded(timeout=8)
        attach_highlighted_bounds(
            driver,
            delete_sheet.getBounds(),
            "删除地点确认Sheet",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DELETE_CONFIRM_BUTTON_XPATH),
            "删除地点确认Sheet-删除按钮",
            timeout=8,
            attach_crop=False,
        )

        trip_edit.tap_confirm_delete_poi(timeout=8)
        trip_edit.wait_delete_confirm_closed(timeout=8)
        trip_edit.wait_day_1_after_wangjiao_deleted(timeout=12)

        after_texts = trip_edit.visible_child_list_texts()
        assert not any(DELETE_POI in text for text in after_texts), (
            f"删除后 Day1 列表仍展示“{DELETE_POI}”，当前列表文本={after_texts}"
        )
        assert any(f"2.{NEXT_POI_AFTER_DELETE}" in text for text in after_texts), (
            f"删除后未看到相邻 POI 重新排序为 2.{NEXT_POI_AFTER_DELETE}，"
            f"当前列表文本={after_texts}"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.DAY_1_CHILD_REORDERED_SECOND_POI_XPATH),
            f"删除后Day1第二个POI-{NEXT_POI_AFTER_DELETE}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.CHILD_DISTANCE_XPATH),
            "删除后Day1相邻距离",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击编辑完成，校验回到详情页后 Day1 行程轴中旺角消失"):
        complete = trip_edit.edit_complete_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            complete.getBounds(),
            "编辑行程页编辑完成按钮",
        )
        complete.click()
        time.sleep(1.2)
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)

        day_1 = trip_detail.scroll_until_xpath_visible(
            trip_detail.DAY_1_XPATH,
            "行程详情页第1天行程轴",
            max_swipes=5,
            timeout=8,
        )
        attach_highlighted_bounds(driver, day_1.getBounds(), "删除后详情页第1天行程轴")

        distance = trip_detail.scroll_until_xpath_visible(
            trip_detail.ROUTE_DISTANCE_XPATH,
            "删除后行程详情页路线距离",
            max_swipes=4,
            timeout=8,
        )
        attach_highlighted_bounds(driver, distance.getBounds(), "删除后行程详情页路线距离")

        next_poi = trip_detail.scroll_until_xpath_visible(
            trip_detail.route_day_poi_xpath(NEXT_POI_AFTER_DELETE),
            f"删除后行程详情页POI-{NEXT_POI_AFTER_DELETE}",
            max_swipes=4,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            next_poi.getBounds(),
            f"删除后详情页保留POI-{NEXT_POI_AFTER_DELETE}",
        )
        _fail_if_day1_route_still_has_poi(trip_detail, DELETE_POI, max_swipes=4)
