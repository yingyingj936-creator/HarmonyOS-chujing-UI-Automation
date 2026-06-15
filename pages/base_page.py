from typing import Any

from hypium import BY


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
        return component

    def wait_xpath(self, xpath: str, name: str, *, timeout: float = 8) -> Any:
        return self.wait_component(BY.xpath(xpath), name, timeout=timeout)

    def wait_text(self, text: str, name: str | None = None, *, timeout: float = 8) -> Any:
        return self.wait_component(
            BY.text(text),
            name or f"文本“{text}”",
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
        component = self.wait_xpath(xpath, name, timeout=timeout)
        if offset is None:
            component.click()
        else:
            self.driver.click(component, offset=offset)
        return component

    def tap_text(
        self,
        text: str,
        name: str | None = None,
        *,
        timeout: float = 8,
    ) -> Any:
        component = self.wait_text(text, name, timeout=timeout)
        component.click()
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
        return component

    def find_xpath(self, xpath: str) -> Any | None:
        return self.driver.find_component(BY.xpath(xpath))
