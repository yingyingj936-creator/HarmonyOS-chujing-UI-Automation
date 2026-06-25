import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务")
@allure.story("附近页切换目的地同步刷新首页")
def test_nearby_destination_switch_to_thailand(driver) -> None:
    """验证在附近页切换目的地为泰国后，附近页和首页数据同步刷新。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)
    destination_page = SelectDestinationPage(driver)
    home_page = OutboundHomePage(driver)

    with allure.step("前置准备：进入底部导航“附近”页"):
        navigation.tap_nearby()
        nearby.wait_loaded(timeout=10)
        before_region = nearby.current_region_text(timeout=8)
        before_poi_names = nearby.wait_poi_names_loaded(minimum=2, timeout=8)
        allure.attach(
            f"切换前地区：{before_region}\n\n" + "\n".join(before_poi_names),
            name="附近页-切换前地区和POI",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.region_xpath(before_region)),
            f"附近页-切换前地区-{before_region}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击附近页左上角切换地区入口，显示选择目的地页"):
        nearby.tap_region_selector(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.text(destination_page.PAGE_TITLE_TEXT),
            "目的地选择页-选择旅行目的地",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击“泰国”，校验附近页地图和列表刷新为泰国数据"):
        destination_page.choose_destination("泰国")
        after_poi_names = nearby.wait_region_refreshed(
            "泰国",
            previous_poi_names=before_poi_names,
            timeout=12,
        )
        allure.attach(
            "切换后地区：泰国\n\n" + "\n".join(after_poi_names),
            name="附近页-泰国POI列表",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.region_xpath("泰国")),
            "附近页-左上角地区-泰国",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.MAP_XPATH),
            "附近页-泰国地图区域",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            "附近页-泰国POI列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：返回首页，校验首页左上角地区同步为泰国并刷新首页数据"):
        navigation.tap_home()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.region_dropdown_xpath("泰国")),
            "首页左上角地区-泰国",
            timeout=8,
            attach_crop=False,
        )
        card = home_page.find_visible_guide_for_destination("泰国", max_swipes=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.guide_cover_xpath(card.post_id)),
            f"首页泰国攻略卡片-{card.title}",
            timeout=8,
            attach_crop=False,
        )
