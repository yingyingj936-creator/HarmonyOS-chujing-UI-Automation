import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务")
@allure.story("底部导航切换")
def test_switch_bottom_navigation_tabs(driver) -> None:
    """验证底部四个导航页签可切换并展示对应页面内容。"""
    navigation = BottomNavigation(driver)

    with allure.step("步骤1：点击底部导航“行程”，展示行程页"):
        navigation.tap_trip()
        assert_visible_and_attach_highlight(
            driver,
            BY.text(navigation.TRIP_MARKER_TEXT),
            "行程页-创建行程",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击底部导航“附近”，展示附近页"):
        navigation.tap_nearby()
        assert_visible_and_attach_highlight(
            driver,
            BY.text(navigation.NEARBY_MARKER_TEXT),
            "附近页-探索附近",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击底部导航“我的”，展示我的页"):
        navigation.tap_mine()
        assert_visible_and_attach_highlight(
            driver,
            BY.text(navigation.MINE_MARKER_TEXT),
            "我的页-小星星的旅程",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击底部导航“首页”，返回首页"):
        navigation.tap_home()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(navigation.HOME_MARKER_XPATH),
            "首页-搜索服务、地图、帖子",
            timeout=8,
            attach_crop=False,
        )
