import allure
import pytest

from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage


@allure.feature("出境服务卡片")
@allure.story("切换出境目的地")
@pytest.mark.parametrize(
    "destination, expected_text",
    [("澳门", "澳门"), ("曼谷", "曼谷"), ("香港", "香港")],
)
def test_switch_region(driver, destination: str, expected_text: str) -> None:
    """验证‘切换出境目的地’功能。"""
    allure.dynamic.title(f"切换出境目的地为{destination}")

    home_page = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)

    with allure.step("步骤一：点击首页地区切换下拉按钮"):
        home_page.tap_region_selector()

    with allure.step("步骤二：验证跳转到选择旅行目的地页"):
        assert destination_page.is_loaded(), "未进入‘选择旅行目的地’页面"

    with allure.step(f"步骤三：选择目的地：{destination}"):
        destination_page.choose_destination(destination)

    with allure.step("断言一：页面自动返回出境服务卡片首页"):
        assert home_page.has_region_text(expected_text), (
            f"未返回首页或地区选择器未显示‘{expected_text}’"
        )

    with allure.step(f"断言二：首页地区选择器已刷新为{expected_text}"):
        assert home_page.has_region_text(expected_text), (
            f"地区选择器文本未更新为‘{expected_text}’"
        )
