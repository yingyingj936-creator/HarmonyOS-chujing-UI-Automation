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


POI_NAME = "露台餐厅"
ANCHOR_POI_NAME = "Bakehouse（尖沙咀店）"


def _return_from_service_to_poi_detail(driver, poi_detail: PoiDetailPage) -> None:
    """从关联元服务返回 POI 详情，优先系统返回，不成功再使用侧滑返回。"""
    driver.press_back()
    time.sleep(1.5)
    if driver.wait_for_component(BY.xpath(poi_detail.title_xpath(POI_NAME)), timeout=4):
        return

    poi_detail.system_gesture_back()
    poi_detail.wait_detail_present(POI_NAME, timeout=8)


def _ensure_target_poi_available(
    driver,
    nearby: NearbyPage,
    poi_detail: PoiDetailPage,
):
    """确保附近列表中能看到目标 POI；默认列表没有时切到 Bakehouse 周边。"""
    try:
        return nearby.scroll_poi_into_view(POI_NAME, max_swipes=3)
    except RuntimeError as exc:
        allure.attach(
            str(exc),
            name="前置补充-当前附近列表未展示目标POI",
            attachment_type=allure.attachment_type.TEXT,
        )

    with allure.step(f"前置补充：刷新到“{ANCHOR_POI_NAME}”周边，确保列表展示“{POI_NAME}”"):
        nearby.open_search_layer(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.recommended_poi_text_xpath(ANCHOR_POI_NAME)),
            f"搜索弹层推荐地点-{ANCHOR_POI_NAME}",
            timeout=8,
            attach_crop=False,
        )
        nearby.tap_recommended_poi(ANCHOR_POI_NAME, timeout=8)
        poi_detail.wait_detail_loaded(ANCHOR_POI_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(ANCHOR_POI_NAME)),
            f"POI详情标题-{ANCHOR_POI_NAME}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.LOCATION_BUTTON_XPATH),
            f"{ANCHOR_POI_NAME}-左下角定位按钮",
            timeout=8,
            attach_crop=False,
        ).click()
        poi_detail.wait_detail_closed(timeout=8)
        nearby.wait_selected_poi_surrounding_loaded(ANCHOR_POI_NAME, timeout=12)
        return nearby.scroll_poi_into_view(POI_NAME, max_swipes=8)


@allure.feature("出境服务")
@allure.story("附近页 POI 详情相关推荐、看点评和定位刷新")
def test_nearby_poi_recommendation_review_and_locate(driver) -> None:
    """验证附近页露台餐厅可打开详情、进入推荐帖子和点评服务，并定位刷新周边。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)
    poi_detail = PoiDetailPage(driver)
    post_detail = PostDetailPage(driver)

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

    with allure.step(f"步骤1：点击附近列表的“{POI_NAME}”，校验 POI 详情名称、评分、图集和相关推荐"):
        poi_item = _ensure_target_poi_available(driver, nearby, poi_detail)
        attach_highlighted_bounds(driver, poi_item.getBounds(), f"附近列表POI-{POI_NAME}")
        nearby.tap_poi_in_list(POI_NAME, max_swipes=1)
        poi_detail.wait_detail_loaded(POI_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(POI_NAME)),
            f"POI详情标题-{POI_NAME}",
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
        poi_detail.wait_detail_present(POI_NAME, timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(POI_NAME)),
            f"返回POI详情-{POI_NAME}",
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
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.SERVICE_TITLE_XPATH),
            "看点评服务页标题",
            timeout=12,
            attach_crop=False,
        )

    with allure.step(f"步骤4：返回 POI 详情后点击左下角定位，校验刷新为“{POI_NAME}”周边数据"):
        _return_from_service_to_poi_detail(driver, poi_detail)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(POI_NAME)),
            f"看点评返回POI详情-{POI_NAME}",
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
            POI_NAME,
            timeout=12,
        )
        allure.attach(
            "\n".join(surrounding_names),
            name=f"附近页-{POI_NAME}-周边POI列表",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.selected_poi_label_xpath(POI_NAME)),
            f"附近页地图选中地点-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.POI_LIST_XPATH),
            f"附近页-{POI_NAME}-周边POI列表",
            timeout=8,
            attach_crop=False,
        )
