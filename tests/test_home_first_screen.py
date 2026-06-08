import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_fullscreen,
)


@allure.feature("出境服务卡片")
@allure.story("首页首屏加载与关键模块展示")
def test_home_first_screen_load_and_modules(driver) -> None:
    """
    用例：验证首页首屏 5 秒内加载完成，且关键模块展示完整。
    """
    home = OutboundHomePage(driver)

    with allure.step("步骤1：启动应用并在 5 秒内完成首页首屏加载"):
        assert home.wait_first_screen_loaded(timeout=5), (
            "应用启动后超过 5 秒首页仍未完成加载，疑似白屏或长时间空白"
        )
        attach_fullscreen(driver, "首页首屏-加载完成")

    with allure.step("步骤2：校验左上角目的地展示为中国香港"):
        assert_visible_and_attach_highlight(
            driver,
            BY.text("中国香港"),
            "左上角目的地-中国香港",
            timeout=5,
        )

    with allure.step("步骤3：校验搜索框、金刚区、热门路线、瀑布流展示"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.SEARCH_BAR_XPATH),
            "搜索框",
            timeout=5,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.KINGKONG_PROXY_XPATH),
            "金刚区（代理容器）",
            timeout=5,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.HOT_ROUTES_SECTION_XPATH),
            "热门路线模块",
            timeout=5,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(home.WATERFALL_SECTION_XPATH),
            "瀑布流模块",
            timeout=5,
        )

    with allure.step("步骤4：校验底部导航完整且首页处于激活态"):
        assert_visible_and_attach_highlight(
            driver, BY.xpath(home.BOTTOM_HOME_TAB_XPATH), "底部导航-首页", timeout=5
        )
        assert_visible_and_attach_highlight(
            driver, BY.xpath(home.BOTTOM_TRIP_TAB_XPATH), "底部导航-行程", timeout=5
        )
        assert_visible_and_attach_highlight(
            driver, BY.xpath(home.BOTTOM_NEARBY_TAB_XPATH), "底部导航-附近", timeout=5
        )
        assert_visible_and_attach_highlight(
            driver, BY.xpath(home.BOTTOM_MINE_TAB_XPATH), "底部导航-我的", timeout=5
        )
        assert home.is_home_tab_active(timeout=5), "首页未处于激活态"
