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
        f"{service_name}服务页",
        timeout=15,
    )
    if stay_in_service:
        return

    service_page.press_system_back()
    local_service.wait_xpath(
        local_service.PAGE_TITLE_XPATH,
        "本地服务列表页",
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
        "本地服务列表页",
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
    local_service: LocalServicePage,
    service_page: ServiceDetailPage,
    multitask: MultiTaskPage,
    *,
    fallback_service: str,
) -> None:
    if multitask.is_open():
        return

    for _ in range(5):
        if home.wait_loaded(timeout=1):
            break
        home.driver.press_back()
    if not home.wait_loaded(timeout=3):
        raise RuntimeError("删除任务后未能返回首页，无法重新打开多任务列表")

    home.ensure_kingkong_first_page()
    home.tap_local_service_entry()
    local_service.wait_xpath(
        local_service.PAGE_TITLE_XPATH,
        "本地服务列表页",
        timeout=10,
    )
    _open_service_from_local_list(
        local_service,
        service_page,
        fallback_service,
        stay_in_service=True,
    )
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
        with allure.step("前置准备：打开5个三方元服务任务"):
            prepared_services = _prepare_external_tasks(
                home,
                local_service,
                service_page,
            )

        with allure.step("步骤1：打开多任务列表，校验任务计数与卡片数量一致"):
            multitask.open()
            initial_count, initial_titles = multitask.wait_count_consistent(
                timeout=12,
            )
            external_count = initial_count - 1
            assert multitask.HOME_TITLE in initial_titles, (
                f"固定首页任务丢失：{initial_titles}"
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(multitask.PANEL_XPATH),
                f"多任务计数{initial_count}与任务卡片数量一致",
                timeout=8,
                attach_crop=False,
            )
            assert external_count >= len(prepared_services), (
                "已打开的三方服务未完整出现在多任务列表："
                f"预期至少{len(prepared_services)}个三方任务，"
                f"实际{external_count}个，全部任务：{initial_titles}"
            )

        with allure.step("步骤2：删除一个三方服务，其它任务继续展示"):
            deleted_title = multitask.delete_first_external_task()
            fallback_service = next(
                (
                    service_name
                    for service_name in prepared_services
                    if service_name != deleted_title
                ),
                prepared_services[0],
            )
            _reopen_multitask_from_home(
                home,
                local_service,
                service_page,
                multitask,
                fallback_service=fallback_service,
            )
            remaining_count, remaining_titles = multitask.wait_count_consistent(
                timeout=8,
            )
            assert deleted_title not in remaining_titles, (
                f"服务“{deleted_title}”删除后仍显示：{remaining_titles}"
            )
            assert multitask.HOME_TITLE in remaining_titles, (
                f"删除三方服务后固定首页丢失：{remaining_titles}"
            )
            assert remaining_count <= initial_count, (
                f"删除后任务数未减少或保持合理范围："
                f"初始={initial_count}, 当前={remaining_count}, {remaining_titles}"
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
            if multitask.is_open():
                multitask.wait_only_home(timeout=8)
                assert_visible_and_attach_highlight(
                    driver,
                    BY.xpath(multitask.HOME_CARD_XPATH),
                    "一键清除后-仅保留出境服务首页",
                    timeout=8,
                    attach_crop=False,
                )
            else:
                assert_visible_and_attach_highlight(
                    driver,
                    BY.xpath(home.SEARCH_BAR_XPATH),
                    "一键清除后浮层自动收起-固定首页正常展示",
                    timeout=8,
                    attach_crop=False,
                )

        with allure.step("步骤4：点击右上角叉号关闭多任务列表"):
            if multitask.is_open():
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

