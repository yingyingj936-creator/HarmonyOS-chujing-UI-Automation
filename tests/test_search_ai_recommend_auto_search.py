import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.outbound_search import OutboundSearchPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("搜索功能")
@allure.story("AI推荐词自动搜索")
@allure.title("TC-SEARCH-001 验证搜索框AI推荐词自动搜索功能")
def test_search_ai_recommend_keyword_auto_search(driver) -> None:
    """验证点击搜索启动页搜索按钮后，AI 推荐词可自动填充并触发搜索。"""
    home_page = OutboundHomePage(driver)
    search_page = OutboundSearchPage(driver)

    with allure.step("步骤1：在首页顶部点击搜索输入框，进入搜索启动页并展示AI推荐词"):
        home_page.wait_xpath(home_page.SEARCH_BAR_XPATH, "首页顶部搜索框", timeout=8)
        search_page.tap_home_search()
        search_page.wait_search_start_loaded(timeout=8)
        recommend_keyword, recommend_input = (
            search_page.current_ai_recommend_keyword(timeout=8)
        )
        assert_visible_and_attach_highlight(
            driver,
            recommend_input,
            f"搜索启动页AI推荐词-{recommend_keyword}",
            timeout=8,
            attach_crop=False,
        )
        assert driver.wait_for_component(
            BY.xpath(search_page.KEYBOARD_PANEL_XPATH),
            timeout=3,
        ), "进入搜索启动页后，搜索框未自动获得焦点或键盘未弹出"
        allure.attach(
            recommend_keyword,
            name="本次读取到的AI推荐词",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("步骤2：查看搜索启动页加载完成，无白屏或加载失败"):
        assert driver.wait_for_component(BY.text("加载失败"), timeout=1) is None, (
            "搜索启动页出现加载失败提示"
        )
        assert driver.wait_for_component(BY.text("网络异常"), timeout=1) is None, (
            "搜索启动页出现网络异常提示"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            "搜索启动页-榜单模块",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击搜索按钮，AI推荐词自动搜索并展示相关结果"):
        search_page.tap_search_button()
        search_page.wait_result_loaded(timeout=10)
        result_input = search_page.wait_result_keyword_filled(
            recommend_keyword,
            timeout=10,
        )
        result_content = search_page.wait_result_has_visible_content(timeout=10)
        assert driver.wait_for_component(BY.text("暂无结果"), timeout=1) is None, (
            "AI推荐词搜索后出现空结果"
        )
        assert driver.wait_for_component(BY.text("加载失败"), timeout=1) is None, (
            "AI推荐词搜索后出现加载失败"
        )
        assert_visible_and_attach_highlight(
            driver,
            result_input,
            f"搜索结果页顶部关键词-{recommend_keyword}",
            timeout=8,
            attach_crop=False,
        )
        allure.attach(
            f"AI推荐词：{recommend_keyword}\n结果内容组件：{result_content.getBounds()}",
            name="AI推荐词搜索结果校验",
            attachment_type=allure.attachment_type.TEXT,
        )
