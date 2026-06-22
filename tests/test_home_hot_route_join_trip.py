import allure
from hypium import BY

from pages.add_to_trip import AddToTripPage
from pages.bottom_navigation import BottomNavigation
from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"
TRIP_NAME = "热门路线--加入我的行程"


@allure.feature("首页热门路线")
@allure.story("热门路线加入我的行程")
def test_home_hot_route_join_trip(driver) -> None:
    """验证热门路线可重命名后创建为我的行程，并在行程列表展示路线数据。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)
    add_to_trip = AddToTripPage(driver)
    trip_detail = TripDetailPage(driver)
    trip_manager = TripManagerPage(driver)
    navigation = BottomNavigation(driver)

    with allure.step("前置条件：普通用户已登录，并进入“香港逛吃两日游”详情页"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.overview_title_xpath(ROUTE_NAME)),
            "热门路线详情页-香港逛吃两日游",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击“加入我的行程”按钮，校验命名弹窗和原名称自动回显"):
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
            BY.xpath(add_to_trip.TRIP_NAME_DIALOG_TITLE_XPATH),
            "创建行程命名弹窗",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(add_to_trip.trip_name_input_value_xpath(ROUTE_NAME)),
            "创建行程弹窗-原路线名称自动回显",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤2：清空原名称，输入行程名称“{TRIP_NAME}”"):
        add_to_trip.clear_and_input_trip_name(TRIP_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(add_to_trip.trip_name_input_value_xpath(TRIP_NAME)),
            f"创建行程弹窗-新名称{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击创建并添加，校验跳转至该行程详情页"):
        add_to_trip.tap_create_and_add()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(TRIP_NAME)),
            f"行程详情页标题-{TRIP_NAME}",
            timeout=12,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.ROUTE_DAY_1_XPATH),
            "行程详情页-第1天路线数据",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：进入底部导航“行程”，校验我的行程列表新增该行程且天数、地点数据一致"):
        trip_detail.tap_back_button()
        if driver.wait_for_component(BY.xpath(home.SEARCH_BAR_XPATH), timeout=2) is None:
            route_detail.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.SEARCH_BAR_XPATH),
            "返回首页-搜索框",
            timeout=8,
            attach_crop=False,
        )

        navigation.tap_trip()
        trip_manager.pull_to_refresh()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.route_trip_card_title_xpath(TRIP_NAME)),
            f"我的行程列表-新增行程{TRIP_NAME}",
            timeout=10,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.route_trip_card_summary_xpath(TRIP_NAME)),
            "我的行程列表-路线天数和POI点数据",
            timeout=8,
            attach_crop=False,
        )

