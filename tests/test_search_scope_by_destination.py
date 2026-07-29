import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.outbound_search import OutboundSearchPage
from pages.select_destination import SelectDestinationPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("搜索功能")
@allure.story("搜索范围随目的地切换")
def test_search_scope_updates_with_destination(driver) -> None:
    """验证搜索提示和搜索结果随首页目的地从中国香港切换到泰国。"""
    home_page = OutboundHomePage(driver)
    search_page = OutboundSearchPage(driver)
    destination_page = SelectDestinationPage(driver)

    with allure.step("前置准备：确保当前首页目的地为中国香港"):
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

    with allure.step("步骤1：在中国香港首页点击搜索框"):
        search_page.tap_home_search()

    with allure.step("步骤2：校验搜索框展示目的地提示或 AI 推荐词"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.search_start_input_xpath("中国香港")),
            "搜索框-中国香港范围或AI推荐词",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：输入“香港”并点击搜索，校验香港相关结果"):
        search_page.input_and_tap_search("香港")
        assert_visible_and_attach_highlight(
            driver,
            BY.text("香港经典一日游"),
            "香港搜索结果-香港经典一日游",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击搜索页内返回按钮回首页"):
        search_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.region_dropdown_xpath("中国香港")),
            "返回首页-中国香港",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：切换首页目的地为泰国"):
        home_page.tap_region_selector()
        assert_visible_and_attach_highlight(
            driver,
            BY.text(destination_page.PAGE_TITLE_TEXT),
            "目的地选择页-选择旅行目的地",
            timeout=8,
            attach_crop=False,
        )
        destination_page.choose_destination("泰国")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.region_dropdown_xpath("泰国")),
            "首页目的地-泰国",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤6：在泰国首页点击搜索框"):
        search_page.tap_home_search()

    with allure.step("步骤7：校验搜索框展示目的地提示或 AI 推荐词"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.search_start_input_xpath("泰国")),
            "搜索框-泰国范围或AI推荐词",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤8：输入“泰国”并点击搜索，校验泰国相关结果"):
        search_page.input_and_tap_search("泰国")
        assert_visible_and_attach_highlight(
            driver,
            BY.text("泰国国家博物馆"),
            "泰国搜索结果-泰国国家博物馆",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤9：点击搜索页内返回按钮回首页"):
        search_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.region_dropdown_xpath("泰国")),
            "返回首页-泰国",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("清理：恢复首页目的地为中国香港"):
        home_page.tap_region_selector()
        destination_page.choose_destination("中国香港")
