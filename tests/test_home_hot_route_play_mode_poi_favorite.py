import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.mine_page import MinePage
from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


ROUTE_NAME = "香港逛吃两日游"
POI_NAME = RouteDetailPage.PLAY_MODE_POI_2_NAME


def _open_play_mode_poi_detail(
    home: OutboundHomePage,
    route_detail: RouteDetailPage,
) -> None:
    """从首页进入热门路线游玩模式，并打开固定地点详情。"""
    home.restore_top(max_swipes=12)
    home.tap_hot_route_card(ROUTE_NAME)
    route_detail.wait_loaded(ROUTE_NAME, timeout=15)
    route_detail.tap_one_click_play(timeout=12)
    route_detail.tap_play_mode_day_1_tab(timeout=10)
    route_detail.tap_play_mode_poi_2_bubble(timeout=10)


def _return_home_from_play_mode_poi_detail(
    home: OutboundHomePage,
    route_detail: RouteDetailPage,
) -> None:
    """从游玩模式地点详情返回首页。"""
    route_detail.close_play_mode_poi_detail(timeout=10)
    route_detail.exit_play_mode(ROUTE_NAME, timeout=10)
    route_detail.tap_back_button()
    assert home.wait_loaded(timeout=12), "从路线详情返回后未回到首页"


def _go_to_mine_favorite_places(
    navigation: BottomNavigation,
    mine: MinePage,
) -> None:
    """进入我的页收藏地点列表。"""
    navigation.tap_mine()
    mine.wait_content_loaded()
    mine.tap_favorite_places_tab()


@allure.feature("收藏管理")
@allure.story("游玩模式地点收藏与我的收藏地点同步")
def test_play_mode_poi_favorite_syncs_with_mine_collection(driver) -> None:
    """验证游玩模式地点收藏、我的收藏地点同步和取消收藏移除。"""
    home = OutboundHomePage(driver)
    route_detail = RouteDetailPage(driver)
    navigation = BottomNavigation(driver)
    mine = MinePage(driver)

    with allure.step(f"前置准备：进入游玩模式并打开未收藏地点“{POI_NAME}”详情"):
        _open_play_mode_poi_detail(home, route_detail)
        route_detail.ensure_poi_favorite_unselected()
        assert not route_detail.is_poi_favorite_highlighted(), (
            f"前置准备失败：地点“{POI_NAME}”仍为已收藏状态"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.play_mode_poi_title_xpath(POI_NAME)),
            f"游玩模式地点详情-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击地点详情收藏按钮，校验按钮变为已收藏"):
        route_detail.tap_poi_favorite()
        assert route_detail.wait_poi_favorite_highlighted(True), (
            "点击收藏后，游玩模式地点收藏按钮未变为高亮状态"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_FAVORITE_BUTTON_XPATH),
            f"地点收藏按钮已高亮-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：进入我的页收藏地点列表，校验新增该地点"):
        _return_home_from_play_mode_poi_detail(home, route_detail)
        _go_to_mine_favorite_places(navigation, mine)
        mine.scroll_favorite_place_into_view(POI_NAME, max_swipes=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.favorite_place_xpath(POI_NAME)),
            f"我的收藏地点已新增-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：返回游玩模式查看该地点详情，校验收藏状态仍高亮"):
        navigation.tap_home()
        assert home.wait_loaded(timeout=12), "从我的页切回首页失败"
        _open_play_mode_poi_detail(home, route_detail)
        assert route_detail.wait_poi_favorite_highlighted(True), (
            f"重新进入游玩模式后，地点“{POI_NAME}”收藏状态未保持高亮"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_FAVORITE_BUTTON_XPATH),
            f"重新进入后收藏状态仍高亮-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤4：取消收藏，校验地点详情收藏按钮取消高亮"):
        route_detail.tap_poi_favorite()
        assert route_detail.wait_poi_favorite_highlighted(False), (
            "点击取消收藏后，游玩模式地点收藏按钮仍为高亮状态"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_detail.POI_DETAIL_FAVORITE_BUTTON_XPATH),
            f"地点收藏按钮已取消高亮-{POI_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：再次进入我的收藏地点列表，校验该地点已移除"):
        _return_home_from_play_mode_poi_detail(home, route_detail)
        _go_to_mine_favorite_places(navigation, mine)
        assert mine.wait_favorite_place_absent(POI_NAME, timeout=10), (
            f"取消收藏后，我的收藏地点列表仍显示“{POI_NAME}”"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FAVORITE_PLACES_TAB_XPATH),
            "我的收藏地点列表已刷新",
            timeout=8,
            attach_crop=False,
        )
