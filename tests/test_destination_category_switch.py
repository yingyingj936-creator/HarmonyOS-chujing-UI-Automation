import allure

from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage


@allure.feature("选择目的地")
@allure.story("左侧分类切换")
def test_destination_category_switch_flow(driver) -> None:
    """验证‘选择目的地’页面左侧分类切换流程（单用例多步骤）。"""
    home_page = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)

    with allure.step("步骤一：进入选择目的地页"):
        home_page.tap_region_selector()
        assert destination_page.is_loaded(), "未进入‘选择旅行目的地’页面"

    with allure.step("步骤二：点击热门分类，并校验热门地区列表展示"):
        destination_page.tap_hot_category()
        assert destination_page.is_hot_section_displayed(), "点击‘热门’后未展示热门地区列表"

    with allure.step("步骤三：点击港澳分类，并校验港澳地区列表展示"):
        destination_page.tap_hk_macao_category()
        assert destination_page.is_hk_macao_section_displayed(), (
            "点击‘港澳’后未展示港澳地区列表"
        )

    with allure.step("步骤四：点击当前/历史，并校验当前定位地区区域展示"):
        destination_page.tap_first_current_history_entry()
        assert destination_page.is_current_location_section_displayed(), (
            "点击‘当前/历史’后未展示当前定位地区区域"
        )
