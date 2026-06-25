import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from pages.poi_detail import PoiDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


POI_NAME = "Bakehouse（尖沙咀店）"


@allure.feature("出境服务")
@allure.story("附近页搜索推荐地点与周边刷新")
def test_nearby_search_recommended_poi_and_locate(driver) -> None:
    """验证附近页搜索弹层推荐地点可打开详情，并可定位刷新周边列表。"""
    navigation = BottomNavigation(driver)
    nearby = NearbyPage(driver)
    poi_detail = PoiDetailPage(driver)

    with allure.step("前置条件：普通用户进入底部导航“附近”页"):
        navigation.tap_nearby()
        nearby.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(navigation.tab_xpath("附近")),
            "底部导航-附近页签",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击底部抽屉搜索框，校验搜索弹层展示当前选择、重新定位和推荐地点"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.SEARCH_ENTRY_XPATH),
            "附近页底部抽屉搜索框",
            timeout=8,
            attach_crop=False,
        )
        nearby.open_search_layer(timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.SEARCH_CURRENT_SELECTION_XPATH),
            "搜索弹层-当前选择",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.SEARCH_RELOCATE_XPATH),
            "搜索弹层-重新定位",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.SEARCH_RECOMMEND_TITLE_XPATH),
            "搜索弹层-推荐地点",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤2：点击推荐地点“{POI_NAME}”，校验拉起 POI 详情"):
        recommended_poi = assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.recommended_poi_text_xpath(POI_NAME)),
            f"搜索弹层推荐地点-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )
        attach_highlighted_bounds(
            driver,
            recommended_poi.getBounds(),
            f"点击前推荐地点-{POI_NAME}",
        )
        nearby.tap_recommended_poi(POI_NAME, timeout=8)
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

    with allure.step("步骤3：上拉滑动查看 POI 详情内容，校验详情和相关推荐"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.DETAIL_LINK_XPATH),
            "POI详情-详情入口",
            timeout=8,
            attach_crop=False,
        )
        recommendation_title = poi_detail.scroll_detail_until_xpath_visible(
            poi_detail.RECOMMENDATION_TITLE_XPATH,
            "POI详情相关推荐标题",
            max_swipes=6,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            recommendation_title.getBounds(),
            "POI详情相关推荐标题",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.RECOMMENDATION_LIST_XPATH),
            "POI详情相关推荐列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤4：点击左下角定位按钮，校验地图和列表刷新为“{POI_NAME}”周边数据"):
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
