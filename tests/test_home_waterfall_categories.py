import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from utils.allure_visual import assert_visible_and_attach_highlight


CATEGORY_TABS = ("发现", "入境", "出行", "美食", "游玩", "购物", "住宿", "其他")
SWITCH_TABS = ("入境", "购物", "其他")


@allure.feature("出境服务卡片")
@allure.story("首页攻略瀑布流分类切换")
def test_home_waterfall_category_switching(driver) -> None:
    """验证攻略分类展示完整，切换后加载对应瀑布流并可返回发现。"""
    home = OutboundHomePage(driver)

    try:
        home.select_guide_category("发现")

        with allure.step("步骤1：查看首页攻略分类栏，默认显示发现瀑布流"):
            initial_post_ids = home.scroll_to_waterfall()
            for tab_name in CATEGORY_TABS[:-1]:
                assert driver.wait_for_component(
                    BY.xpath(home.category_tab_xpath(tab_name)),
                    timeout=2,
                ) is not None, f"首页攻略分类缺少“{tab_name}”"
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.category_tab_xpath("发现")),
                "首页攻略默认分类-发现",
                timeout=8,
                attach_crop=False,
            )

        current_post_ids = initial_post_ids
        for tab_name in SWITCH_TABS:
            with allure.step(f"步骤2：切换到“{tab_name}”，加载对应攻略瀑布流"):
                current_post_ids = home.switch_guide_category(
                    tab_name,
                    current_post_ids,
                )
                assert_visible_and_attach_highlight(
                    driver,
                    BY.xpath(home.category_tab_xpath(tab_name)),
                    f"首页攻略分类已切换-{tab_name}",
                    timeout=8,
                    attach_crop=False,
                )

        with allure.step("步骤3：切回“发现”，重新展示发现瀑布流"):
            discover_post_ids = home.switch_guide_category(
                "发现",
                current_post_ids,
            )
            assert discover_post_ids, "切回发现后瀑布流没有攻略数据"
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.category_tab_xpath("发现")),
                "首页攻略分类已切回-发现",
                timeout=8,
                attach_crop=False,
            )
    finally:
        try:
            home.select_guide_category("发现")
        finally:
            home.restore_top()
