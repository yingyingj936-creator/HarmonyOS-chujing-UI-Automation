import subprocess
import pytest
from hypium import UiDriver

TARGET_DEVICE = "172.16.129.108:5555"


def _connect_hdc_target() -> None:
    """确保 hdc 已连接到目标设备。"""
    subprocess.run(["hdc", "tconn", TARGET_DEVICE], check=True)


@pytest.fixture(scope="session")
def driver():
    """全局 driver：连接设备并在会话结束后释放资源。"""
    _connect_hdc_target()
    ui_driver = UiDriver.connect(device_sn=TARGET_DEVICE)
    yield ui_driver
    ui_driver.close()
