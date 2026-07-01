import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"


@allure.feature("首页热门路线")
@allure.story("多日路线第1天POI详情")
def test_home_hot_route_day1_poi_detail(driver) -> None:
    """验证多日路线第1天列表进入POI详情后，核心信息完整展示并可关闭返回。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户进入“香港逛吃两日游”详情页，并切换到第1天视图"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        route_detail.tap_day_1_tab(timeout=10)
        route_detail.wait_day_1_route_list(timeout=10)

    with allure.step("步骤1：查看“第1天”标签下地图背景"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.MAP_VIEW_XPATH),
            "第1天地图背景，展示第1天路线",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看“第1天”标签下卡片陈列，校验地点顺序、简介和相邻地点距离"):
        route_detail.wait_day_1_route_list(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_FIRST_POI_CARD_XPATH),
            "第1天第1个POI卡片，展示名称和简介缩略内容",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击“第1天”标签下地点，校验地点详情信息和底部操作区"):
        route_detail.tap_day_1_first_poi(timeout=10, verify_full_detail=True)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_HEADER_XPATH),
            "POI详情标题和英文名",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击右上角叉号，退出地点详情并回到第1天列表"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_CLOSE_XPATH),
            "POI详情右上角关闭按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.close_day_1_poi_detail(timeout=10)

