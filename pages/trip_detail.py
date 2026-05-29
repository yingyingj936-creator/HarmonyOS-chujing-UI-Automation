from typing import Any
from hypium import BY

class TripDetailPage:
    PAGE_NAME = "TripDetailPage"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def is_loaded(self, timeout: float = 0) -> bool:
        """校验是否进入了具体的行程详情页"""
        if timeout > 0:
            return self.driver.wait_for_component(BY.text("编辑行程"), timeout=timeout)
        return self.driver.find_component(BY.text("编辑行程")) is not None
