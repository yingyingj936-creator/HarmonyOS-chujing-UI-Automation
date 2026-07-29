import allure
from hypium import BY

from pages.add_to_trip import AddToTripPage
from pages.bottom_navigation import BottomNavigation
from pages.outbound_home import OutboundHomePage
from pages.outbound_search import OutboundSearchPage
from pages.poi_detail import PoiDetailPage
from pages.select_destination import SelectDestinationPage
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import assert_visible_and_attach_highlight


TRIP_NAME = "POI加行程test"
POI_NAME = "旺角"


@allure.feature("行程管理")
@allure.story("POI 创建行程并重复添加")
def test_add_poi_to_new_trip_twice(driver) -> None:
    """验证旺角 POI 创建行程、二次添加及行程列表持久化。"""
    home_page = OutboundHomePage(driver)
    search_page = OutboundSearchPage(driver)
    poi_page = PoiDetailPage(driver)
    add_to_trip_page = AddToTripPage(driver)
    trip_detail_page = TripDetailPage(driver)
    trip_manager_page = TripManagerPage(driver)
    destination_page = SelectDestinationPage(driver)
    navigation = BottomNavigation(driver)

    with allure.step("前置准备：确保目的地为中国香港并进入搜索启动页"):
        hongkong_selector = BY.xpath(home_page.region_dropdown_xpath("中国香港"))
        if not driver.wait_for_component(hongkong_selector, timeout=2):
            home_page.tap_region_selector()
            destination_page.choose_destination("中国香港")
        search_page.tap_home_search()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            "搜索启动页-必玩榜",
            timeout=8,
            attach_crop=False,
        )
        search_page.dismiss_keyboard()

    with allure.step("步骤1：点击榜单地点“旺角”，进入对应详情页"):
        search_page.scroll_ranking_poi_into_view(POI_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.ranking_poi_xpath(POI_NAME)),
            "搜索榜单POI-旺角",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_ranking_poi(POI_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(POI_NAME)),
            "POI详情页-旺角",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击详情，查看地点位置、评分和简介"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.DETAIL_LINK_XPATH),
            "POI详情入口-详情",
            timeout=8,
            attach_crop=False,
        )
        poi_page.tap_detail_link()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.LOCATION_DETAIL_TITLE_XPATH),
            "地点详情-位置评分简介",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击地点详情页内返回按钮，返回地点详情页"):
        poi_page.tap_location_detail_back()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(POI_NAME)),
            "返回POI详情页-旺角",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击添加到我的行程，拉起添加至行程弹窗"):
        poi_page.tap_add_to_trip()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(add_to_trip_page.SHEET_TITLE_XPATH),
            "添加至行程弹窗",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：点击新建，拉起创建行程弹窗"):
        add_to_trip_page.tap_new_trip()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(add_to_trip_page.TRIP_NAME_INPUT_XPATH),
            "创建行程-名称输入框",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤6：创建“{TRIP_NAME}”并验证一个旺角待规划点"):
        add_to_trip_page.input_trip_name(TRIP_NAME)
        add_to_trip_page.tap_create_and_add()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail_page.title_xpath(TRIP_NAME)),
            f"行程详情标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail_page.first_unplanned_poi_xpath(POI_NAME)),
            "待规划POI-第一个旺角",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤7：点击行程详情页内返回按钮，返回添加至行程弹窗"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail_page.BACK_BUTTON_XPATH),
            "行程详情页-返回按钮",
            timeout=8,
            attach_crop=False,
        )
        trip_detail_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(add_to_trip_page.trip_card_xpath(TRIP_NAME)),
            f"添加至行程弹窗-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤8：点击刚创建的行程，再次添加旺角"):
        add_to_trip_page.tap_trip(TRIP_NAME)

    with allure.step("步骤9：点击添加至行程弹窗右上角关闭按钮"):
        add_to_trip_page.tap_close()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(POI_NAME)),
            "关闭弹窗返回POI详情页-旺角",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤10：依次点击页面内返回按钮回首页，进入底部行程页"):
        poi_page.tap_back_button(POI_NAME)
        search_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.SEARCH_BAR_XPATH),
            "返回首页-搜索框",
            timeout=8,
            attach_crop=False,
        )
        navigation.tap_trip()

    with allure.step("步骤11：下拉刷新我的行程，验证新建行程已展示"):
        trip_manager_page.pull_to_refresh()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager_page.trip_card_xpath(TRIP_NAME)),
            f"下拉刷新后我的行程列表-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤12：进入行程详情，验证标题和两个旺角待规划点"):
        trip_manager_page.tap_trip(TRIP_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail_page.title_xpath(TRIP_NAME)),
            f"最终行程详情标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail_page.first_unplanned_poi_xpath(POI_NAME)),
            "最终待规划POI-第一个旺角",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail_page.second_unplanned_poi_xpath(POI_NAME)),
            "最终待规划POI-第二个旺角",
            timeout=8,
            attach_crop=False,
        )

