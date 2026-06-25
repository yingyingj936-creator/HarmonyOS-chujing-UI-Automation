import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务")
@allure.story("附近页左侧分类切换")
def test_nearby_category_switch_refreshes_list_and_map(driver) -> None:
    """验证附近页左侧分类切换后，地图和 POI 列表同步刷新。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)

    with allure.step("前置准备：进入底部导航“附近”页"):
        navigation.tap_nearby()
        nearby.wait_loaded(timeout=10)
        current_names = nearby.wait_poi_names_loaded(minimum=2, timeout=8)
        allure.attach(
            "\n".join(current_names),
            name="附近页-初始可见POI",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.EXPLORE_NEARBY_XPATH),
            "附近页-初始分类-探索附近",
            timeout=8,
            attach_crop=False,
        )

    category_cases: tuple[tuple[str, str, str, tuple[str, ...]], ...] = (
        ("步骤1", "找酒店", "酒店", ("酒店", "住宿", "hotel", "artus")),
        ("步骤2", "必玩榜", "景点", ("博物馆", "文化", "码头", "景点", "太平山", "维多利亚", "迪士尼", "星光大道")),
        ("步骤3", "找美食", "美食", ("餐厅", "Arabica", "Café", "Cafe", "Bakery", "轩", "唐阁", "酒廊", "冰室")),
    )

    for step_label, category_name, data_type, expected_keywords in category_cases:
        with allure.step(f"{step_label}：点击左侧“{category_name}”，校验刷新为{data_type}相关数据"):
            visible_categories_before_tap = nearby.visible_left_category_names()
            allure.attach(
                "\n".join(visible_categories_before_tap),
                name=f"{step_label}-点击前左侧可见分类",
                attachment_type=allure.attachment_type.TEXT,
            )
            current_names = nearby.tap_category_and_wait_refresh(
                category_name,
                previous_poi_names=current_names,
                expected_keywords=expected_keywords,
                timeout=10,
            )
            assert nearby.names_match_keywords(current_names, expected_keywords), (
                f"点击“{category_name}”后，POI列表未展示{data_type}相关数据：{current_names}"
            )
            allure.attach(
                "\n".join(current_names),
                name=f"{step_label}-附近页-{category_name}-可见POI",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(nearby.category_text_xpath(category_name)),
                f"{step_label}-附近页-左侧分类-{category_name}",
                timeout=8,
                attach_crop=False,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(nearby.MAP_XPATH),
                f"{step_label}-附近页-{category_name}-地图区域",
                timeout=8,
                attach_crop=False,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(nearby.POI_LIST_XPATH),
                f"{step_label}-附近页-{category_name}-POI列表",
                timeout=8,
                attach_crop=False,
            )
