import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.taxi_service import TaxiServicePage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务卡片")
@allure.story("首页金刚区打车服务入口")
def test_taxi_service_entry_and_uber_navigation(driver) -> None:
    """验证首页打车入口、Uber 服务及两级返回流程。"""
    home = OutboundHomePage(driver)
    taxi_page = TaxiServicePage(driver)

    with allure.step("步骤1：查看首页金刚区入口"):
        home.ensure_kingkong_first_page()
        for entry_name in ("乘车码", "打车", "境外上网"):
            home.wait_xpath(
                f'{home.HOME_RECOMMENDS_SECTION_XPATH}'
                f'//Text[@text="{entry_name}"]',
                f"首页金刚区“{entry_name}”入口",
                timeout=8,
            )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.KINGKONG_ENTRY_GRID_XPATH),
            "首页金刚区-乘车码打车境外上网",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击“打车”，展示打车应用列表"):
        home.tap_taxi_entry()
        taxi_page.wait_xpath(
            taxi_page.GAODE_APP_XPATH,
            "高德打车",
            timeout=10,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(taxi_page.APP_LIST_XPATH),
            "打车应用列表-高德打车Uber",
            timeout=10,
            attach_crop=False,
        )

    with allure.step("步骤3：点击 Uber，进入 Uber 服务"):
        taxi_page.tap_uber()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(taxi_page.UBER_PAGE_TITLE_XPATH),
            "Uber服务页",
            timeout=15,
            attach_crop=False,
        )

    with allure.step("步骤4：系统侧滑返回打车应用列表"):
        taxi_page.system_gesture_back()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(taxi_page.PAGE_TITLE_XPATH),
            "侧滑返回-打车应用列表",
            timeout=12,
            attach_crop=False,
        )

    with allure.step("步骤5：点击页面内返回按钮回到首页"):
        taxi_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.SEARCH_BAR_XPATH),
            "返回首页-搜索框",
            timeout=12,
            attach_crop=False,
        )
