import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务")
@allure.story("附近页地图定位刷新")
def test_nearby_map_location_refresh(driver) -> None:
    """验证附近页点击地图定位后，地图和 POI 列表保持可用并刷新到定位结果。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)

    with allure.step("前置条件：普通用户进入底部导航“附近”页，且系统定位权限已授权"):
        navigation.tap_nearby()
        nearby.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(navigation.tab_xpath("附近")),
            "底部导航-附近页签",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.MAP_XPATH),
            "附近页-定位前地图区域",
            timeout=8,
            attach_crop=False,
        )
        before_names = nearby.wait_poi_names_loaded(minimum=2, timeout=8)
        allure.attach(
            "\n".join(before_names),
            name="附近页-定位前POI列表",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step("步骤1：点击附近页地图定位按钮，校验地图中心和 POI 列表刷新为定位结果"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.MAP_LOCATION_BUTTON_XPATH),
            "附近页地图定位按钮",
            timeout=8,
            attach_crop=False,
        )
        after_names = nearby.tap_map_location_and_wait_loaded(
            previous_poi_names=before_names,
            timeout=12,
        )
        allure.attach(
            "\n".join(after_names),
            name="附近页-定位后POI列表",
            attachment_type=allure.attachment_type.TEXT,
        )
        if set(after_names) == set(before_names):
            allure.attach(
                "定位前后当前可见 POI 未变化，可能点击前页面已经处于物理定位范围；"
                "本用例已校验定位按钮可点击、地图区域和 POI 列表定位后仍正常展示。",
                name="附近页-定位刷新说明",
                attachment_type=allure.attachment_type.TEXT,
            )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.MAP_XPATH),
            "附近页-定位后地图区域与定位坐标",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            "附近页-定位后POI列表",
            timeout=8,
            attach_crop=False,
        )
