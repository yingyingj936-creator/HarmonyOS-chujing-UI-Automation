import subprocess
import time

import pytest
from hypium import UiDriver

TARGET_DEVICE = "172.16.129.108:5555"
OUTBOUND_SERVICE_BUNDLE = "com.atomicservice.5765880207855877209"
OUTBOUND_SERVICE_ABILITY = "EntryAbility"


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
