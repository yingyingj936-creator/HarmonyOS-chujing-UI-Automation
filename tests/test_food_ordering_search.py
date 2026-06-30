import allure
from hypium import BY

from pages.food_ordering import FoodOrderingPage
from pages.local_service import LocalServicePage
from pages.outbound_home import OutboundHomePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


@allure.feature("本地服务")
@allure.story("掌上美食服务搜索与清除")
def test_food_ordering_search_and_clear(driver) -> None:
    """验证点餐服务搜索、服务跳转、侧滑返回和搜索清除。"""
    home = OutboundHomePage(driver)
    local_service = LocalServicePage(driver)
    ordering_page = FoodOrderingPage(driver)
    service_page = ServiceDetailPage(driver)
    service_name = "ONE POKE ROCK"

    with allure.step("前置准备：从首页进入掌上美食点餐列表"):
        home.ensure_kingkong_first_page()
        home.tap_local_service_entry()
        local_service.wait_xpath(
            local_service.PAGE_TITLE_XPATH,
            "本地服务页标题“服务”",
            timeout=10,
        )
        local_service.tap_category("美食")
        local_service.wait_category_highlighted("美食", timeout=5)
        food_ordering_card = local_service.ensure_food_ordering_card_visible(
            timeout=8
        )
        attach_highlighted_bounds(
            driver,
            food_ordering_card.getBounds(),
            "前置准备-掌上美食卡片",
        )
        local_service.tap_food_ordering_card(food_ordering_card)
        ordering_page.wait_xpath(
            ordering_page.PAGE_TITLE_XPATH,
            "点餐页标题",
            timeout=10,
        )

    with allure.step("步骤1：在搜索框输入“ONE”，展示相关搜索结果"):
        ordering_page.input_search_keyword("ONE")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(ordering_page.search_result_row_xpath(service_name)),
            "点餐搜索-ONE相关结果",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击搜索结果第一条，进入对应服务"):
        ordering_page.tap_search_result(service_name)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(service_page.title_xpath(service_name)),
            "ONE-POKE-ROCK服务页",
            timeout=15,
            attach_crop=False,
        )

    with allure.step("步骤3：系统侧滑返回搜索结果页"):
        ordering_page.system_gesture_back()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(ordering_page.search_result_row_xpath(service_name)),
            "侧滑返回-ONE搜索结果仍展示",
            timeout=12,
            attach_crop=False,
        )

    with allure.step("步骤4：点击搜索框清空按钮，清除搜索结果"):
        ordering_page.tap_clear_search()
        ordering_page.wait_search_cleared(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(ordering_page.ORDER_CONTENT_XPATH),
            "清除搜索-恢复默认点餐列表",
            timeout=8,
            attach_crop=False,
        )

