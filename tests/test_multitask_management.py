import allure
from hypium import BY

from pages.multitask import MultiTaskPage
from pages.outbound_home import OutboundHomePage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务卡片")
@allure.story("多任务列表管理")
def test_multitask_delete_clear_and_close(driver) -> None:
    """验证多任务计数、单项删除、一键清除和关闭浮层。"""
    home = OutboundHomePage(driver)
    multitask = MultiTaskPage(driver)

    try:
        with allure.step("步骤1：打开多任务列表，核对计数和任务卡片"):
            multitask.open()
            initial_count, initial_titles = multitask.wait_count_consistent()
            external_count = initial_count - 1
            assert multitask.HOME_TITLE in initial_titles, (
                f"多任务列表未展示固定首页，实际任务：{initial_titles}"
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(multitask.PANEL_XPATH),
                f"多任务列表-计数{initial_count}与卡片数一致",
                timeout=8,
                attach_crop=False,
            )
            assert external_count >= 5, (
                "前置条件不满足：至少需要打开5个三方元服务，"
                f"当前仅有{external_count}个，全部任务：{initial_titles}"
            )

        with allure.step("步骤2：删除一个三方服务，其它任务继续展示"):
            deleted_title = multitask.delete_first_external_task()
            remaining_count, remaining_titles = multitask.wait_count_consistent(
                expected_count=initial_count - 1,
                timeout=8,
            )
            assert deleted_title not in remaining_titles, (
                f"服务“{deleted_title}”删除后仍显示：{remaining_titles}"
            )
            assert multitask.HOME_TITLE in remaining_titles, (
                f"删除三方服务后固定首页丢失：{remaining_titles}"
            )
            assert remaining_count == len(remaining_titles), (
                f"删除后计数与实际任务不一致："
                f"{remaining_count}/{remaining_titles}"
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(multitask.TASK_GRID_XPATH),
                f"删除{deleted_title}后-其它任务正常展示",
                timeout=8,
                attach_crop=False,
            )

        with allure.step("步骤3：点击一键清除，仅保留固定首页"):
            multitask.tap_clear_all()
            multitask.reopen_if_closed()
            multitask.wait_only_home(timeout=8)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(multitask.HOME_CARD_XPATH),
                "一键清除后-仅保留出境服务首页",
                timeout=8,
                attach_crop=False,
            )

        with allure.step("步骤4：点击右上角叉号关闭多任务列表"):
            multitask.close()
            multitask.wait_closed(timeout=8)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.SEARCH_BAR_XPATH),
                "多任务列表关闭-返回首页",
                timeout=8,
                attach_crop=False,
            )
    finally:
        if multitask.is_open():
            try:
                multitask.close()
                multitask.wait_closed(timeout=3)
            except RuntimeError:
                driver.press_back()
