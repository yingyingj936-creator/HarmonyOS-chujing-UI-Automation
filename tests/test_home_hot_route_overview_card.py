import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"


@allure.feature("首页热门路线")
@allure.story("全览路线卡片进入单日视图")
def test_home_hot_route_overview_day_card_to_day_view(driver) -> None:
    """验证全览标签下点击第1天卡片后进入第1天视图。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户进入“香港逛吃两日游”详情页"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_loaded = route_detail.wait_loaded(ROUTE_NAME, timeout=15)

    with allure.step("步骤1：查看“全览”标签下地图背景，校验全览标签已默认选中"):
        route_detail.wait_itinerary_tabs(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            route_loaded["map"],
            "全览地图背景，展示所有天数路线",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看“全览”标签下卡片陈列，校验每天行程摘要、地点数和地点条目"):
        route_detail.wait_overview_day_cards(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_OVERVIEW_CARD_XPATH),
            "全览下第1天行程摘要卡片，包含地点数和地点条目",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击“全览”标签下第1天卡片，校验第1天标签同步高亮并进入第1天视图"):
        route_detail.tap_day_1_overview_card(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_SELECTED_TAB_XPATH),
            "点击全览第1天卡片后，第1天标签已高亮",
            timeout=8,
            attach_crop=False,
        )

