import allure
from hypium import BY

from pages.local_service import LocalServicePage
from pages.outbound_home import OutboundHomePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("本地服务")
@allure.story("服务列表搜索与清除")
def test_local_service_search_and_clear(driver) -> None:
    """验证本地服务搜索、第二条结果跳转、侧滑返回和清除。"""
    home = OutboundHomePage(driver)
    local_service = LocalServicePage(driver)
    service_page = ServiceDetailPage(driver)
    keyword = "U"
    second_result = "Dufry"

    with allure.step("前置准备：从首页进入本地服务列表"):
        home.ensure_kingkong_first_page()
        home.tap_local_service_entry()
        local_service.wait_xpath(
            local_service.PAGE_TITLE_XPATH,
            "本地服务页标题“服务”",
            timeout=10,
        )

    with allure.step("步骤1：点击搜索服务输入框，确认输入框可用"):
        local_service.tap_search_input()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(local_service.SEARCH_INPUT_XPATH),
            "本地服务-搜索输入框已激活",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：输入“U”并点击搜索，仅展示匹配服务"):
        local_service.input_search_keyword(keyword)
        local_service.tap_search_button()
        result_names = local_service.wait_search_results_match(
            keyword,
            timeout=8,
        )
        assert "YouTube" in result_names, (
            f"搜索结果预期包含 YouTube，实际为：{result_names}"
        )
        assert second_result in result_names, (
            f"搜索结果预期包含 {second_result}，实际为：{result_names}"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(local_service.search_result_row_xpath(second_result)),
            "本地服务-U搜索结果第二条-Dufry",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击列表第2个结果，进入 Dufry 服务"):
        local_service.tap_search_result(second_result)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(service_page.title_xpath(second_result)),
            "Dufry服务页",
            timeout=15,
            attach_crop=False,
        )

    with allure.step("步骤4：侧滑返回并点击输入框清空按钮，清除搜索结果"):
        local_service.system_gesture_back()
        local_service.wait_xpath(
            local_service.search_result_row_xpath(second_result),
            "返回后的Dufry搜索结果",
            timeout=12,
        )
        local_service.tap_clear_search()
        local_service.wait_search_cleared(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(local_service.SERVICE_CONTAINER_XPATH),
            "清除搜索-恢复默认本地服务列表",
            timeout=8,
            attach_crop=False,
        )


