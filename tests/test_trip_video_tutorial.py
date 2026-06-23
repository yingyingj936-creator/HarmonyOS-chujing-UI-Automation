import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.trip_manager import TripManagerPage
from pages.trip_video_tutorial import TripVideoTutorialPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("行程管理")
@allure.story("查看视频教程")
def test_trip_video_tutorial_open_and_back(driver) -> None:
    """验证行程页可打开视频教程，教程内容正常加载，并可返回行程页。"""
    navigation = BottomNavigation(driver)
    trip_manager = TripManagerPage(driver)
    tutorial = TripVideoTutorialPage(driver)

    with allure.step("前置条件：普通用户进入行程页"):
        navigation.tap_trip()
        trip_manager.wait_loaded(timeout=10)
        trip_manager.scroll_to_my_trips_area(max_swipes=8)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.VIDEO_TUTORIAL_XPATH),
            "行程页-查看视频教程入口",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击“查看视频教程”，跳转到视频教程页"):
        trip_manager.tap_video_tutorial(timeout=8)
        tutorial.wait_loaded(timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(tutorial.TUTORIAL_TITLE_XPATH),
            "视频教程页-标题",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：查看视频教程，校验教程内容加载正常无白屏"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(tutorial.TUTORIAL_TITLE_XPATH),
            "视频教程页-非白屏内容",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击返回按钮，回到行程页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(tutorial.BACK_BUTTON_XPATH),
            "视频教程页-返回按钮",
            timeout=8,
            attach_crop=False,
        )
        tutorial.tap_back(timeout=8)
        trip_manager.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(trip_manager.CREATE_TRIP_TITLE_XPATH),
            "返回行程页-创建行程区域",
            timeout=8,
            attach_crop=False,
        )
