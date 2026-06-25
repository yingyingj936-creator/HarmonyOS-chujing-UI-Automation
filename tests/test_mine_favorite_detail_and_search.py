import time

import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.mine_page import MinePage
from pages.poi_detail import PoiDetailPage
from pages.post_detail import PostDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


SEARCH_KEYWORD = "香港"


def _return_to_mine_favorites(
    driver,
    navigation: BottomNavigation,
    mine: MinePage,
) -> None:
    """返回我的页收藏区域，供同一用例继续执行下一步。"""
    for _ in range(3):
        try:
            mine.wait_content_loaded(timeout=3)
            mine.scroll_favorites_area_into_view(max_swipes=4)
            return
        except RuntimeError:
            driver.press_back()
            time.sleep(1)

    navigation.tap_mine()
    mine.wait_content_loaded(timeout=10)
    mine.scroll_favorites_area_into_view(max_swipes=6)


@allure.feature("收藏管理")
@allure.story("我的页收藏地点、收藏帖子和收藏搜索")
def test_mine_favorite_place_post_and_search(driver) -> None:
    """验证我的收藏地点/帖子可打开详情，并可搜索收藏内容。"""
    navigation = BottomNavigation(driver)
    mine = MinePage(driver)
    poi_detail = PoiDetailPage(driver)
    post_detail = PostDetailPage(driver)

    with allure.step("前置条件：进入底部导航“我的”页并展示收藏区域"):
        navigation.tap_mine()
        mine.wait_content_loaded(timeout=15)
        mine.scroll_favorites_area_into_view(max_swipes=6)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FAVORITES_TITLE_XPATH),
            "我的页-收藏区域",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击收藏地点Tab下第一条POI，校验跳转POI详情"):
        mine.tap_favorite_places_tab()
        place_name, place_component = mine.wait_first_visible_favorite_item("地点")
        attach_highlighted_bounds(
            driver,
            place_component.getBounds(),
            f"收藏地点POI-{place_name}",
        )
        place_component.click()
        poi_detail.wait_detail_present(place_name, timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_detail.title_xpath(place_name)),
            f"POI详情标题-{place_name}",
            timeout=8,
            attach_crop=False,
        )
        try:
            poi_detail.close_detail(timeout=5)
        except RuntimeError:
            driver.press_back()
            time.sleep(1)
        _return_to_mine_favorites(driver, navigation, mine)

    with allure.step("步骤2：点击收藏帖子Tab下第一篇帖子，校验跳转帖子详情"):
        mine.tap_favorite_posts_tab()
        post_title, post_component = mine.wait_first_visible_favorite_item("帖子")
        attach_highlighted_bounds(
            driver,
            post_component.getBounds(),
            f"收藏帖子-{post_title}",
        )
        post_component.click()
        post_detail.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(post_detail.CONTENT_LIST_XPATH),
            "帖子详情页-内容区域",
            timeout=8,
            attach_crop=False,
        )
        try:
            post_detail.tap_back_button()
        except RuntimeError:
            driver.press_back()
            time.sleep(1)
        _return_to_mine_favorites(driver, navigation, mine)

    with allure.step("步骤3：点击收藏搜索框，输入“香港”并校验可搜索出对应内容"):
        mine.input_favorite_search(SEARCH_KEYWORD)
        result_text, result_component = mine.wait_favorite_search_result(
            SEARCH_KEYWORD,
            timeout=10,
        )
        attach_highlighted_bounds(
            driver,
            result_component.getBounds(),
            f"收藏搜索结果-{result_text}",
        )
