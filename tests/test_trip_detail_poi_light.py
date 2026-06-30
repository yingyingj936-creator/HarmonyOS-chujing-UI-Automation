import allure
import pytest
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


TRIP_NAME = "香港逛吃两日游"
POI_NAME = "尖沙咀"
POI_ENGLISH_NAME = "Tsim Sha Tsui"


@allure.feature("行程管理")
@allure.story("我的行程详情页 POI 点亮")
def test_trip_detail_poi_light_and_close(driver) -> None:
    """验证我的行程详情页内 POI 详情可浏览、可点亮并可关闭回到行程详情页。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    trip_detail = TripDetailPage(driver)

    with allure.step("前置条件：普通用户已登录，进入“香港逛吃两日游”行程详情页"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        try:
            trip_manager.scroll_trip_into_view(TRIP_NAME, max_swipes=10)
        except RuntimeError as exc:
            visible_titles = [
                title
                for _, title in trip_manager.current_visible_trip_cards_with_titles()
            ]
            pytest.fail(
                f"前置条件不满足：我的行程列表未找到“{TRIP_NAME}”。"
                f"当前可见行程={visible_titles}；原始错误={exc}"
            )

        trip_card = assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.trip_card_xpath(TRIP_NAME)),
            f"我的行程列表-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
        trip_card.click()
        trip_loaded = trip_detail.wait_loaded(TRIP_NAME, timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            trip_loaded["title"],
            f"行程详情页标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击 Day1 的“尖沙咀”，校验拉起 POI 详情"):
        poi = trip_detail.scroll_until_xpath_visible(
            trip_detail.route_day_poi_xpath(POI_NAME),
            f"Day1地点-{POI_NAME}",
            max_swipes=8,
            timeout=8,
        )
        attach_highlighted_bounds(driver, poi.getBounds(), f"Day1地点-{POI_NAME}")
        poi.click()
        trip_detail.wait_poi_detail_loaded(
            english_name=POI_ENGLISH_NAME,
            timeout=12,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.poi_detail_english_name_xpath(POI_ENGLISH_NAME)),
            f"POI详情英文名-{POI_ENGLISH_NAME}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：滑动查看 POI 详情，校验图集、详情和相关推荐模块"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.POI_DETAIL_GALLERY_XPATH),
            "POI详情图集",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.POI_DETAIL_INTRO_XPATH),
            "POI详情简介与详情入口",
            timeout=8,
            attach_crop=False,
        )
        tips = trip_detail.scroll_poi_detail_until_xpath_visible(
            trip_detail.POI_DETAIL_TIPS_XPATH,
            "POI详情游玩提示",
            max_swipes=4,
            timeout=8,
        )
        attach_highlighted_bounds(driver, tips.getBounds(), "POI详情游玩提示")
        trip_detail.swipe_poi_detail_up()
        recommend_title = trip_detail.scroll_poi_detail_until_xpath_visible(
            trip_detail.POI_DETAIL_RECOMMEND_TITLE_XPATH,
            "POI详情相关推荐标题",
            max_swipes=4,
            timeout=8,
        )
        attach_highlighted_bounds(
            driver,
            recommend_title.getBounds(),
            "POI详情相关推荐标题",
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.POI_DETAIL_RECOMMEND_LIST_XPATH),
            "POI详情相关推荐列表",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击左下角点亮按钮，通过报告截图查看按钮高亮态"):
        before_button = trip_detail.poi_detail_light_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            before_button.getBounds(),
            "POI详情左下角点亮按钮-点击前",
        )
        after_button = trip_detail.tap_poi_detail_light_button(timeout=8)
        attach_highlighted_bounds(
            driver,
            after_button.getBounds(),
            "POI详情左下角点亮按钮-点击后",
        )

    with allure.step("步骤4：系统侧滑退出 POI 详情，回到行程详情页"):
        trip_detail.gesture_back_from_poi_detail(TRIP_NAME, timeout=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_detail.route_trip_title_xpath(TRIP_NAME)),
            f"侧滑返回后的行程详情页标题-{TRIP_NAME}",
            timeout=8,
            attach_crop=False,
        )
