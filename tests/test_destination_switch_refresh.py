from dataclasses import dataclass

import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage
from utils.allure_visual import assert_visible_and_attach_highlight


@dataclass(frozen=True)
class DestinationRefreshCase:
    destination: str
    nearby_region_text: str


DESTINATION_CASES = (
    DestinationRefreshCase(
        destination="中国澳门",
        nearby_region_text="中国澳门",
    ),
    DestinationRefreshCase(
        destination="温哥华",
        nearby_region_text="温哥华",
    ),
    DestinationRefreshCase(
        destination="中国香港",
        nearby_region_text="中国香港",
    ),
)


def _nearby_region_xpath(region_text: str) -> str:
    return f'//*[@id="NearRootId"]//Text[@text="{region_text}"]'


@allure.feature("出境服务")
@allure.story("连续切换目的地刷新首页与附近数据")
def test_destination_switch_refresh_home_and_nearby(driver) -> None:
    """验证连续切换目的地后，首页瀑布流与附近页地区数据刷新。"""
    home_page = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)
    navigation = BottomNavigation(driver)

    for case in DESTINATION_CASES:
        with allure.step(f"切换目的地为“{case.destination}”"):
            home_page.tap_region_selector()
            assert_visible_and_attach_highlight(
                driver,
                BY.text(destination_page.PAGE_TITLE_TEXT),
                "目的地选择页-选择旅行目的地",
                timeout=8,
                attach_crop=False,
            )
            destination_page.choose_destination(case.destination)

        with allure.step(f"校验首页刷新为“{case.destination}”"):
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home_page.region_dropdown_xpath(case.destination)),
                f"首页左上角地区-{case.destination}",
                timeout=8,
                attach_crop=False,
            )
            card = home_page.find_visible_guide_for_destination(case.destination)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home_page.guide_cover_xpath(card.post_id)),
                f"首页瀑布流目的地-{case.destination}-{card.title}",
                timeout=8,
                attach_crop=False,
            )

        with allure.step(f"校验附近页刷新为“{case.nearby_region_text}”"):
            navigation.tap_nearby()
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(_nearby_region_xpath(case.nearby_region_text)),
                f"附近页左上角地区-{case.nearby_region_text}",
                timeout=8,
                attach_crop=False,
            )

        with allure.step("通过底部导航返回首页，准备下一次目的地切换"):
            navigation.tap_home()
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home_page.region_dropdown_xpath(case.destination)),
                f"返回首页-{case.destination}",
                timeout=8,
                attach_crop=False,
            )
            home_page.restore_top()
