import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务")
@allure.story("附近页排序切换")
def test_nearby_sort_by_rating_and_distance(driver) -> None:
    """验证附近页可在距离优先和评分优先之间切换，并按目标规则排序。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)

    with allure.step("前置准备：进入底部导航“附近”页，确认默认距离优先"):
        navigation.tap_nearby()
        nearby.wait_loaded(timeout=10)
        distance_records = nearby.wait_poi_records_sorted_by_distance(
            minimum=3,
            timeout=10,
        )
        allure.attach(
            nearby.format_poi_records(distance_records),
            name="附近页-默认距离优先POI记录",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.sort_text_xpath("距离优先")),
            "附近页-默认排序-距离优先",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            "附近页-默认距离优先POI列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击“距离优先”，选择“评分优先”，校验列表按评分从高到低排列"):
        nearby.open_sort_dropdown("距离优先", timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.sort_option_xpath("评分优先")),
            "附近页-排序选项-评分优先",
            timeout=8,
            attach_crop=False,
        )
        nearby.tap_sort_option("评分优先", timeout=8)
        rating_records = nearby.wait_poi_records_sorted_by_rating(
            minimum=3,
            timeout=12,
        )
        assert nearby.records_sorted_by_rating_desc(rating_records), (
            "选择评分优先后，当前可见POI未按评分从高到低排列："
            f"{nearby.format_poi_records(rating_records)}"
        )
        allure.attach(
            nearby.format_poi_records(rating_records),
            name="附近页-评分优先POI记录",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.sort_text_xpath("评分优先")),
            "附近页-当前排序-评分优先",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            "附近页-评分优先POI列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：重新选择“距离优先”，校验列表按距离从近到远排列"):
        nearby.open_sort_dropdown("评分优先", timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.sort_option_xpath("距离优先")),
            "附近页-排序选项-距离优先",
            timeout=8,
            attach_crop=False,
        )
        nearby.tap_sort_option("距离优先", timeout=8)
        distance_records = nearby.wait_poi_records_sorted_by_distance(
            minimum=3,
            timeout=12,
        )
        assert nearby.records_sorted_by_distance_asc(distance_records), (
            "重新选择距离优先后，当前可见POI未按距离从近到远排列："
            f"{nearby.format_poi_records(distance_records)}"
        )
        allure.attach(
            nearby.format_poi_records(distance_records),
            name="附近页-重新距离优先POI记录",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.sort_text_xpath("距离优先")),
            "附近页-当前排序-距离优先",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            "附近页-重新距离优先POI列表",
            timeout=8,
            attach_crop=False,
        )
