import time

import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.mine_page import MinePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


def _return_to_mine(driver, navigation: BottomNavigation, mine: MinePage) -> None:
    """从三方服务返回我的页；优先系统返回，必要时再点底部我的页签。"""
    for _ in range(3):
        try:
            mine.wait_content_loaded(timeout=3)
            return
        except RuntimeError:
            driver.press_back()
            time.sleep(1)

    navigation.tap_mine()
    mine.wait_content_loaded(timeout=10)


@allure.feature("出境服务")
@allure.story("我的页最近使用服务排序")
def test_mine_recent_service_moves_to_first_after_open(driver) -> None:
    """验证我的页最近使用末尾服务可打开，返回后该服务移动到最近使用第一位。"""
    navigation = BottomNavigation(driver)
    mine = MinePage(driver)
    service_page = ServiceDetailPage(driver)

    with allure.step("前置条件：普通用户进入底部导航“我的”页"):
        navigation.tap_mine()
        mine.wait_content_loaded(timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(navigation.tab_xpath("我的")),
            "底部导航-我的页签",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.PROFILE_TITLE_XPATH),
            "我的页-小星星的旅程",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：滑动查看最近使用服务，定位当前末尾服务"):
        initial_names = mine.wait_recent_services_visible(timeout=10)
        allure.attach(
            "\n".join(initial_names),
            name="我的页-最近使用初始可见服务",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.RECENT_SERVICES_TITLE_XPATH),
            "我的页-最近使用标题",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.RECENT_SERVICES_GRID_XPATH),
            "我的页-最近使用服务列表",
            timeout=8,
            attach_crop=False,
        )
        tail_service = mine.swipe_recent_services_to_tail(max_swipes=8)
        tail_component = mine.recent_service_component(tail_service, timeout=8)
        attach_highlighted_bounds(
            driver,
            tail_component.getBounds(),
            f"我的页-最近使用末尾服务-{tail_service}",
        )

    with allure.step(f"步骤2：点击末尾服务“{tail_service}”，校验能够跳转该服务"):
        mine.tap_recent_service(tail_service, timeout=8)
        service_title = service_page.wait_loaded(tail_service, timeout=12)
        attach_highlighted_bounds(
            driver,
            service_title.getBounds(),
            f"三方服务页标题-{service_title.getText()}",
        )

    with allure.step(f"步骤3：回到我的页，校验“{tail_service}”移动到最近使用第一位"):
        _return_to_mine(driver, navigation, mine)
        ordered_names = mine.wait_recent_service_first(tail_service, timeout=15)
        allure.attach(
            "\n".join(ordered_names),
            name="我的页-返回后最近使用可见顺序",
            attachment_type=allure.attachment_type.TEXT,
        )
        first_component = mine.recent_service_component(tail_service, timeout=8)
        attach_highlighted_bounds(
            driver,
            first_component.getBounds(),
            f"我的页-最近使用第一位-{tail_service}",
        )
