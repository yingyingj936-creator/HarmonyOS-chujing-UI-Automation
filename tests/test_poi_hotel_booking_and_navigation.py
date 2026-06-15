import allure
from hypium import BY

from pages.outbound_search import OutboundSearchPage
from pages.poi_detail import PoiDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


POI_NAME = "合和酒店"
RANKING_NAME = "住宿榜"


@allure.feature("POI 外部服务")
@allure.story("酒店预订与地图导航")
def test_poi_hotel_booking_and_navigation(driver) -> None:
    """验证从住宿榜单进入 Booking，并通过导航跳转花瓣地图。"""
    search_page = OutboundSearchPage(driver)
    poi_page = PoiDetailPage(driver)

    with allure.step("前置准备：从首页进入搜索启动页"):
        search_page.tap_home_search()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            "搜索启动页-必玩榜",
            timeout=8,
            attach_crop=False,
        )
        search_page.dismiss_keyboard()

    with allure.step("步骤1：向右滑动到香港平价住宿榜单"):
        search_page.browse_ranking_to_right_until_visible(
            POI_NAME,
            max_swipes=8,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.text(RANKING_NAME),
            f"搜索榜单-{RANKING_NAME}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.ranking_poi_xpath(POI_NAME)),
            f"{RANKING_NAME}POI-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤2：点击“{POI_NAME}”，拉起 POI 详情页"):
        search_page.tap_ranking_poi(POI_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(POI_NAME)),
            f"POI详情页-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击右下角“订酒店”，进入 Booking 服务"):
        poi_page.tap_book_hotel()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.BOOKING_TITLE_XPATH),
            "Booking服务",
            timeout=12,
            attach_crop=False,
        )

    with allure.step("步骤4：通过系统右侧边缘左滑手势返回 POI 详情页"):
        poi_page.system_gesture_back()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(POI_NAME)),
            f"系统手势返回POI详情页-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：点击右下角“导航”，进入花瓣地图"):
        poi_page.tap_navigation()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.MAP_START_NAVIGATION_XPATH),
            f"花瓣地图导航页-{POI_NAME}",
            timeout=12,
            attach_crop=False,
        )
