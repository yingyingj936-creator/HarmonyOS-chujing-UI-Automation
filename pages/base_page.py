import time
from typing import Any

from hypium import BY

from utils.component_cache import (
    invalidate_component_cache,
    recent_component,
    remember_component,
)
from utils.ui_snapshot import UiSnapshot, cached_snapshot


class BasePage:
    """页面对象公共的等待、点击和输入能力。"""

    PAGE_NAME = "BasePage"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def wait_component(
        self,
        selector: Any,
        name: str,
        *,
        timeout: float = 8,
    ) -> Any:
        component = self.driver.wait_for_component(selector, timeout=timeout)
        if component is None:
            raise RuntimeError(
                f"[{self.PAGE_NAME}] 未找到{name}，timeout={timeout}s"
            )
        remember_component(self.driver, selector, component)
        return component

    def wait_xpath(self, xpath: str, name: str, *, timeout: float = 8) -> Any:
        return self.wait_component(BY.xpath(xpath), name, timeout=timeout)

    def wait_any_xpath(
        self,
        xpaths: tuple[str, ...],
        name: str,
        *,
        timeout: float = 8,
    ) -> Any:
        if not xpaths:
            raise ValueError("xpaths 不能为空")
        return self.wait_xpath(" | ".join(xpaths), name, timeout=timeout)

    def wait_text(self, text: str, name: str | None = None, *, timeout: float = 8) -> Any:
        has_unsafe_log_text = any(
            ord(character) > 0xFFFF or 0xD800 <= ord(character) <= 0xDFFF
            for character in text
        )
        if has_unsafe_log_text:
            deadline = time.time() + timeout
            while time.time() < deadline:
                components = self.driver.find_all_components(BY.xpath("//Text"))
                if components is None:
                    time.sleep(0.3)
                    continue
                if not isinstance(components, list):
                    components = [components]
                for component in components:
                    if component.getText().strip() == text:
                        remember_component(self.driver, BY.text(text), component)
                        return component
                time.sleep(0.3)
            raise RuntimeError(
                f"[{self.PAGE_NAME}] text not found: {name or 'target'}, timeout={timeout}s"
            )

        return self.wait_component(
            BY.text(text),
            name or f"text {text}",
            timeout=timeout,
        )
    def tap_xpath(
        self,
        xpath: str,
        name: str,
        *,
        timeout: float = 8,
        offset: tuple[float, float] | None = None,
    ) -> Any:
        selector = BY.xpath(xpath)
        component = recent_component(self.driver, selector)
        if component is None:
            component = self.wait_component(selector, name, timeout=timeout)
        if offset is None:
            component.click()
        else:
            self.driver.click(component, offset=offset)
        invalidate_component_cache(self.driver)
        return component

    def tap_text(
        self,
        text: str,
        name: str | None = None,
        *,
        timeout: float = 8,
    ) -> Any:
        selector = BY.text(text)
        component = recent_component(self.driver, selector)
        if component is None:
            component = self.wait_text(text, name, timeout=timeout)
        component.click()
        invalidate_component_cache(self.driver)
        return component

    def input_xpath(
        self,
        xpath: str,
        value: str,
        name: str,
        *,
        timeout: float = 8,
    ) -> Any:
        component = self.wait_xpath(xpath, name, timeout=timeout)
        component.inputText(value)
        invalidate_component_cache(self.driver)
        return component

    def find_xpath(self, xpath: str) -> Any | None:
        selector = BY.xpath(xpath)
        try:
            component = cached_snapshot(self.driver).find_xpath(xpath)
        except Exception:
            component = self.driver.find_component(selector)
        if component is not None:
            remember_component(self.driver, selector, component)
        return component

    def cached_xpath(
        self,
        xpath: str,
        *,
        max_age_seconds: float = 5.0,
    ) -> Any | None:
        """复用当前页面状态下近期定位过的组件，未命中时再查询 UI 树。"""
        selector = BY.xpath(xpath)
        component = recent_component(
            self.driver,
            selector,
            max_age_seconds=max_age_seconds,
        )
        if component is not None:
            return component
        return self.find_xpath(xpath)

    def snapshot_xpaths(
        self,
        requirements: dict[str, tuple[str, str]],
        *,
        timeout: float = 8,
        retry_interval: float = 0.2,
    ) -> dict[str, Any]:
        """按快照重试整组条件，每次抓取后在本地完成全部 XPath 断言。"""
        if not requirements:
            raise ValueError("requirements 不能为空")

        invalidate_component_cache(self.driver)
        deadline = time.monotonic() + timeout
        snapshot = UiSnapshot(self.driver)
        missing_names: list[str] = []

        while True:
            snapshot.capture()
            components: dict[str, Any] = {}
            missing_names.clear()
            for key, (xpath, name) in requirements.items():
                component = snapshot.find_xpath(xpath)
                if component is None:
                    missing_names.append(name)
                    continue
                components[key] = component

            if not missing_names:
                for key, (xpath, _) in requirements.items():
                    remember_component(self.driver, BY.xpath(xpath), components[key])
                return components

            remaining = deadline - time.monotonic()
            if remaining <= 0:
                missing = "、".join(missing_names)
                raise RuntimeError(
                    f"[{self.PAGE_NAME}] UI 快照未找到：{missing}，timeout={timeout}s"
                )
            time.sleep(min(retry_interval, remaining))
