from datetime import datetime

import allure
from hypium import BY

from pages.add_to_trip import AddToTripPage
from pages.bottom_navigation import BottomNavigation
from pages.reference_hot_routes import ReferenceHotRoutesPage
from pages.route_detail import RouteDetailPage
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港离岛慢游线"
ROUTE_POI_NAME = "牛皮厂秘密花园"


def _open_reference_hot_routes(
    navigation: BottomNavigation,
    trip_manager: TripManagerPage,
    reference_routes: ReferenceHotRoutesPage,
) -> None:
    """从首页进入行程页，再进入参考热门路线列表。"""
    navigation.tap_trip()
    trip_manager.wait_loaded(timeout=10)
    trip_manager.tap_hot_route_reference(timeout=8)
    reference_routes.wait_loaded(timeout=10)


def _return_to_trip_page(
    driver,
    trip_detail: TripDetailPage,
    route_detail: RouteDetailPage,
    reference_routes: ReferenceHotRoutesPage,
    trip_manager: TripManagerPage,
) -> None:
    """从行程详情页逐级返回行程页。"""
    trip_detail.tap_back_button()

    if driver.wait_for_component(BY.xpath(route_detail.ROOT_XPATH), timeout=2):
        route_detail.tap_back_button()

    if driver.wait_for_component(
        BY.xpath(reference_routes.CURRENT_REGION_XPATH),
        timeout=2,
    ):
        reference_routes.tap_back(timeout=8)

    trip_manager.wait_loaded(timeout=10)


@allure.feature("行程管理")
@allure.story("参考热门路线加入我的行程")
def test_reference_hot_route_join_trip_and_show_in_my_trip_list(driver) -> None:
    """验证参考热门路线可进入详情、创建为我的行程并在列表展示。"""
    trip_name = f"{ROUTE_NAME}{datetime.now():%M%S}"
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    reference_routes = ReferenceHotRoutesPage(driver)
    route_detail = RouteDetailPage(driver)
    add_to_trip = AddToTripPage(driver)
    trip_detail = TripDetailPage(driver)

    with allure.step("前置条件：普通用户进入参考热门路线列表"):
        _open_reference_hot_routes(navigation, trip_manager, reference_routes)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(reference_routes.ROUTE_LIST_XPATH),
            "参考热门路线列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤1：点击列表路线卡片“{ROUTE_NAME}”，进入路线详情页"):
        reference_routes.scroll_route_into_view(ROUTE_NAME, max_swipes=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(reference_routes.route_card_xpath(ROUTE_NAME)),
            f"参考热门路线卡片-{ROUTE_NAME}",
            timeout=8,
            attach_crop=False,
        )
        reference_routes.tap_route_card(ROUTE_NAME, timeout=8)
        route_detail.wait_generic_route_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.overview_title_xpath(ROUTE_NAME)),
            f"路线详情页-{ROUTE_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击加入我的行程，创建并添加，校验跳转行程详情页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.ROUTE_JOIN_TRIP_BUTTON_XPATH),
            "路线详情-加入我的行程按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.tap_join_trip(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(add_to_trip.trip_name_input_value_xpath(ROUTE_NAME)),
            f"创建行程弹窗-默认名称{ROUTE_NAME}",
            timeout=8,
            attach_crop=False,
        )
        add_to_trip.clear_and_input_trip_name(trip_name)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(add_to_trip.trip_name_input_value_xpath(trip_name)),
            f"创建行程弹窗-用例行程名称{trip_name}",
            timeout=8,
            attach_crop=False,
        )
        add_to_trip.tap_create_and_add()
        trip_detail.wait_generic_route_trip_detail(trip_name, timeout=15)
        plan_texts = trip_detail.visible_texts()
        allure.attach(
            "\n".join(plan_texts),
            "行程详情页文本",
            allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(trip_name)),
            f"行程详情页标题-{trip_name}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_poi_xpath(ROUTE_POI_NAME)),
            f"行程详情页-路线POI{ROUTE_POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：查看我的行程列表，校验该行程及信息一致"):
        _return_to_trip_page(
            driver,
            trip_detail,
            route_detail,
            reference_routes,
            trip_manager,
        )
        trip_manager.pull_to_refresh()
        trip_manager.scroll_trip_into_view(trip_name, max_swipes=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.trip_card_with_summary_xpath(trip_name)),
            f"我的行程列表-{trip_name}",
            timeout=8,
            attach_crop=False,
        )
