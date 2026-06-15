import allure
from hypium import BY

from pages.local_service import LocalServicePage
from pages.outbound_home import OutboundHomePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务卡片")
@allure.story("首页本地服务分类与 BBC News")
def test_local_service_categories_and_bbc_news(driver) -> None:
    """验证本地服务列表、分类刷新和 BBC News 服务跳转。"""
    home = OutboundHomePage(driver)
    local_service = LocalServicePage(driver)
    service_page = ServiceDetailPage(driver)
    initial_service_texts = ()

    with allure.step("前置准备：恢复金刚区默认第一屏"):
        home.ensure_kingkong_first_page()

    with allure.step("步骤1：点击首页金刚区“本地服务”"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.LOCAL_SERVICE_ENTRY_XPATH),
            "首页金刚区-本地服务入口",
            timeout=8,
            attach_crop=False,
        )
        home.tap_local_service_entry()

    with allure.step("步骤2：查看本地服务分类与右侧服务列表"):
        local_service.wait_xpath(
            local_service.PAGE_TITLE_XPATH,
            "本地服务页标题“服务”",
            timeout=10,
        )
        for category_name in ("入境", "出行", "美食"):
            local_service.wait_xpath(
                local_service.category_xpath(category_name),
                f"左侧分类“{category_name}”",
                timeout=8,
            )
        initial_service_texts = local_service.wait_service_content(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(local_service.SERVICE_CONTAINER_XPATH),
            "本地服务-分类与服务列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：依次切换美食、住宿、其他分类"):
        previous_texts = initial_service_texts
        for category_name in ("美食", "住宿", "其他"):
            local_service.tap_category(category_name)
            local_service.wait_category_highlighted(
                category_name,
                timeout=5,
            )
            previous_texts = local_service.wait_service_content(
                previous_texts=previous_texts,
                timeout=8,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(local_service.SERVICE_CONTAINER_XPATH),
                f"本地服务-{category_name}分类高亮及服务刷新",
                timeout=8,
                attach_crop=False,
            )

    with allure.step("步骤4：点击 BBC News 并进入对应服务"):
        local_service.tap_bbc_news()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(service_page.title_xpath("BBC News")),
            "BBC News服务页",
            timeout=15,
            attach_crop=False,
        )
