import time
from math import ceil
from pathlib import Path
from tempfile import TemporaryDirectory

from hypium import BY
from PIL import Image

from pages.base_page import BasePage


class PoiDetailPage(BasePage):
    """POI 详情页面对象。"""

    PAGE_NAME = "PoiDetailPage"
    BACK_BUTTON_XPATH_TEMPLATE = (
        '//Row[.//Text[@text="{poi_name}"]]/Row[./Image]'
    )
    # HarmonyOS XPath 的 contains() 可能错误命中空文本，限定到 POI 主内容区。
    DETAIL_LINK_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[@clickable="true"]'
    )
    LOCATION_DETAIL_TITLE_XPATH = '//Text[@text="地点详情"]'
    LOCATION_DETAIL_BACK_XPATH = (
        '//Row[./Text[@text="地点详情"]]/Row[./Image]'
    )
    ADD_TO_TRIP_XPATH = '//Text[@text="添加到我的行程"]'
    FAVORITE_BUTTON_XPATH = (
        '//Row[.//Text[@text="导航"]]/Row[1]'
    )
    FAVORITE_SELECTED_BACKGROUND = "#1AFFBF00"
    BOOK_HOTEL_BUTTON_XPATH = (
        '//Row[@clickable="true" and ./Text[@text="订酒店"]]'
    )
    NAVIGATION_BUTTON_XPATH = (
        '//Row[@clickable="true" and ./Text[@text="导航"]]'
    )
    BOOKING_TITLE_XPATH = '//Text[@id="title" and @text="Booking"]'
    TASK_LIMIT_CONTINUE_XPATH = '//Text[@text="继续"]'
    MAP_START_NAVIGATION_XPATH = (
        '//Button[@id="direction_routes_result_start_navigation_button"]'
    )
    MAP_ROUTE_PANEL_XPATH = (
        '//*[@id="direction_routes_result_start_navigation_button" '
        'or @text="路线" or @text="花瓣地图" or contains(@text, "路线")]'
    )
    PETAL_MAP_MARK_XPATH = '//Text[@text="花瓣地图"]'
    RECOMMENDATION_TITLE_XPATH = '//Text[@text="相关推荐"]'
    RECOMMENDATION_LIST_XPATH = (
        '//*[@id="discovery_list_poidetail"]'
    )

    @staticmethod
    def title_xpath(poi_name: str) -> str:
        return f'//Text[@text="{poi_name}"]'

    @classmethod
    def back_button_xpath(cls, poi_name: str) -> str:
        return cls.BACK_BUTTON_XPATH_TEMPLATE.format(poi_name=poi_name)

    def tap_back_button(self, poi_name: str) -> None:
        """点击 POI 详情页顶部栏的页面内返回按钮。"""
        xpath = self.back_button_xpath(poi_name)
        self.tap_xpath(xpath, f"“{poi_name}”详情页返回按钮")

    def press_system_back(self) -> None:
        """使用系统返回键离开 POI 详情页。"""
        self.driver.press_back()

    def tap_detail_link(self) -> None:
        """
        点击 POI 简介末尾蓝色“详情”。

        UI 树把整段简介合并成一个 Text，普通 component.click() 会点击段落中心，
        但实际只有蓝色“详情”Span 可触发跳转，因此从截图中识别蓝色文字坐标。
        """
        selector = BY.xpath(self.DETAIL_LINK_XPATH)
        component = self.wait_component(selector, "POI 地点详情入口")

        bounds = component.getBounds()
        left = int(bounds.left)
        top = int(bounds.top)
        right = int(bounds.right)
        bottom = int(bounds.bottom)

        with TemporaryDirectory() as temp_dir:
            screenshot_path = Path(temp_dir) / "poi_detail.jpeg"
            saved_path = Path(
                self.driver.capture_screen(str(screenshot_path), in_pc=True)
            )
            with Image.open(saved_path) as screenshot:
                image = screenshot.convert("RGB")
                blue_points = self._find_blue_points(
                    image,
                    left=max(0, left),
                    top=max(0, top),
                    right=min(image.width, right),
                    bottom=min(image.height, bottom),
                )

        if not blue_points:
            raise RuntimeError(
                "已定位 POI 简介，但未识别到蓝色“详情”文字，无法安全点击"
            )

        click_x = round(sum(x for x, _ in blue_points) / len(blue_points))
        click_y = round(sum(y for _, y in blue_points) / len(blue_points))
        self.driver.click((click_x, click_y))

    def tap_location_detail_back(self) -> None:
        """点击地点详情页顶部栏的页面内返回按钮。"""
        self.tap_xpath(self.LOCATION_DETAIL_BACK_XPATH, "地点详情返回按钮")

    def tap_add_to_trip(self) -> None:
        """点击“添加到我的行程”。"""
        self.tap_xpath(self.ADD_TO_TRIP_XPATH, "添加到我的行程")

    def tap_favorite(self) -> None:
        """点击 POI 详情页左下角收藏按钮。"""
        self.tap_xpath(self.FAVORITE_BUTTON_XPATH, "POI 收藏按钮")

    def tap_book_hotel(self) -> None:
        """点击 POI 详情页右下角“订酒店”。"""
        self.tap_xpath(self.BOOK_HOTEL_BUTTON_XPATH, "订酒店按钮")
        self._continue_task_limit_prompt_if_present()

    def tap_navigation(self) -> None:
        """点击 POI 详情页右下角“导航”。"""
        self.tap_xpath(self.NAVIGATION_BUTTON_XPATH, "导航按钮")
        self._continue_task_limit_prompt_if_present()

    def _continue_task_limit_prompt_if_present(self) -> None:
        """兼容任务数量上限提示弹窗，出现时点击“继续”进入服务。"""
        continue_button = self.driver.wait_for_component(
            BY.xpath(self.TASK_LIMIT_CONTINUE_XPATH),
            timeout=2,
        )
        if continue_button is None:
            return
        continue_button.click()
        time.sleep(1.5)

    def system_gesture_back(self) -> None:
        """从屏幕右边缘左滑，执行 HarmonyOS 系统返回手势。"""
        self.driver.swipe_to_back(side="RIGHT")

    @classmethod
    def recommendation_card_xpath(cls, index: int) -> str:
        return f'{cls.RECOMMENDATION_LIST_XPATH}/Column[{index}]'

    def load_more_recommendations(
        self,
        *,
        minimum_browsed_cards: int = 25,
        swipe_distance: int = 75,
    ) -> str:
        """
        大幅连续上滑相关推荐瀑布流，并返回滑动后的一张可见帖子卡片。

        相关推荐为两列虚拟瀑布流，UI 树只保留当前渲染卡片，无法直接使用
        Column[25] 定位第 25 篇。按每次至少浏览一行计算，浏览 25 篇至少
        需要上滑 13 次。
        """
        recommendation_list = self.wait_xpath(
            self.RECOMMENDATION_LIST_XPATH,
            "相关推荐瀑布流",
        )

        required_swipes = ceil(minimum_browsed_cards / 2)
        for _ in range(required_swipes):
            self.driver.swipe(
                "UP",
                distance=swipe_distance,
                area=recommendation_list,
            )
            time.sleep(1)

        list_bounds = recommendation_list.getBounds()
        for index in range(12, 0, -1):
            card_xpath = self.recommendation_card_xpath(index)
            card = self.driver.wait_for_component(
                BY.xpath(card_xpath),
                timeout=0.4,
            )
            if card is None:
                continue

            card_bounds = card.getBounds()
            if (
                card_bounds.bottom > list_bounds.top
                and card_bounds.top < list_bounds.bottom
            ):
                return card_xpath

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 大幅滑动 {required_swipes} 次后，"
            "相关推荐区域没有可见帖子，可能加载失败"
        )

    def tap_recommendation_card(self, card_xpath: str) -> None:
        """点击已加载并进入可见区域的相关推荐帖子卡片。"""
        self.tap_xpath(card_xpath, "相关推荐帖子")

    def is_favorite_highlighted(self) -> bool:
        """通过按钮背景色判断收藏星标是否为黄色高亮。"""
        component = self.wait_xpath(
            self.FAVORITE_BUTTON_XPATH,
            "POI 收藏按钮",
        )
        background = component.getAllProperties().to_dict().get(
            "backgroundColor",
            "",
        )
        return background.upper() == self.FAVORITE_SELECTED_BACKGROUND

    def wait_favorite_highlighted(
        self,
        expected: bool,
        *,
        timeout: float = 5,
    ) -> bool:
        """等待收藏按钮切换到期望的高亮状态。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.is_favorite_highlighted() is expected:
                return True
            time.sleep(0.4)
        return False

    def ensure_favorite_unselected(self) -> None:
        """重复执行用例时，先将 POI 恢复为未收藏状态。"""
        if not self.is_favorite_highlighted():
            return
        self.tap_favorite()
        if not self.wait_favorite_highlighted(False):
            raise RuntimeError("无法将 POI 收藏按钮恢复为未高亮状态")

    @staticmethod
    def _find_blue_points(
        image: Image.Image,
        *,
        left: int,
        top: int,
        right: int,
        bottom: int,
    ) -> list[tuple[int, int]]:
        """查找简介区域内蓝色链接文字的像素坐标。"""
        points: list[tuple[int, int]] = []
        pixels = image.load()
        for y in range(top, bottom):
            for x in range(left, right):
                red, green, blue = pixels[x, y]
                if (
                    blue >= 145
                    and blue > red * 1.4
                    and blue > green * 1.12
                ):
                    points.append((x, y))
        return points
