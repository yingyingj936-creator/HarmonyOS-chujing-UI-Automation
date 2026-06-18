import allure
from hypium import BY

from pages.food_ordering import FoodOrderingPage
from pages.local_service import LocalServicePage
from pages.outbound_home import OutboundHomePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("本地服务")
@allure.story("掌上美食分类与商户跳转")
def test_food_ordering_categories_and_lige(driver) -> None:
    """验证掌上美食入口、分类刷新、商户服务和手势返回状态。"""
    home = OutboundHomePage(driver)
    local_service = LocalServicePage(driver)
    ordering_page = FoodOrderingPage(driver)
    service_page = ServiceDetailPage(driver)

    with allure.step("前置准备：从首页进入本地服务列表"):
        home.ensure_kingkong_first_page()
        home.tap_local_service_entry()
        local_service.wait_xpath(
            local_service.PAGE_TITLE_XPATH,
            "本地服务页标题“服务”",
            timeout=10,
        )

    with allure.step("步骤1：点击“美食”分类并查看掌上美食卡片"):
        local_service.tap_category("美食")
        local_service.wait_category_highlighted("美食", timeout=5)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(local_service.FOOD_ORDERING_CARD_XPATH),
            "美食分类-掌上美食卡片",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击掌上美食卡片，进入点餐列表"):
        local_service.tap_food_ordering_card()
        ordering_page.wait_xpath(
            ordering_page.PAGE_TITLE_XPATH,
            "点餐页标题",
            timeout=10,
        )
        initial_order_texts = ordering_page.wait_order_content(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(ordering_page.ORDER_CONTENT_XPATH),
            "掌上美食-点餐列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：依次切换海鲜、中餐、快餐分类"):
        previous_texts = initial_order_texts
        for index, category_name in enumerate(("海鲜", "中餐", "快餐")):
            ordering_page.tap_category(category_name)
            ordering_page.wait_category_highlighted(
                category_name,
                timeout=5,
            )
            previous_texts = ordering_page.wait_order_content(
                previous_texts=None if index == 0 else previous_texts,
                timeout=8,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(ordering_page.ORDER_CONTENT_XPATH),
                f"点餐-{category_name}分类高亮及商户刷新",
                timeout=8,
                attach_crop=False,
            )

    with allure.step("步骤4：点击快餐分类首个商户，进入商户服务"):
        merchant_name = ordering_page.tap_first_visible_order()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(service_page.title_xpath(merchant_name)),
            f"{merchant_name}服务页",
            timeout=15,
            attach_crop=False,
        )

    with allure.step("步骤5：系统侧滑返回，保持在快餐分类"):
        ordering_page.system_gesture_back()
        ordering_page.wait_xpath(
            ordering_page.PAGE_TITLE_XPATH,
            "返回后的点餐页",
            timeout=12,
        )
        ordering_page.wait_category_highlighted("快餐", timeout=5)
        ordering_page.wait_xpath(
            ordering_page.order_row_xpath(merchant_name),
            f"快餐分类中的“{merchant_name}”",
            timeout=8,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(ordering_page.ORDER_CONTENT_XPATH),
            "侧滑返回点餐列表-仍在快餐分类",
            timeout=8,
            attach_crop=False,
        )
