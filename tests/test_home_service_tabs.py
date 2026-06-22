import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务卡片")
@allure.story("首页金刚区酒店与火车入口")
def test_home_hotel_and_train_entries(driver) -> None:
    """验证首页酒店、火车标签内容及对应查询页面可正常打开。"""
    home = OutboundHomePage(driver)

    with allure.step("步骤1：查看首页金刚区入口"):
        home.ensure_kingkong_first_page()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.SERVICE_TAB_ROW_XPATH),
            "首页金刚区-首页酒店火车Tab",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击酒店标签，展示酒店查询内容"):
        home.tap_service_tab("酒店")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.HOTEL_QUERY_BUTTON_XPATH),
            "酒店Tab-查询酒店",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击“查询酒店”，进入酒店查询页"):
        home.tap_hotel_query()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.HOTEL_RESULTS_FILTER_XPATH),
            "酒店查询页-价格等级筛选",
            timeout=15,
            attach_crop=False,
        )

    with allure.step("流程衔接：返回首页，继续验证火车入口"):
        driver.press_back()
        home.wait_xpath(home.HOME_ROOT_XPATH, "出境服务首页", timeout=12)

    with allure.step("步骤4：点击火车标签，展示火车票查询内容"):
        home.tap_service_tab("火车")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.TRAIN_QUERY_BUTTON_XPATH),
            "火车Tab-查询火车票",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：点击“目的地”，进入火车票目的地页"):
        home.tap_train_destination()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.TRAIN_DESTINATION_PAGE_TITLE_XPATH),
            "火车票查询页-目的地",
            timeout=15,
            attach_crop=False,
        )


