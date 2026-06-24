import allure
import pytest
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


TRIP_NAME = "香港逛吃两日游"
FIRST_DAY_POI = "通菜街"
SECOND_DAY_POI = "旺角"


@allure.feature("行程管理")
@allure.story("我的行程详情页布局")
def test_trip_detail_layout_for_hongkong_food_route(driver) -> None:
    """验证从我的行程进入香港逛吃两日游详情页后，核心布局模块展示完整。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)

    with allure.step("前置条件：普通用户已登录，行程列表存在“香港逛吃两日游”"):
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

    with allure.step("步骤1：点击行程卡片“香港逛吃两日游”，校验进入行程详情页"):
        trip_manager.tap_trip(TRIP_NAME)
        trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(TRIP_NAME)),
            f"行程详情页标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看行程详情页顶部标题和重命名入口"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(TRIP_NAME)),
            "行程详情顶部标题",
            timeout=8,
            attach_crop=False,
        )
        rename_button = trip_detail.wait_rename_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            rename_button.getBounds(),
            "行程详情顶部重命名入口",
        )

    with allure.step("步骤3：查看地图缩略图、概览路线和查看地图按钮"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.MAP_THUMBNAIL_XPATH),
            "行程详情地图缩略图及路线概览区域",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.VIEW_MAP_BUTTON_XPATH),
            "行程详情查看地图按钮",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：查看按天展示的单天行程路线、POI名称和两点间距离"):
        day_1 = trip_detail.scroll_until_xpath_visible(
            trip_detail.DAY_1_XPATH,
            "第1天行程路线",
            max_swipes=5,
            timeout=8,
        )
        attach_highlighted_bounds(driver, day_1.getBounds(), "第1天行程路线")

        first_poi = trip_detail.scroll_until_xpath_visible(
            trip_detail.route_day_poi_xpath(FIRST_DAY_POI),
            f"第1天POI-{FIRST_DAY_POI}",
            max_swipes=5,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            first_poi.getBounds(),
            f"第1天POI名称-{FIRST_DAY_POI}",
        )

        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_poi_with_icon_xpath(FIRST_DAY_POI)),
            f"第1天POI图标和名称-{FIRST_DAY_POI}",
            timeout=8,
            attach_crop=False,
        )

        distance = trip_detail.scroll_until_xpath_visible(
            trip_detail.ROUTE_DISTANCE_XPATH,
            "POI两点之间距离",
            max_swipes=4,
            timeout=8,
        )
        attach_highlighted_bounds(driver, distance.getBounds(), "POI两点之间距离")

        second_poi = trip_detail.scroll_until_xpath_visible(
            trip_detail.route_day_poi_xpath(SECOND_DAY_POI),
            f"第1天POI-{SECOND_DAY_POI}",
            max_swipes=4,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            second_poi.getBounds(),
            f"第1天POI名称-{SECOND_DAY_POI}",
        )

    with allure.step("步骤5：查看底部编辑行程按钮"):
        edit_button = trip_detail.scroll_until_xpath_visible(
            trip_detail.EDIT_TRIP_BUTTON_XPATH,
            "编辑行程按钮",
            max_swipes=8,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            edit_button.getBounds(),
            "行程详情底部编辑行程按钮",
        )
        allure.attach(
            "\n".join(trip_detail.visible_texts()),
            "行程详情页当前可见文本",
            allure.attachment_type.TEXT,
        )
