import allure
from hypium import BY

from pages.outbound_search import OutboundSearchPage
from utils.allure_visual import assert_visible_and_attach_highlight


HISTORY_KEYWORD = "香港"


def _ensure_history_keyword(
    driver,
    search_page: OutboundSearchPage,
    keyword: str,
) -> None:
    """确保单条执行时搜索启动页也具备指定历史词。"""
    history_selector = BY.xpath(search_page.history_keyword_xpath(keyword))
    if driver.wait_for_component(history_selector, timeout=2) is not None:
        return

    search_page.input_and_tap_search(keyword)
    if (
        driver.wait_for_component(
            BY.xpath(search_page.input_value_xpath(keyword)),
            timeout=8,
        )
        is None
    ):
        raise AssertionError(f"搜索“{keyword}”后输入框未保留关键词")

    search_page.tap_clear_input()
    if driver.wait_for_component(history_selector, timeout=8) is None:
        raise AssertionError(f"搜索历史中未生成“{keyword}”")


@allure.feature("搜索功能")
@allure.story("一键删除搜索历史")
def test_clear_search_history(driver) -> None:
    """验证一键删除后搜索历史模块和历史词均不再显示。"""
    search_page = OutboundSearchPage(driver)
    history_selector = BY.xpath(
        search_page.history_keyword_xpath(HISTORY_KEYWORD)
    )

    with allure.step("前置准备：进入搜索启动页并确保存在搜索记录"):
        search_page.tap_home_search()
        _ensure_history_keyword(driver, search_page, HISTORY_KEYWORD)
        search_page.dismiss_keyboard()

    with allure.step("步骤1：查看搜索启动页搜索历史"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.SEARCH_HISTORY_TITLE_XPATH),
            "搜索启动页-搜索历史模块",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            history_selector,
            f"搜索历史词-{HISTORY_KEYWORD}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击右侧一键删除按钮，搜索历史模块隐藏"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.CLEAR_HISTORY_BUTTON_XPATH),
            "搜索历史一键删除按钮",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_clear_history()

        assert search_page.wait_history_hidden(timeout=8), (
            "点击一键删除后，搜索历史模块仍然显示"
        )
        assert driver.wait_for_component(history_selector, timeout=1) is None, (
            f"点击一键删除后，搜索历史词“{HISTORY_KEYWORD}”仍然显示"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            "删除搜索历史后-必玩榜",
            timeout=8,
            attach_crop=False,
        )
