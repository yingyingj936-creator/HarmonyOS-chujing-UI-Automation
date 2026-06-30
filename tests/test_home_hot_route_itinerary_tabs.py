import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"


@allure.feature("首页热门路线")
@allure.story("多日路线行程规划切换")
def test_home_hot_route_itinerary_tabs(driver) -> None:
    """验证多日路线详情页行程规划标签切换。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户进入“香港逛吃两日游”详情页"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_loaded = route_detail.wait_loaded(ROUTE_NAME, timeout=15)

    with allure.step("步骤1：查看行程规划模块，默认展示全览路线列表"):
        route_detail.wait_itinerary_tabs(timeout=10)
        route_detail.wait_overview_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            route_loaded["map"],
            "全览路线地图背景",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：依次点击“第1天”和“第2天”，校验对应天数列表和地图背景"):
        route_detail.tap_day_1_tab(timeout=10)
        route_detail.wait_day_1_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_SELECTED_TAB_XPATH),
            "第1天标签已选中，地图背景已渲染",
            timeout=8,
            attach_crop=False,
        )

        route_detail.tap_day_2_tab(timeout=10)
        route_detail.wait_day_2_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_2_SELECTED_TAB_XPATH),
            "第2天标签已选中，地图背景已渲染",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：切回全览，校验恢复展示全览路线列表"):
        route_detail.tap_overview_tab(timeout=10)
        route_detail.wait_overview_itinerary(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_TITLE_XPATH),
            "切回全览后的第1天路线",
            timeout=8,
            attach_crop=False,
        )

