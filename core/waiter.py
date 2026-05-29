from __future__ import annotations

import time
from typing import Any

from hypium import BY


class UiWait:
    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def until_text(self, text: str, timeout: float = 8, error_message: str | None = None):
        if self.driver.wait_for_component(BY.text(text), timeout=timeout):
            return self.driver.find_component(BY.text(text))
        raise AssertionError(error_message or f"Timed out waiting text: {text}")

    def until_xpath(
        self, xpath: str, timeout: float = 8, error_message: str | None = None
    ):
        if self.driver.wait_for_component(BY.xpath(xpath), timeout=timeout):
            return self.driver.find_component(BY.xpath(xpath))
        raise AssertionError(error_message or f"Timed out waiting xpath: {xpath}")

    def pause(self, seconds: float) -> None:
        time.sleep(seconds)

