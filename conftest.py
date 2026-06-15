import os
import subprocess
import time
from dataclasses import replace
from pathlib import Path

import pytest
from hypium import BY, UiDriver

from core.settings import AppSettings, load_settings
from pages.bottom_navigation import BottomNavigation
from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage

FILE_ORDER = {
    "test_home_first_screen.py": 1,
    "test_home_waterfall_categories.py": 2,
    "test_home_waterfall_pagination.py": 3,
    "test_home_service_tabs.py": 4,
    "test_taxi_service_entry.py": 5,
    "test_scenic_youtube_entries.py": 6,
    "test_local_service_categories.py": 7,
    "test_local_service_search.py": 8,
    "test_food_ordering_categories.py": 9,
    "test_food_ordering_search.py": 10,
    "test_multitask_management.py": 11,
    "test_multitask_return_home.py": 12,
    "test_bottom_navigation.py": 13,
    "test_destination_selector_browse.py": 14,
    "test_destination_switch_refresh.py": 15,
    "test_search_scope_by_destination.py": 16,
    "test_search_start_page_interactions.py": 17,
    "test_poi_add_to_trip.py": 18,
    "test_favorite_poi_from_ranking.py": 19,
    "test_poi_hotel_booking_and_navigation.py": 20,
    "test_poi_recommendation_post.py": 21,
    "test_clear_search_history.py": 22,
    "test_search_result_groups.py": 23,
}


def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--config",
        action="store",
        default=None,
        help="Path to TOML config file. Default: configs/default.toml",
    )
    parser.addoption(
        "--device",
        action="store",
        default=None,
        help="Override USB device serial. Use 'auto' for the only connected USB device.",
    )
    parser.addoption("--bundle", action="store", default=None, help="Override bundle")
    parser.addoption("--ability", action="store", default=None, help="Override ability")
    parser.addoption(
        "--disable-file-order",
        action="store_true",
        default=False,
        help="Disable custom FILE_ORDER and run by pytest default collection order.",
    )


def pytest_configure(config: pytest.Config) -> None:
    config._app_settings = load_settings(
        config.getoption("--config"),
        target_device=config.getoption("--device"),
        bundle=config.getoption("--bundle"),
        ability=config.getoption("--ability"),
        enable_file_order=not config.getoption("--disable-file-order"),
    )


def _hdc_executable() -> str:
    """优先使用 CI 注入的 HDC_EXE，本地默认使用 PATH 中的 hdc。"""
    return os.environ.get("HDC_EXE", "hdc")


def _list_usb_targets() -> list[str]:
    """返回当前通过 USB 连接的 HDC 设备序列号。"""
    result = subprocess.run(
        [_hdc_executable(), "list", "targets"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    targets = []
    for line in result.stdout.splitlines():
        target = line.strip()
        if not target or target == "[Empty]":
            continue
        # 无线目标使用 ip:port；USB 目标为设备序列号。
        if ":" not in target:
            targets.append(target)
    return targets


def _resolve_usb_target(configured_target: str) -> str:
    """校验并返回测试使用的 USB 设备序列号。"""
    usb_targets = _list_usb_targets()
    if not usb_targets:
        raise RuntimeError(
            "未检测到 USB 设备。请连接数据线、开启设备调试，"
            "并确认 `hdc list targets` 能显示设备序列号。"
        )

    if configured_target.lower() == "auto":
        if len(usb_targets) == 1:
            return usb_targets[0]
        raise RuntimeError(
            "检测到多台 USB 设备，请将 configs/default.toml 中的 "
            f"target_device 设置为其中一个序列号：{usb_targets}"
        )

    if configured_target not in usb_targets:
        raise RuntimeError(
            f"配置的 USB 设备 {configured_target!r} 未连接，"
            f"当前可用设备：{usb_targets}"
        )
    return configured_target


@pytest.fixture(scope="session")
def app_settings(pytestconfig: pytest.Config) -> AppSettings:
    settings = pytestconfig._app_settings
    usb_serial = _resolve_usb_target(settings.target_device)
    print(f"[Device] 使用 USB 设备：{usb_serial}")
    return replace(settings, target_device=usb_serial)


def _start_outbound_service(settings: AppSettings) -> None:
    """启动出境服务元服务并等待页面完成渲染。"""
    subprocess.run(
        [
            _hdc_executable(),
            "-t",
            settings.target_device,
            "shell",
            "aa",
            "start",
            "-b",
            settings.bundle,
            "-a",
            settings.ability,
        ],
        check=True,
    )
    time.sleep(settings.startup_wait_seconds)


@pytest.fixture(scope="session")
def driver(app_settings: AppSettings):
    """全局 driver：连接设备并在会话结束后释放资源。"""
    ui_driver = UiDriver.connect(device_sn=app_settings.target_device)
    _start_outbound_service(app_settings)
    try:
        yield ui_driver
    finally:
        ui_driver.close()


def _return_to_home(driver, settings: AppSettings) -> bool:
    """优先通过底部导航回首页，否则逐层返回。"""
    home = OutboundHomePage(driver)
    navigation = BottomNavigation(driver)

    for _ in range(settings.cleanup_back_steps):
        if home.is_at_home():
            return True

        home_tab = driver.wait_for_component(
            BY.xpath(home.BOTTOM_HOME_TAB_XPATH),
            timeout=0.5,
        )
        if home_tab is not None:
            try:
                navigation.tap_home(timeout=2)
                if home.wait_loaded(timeout=3):
                    return True
            except RuntimeError:
                pass

        driver.press_back()
        time.sleep(settings.cleanup_back_interval_seconds)

    return home.is_at_home()


def _restore_default_destination(driver, settings: AppSettings) -> bool:
    """在首页恢复配置指定的默认目的地。"""
    home = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)
    destination_selector = BY.xpath(
        home.region_dropdown_xpath(settings.default_destination)
    )

    if driver.wait_for_component(destination_selector, timeout=1) is not None:
        return True

    try:
        home.tap_region_selector()
        destination_page.choose_destination(settings.default_destination)
    except (AssertionError, RuntimeError):
        return False

    return driver.wait_for_component(destination_selector, timeout=8) is not None


def _prepare_home(driver, settings: AppSettings) -> bool:
    return _return_to_home(driver, settings) and _restore_default_destination(
        driver,
        settings,
    )


@pytest.fixture(scope="function", autouse=True)
def reset_to_home(driver, app_settings: AppSettings):
    """
    每个用例执行前后都恢复首页，避免前一条用例的导航栈污染后续用例。
    """
    print("\n[Setup] 正在确认测试从首页开始...")
    if not _prepare_home(driver, app_settings):
        _start_outbound_service(app_settings)
        if not _prepare_home(driver, app_settings):
            pytest.fail("前置恢复首页失败，终止当前用例")

    yield

    print("\n[Cleanup] 正在重置环境回到首页...")
    if not _prepare_home(driver, app_settings):
        pytest.fail("后置恢复首页或默认目的地失败，设备状态可能污染后续用例")
    print(
        f"[Cleanup] 已确认回到首页，目的地={app_settings.default_destination}"
    )


def _item_filename(item: pytest.Item) -> str:
    """兼容不同 pytest 版本，提取测试项所在文件名。"""
    item_path = getattr(item, "path", None)
    if item_path is not None:
        return Path(item_path).name
    return item.fspath.basename


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """
    按文件优先级重排收集到的测试项：
    1) FILE_ORDER 中的文件按指定顺序执行；
    2) 未指定文件统一排在后面；
    3) 同文件内维持 pytest 原始收集顺序。
    """
    if not config._app_settings.enable_file_order:
        return

    indexed_items = list(enumerate(items))
    indexed_items.sort(
        key=lambda pair: (FILE_ORDER.get(_item_filename(pair[1]), 999), pair[0])
    )
    items[:] = [item for _, item in indexed_items]

