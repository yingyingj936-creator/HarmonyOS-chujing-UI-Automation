import subprocess
import time
from pathlib import Path

import pytest
from hypium import UiDriver

TARGET_DEVICE = "172.16.129.108:5555"
OUTBOUND_SERVICE_BUNDLE = "com.atomicservice.5765880207855877209"
OUTBOUND_SERVICE_ABILITY = "EntryAbility"
FILE_ORDER = {
    "test_region_switch.py": 1,
    "test_destination_category_switch.py": 2,
}


def _connect_hdc_target() -> None:
    """确保 hdc 已连接到目标设备。"""
    subprocess.run(["hdc", "tconn", TARGET_DEVICE], check=True)


def _start_outbound_service() -> None:
    """启动出境服务元服务并等待页面完成渲染。"""
    subprocess.run(
        [
            "hdc",
            "shell",
            "aa",
            "start",
            "-b",
            OUTBOUND_SERVICE_BUNDLE,
            "-a",
            OUTBOUND_SERVICE_ABILITY,
        ],
        check=True,
    )
    time.sleep(4)


@pytest.fixture(scope="session")
def driver():
    """全局 driver：连接设备并在会话结束后释放资源。"""
    _connect_hdc_target()
    ui_driver = UiDriver.connect(device_sn=TARGET_DEVICE)
    _start_outbound_service()
    yield ui_driver
    ui_driver.close()


def _item_filename(item: pytest.Item) -> str:
    """兼容不同 pytest 版本，提取测试项所在文件名。"""
    item_path = getattr(item, "path", None)
    if item_path is not None:
        return Path(item_path).name
    return item.fspath.basename


def pytest_collection_modifyitems(items: list[pytest.Item]) -> None:
    """
    按文件优先级重排收集到的测试项：
    1) FILE_ORDER 中的文件按指定顺序执行；
    2) 未指定文件统一排在后面；
    3) 同文件内维持 pytest 原始收集顺序。
    """
    indexed_items = list(enumerate(items))
    indexed_items.sort(
        key=lambda pair: (FILE_ORDER.get(_item_filename(pair[1]), 999), pair[0])
    )
    items[:] = [item for _, item in indexed_items]
