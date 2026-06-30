import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.mine_page import MinePage
from pages.outbound_home import OutboundHomePage
from pages.outbound_search import OutboundSearchPage
from pages.poi_detail import PoiDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


POI_NAME = "华嫂冰室"


@allure.feature("收藏管理")
@allure.story("从搜索榜单收藏 POI 并在我的收藏中查看")
def test_favorite_poi_from_ranking(driver) -> None:
    """验证榜单浏览、POI 收藏高亮及收藏地点列表展示。"""
    home_page = OutboundHomePage(driver)
    search_page = OutboundSearchPage(driver)
    poi_page = PoiDetailPage(driver)
    mine_page = MinePage(driver)
    navigation = BottomNavigation(driver)

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

    with allure.step("步骤1：向右滑动浏览榜单，查看美食榜"):
        search_page.swipe_ranking_right_until_visible(POI_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.text("美食榜"),
            "搜索榜单-美食榜",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.ranking_poi_xpath(POI_NAME)),
            f"美食榜POI-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(f"步骤2：点击“{POI_NAME}”，拉起 POI 详情页"):
        search_page.tap_ranking_poi(POI_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(POI_NAME)),
            f"POI详情页-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击左下角收藏，验证收藏按钮高亮"):
        poi_page.ensure_favorite_unselected()
        poi_page.tap_favorite()
        assert poi_page.wait_favorite_highlighted(True), (
            "点击收藏后，收藏按钮未切换为黄色高亮状态"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.FAVORITE_BUTTON_XPATH),
            f"POI收藏按钮已高亮-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：退出至首页，进入我的收藏地点列表"):
        poi_page.tap_back_button(POI_NAME)
        search_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.SEARCH_BAR_XPATH),
            "返回首页-搜索框",
            timeout=8,
            attach_crop=False,
        )
        navigation.tap_mine()
        mine_page.tap_favorite_places_tab()
        mine_page.scroll_favorite_place_into_view(POI_NAME)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine_page.favorite_place_xpath(POI_NAME)),
            f"我的收藏地点-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("用例清理：取消本次新增收藏并恢复收藏地点默认页"):
        place_component = mine_page.wait_xpath(
            mine_page.favorite_place_xpath(POI_NAME),
            f"待取消收藏地点-{POI_NAME}",
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            place_component.getBounds(),
            f"清理收藏地点-{POI_NAME}",
        )
        mine_page.tap_favorite_item(POI_NAME, place_component)
        poi_page.wait_detail_present(POI_NAME, timeout=10)
        if poi_page.is_favorite_highlighted():
            poi_page.tap_favorite()
            assert poi_page.wait_favorite_highlighted(False), "清理时取消地点收藏失败"
        try:
            poi_page.close_detail(timeout=6)
        except RuntimeError:
            poi_page.press_system_back()
        mine_page.wait_content_loaded(timeout=10)
        mine_page.restore_favorites_default_state()
