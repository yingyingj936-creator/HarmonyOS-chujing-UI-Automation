import subprocess
import time
from pathlib import Path

import pytest
from hypium import UiDriver

from core.settings import AppSettings, load_settings
from pages.outbound_home import OutboundHomePage

FILE_ORDER = {
    "test_home_first_screen.py": 1,
    "test_bottom_navigation.py": 2,
    "test_region_switch.py": 3,
    "test_destination_category_switch.py": 4,
    "test_search_flow.py": 5,
    "test_add_trip.py": 6,
    "test_collection_posts.py": 7,
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
        help="Override target device serial, e.g. 172.20.10.9:5555",
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


@pytest.fixture(scope="session")
def app_settings(pytestconfig: pytest.Config) -> AppSettings:
    return pytestconfig._app_settings


def _connect_hdc_target(target_device: str) -> None:
    """确保 hdc 已连接到目标设备。"""
    subprocess.run(["hdc", "tconn", target_device], check=True)


def _start_outbound_service(settings: AppSettings) -> None:
    """启动出境服务元服务并等待页面完成渲染。"""
    subprocess.run(
        [
            "hdc",
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
    _connect_hdc_target(app_settings.target_device)
    ui_driver = UiDriver.connect(device_sn=app_settings.target_device)
    _start_outbound_service(app_settings)
    yield ui_driver
    ui_driver.close()


@pytest.fixture(scope="function", autouse=True)
def reset_to_home(driver, app_settings: AppSettings):
    """
    每个用例执行前后的状态重置器：
    1. 前置：不做操作（假设上一个用例清理干净了）。
    2. 后置：无论成功失败，强制连按返回键回到首页，为下个用例准备。
    """
    home = OutboundHomePage(driver)

    yield  # 这里执行具体的测试用例逻辑

    # --- 后置清理逻辑 ---
    print("\n[Cleanup] 正在重置环境回到首页...")

    # 策略：最多尝试返回 4 次（详情页 -> 路线页 -> 首页）
    for _ in range(app_settings.cleanup_back_steps):
        if home.is_at_home():  # 需要在 OutboundHomePage 实现这个方法
            print("[Cleanup] 已确认回到首页")
            break
        driver.press_back()
        time.sleep(app_settings.cleanup_back_interval_seconds)


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

