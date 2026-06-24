import allure
import pytest
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_fullscreen,
    attach_highlighted_bounds,
)


NEW_TRIP_NAME = "重命名"


def _visible_titles_text(trip_manager: TripManagerPage) -> str:
    titles = [
        title
        for _, title in trip_manager.current_visible_trip_cards_with_titles()
    ]
    return "\n".join(titles)


def _rename_current_detail(
    driver,
    trip_detail: TripDetailPage,
    target_name: str,
    *,
    attach_evidence: bool = False,
) -> None:
    trip_detail.tap_rename_entry(timeout=8)
    trip_detail.wait_rename_dialog_loaded(timeout=8)
    trip_detail.clear_and_input_rename(target_name)
    if attach_evidence:
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.rename_input_value_xpath(target_name)),
            f"行程重命名弹窗-输入新名称{target_name}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.RENAME_CONFIRM_BUTTON_XPATH),
            "行程重命名弹窗-确认按钮",
            timeout=8,
            attach_crop=False,
        )
    trip_detail.tap_rename_confirm(timeout=8)
    assert_visible_and_attach_highlight(
        driver,
        BY.xpath(trip_detail.route_trip_title_xpath(target_name)),
        f"行程详情页标题更新为{target_name}",
        timeout=12,
        attach_crop=False,
    )


def _restore_original_name(
    driver,
    navigation: BottomNavigation,
    trip_manager: TripManagerPage,
    trip_detail: TripDetailPage,
    original_name: str,
) -> None:
    """尽量恢复原行程名，避免污染后续用例数据。"""
    try:
        trip_detail.close_rename_dialog_if_present()

        if driver.wait_for_component(
            BY.xpath(trip_detail.title_xpath(NEW_TRIP_NAME)),
            timeout=1,
        ) is None:
            try:
                navigation.tap_trip(timeout=3)
                trip_manager.wait_loaded(timeout=6)
            except Exception:
                pass
            trip_manager.scroll_trip_into_view(NEW_TRIP_NAME, max_swipes=8)
            trip_manager.tap_trip(NEW_TRIP_NAME)
            trip_detail.wait_loaded(NEW_TRIP_NAME, timeout=10)

        _rename_current_detail(
            driver,
            trip_detail,
            original_name,
            attach_evidence=False,
        )
        trip_detail.tap_back_button()
        trip_manager.wait_loaded(timeout=8)
    except Exception as exc:
        allure.attach(
            str(exc),
            "清理失败-未能恢复原行程名称",
            allure.attachment_type.TEXT,
        )


@allure.feature("行程管理")
@allure.story("行程详情重命名并同步到我的行程列表")
def test_rename_trip_from_detail_and_sync_to_trip_list(driver) -> None:
    """验证在我的行程详情页重命名后，详情页和我的行程列表同步更新。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)
    original_name = ""
    renamed = False

    try:
        with allure.step("前置条件：普通用户已登录，进入行程页并确认至少有一个我的行程"):
            navigation.tap_trip()
            trip_manager.wait_loaded(timeout=10)
            card_infos = trip_manager.visible_trip_cards_with_titles(max_swipes=8)
            if not card_infos:
                pytest.skip("前置条件不满足：我的行程列表没有可操作行程")

            visible_titles = [title for _, title in card_infos]
            if NEW_TRIP_NAME in visible_titles:
                pytest.skip(
                    f"当前可见行程列表已存在“{NEW_TRIP_NAME}”，无法可靠验证重命名同步"
                )

            target_card, original_name = card_infos[0]
            if original_name == NEW_TRIP_NAME:
                pytest.skip("目标行程当前名称已经是“重命名”，无法验证名称变更")

            attach_highlighted_bounds(
                driver,
                target_card.getBounds(),
                f"我的行程列表-待重命名行程{original_name}",
            )
            allure.attach(
                "\n".join(visible_titles),
                "重命名前可见行程列表",
                allure.attachment_type.TEXT,
            )

        with allure.step("步骤1：点击行程卡片进入详情页，再点击右上角编辑或重命名入口"):
            trip_manager.tap_trip(original_name)
            trip_detail.wait_loaded(original_name, timeout=12)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(trip_detail.route_trip_title_xpath(original_name)),
                f"行程详情页-原标题{original_name}",
                timeout=8,
                attach_crop=False,
            )

            rename_entry = trip_detail.wait_rename_button(timeout=8)
            attach_highlighted_bounds(
                driver,
                rename_entry.getBounds(),
                "行程详情页右上角编辑或重命名入口",
            )
            trip_detail.tap_rename_entry(timeout=8)
            rename_input = trip_detail.wait_rename_dialog_loaded(timeout=8)
            attach_highlighted_bounds(
                driver,
                rename_input.getBounds(),
                "行程重命名弹窗-输入框",
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(trip_detail.rename_input_value_xpath(original_name)),
                f"行程重命名弹窗-原名称回显{original_name}",
                timeout=8,
                attach_crop=False,
            )

        with allure.step("步骤2：在重命名弹窗输入“重命名”，点击确定"):
            trip_detail.clear_and_input_rename(NEW_TRIP_NAME)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(trip_detail.rename_input_value_xpath(NEW_TRIP_NAME)),
                f"行程重命名弹窗-新名称{NEW_TRIP_NAME}",
                timeout=8,
                attach_crop=False,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(trip_detail.RENAME_CONFIRM_BUTTON_XPATH),
                "行程重命名弹窗-确定按钮",
                timeout=8,
                attach_crop=False,
            )
            trip_detail.tap_rename_confirm(timeout=8)
            renamed = True

        with allure.step("步骤3：校验详情页标题更新，并返回行程列表查看名称同步"):
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(trip_detail.route_trip_title_xpath(NEW_TRIP_NAME)),
                f"行程详情页标题更新为{NEW_TRIP_NAME}",
                timeout=12,
                attach_crop=False,
            )

            trip_detail.tap_back_button()
            trip_manager.wait_loaded(timeout=10)
            trip_manager.scroll_trip_into_view(NEW_TRIP_NAME, max_swipes=8)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(trip_manager.trip_list_title_xpath(NEW_TRIP_NAME)),
                f"我的行程列表卡片名称同步更新为{NEW_TRIP_NAME}",
                timeout=10,
                attach_crop=False,
            )
            if trip_manager.find_xpath(
                trip_manager.trip_list_title_xpath(original_name)
            ) is not None:
                attach_fullscreen(driver, f"旧名称仍残留-{original_name}")
                raise AssertionError(f"我的行程列表中旧名称仍残留：{original_name}")

            allure.attach(
                _visible_titles_text(trip_manager),
                "重命名后可见行程列表",
                allure.attachment_type.TEXT,
            )
    finally:
        if renamed and original_name:
            with allure.step("清理：将行程名称恢复为原名称，避免影响后续用例"):
                _restore_original_name(
                    driver,
                    navigation,
                    trip_manager,
                    trip_detail,
                    original_name,
                )
