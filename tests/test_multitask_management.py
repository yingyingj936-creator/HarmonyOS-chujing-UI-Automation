import allure
from hypium import BY

from pages.local_service import LocalServicePage
from pages.multitask import MultiTaskPage
from pages.outbound_home import OutboundHomePage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


def _open_service_from_local_list(
    local_service: LocalServicePage,
    service_page: ServiceDetailPage,
    service_name: str,
    *,
    stay_in_service: bool = False,
) -> None:
    if service_name in {"YouTube", "Dufry", "BBC News"}:
        local_service.tap_search_input()
        local_service.input_search_keyword(service_name)
        local_service.tap_search_button()
        local_service.wait_search_results_match(service_name, timeout=8)
        local_service.tap_search_result(service_name)
        should_clear_search = True
    else:
        local_service.tap_service(service_name)
        should_clear_search = False

    service_page.wait_xpath(
        service_page.title_xpath(service_name),
        f"{service_name} service page",
        timeout=15,
    )
    if stay_in_service:
        return

    service_page.press_system_back()
    local_service.wait_xpath(
        local_service.PAGE_TITLE_XPATH,
        "local service page",
        timeout=10,
    )
    if should_clear_search:
        local_service.tap_clear_search()
        local_service.wait_search_cleared(timeout=8)


def _prepare_external_tasks(
    home: OutboundHomePage,
    local_service: LocalServicePage,
    service_page: ServiceDetailPage,
) -> tuple[str, ...]:
    service_names = ("Papago+", "Xe", "YouTube", "Dufry", "BBC News")
    home.ensure_kingkong_first_page()
    home.tap_local_service_entry()
    local_service.wait_xpath(
        local_service.PAGE_TITLE_XPATH,
        "local service page",
        timeout=10,
    )
    for index, service_name in enumerate(service_names):
        _open_service_from_local_list(
            local_service,
            service_page,
            service_name,
            stay_in_service=index == len(service_names) - 1,
        )
    return service_names


def _reopen_multitask_from_home(
    home: OutboundHomePage,
    multitask: MultiTaskPage,
) -> None:
    if multitask.is_open():
        return
    for _ in range(3):
        if home.wait_loaded(timeout=1):
            break
        home.driver.press_back()
    home.restore_top(max_swipes=12)
    multitask.open()


@allure.feature("出境服务卡片")
@allure.story("多任务列表管理")
def test_multitask_delete_clear_and_close(driver) -> None:
    """验证多任务计数、单项删除、一键清除和关闭浮层。"""
    home = OutboundHomePage(driver)
    local_service = LocalServicePage(driver)
    service_page = ServiceDetailPage(driver)
    multitask = MultiTaskPage(driver)

    try:
        with allure.step("Prepare 5 external service tasks"):
            prepared_services = _prepare_external_tasks(
                home,
                local_service,
                service_page,
            )

        with allure.step("Step 1: open multitask and verify task count"):
            multitask.open()
            initial_count, initial_titles = multitask.wait_count_consistent(
                timeout=12,
            )
            external_count = initial_count - 1
            assert multitask.HOME_TITLE in initial_titles, (
                f"Pinned home task is missing: {initial_titles}"
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(multitask.PANEL_XPATH),
                f"multitask count {initial_count} matches cards",
                timeout=8,
                attach_crop=False,
            )
            assert external_count >= len(prepared_services), (
                "Prepared services are missing from multitask list: "
                f"expected at least {len(prepared_services)} external tasks, "
                f"actual {external_count}, all tasks: {initial_titles}"
            )

        with allure.step("步骤2：删除一个三方服务，其它任务继续展示"):
            deleted_title = multitask.delete_first_external_task()
            _reopen_multitask_from_home(home, multitask)
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
