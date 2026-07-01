from __future__ import annotations

from typing import Any

from hypium import BY
from hypium.uidriver.uitree.uitree import UiTree


class UiSnapshot:
    """一次抓取设备 UI 树，并在本地执行多个只读 XPath 查询。"""

    def __init__(self, driver: Any) -> None:
        # Hypium 的动作层 UiDriver 会把未知属性访问记为弃用警告；UiTree
        # 实际需要的是动作层内部已创建的原子驱动。
        driver_impl = object.__getattribute__(driver, "_driver_impl")
        atomic_driver = object.__getattribute__(driver_impl, "driver")
        self._tree = UiTree(atomic_driver)
        self._captured = False

    def capture(self) -> "UiSnapshot":
        self._tree.refresh()
        self._captured = True
        return self

    def _require_captured(self) -> None:
        if not self._captured:
            raise RuntimeError("UI 快照尚未抓取，请先调用 capture()")

    def find_xpath(self, xpath: str) -> Any | None:
        self._require_captured()
        return self._tree.find_component(BY.xpath(xpath), refresh=False)

    def find_all_xpath(self, xpath: str) -> list[Any]:
        self._require_captured()
        return self._tree.find_all_components(BY.xpath(xpath), refresh=False)

    def require_xpath(self, xpath: str, name: str) -> Any:
        component = self.find_xpath(xpath)
        if component is None:
            raise RuntimeError(f"UI 快照中未找到{name}")
        return component
