import allure
from hypium import BY

from pages.local_service import LocalServicePage
from pages.multitask import MultiTaskPage
from pages.outbound_home import OutboundHomePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务卡片")
@allure.story("从三方服务通过多任务返回首页")
def test_return_home_from_papago_multitask(driver) -> None:
    """验证打开 Papago+ 后可通过多任务固定首页卡片返回首页。"""
    home = OutboundHomePage(driver)
    local_service = LocalServicePage(driver)
    service_page = ServiceDetailPage(driver)
    multitask = MultiTaskPage(driver)
    service_name = "Papago+"

    try:
        with allure.step("步骤1：从首页打开 Papago+ 服务"):
            home.ensure_kingkong_first_page()
            home.tap_local_service_entry()
            local_service.wait_xpath(
                local_service.PAGE_TITLE_XPATH,
                "本地服务页标题“服务”",
                timeout=10,
            )
            local_service.tap_service(service_name)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(service_page.title_xpath(service_name)),
                "Papago+服务拉起成功",
                timeout=15,
                attach_crop=False,
            )

        with allure.step("步骤2：点击多任务按钮，拉起多任务列表"):
            multitask.open()
            multitask.wait_xpath(
                multitask.HOME_CARD_XPATH,
                "多任务列表中的出境服务首页",
                timeout=8,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(multitask.PANEL_XPATH),
                "Papago+内拉起多任务列表",
                timeout=8,
                attach_crop=False,
            )

        with allure.step("步骤3：点击列表第一个出境服务首页"):
            multitask.tap_home_card()
            multitask.wait_closed(timeout=8)
            assert home.wait_first_screen_loaded(timeout=8), (
                "点击多任务列表中的出境服务首页后未返回卡片首页"
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.SEARCH_BAR_XPATH),
                "多任务切换成功-返回出境服务首页",
                timeout=8,
                attach_crop=False,
            )
    finally:
        if multitask.is_open():
            try:
                multitask.close()
                multitask.wait_closed(timeout=3)
            except RuntimeError:
                driver.press_back()
