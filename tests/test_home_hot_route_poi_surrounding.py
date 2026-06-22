import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"
SURROUNDING_CATEGORIES = ("酒店", "美食", "景点")


@allure.feature("首页热门路线")
@allure.story("路线POI详情周边推荐")
def test_home_hot_route_poi_surrounding_recommendations(driver) -> None:
    """验证通菜街 POI 详情页周边推荐分类、周边 POI 详情与关闭返回。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)

    with allure.step("前置条件：普通用户进入“香港逛吃两日游”通菜街地点详情页"):
        home.restore_top(max_swipes=12)
        home.tap_hot_route_card(ROUTE_NAME)
        route_detail.wait_loaded(ROUTE_NAME, timeout=15)
        route_detail.tap_day_1_tab(timeout=10)
        route_detail.wait_day_1_route_list(timeout=10)
        route_detail.tap_day_1_first_poi(timeout=10)

    with allure.step("步骤1：查看周边推荐，校验分类和周边地点卡片信息"):
        route_detail.wait_surrounding_categories(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_SURROUNDING_XPATH),
            "POI详情-周边推荐标题",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.SURROUNDING_CATEGORY_GROUP_XPATH),
            "POI详情-周边推荐分类，包含景点、酒店、美食",
            timeout=8,
            attach_crop=False,
        )
        route_detail.wait_surrounding_poi_list(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.SURROUNDING_POI_CARD_XPATH),
            "POI详情-周边POI卡片，展示名称、评分、简介和缩略图",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.SURROUNDING_POI_DISTANCE_XPATH),
            "POI详情-周边POI相邻距离",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：依次点击不同周边推荐分类，校验列表刷新展示"):
        for category_name in SURROUNDING_CATEGORIES:
            route_detail.tap_surrounding_category(category_name, timeout=10)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(route_detail.surrounding_category_xpath(category_name)),
                f"周边推荐分类-{category_name}",
                timeout=8,
                attach_crop=False,
            )
            route_detail.wait_surrounding_poi_list(timeout=10)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(route_detail.SURROUNDING_POI_CARD_XPATH),
                f"周边推荐-{category_name}分类POI列表",
                timeout=8,
                attach_crop=False,
            )

    with allure.step("步骤3：点击周边地点，校验拉起周边地点详情"):
        route_detail.tap_surrounding_first_poi(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_ANY_HEADER_XPATH),
            "周边POI详情-名称和英文名",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_ROOT_XPATH),
            "周边POI详情-标签、评分、图集、简介、添加到我的行程和周边推荐",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_NAVIGATION_XPATH),
            "周边POI详情-底部导航入口",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击右上角叉号，退出周边地点详情并回到第1天列表"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_CLOSE_XPATH),
            "周边POI详情-右上角关闭按钮",
            timeout=8,
            attach_crop=False,
        )
        route_detail.close_day_1_poi_detail(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.DAY_1_FIRST_POI_CARD_XPATH),
            "关闭周边POI详情后回到第1天列表",
            timeout=8,
            attach_crop=False,
        )

