import allure
import pytest

from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage

CATEGORY_SWITCH_CASES = [
    pytest.param(
        "热门",
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Column[1]/Column[3]',
        '//*[@text="热门"]',
        "展示热门地区列表",
        id="hot-category",
    ),
    pytest.param(
        "港澳",
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Column[1]/Column[4]',
        '//*[@text="港澳"]',
        "展示港澳地区列表",
        id="hk-macao-category",
    ),
    pytest.param(
        "当前/历史",
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Column[1]/Column[2]',
        '//*[@id="zycnb"]/NavigationContent[1]/NavDestination[1]/NavDestinationContent[1]/Column[1]/Stack[1]/SideBarContainer[1]/Row[1]/List[1]/ListItemGroup[1]/Grid[1]/GridItem[1]/Row[1]/Image[1]',
        "展示当前定位地区区域",
        id="current-history-category",
    ),
]


@allure.feature("选择目的地")
@allure.story("左侧分类切换")
@pytest.mark.parametrize(
    "tab_name, click_xpath, assert_xpath, assert_desc",
    CATEGORY_SWITCH_CASES,
)
def test_destination_category_switch(
    driver,
    tab_name: str,
    click_xpath: str,
    assert_xpath: str,
    assert_desc: str,
) -> None:
    """验证‘选择目的地’页面左侧分类切换功能。"""
    allure.dynamic.title(f"左侧分类切换-{tab_name}")

    home_page = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)

    with allure.step("步骤一：点击首页地区切换下拉按钮"):
        home_page.tap_region_selector()

    with allure.step("步骤二：验证跳转到选择旅行目的地页"):
        assert destination_page.is_loaded(), "未进入‘选择旅行目的地’页面"

    with allure.step(f"步骤三：点击左侧分类【{tab_name}】"):
        destination_page.tap_by_xpath(click_xpath, tab_name)

    with allure.step(f"断言：{assert_desc}"):
        assert destination_page.is_element_displayed_by_xpath(assert_xpath, tab_name), (
            f"分类‘{tab_name}’切换后未正确展示内容，期望元素 xpath：{assert_xpath}"
        )
