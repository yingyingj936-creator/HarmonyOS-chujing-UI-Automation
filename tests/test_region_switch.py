import allure
from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage


@allure.feature("出境服务卡片")
@allure.story("切换出境目的地")
@allure.title("从香港切换为澳门")
def test_switch_region_to_macao(driver):
    """验证‘切换出境目的地’功能。"""
    home_page = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)

    with allure.step("步骤一：点击首页右上角地区选择器（香港）"):
        home_page.tap_region_selector()

    with allure.step("步骤二：验证跳转到选择旅行目的地页"):
        assert destination_page.is_loaded(), "未进入‘选择旅行目的地’页面"

    with allure.step("步骤三：选择澳门"):
        destination_page.choose_macao()

    with allure.step("断言一：页面自动返回出境服务卡片首页"):
        assert home_page.has_region_text("澳门"), "未返回首页或地区选择器未显示‘澳门’"

    with allure.step("断言二：首页地区选择器已刷新为澳门"):
        assert home_page.has_region_text("澳门"), "地区选择器文本未更新为‘澳门’"
