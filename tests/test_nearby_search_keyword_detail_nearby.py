import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.nearby_page import NearbyPage
from pages.poi_detail import PoiDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


SEARCH_KEYWORD = "星光"
POI_NAME = "星光大道"
POI_TYPE = "景点"


@allure.feature("出境服务")
@allure.story("附近页关键词搜索、详情和看附近")
def test_nearby_search_keyword_detail_and_nearby(driver) -> None:
    """验证附近页搜索星光后可查看星光大道详情，并通过看附近刷新周边数据。"""
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

    with allure.step(f"步骤2：点击搜索框输入“{SEARCH_KEYWORD}”，校验结果列表展示名称、类型、评分、看附近和详情"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.SEARCH_INPUT_XPATH),
            "附近页搜索输入框",
            timeout=8,
            attach_crop=False,
        )
        nearby.input_search_keyword(SEARCH_KEYWORD, timeout=8)
        nearby.wait_search_result_loaded(POI_NAME, poi_type=POI_TYPE, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.search_result_text_xpath(POI_NAME)),
            f"搜索结果名称-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )
        detail_button = nearby.search_result_action_component(POI_NAME, "详情", timeout=8)
        attach_highlighted_bounds(driver, detail_button.getBounds(), "搜索结果-详情按钮")
        nearby_button = nearby.search_result_action_component(POI_NAME, "看附近", timeout=8)
        attach_highlighted_bounds(driver, nearby_button.getBounds(), "搜索结果-看附近按钮")

    with allure.step(f"步骤3：点击“{POI_NAME}”搜索结果的“详情”，校验拉起 POI 详情和相关推荐"):
        detail_button = nearby.search_result_action_component(POI_NAME, "详情", timeout=8)
        attach_highlighted_bounds(driver, detail_button.getBounds(), f"{POI_NAME}-详情按钮")
        nearby.tap_search_result_action(POI_NAME, "详情", timeout=8)
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
        attach_highlighted_bounds(driver, recommendation_title.getBounds(), "POI详情相关推荐标题")
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.RECOMMENDATION_LIST_XPATH),
            "POI详情相关推荐列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：点击 POI 详情右上角叉号，校验回到搜索结果页"):
        close_button = poi_detail.close_button(timeout=8)
        attach_highlighted_bounds(driver, close_button.getBounds(), "POI详情右上角叉号")
        poi_detail.close_detail(timeout=8)
        nearby.wait_search_result_loaded(POI_NAME, poi_type=POI_TYPE, timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(nearby.search_result_text_xpath(POI_NAME)),
            f"返回搜索结果页-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤5：点击“{POI_NAME}”的“看附近”，校验地图和列表刷新为该 POI 周边数据"):
        nearby_button = nearby.search_result_action_component(POI_NAME, "看附近", timeout=8)
        attach_highlighted_bounds(driver, nearby_button.getBounds(), f"{POI_NAME}-看附近按钮")
        nearby.tap_search_result_action(POI_NAME, "看附近", timeout=8)
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
