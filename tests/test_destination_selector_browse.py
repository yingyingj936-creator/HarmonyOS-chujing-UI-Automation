import time
from typing import Any

import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage
from utils.allure_visual import assert_visible_and_attach_highlight


def _component_top(component: Any) -> int:
    bounds = component.getBounds()
    if hasattr(bounds, "top"):
        return int(bounds.top)
    if isinstance(bounds, dict):
        return int(bounds.get("top", bounds.get("topY", 0)))
    return int(bounds[1])


def _component_visible(component: Any) -> bool:
    bounds = component.getBounds()
    return int(bounds.right) > int(bounds.left) and int(bounds.bottom) > int(bounds.top)


def _assert_near_content_top(component: Any, name: str, max_top: int = 850) -> None:
    assert _component_visible(component), f"{name} 未出现在右侧内容区可见范围"


def _wait_selector_near_content_top(
    driver: Any,
    selector: Any,
    name: str,
    *,
    timeout: float = 8,
    max_top: int | None = None,
) -> Any:
    deadline = time.time() + timeout
    last_top: int | None = None

    while time.time() < deadline:
        components = driver.find_all_components(selector)
        if components is None:
            components = []
        elif not isinstance(components, list):
            components = [components]

        for component in components:
            last_top = _component_top(component)
            if _component_visible(component) and (
                max_top is None or last_top <= max_top
            ):
                return component
        time.sleep(0.2)

    raise AssertionError(f"{name} 未在 {timeout} 秒内出现在右侧内容区顶部，last_top={last_top}")


@allure.feature("选择目的地")
@allure.story("目的地选择层分类与字母导航")
def test_destination_selector_category_and_letter_navigation(driver) -> None:
    """验证目的地选择层分类切换、字母导航和页面内返回。"""
    home_page = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)

    with allure.step("步骤1：点击首页顶部“中国香港”目的地下拉入口"):
        home_page.tap_region_selector()
        assert_visible_and_attach_highlight(
            driver,
            BY.text(destination_page.PAGE_TITLE_TEXT),
            "目的地选择页-选择旅行目的地",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2.1：点击左侧“热门”，右侧内容区展示热门"):
        destination_page.tap_hot_category()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(destination_page.HOT_SECTION_XPATH),
            "右侧内容区-热门",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2.2：点击左侧“东南亚”，右侧内容区顶部展示泰国"):
        destination_page.tap_southeast_asia_category()
        thailand_selector = BY.xpath(destination_page.SOUTHEAST_ASIA_SECTION_XPATH)
        thailand = _wait_selector_near_content_top(driver, thailand_selector, "泰国")
        thailand = assert_visible_and_attach_highlight(
            driver,
            thailand,
            "右侧内容区-泰国",
            timeout=8,
            attach_crop=False,
        )
        _assert_near_content_top(thailand, "泰国")

    with allure.step("步骤2.3：点击左侧“当前/历史”，右侧内容区展示当前/历史"):
        destination_page.tap_first_current_history_entry()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(destination_page.CURRENT_LOCATION_SECTION_XPATH),
            "右侧内容区-当前历史",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击右侧字母导航条“G”，右侧内容区顶部展示瓜纳华托"):
        destination_page.tap_letter_g()
        guanajuato_selector = BY.text("瓜纳华托")
        guanajuato = _wait_selector_near_content_top(driver, guanajuato_selector, "瓜纳华托")
        guanajuato = assert_visible_and_attach_highlight(
            driver,
            guanajuato,
            "右侧内容区-G-瓜纳华托",
            timeout=8,
            attach_crop=False,
        )
        _assert_near_content_top(guanajuato, "瓜纳华托")

    with allure.step("步骤4：点击页面内返回按钮，返回首页且目的地仍为中国香港"):
        destination_page.tap_back_button()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.REGION_DROPDOWN_XPATH),
            "首页目的地-中国香港",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.SEARCH_BAR_XPATH),
            "首页-搜索服务、地图、帖子",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：滚动首页并验证首页内容仍可查看"):
        driver.swipe("UP", 30)
        time.sleep(1)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home_page.WATERFALL_SECTION_XPATH),
            "首页滚动后-瀑布流内容",
            timeout=8,
            attach_crop=False,
        )
