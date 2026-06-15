import allure
from hypium import BY

from pages.outbound_search import OutboundSearchPage
from pages.poi_detail import PoiDetailPage
from pages.post_detail import PostDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


POI_NAME = "维多利亚港"
TARGET_RECOMMENDATION_INDEX = 25


@allure.feature("POI 相关推荐")
@allure.story("加载更多推荐帖子并进入帖子详情")
def test_poi_recommendation_post(driver) -> None:
    """验证 POI 相关推荐可连续加载，并能进入任意帖子详情页。"""
    search_page = OutboundSearchPage(driver)
    poi_page = PoiDetailPage(driver)
    post_page = PostDetailPage(driver)

    with allure.step("前置准备：从首页进入搜索启动页"):
        search_page.tap_home_search()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.PLAY_RANKING_TITLE_XPATH),
            "搜索启动页-必玩榜",
            timeout=8,
            attach_crop=False,
        )
        search_page.dismiss_keyboard()

    with allure.step(f"步骤1：点击“{POI_NAME}”，拉起 POI 详情页"):
        search_page.tap_ranking_poi(POI_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(POI_NAME)),
            f"POI详情页-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(
        f"步骤2：大幅连续向下浏览，至少加载到第"
        f"{TARGET_RECOMMENDATION_INDEX}篇相关推荐帖子"
    ):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.RECOMMENDATION_TITLE_XPATH),
            "POI详情页-相关推荐",
            timeout=8,
            attach_crop=False,
        )
        card_xpath = poi_page.load_more_recommendations(
            minimum_browsed_cards=TARGET_RECOMMENDATION_INDEX,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(card_xpath),
            f"浏览至少{TARGET_RECOMMENDATION_INDEX}篇后的可见推荐帖子",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(
        f"步骤3：点击浏览至少{TARGET_RECOMMENDATION_INDEX}篇后"
        "当前可见的推荐帖子，"
        "进入帖子详情页"
    ):
        poi_page.tap_recommendation_card(card_xpath)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(post_page.CONTENT_LIST_XPATH),
            "帖子详情页-正文内容",
            timeout=8,
            attach_crop=False,
        )
