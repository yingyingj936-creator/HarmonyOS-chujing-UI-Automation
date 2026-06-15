import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.scenic_service import ScenicServicePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务卡片")
@allure.story("首页金刚区景区门票与第二屏服务")
def test_scenic_ticket_and_youtube_entries(driver) -> None:
    """验证景区门票入口、金刚区第二屏及 YouTube 服务跳转。"""
    home = OutboundHomePage(driver)
    scenic_page = ScenicServicePage(driver)
    service_page = ServiceDetailPage(driver)

    with allure.step("前置准备：恢复金刚区默认第一屏"):
        home.ensure_kingkong_first_page()

    with allure.step("步骤1：查看首页金刚区入口及默认第一屏"):
        home.wait_xpath(
            home.SERVICE_TAB_ROW_XPATH,
            "首页、酒店、火车Tab",
            timeout=8,
        )
        home.wait_xpath(
            home.SCENIC_TICKET_ENTRY_XPATH,
            "金刚区第一屏“景区门票”",
            timeout=8,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.HOME_RECOMMENDS_SECTION_XPATH),
            "首页金刚区-顶部Tab与默认第一屏",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击“景区门票”，进入景区列表"):
        home.tap_scenic_ticket_entry()
        scenic_page.wait_xpath(
            scenic_page.FIRST_SCENIC_XPATH,
            "景区列表首项“香港迪士尼乐园”",
            timeout=15,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(scenic_page.LIST_WEB_XPATH),
            "景区门票-景区列表",
            timeout=15,
            attach_crop=False,
        )

    with allure.step("步骤3：点击页面内返回按钮回到首页"):
        scenic_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.SEARCH_BAR_XPATH),
            "景区列表返回首页-搜索框",
            timeout=12,
            attach_crop=False,
        )

    with allure.step("步骤4：横向滑动金刚区到第二屏"):
        home.swipe_kingkong_to_second_page()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.KINGKONG_ENTRY_GRID_XPATH),
            "金刚区第二屏-YouTube等服务",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：点击 YouTube，进入 YouTube 服务"):
        home.tap_youtube_entry()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(service_page.title_xpath("YouTube")),
            "YouTube服务页",
            timeout=15,
            attach_crop=False,
        )
