import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务")
@allure.story("附近页默认内容与列表滑动")
def test_nearby_page_default_content_and_list_scroll(driver) -> None:
    """验证附近页可打开，默认内容展示完整，且列表可上滑查看更多 POI。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)

    with allure.step("步骤1：点击底部导航“附近”，打开附近页"):
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
            BY.xpath(nearby.EXPLORE_NEARBY_XPATH),
            "附近页-探索附近分类",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看附近页地区、地图、找美食分类和POI列表"):
        region_text = nearby.current_region_text(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.region_xpath(region_text)),
            f"附近页-左上角当前地区-{region_text}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.MAP_XPATH),
            "附近页-地图区域",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.FOOD_CATEGORY_XPATH),
            "附近页-找美食分类",
            timeout=8,
            attach_crop=False,
        )
        before_names = nearby.wait_poi_names_loaded(minimum=3, timeout=8)
        allure.attach(
            "\n".join(before_names),
            name="附近页-滑动前可见POI",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            "附近页-POI列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：上滑附近列表，查看更多POI卡片"):
        after_names, scroll_result = nearby.swipe_poi_list_until_more(
            before_names,
            max_swipes=5,
        )
        new_names = tuple(name for name in after_names if name not in before_names)
        assert after_names, "上滑附近列表后POI列表为空"
        allure.attach(
            f"滑动结果：{scroll_result}\n\n" + "\n".join(after_names),
            name="附近页-滑动后可见POI",
            attachment_type=allure.attachment_type.TEXT,
        )
        highlight_name = (
            f"附近页-滑动后POI列表-新增{new_names[0]}"
            if new_names
            else f"附近页-滑动后POI列表-{scroll_result}"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            highlight_name,
            timeout=8,
            attach_crop=False,
        )
