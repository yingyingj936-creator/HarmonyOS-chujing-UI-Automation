import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.reference_hot_routes import ReferenceHotRoutesPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("行程管理")
@allure.story("参考热门路线列表浏览")
def test_trip_reference_hot_routes_list_and_back(driver) -> None:
    """验证行程页可进入参考热门路线页，浏览路线列表并返回行程页。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    reference_routes = ReferenceHotRoutesPage(driver)

    with allure.step("前置条件：普通用户进入行程页"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        trip_manager.scroll_to_create_area(max_swipes=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.CREATE_TRIP_TITLE_XPATH),
            "行程页-创建行程区域",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击“参考热门路线修改”入口，进入参考热门路线页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.HOT_ROUTE_REFERENCE_XPATH),
            "参考热门路线修改入口",
            timeout=8,
            attach_crop=False,
        )
        trip_manager.tap_hot_route_reference(timeout=8)
        reference_routes.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(reference_routes.CURRENT_REGION_XPATH),
            "参考热门路线页-当前地区",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看参考热门路线列表，校验路线卡片展示封面和标题"):
        reference_routes.wait_hot_route_card(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(reference_routes.HOT_ROUTE_CARD_XPATH),
            "参考热门路线列表-路线卡片",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(reference_routes.HOT_ROUTE_TITLE_XPATH),
            "参考热门路线列表-路线标题",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：滑动热门路线列表，校验列表可继续浏览"):
        reference_routes.swipe_hot_route_list()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(reference_routes.ROUTE_LIST_XPATH),
            "滑动后的参考热门路线列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击返回，回到行程页"):
        reference_routes.tap_back(timeout=8)
        trip_manager.wait_loaded(timeout=10)
        trip_manager.scroll_to_create_area(max_swipes=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.CREATE_TRIP_TITLE_XPATH),
            "返回行程页-创建行程区域",
            timeout=8,
            attach_crop=False,
        )
