import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.outbound_search import OutboundSearchPage
from pages.poi_detail import PoiDetailPage
from pages.select_destination import SelectDestinationPage
from utils.allure_visual import assert_visible_and_attach_highlight


def _ensure_history_keyword(
    driver,
    home_page: OutboundHomePage,
    search_page: OutboundSearchPage,
    keyword: str,
    result_marker: str,
) -> None:
    """Create the required search history when the device has no prior state."""
    search_page.tap_home_search()
    history_selector = BY.xpath(search_page.history_keyword_xpath(keyword))

    if driver.wait_for_component(history_selector, timeout=2) is None:
        search_page.input_and_tap_search(keyword)
        if driver.wait_for_component(BY.text(result_marker), timeout=8) is None:
            raise AssertionError(
                f"无法通过搜索“{keyword}”创建历史记录，未出现结果“{result_marker}”"
            )
        search_page.tap_clear_input()
        if driver.wait_for_component(history_selector, timeout=8) is None:
            raise AssertionError(f"搜索历史中未生成“{keyword}”")

    search_page.tap_back_button()
    if (
        driver.wait_for_component(
            BY.xpath(home_page.SEARCH_BAR_XPATH),
            timeout=8,
        )
        is None
    ):
        raise AssertionError("准备搜索历史后未返回首页")


@allure.feature("搜索功能")
@allure.story("搜索启动页榜单、历史词与清除操作")
def test_search_start_page_poi_history_and_clear(driver) -> None:
    """验证搜索启动页榜单 POI、搜索历史及输入框清除流程。"""
    home_page = OutboundHomePage(driver)
    search_page = OutboundSearchPage(driver)
    poi_detail_page = PoiDetailPage(driver)
    destination_page = SelectDestinationPage(driver)

    with allure.step("前置准备：确保首页目的地为中国香港"):
        hongkong_selector = BY.xpath(home_page.region_dropdown_xpath("中国香港"))
        if not driver.wait_for_component(hongkong_selector, timeout=2):
            home_page.tap_region_selector()
            destination_page.choose_destination("中国香港")
        assert_visible_and_attach_highlight(
            driver,
            hongkong_selector,
            "首页目的地-中国香港",
            timeout=8,
            attach_crop=False,
        )
        _ensure_history_keyword(
            driver,
            home_page,
            search_page,
            keyword="香港",
            result_marker="香港经典一日游",
        )

    with allure.step("步骤1：点击首页搜索框，进入搜索启动页"):
        search_page.tap_home_search()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.placeholder_xpath("中国香港")),
            "搜索启动页-搜索框",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看搜索历史和榜单模块"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.SEARCH_HISTORY_TITLE_XPATH),
            "搜索启动页-搜索历史",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            "搜索启动页-必玩榜",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击榜单地点“太平山顶”，进入对应详情页"):
        search_page.tap_ranking_poi("太平山顶")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail_page.title_xpath("太平山顶")),
            "POI详情页-太平山顶",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3.1：点击地点详情页内返回按钮，返回搜索启动页"):
        poi_detail_page.tap_back_button("太平山顶")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.SEARCH_HISTORY_TITLE_XPATH),
            "返回搜索启动页-搜索历史",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击历史词“香港”，自动填充并进入搜索结果页"):
        search_page.tap_history_keyword("香港")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.input_value_xpath("香港")),
            "搜索框自动填充-香港",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.text("香港经典一日游"),
            "香港搜索结果-香港经典一日游",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：点击搜索框清除按钮，回到搜索启动页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.CLEAR_INPUT_BUTTON_XPATH),
            "搜索框清除按钮",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_clear_input()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.placeholder_xpath("中国香港")),
            "清除后搜索框",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.SEARCH_HISTORY_TITLE_XPATH),
            "清除后返回搜索启动页",
            timeout=8,
            attach_crop=False,
        )

