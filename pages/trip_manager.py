from typing import Any
from hypium import BY

class TripManagerPage:
    PAGE_NAME = "TripManagerPage"

    def __init__(self, driver: Any) -> None:
        self.driver = driver

    def has_trip_in_list(self, trip_name: str = "香港逛吃两日游") -> bool:
        """根据 route_mine.json，校验行程列表中是否存在指定行程"""
        # 列表加载可能较慢，建议增加等待
        return self.driver.wait_for_component(BY.text(trip_name), timeout=5)

