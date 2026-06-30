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
SOURCE_POI = "铜锣湾"
TARGET_POI = "希慎广场"


def _text_index(texts: list[str], keyword: str) -> int:
    for index, text in enumerate(texts):
        if keyword in text:
            return index
    return -1


def _assert_visible_order(texts: list[str], first: str, second: str, label: str) -> None:
    first_index = _text_index(texts, first)
    second_index = _text_index(texts, second)
    assert first_index >= 0, f"{label}未看到“{first}”，当前文本={texts}"
    assert second_index >= 0, f"{label}未看到“{second}”，当前文本={texts}"
    assert first_index < second_index, (
        f"{label}顺序不正确，期望“{first}”在“{second}”前面，当前文本={texts}"
    )


def _assert_detail_day2_order(
    trip_detail: TripDetailPage,
    *,
    first: str,
    second: str,
    max_swipes: int = 10,
) -> list[str]:
    """滚动详情页，确认 Day2 行程轴中 first 位于 second 前面。"""
    seen_day2 = False
    day2_texts: list[str] = []
    all_seen_texts: list[str] = []

    for swipe_count in range(max_swipes + 1):
        current_texts = trip_detail.visible_texts()
        all_seen_texts.extend(text for text in current_texts if text not in all_seen_texts)
        if any(
            text in ("第 2 天", "第2天", "Day2") or "第 2 天" in text or "第2天" in text
            for text in current_texts
        ):
            seen_day2 = True

        if seen_day2:
            day2_texts.extend(text for text in current_texts if text not in day2_texts)
            if _text_index(day2_texts, first) >= 0 and _text_index(day2_texts, second) >= 0:
                _assert_visible_order(day2_texts, first, second, "行程详情页Day2")
                allure.attach(
                    "\n".join(day2_texts),
                    "详情页Day2顺序检查文本",
                    allure.attachment_type.TEXT,
                )
                return day2_texts

        if swipe_count < max_swipes:
            trip_detail.swipe_detail_up()

    allure.attach(
        "\n".join(all_seen_texts) or "未读取到可见文本",
        "详情页滚动检查文本",
        allure.attachment_type.TEXT,
    )
    pytest.fail(
        f"详情页未完成 Day2 顺序校验，是否看到Day2={seen_day2}，"
        f"Day2累计文本={day2_texts}"
    )


@allure.feature("行程管理")
@allure.story("编辑路线拖拽调整 Day2 POI 顺序")
def test_trip_edit_reorder_day2_first_poi_below_second(driver) -> None:
    """验证编辑路线中将 Day2 的铜锣湾拖到希慎广场下方后，详情页顺序同步更新。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_edit = TripEditPage(driver)

    with allure.step("前置条件：已进入“香港逛吃两日游”编辑路线页 Day2，且前两个 POI 为铜锣湾、希慎广场"):
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
        trip_edit.tap_day_2_tab(timeout=8)
        trip_edit.wait_day_2_loaded(timeout=10)

        before_texts = trip_edit.visible_child_list_texts()
        _assert_visible_order(before_texts, SOURCE_POI, TARGET_POI, "拖拽前编辑页Day2")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.child_poi_text_xpath(SOURCE_POI)),
            f"拖拽前Day2第一个POI-{SOURCE_POI}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_edit.child_poi_text_xpath(TARGET_POI)),
            f"拖拽前Day2第二个POI-{TARGET_POI}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：长按 Day2 第一个 POI 铜锣湾，移动到第二个 POI 希慎广场下面"):
        source_card = trip_edit.child_poi_card(SOURCE_POI, timeout=8)
        target_card = trip_edit.child_poi_card(TARGET_POI, timeout=8)
        attach_highlighted_bounds(
            driver,
            source_card.getBounds(),
            f"拖拽起点-Day2 POI {SOURCE_POI}",
        )
        attach_highlighted_bounds(
            driver,
            target_card.getBounds(),
            f"拖拽目标-Day2 POI {TARGET_POI}",
        )
        trip_edit.drag_child_poi_below(SOURCE_POI, TARGET_POI, timeout=8)
        after_texts = trip_edit.visible_child_list_texts()
        _assert_visible_order(after_texts, TARGET_POI, SOURCE_POI, "拖拽后编辑页Day2")
        allure.attach(
            "\n".join(after_texts),
            "拖拽后编辑页Day2列表文本",
            allure.attachment_type.TEXT,
        )

    with allure.step("步骤2：点击编辑完成，校验详情页 Day2 POI 顺序更新成功"):
        complete = trip_edit.edit_complete_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            complete.getBounds(),
            "编辑行程页编辑完成按钮",
        )
        complete.click()
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        _assert_detail_day2_order(
            trip_detail,
            first=TARGET_POI,
            second=SOURCE_POI,
            max_swipes=12,
        )
        target_detail = trip_detail.scroll_until_xpath_visible(
            trip_detail.route_day_poi_xpath(TARGET_POI),
            f"行程详情页Day2 POI-{TARGET_POI}",
            max_swipes=2,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            target_detail.getBounds(),
            f"详情页Day2排序后靠前POI-{TARGET_POI}",
        )
