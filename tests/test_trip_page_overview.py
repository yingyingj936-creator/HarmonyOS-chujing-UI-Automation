import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_manager import TripManagerPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("行程管理")
@allure.story("行程页创建区域和我的行程列表展示")
def test_trip_page_create_area_and_my_trip_list(driver) -> None:
    """验证行程页创建行程区域、我的行程列表和视频教程入口展示完整。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)

    with allure.step("步骤1：点击底部导航“行程”，校验行程页打开成功"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(navigation.tab_xpath("行程")),
            "底部导航-行程页签",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.CREATE_TRIP_TITLE_XPATH),
            "行程页-创建行程区域",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看创建行程区域，校验参考热门路线修改入口展示"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.HOT_ROUTE_REFERENCE_XPATH),
            "创建行程区域-参考热门路线修改入口",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：查看我的行程列表和查看视频教程入口"):
        trip_manager.scroll_to_my_trips_area(max_swipes=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.MY_TRIPS_TITLE_XPATH),
            "我的行程区域标题",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.VIDEO_TUTORIAL_XPATH),
            "我的行程区域-查看视频教程入口",
            timeout=8,
            attach_crop=False,
        )
        trip_manager.scroll_to_trip_card_with_required_fields(max_swipes=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.TRIP_CARD_WITH_REQUIRED_FIELDS_XPATH),
            "我的行程列表-字段完整的行程卡片",
            timeout=8,
            attach_crop=False,
        )
