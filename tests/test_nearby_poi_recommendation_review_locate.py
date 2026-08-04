import time

import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from pages.poi_detail import PoiDetailPage
from pages.post_detail import PostDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


def _return_from_service_to_poi_detail(
    driver,
    poi_detail: PoiDetailPage,
    poi_name: str,
) -> None:
    """从关联元服务返回 POI 详情，逐次返回并确认，避免服务页返回动画未完成导致误判。"""
    title_selector = BY.xpath(poi_detail.title_xpath(poi_name))
    for index in range(4):
        if driver.wait_for_component(title_selector, timeout=1.5):
            return
        if index == 0:
            driver.press_back()
        else:
            poi_detail.system_gesture_back()
        time.sleep(1.5)

    poi_detail.wait_detail_present(poi_name, timeout=10)


@allure.feature("出境服务")
@allure.story("附近页 POI 详情相关推荐、看点评和定位刷新")
def test_nearby_poi_recommendation_review_and_locate(driver) -> None:
    """验证附近页列表第一位 POI 可打开详情、进入推荐帖子和点评服务，并定位刷新周边。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)
    poi_detail = PoiDetailPage(driver)
    post_detail = PostDetailPage(driver)
    poi_name = ""

    with allure.step("前置条件：普通用户进入中国香港附近页"):
        navigation.tap_nearby()
        nearby.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.region_xpath("中国香港")),
            "附近页左上角地区-中国香港",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(navigation.tab_xpath("附近")),
            "底部导航-附近页签",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击附近列表第一位 POI，校验 POI 详情名称、评分、图集和相关推荐"):
        poi_name, poi_item = nearby.first_visible_poi_text_component(timeout=10)
        attach_highlighted_bounds(driver, poi_item.getBounds(), f"附近列表第一位POI-{poi_name}")
        nearby.tap_poi_in_list(poi_name, max_swipes=1)
        poi_detail.wait_detail_loaded(poi_name, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(poi_name)),
            f"POI详情标题-{poi_name}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.RATING_XPATH),
            "POI详情评分",
            timeout=8,
            attach_crop=False,
        )
        gallery = poi_detail.wait_gallery_visible(timeout=8)
        attach_highlighted_bounds(driver, gallery.getBounds(), "POI详情图集")
        recommendation_title = poi_detail.scroll_detail_until_xpath_visible(
            poi_detail.RECOMMENDATION_TITLE_XPATH,
            "POI详情相关推荐标题",
            max_swipes=6,
            timeout=8,
        )
        attach_highlighted_bounds(driver, recommendation_title.getBounds(), "POI详情相关推荐标题")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.RECOMMENDATION_LIST_XPATH),
            "POI详情相关推荐列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击相关推荐帖子，校验拉起帖子详情页，并返回 POI 详情"):
        recommendation_card_xpath = poi_detail.recommendation_card_xpath(1)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(recommendation_card_xpath),
            "POI详情相关推荐第一篇帖子",
            timeout=8,
            attach_crop=False,
        )
        poi_detail.tap_recommendation_card(recommendation_card_xpath)
        post_detail.wait_loaded(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(post_detail.CONTENT_LIST_XPATH),
            "帖子详情页内容",
            timeout=8,
            attach_crop=False,
        )
        post_detail.tap_back_button()
        poi_detail.wait_detail_present(poi_name, timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(poi_name)),
            f"返回POI详情-{poi_name}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击底部关联元服务“看点评”，校验跳转到服务内"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.REVIEW_BUTTON_XPATH),
            "POI详情底部关联元服务-看点评",
            timeout=8,
            attach_crop=False,
        )
        poi_detail.tap_review_service()
        service_marker = poi_detail.wait_review_service_loaded(timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            service_marker,
            "看点评服务页标题",
            timeout=12,
            attach_crop=False,
        )

    with allure.step("步骤4：返回 POI 详情后点击左下角定位，校验刷新为该 POI 周边数据"):
        _return_from_service_to_poi_detail(driver, poi_detail, poi_name)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(poi_name)),
            f"看点评返回POI详情-{poi_name}",
            timeout=8,
            attach_crop=False,
        )
        location_button = assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.LOCATION_BUTTON_XPATH),
            "POI详情左下角定位按钮",
            timeout=8,
            attach_crop=False,
        )
        location_button.click()
        poi_detail.wait_detail_closed(timeout=8)
        surrounding_names = nearby.wait_selected_poi_surrounding_loaded(
            poi_name,
            timeout=12,
        )
        allure.attach(
            "\n".join(surrounding_names),
            name=f"附近页-{poi_name}-周边POI列表",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.selected_poi_label_xpath(poi_name)),
            f"附近页地图选中地点-{poi_name}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            f"附近页-{poi_name}-周边POI列表",
            timeout=8,
            attach_crop=False,
        )
