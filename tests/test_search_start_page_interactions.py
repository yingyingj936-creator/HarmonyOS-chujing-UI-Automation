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
@allure.story("搜索启动页模块、大家都在搜、榜单、历史词与清除操作")
def test_search_start_page_poi_history_and_clear(driver) -> None:
    """验证搜索启动页模块、大家都在搜热词、榜单 POI、搜索历史及清除流程。"""
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
            BY.xpath(search_page.search_start_input_xpath("中国香港")),
            "搜索启动页-搜索框或AI推荐词",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看搜索启动页页面内容"):
        search_page.wait_search_start_loaded(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.EVERYONE_SEARCHING_TITLE_XPATH),
            "搜索启动页-大家都在搜",
            timeout=8,
            attach_crop=False,
        )
        assert driver.wait_for_component(
            BY.xpath(search_page.SEARCH_HISTORY_TITLE_XPATH),
            timeout=8,
        ), "搜索启动页未展示搜索历史模块"
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            "搜索启动页-必玩榜",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击“大家都在搜”模块中的任意 AI 推荐词，进入对应搜索结果页"):
        keyword, _ = search_page.first_everyone_searching_keyword(timeout=8)
        allure.attach(
            keyword,
            name="本次点击的大家都在搜AI推荐词",
            attachment_type=allure.attachment_type.TEXT,
        )
        search_page.tap_everyone_searching_keyword(keyword)
        search_page.wait_result_loaded(timeout=10)
        result_input = search_page.wait_result_keyword_filled(
            keyword,
            timeout=10,
        )
        assert search_page.wait_result_has_visible_content(timeout=10), (
            f"点击“大家都在搜”词“{keyword}”后，搜索结果页没有结果内容"
        )
        assert driver.wait_for_component(BY.text("暂无结果"), timeout=1) is None, (
            f"点击“大家都在搜”词“{keyword}”后出现空结果"
        )
        assert driver.wait_for_component(BY.text("加载失败"), timeout=1) is None, (
            f"点击“大家都在搜”词“{keyword}”后出现加载失败"
        )
        assert_visible_and_attach_highlight(
            driver,
            result_input,
            f"大家都在搜搜索结果-{keyword}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击搜索框右侧“×”清除按钮，返回搜索启动页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.CLEAR_INPUT_BUTTON_XPATH),
            "大家都在搜结果页-搜索框清除按钮",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_clear_input()
        assert driver.wait_for_component(
            BY.xpath(search_page.SEARCH_HISTORY_TITLE_XPATH),
            timeout=8,
        ), "清除大家都在搜搜索词后，未返回搜索启动页"
        assert driver.wait_for_component(
            BY.xpath(search_page.EVERYONE_SEARCHING_TITLE_XPATH),
            timeout=8,
        ), "清除大家都在搜搜索词后，未重新展示大家都在搜模块"
        assert driver.wait_for_component(
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            timeout=8,
        ), "清除大家都在搜搜索词后，未重新展示榜单模块"

    with allure.step("步骤5：点击榜单 POI 点“太平山顶”，进入对应详情页"):
        search_page.dismiss_keyboard()
        search_page.scroll_ranking_poi_into_view("太平山顶")
        search_page.tap_ranking_poi("太平山顶")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail_page.title_xpath("太平山顶")),
            "POI详情页-太平山顶",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤6：返回搜索启动页后，点击搜索历史词并进入搜索结果页"):
        poi_detail_page.tap_back_button("太平山顶")
        assert driver.wait_for_component(
            BY.xpath(search_page.SEARCH_HISTORY_TITLE_XPATH),
            timeout=8,
        ), "从太平山顶详情返回后，未回到搜索启动页"
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

    with allure.step("步骤7：点击搜索框右侧“×”清除按钮，回到搜索启动页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.CLEAR_INPUT_BUTTON_XPATH),
            "搜索框清除按钮",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_clear_input()
        assert driver.wait_for_component(
            BY.xpath(search_page.EVERYONE_SEARCHING_TITLE_XPATH),
            timeout=8,
        ), "清除搜索历史词后，未重新展示大家都在搜模块"
        assert driver.wait_for_component(
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            timeout=8,
        ), "清除搜索历史词后，未重新展示榜单模块"
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.search_start_input_xpath("中国香港")),
            "清除后搜索框或AI推荐词",
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

