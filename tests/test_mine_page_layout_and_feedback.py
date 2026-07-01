import time

import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.mine_page import MinePage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


def _return_to_mine(
    driver,
    navigation: BottomNavigation,
    mine: MinePage,
) -> None:
    """从子页面返回“我的”页；优先返回键，兜底点底部导航。"""
    for _ in range(4):
        try:
            mine.wait_content_loaded(timeout=3)
            return
        except RuntimeError:
            driver.press_back()
            time.sleep(1.2)

    navigation.tap_mine()
    mine.wait_content_loaded(timeout=10)


@allure.feature("出境服务")
@allure.story("我的页布局、入口跳转与意见反馈")
def test_mine_page_layout_entries_and_feedback(driver) -> None:
    """验证我的页关键布局、顶部入口跳转、帮助与反馈分类和问题反馈入口。"""
    navigation = BottomNavigation(driver)
    mine = MinePage(driver)

    with allure.step("步骤1：点击底部导航“我的”，进入我的页"):
        navigation.tap_mine()
        mine.wait_layout_loaded(timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(navigation.tab_xpath("我的")),
            "底部导航-我的页签",
            timeout=8,
            attach_crop=False,
        )
    with allure.step("步骤2：查看我的页面布局，校验顶部入口、最近使用和收藏区域"):
        mine.ensure_entry_area_visible()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.mine_entry_xpath("我的订单")),
            "我的页顶部功能入口区域",
            timeout=8,
            attach_crop=False,
        )
        mine.wait_xpath(
            mine.RECENT_SERVICES_GRID_XPATH,
            "我的页最近使用服务列表",
            timeout=8,
        )
        mine.scroll_favorites_area_into_view(max_swipes=4)
        mine.wait_favorites_tabs_loaded(timeout=8)

    with allure.step("步骤3：依次点击我的订单、优惠券、联系人、人工客服、更多并校验跳转"):
        entry_names = ("我的订单", "优惠券", "联系人", "人工客服", "更多")
        for entry_name in entry_names:
            with allure.step(f"步骤3-{entry_name}：点击入口并校验对应页面"):
                mine.ensure_entry_area_visible()
                assert_visible_and_attach_highlight(
                    driver,
                    BY.xpath(mine.mine_entry_xpath(entry_name)),
                    f"我的页入口-{entry_name}-点击前",
                    timeout=8,
                    attach_crop=False,
                )
                mine.tap_entry(entry_name)
                marker = mine.wait_entry_page_loaded(entry_name, timeout=15)
                attach_highlighted_bounds(
                    driver,
                    marker.getBounds(),
                    f"{entry_name}页面-标识",
                )
                allure.attach(
                    marker.getText(),
                    name=f"{entry_name}页面标识文本",
                    attachment_type=allure.attachment_type.TEXT,
                )
                _return_to_mine(driver, navigation, mine)

    with allure.step("步骤4：返回我的页后点击意见反馈，校验帮助与反馈页展示"):
        mine.ensure_entry_area_visible()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.mine_entry_xpath("意见反馈")),
            "我的页入口-意见反馈",
            timeout=8,
            attach_crop=False,
        )
        mine.tap_entry("意见反馈")
        mine.wait_feedback_loaded(timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FEEDBACK_TITLE_XPATH),
            "帮助与反馈页-标题",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FEEDBACK_INITIAL_CATEGORY_XPATH),
            "帮助与反馈页-默认分类桌面卡片",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤5：依次切换帮助与反馈分类“地区定位”和“其他”"):
        mine.tap_feedback_category("地区定位", timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.any_text_xpath("地区定位")),
            "帮助与反馈页-地区定位分类",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FEEDBACK_DISTRICT_QUESTION_XPATH),
            "帮助与反馈页-地区定位问题列表",
            timeout=8,
            attach_crop=False,
        )

        mine.tap_feedback_category("其他", aliases=("其它",), timeout=12)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.any_text_xpath("其他")),
            "帮助与反馈页-其他分类",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤6：点击其他分类下“如何卸载出境服务”，校验问题详情"):
        uninstall_question = assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FEEDBACK_UNINSTALL_QUESTION_XPATH),
            "帮助与反馈页-如何卸载出境服务问题",
            timeout=8,
            attach_crop=False,
        )
        uninstall_question.click()
        time.sleep(1.5)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FEEDBACK_UNINSTALL_QUESTION_XPATH),
            "帮助与反馈页-如何卸载出境服务详情标题",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FEEDBACK_UNINSTALL_ANSWER_XPATH),
            "帮助与反馈页-卸载说明",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤7：回到上一级并点击问题反馈，校验问题反馈页"):
        driver.press_back()
        time.sleep(1.5)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FEEDBACK_PROBLEM_BUTTON_XPATH),
            "帮助与反馈页-问题反馈入口",
            timeout=8,
            attach_crop=False,
        ).click()
        mine.wait_problem_feedback_loaded(timeout=15)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.PROBLEM_FEEDBACK_SERVICE_XPATH),
            "问题反馈页-选择服务",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.PROBLEM_FEEDBACK_DESC_XPATH),
            "问题反馈页-问题描述",
            timeout=8,
            attach_crop=False,
        )
