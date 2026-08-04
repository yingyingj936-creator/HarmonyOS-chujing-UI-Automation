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
    POI_DETAIL_ROOT_XPATH = '//*[@id="map_panel_poidetail"]'
    BACK_BUTTON_XPATH_TEMPLATE = (
        '//Row[.//Text[@text="{poi_name}"]]/Row[./Image]'
    )
    # HarmonyOS XPath 的 contains() 可能错误命中空文本，限定到 POI 主内容区。
    DETAIL_LINK_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[@clickable="true"]'
    )
    GALLERY_XPATH_CANDIDATES = (
        '//*[@id="map_panel_poidetail"]//ListItem/__Common__[@clickable="true"]',
        '//SheetPage[.//Text[@text="导航"]]//__Common__[@clickable="true"]',
    )
    LOCATION_DETAIL_TITLE_XPATH = '//Text[@text="地点详情"]'
    LOCATION_DETAIL_BACK_XPATH = (
        '//Row[./Text[@text="地点详情"]]/Row[./Image]'
    )
    ADD_TO_TRIP_XPATH = '//Text[@text="添加到我的行程"]'
    FAVORITE_BUTTON_XPATH = (
        '//Row[.//Text[@text="导航"]]/Row[1]'
    )
    LOCATION_BUTTON_XPATH = (
        '//Row[.//Text[@text="导航"]]/Row[2]'
    )
    FAVORITE_SELECTED_BACKGROUND = "#1AFFBF00"
    BOOK_HOTEL_BUTTON_XPATH = (
        '//Row[@clickable="true" and ./Text[@text="订酒店"]]'
    )
    NAVIGATION_BUTTON_XPATH = (
        '//Row[@clickable="true" and ./Text[@text="导航"]]'
    )
    REVIEW_BUTTON_XPATH = (
        '//Row[@clickable="true" and ./Text[@text="看点评" or @text="看评"]]'
    )
    SERVICE_TITLE_XPATH = '//Text[@id="title"]'
    REVIEW_SERVICE_READY_XPATH = (
        '//Text[@id="title"] | '
        '//Text[contains(@text, "点评") or contains(@text, "评价") or contains(@text, "评论")]'
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
    PETAL_MAP_TITLE_XPATH = (
        '//Text[@id="title" and '
        '(@text="花瓣地图" or @text="地图" or contains(@text, "Petal"))]'
    )
    PETAL_MAP_NAVIGATION_READY_XPATH_TEMPLATE = (
        '//*[.//Text[@text="花瓣地图"] '
        'and .//Text[contains(@text, {poi_name})] '
        'and (.//Text[@text="我的位置"] '
        'or .//Text[@text="驾车"] '
        'or .//Text[contains(@text, "正在加载")] '
        'or .//*[@id="direction_routes_result_start_navigation_button"])]'
    )
    PETAL_MAP_MARK_XPATH = '//Text[@text="花瓣地图"]'
    RECOMMENDATION_TITLE_XPATH = '//Text[@text="相关推荐"]'
    RECOMMENDATION_LIST_XPATH = (
        '//*[@id="discovery_list_poidetail"]'
    )
    RATING_XPATH = (
        '//*[@id="map_panel_poidetail"]//Text[starts-with(@text, "评分 ")]'
    )

    @staticmethod
    def title_xpath(poi_name: str) -> str:
        return f'//Text[@text="{poi_name}"]'

    @staticmethod
    def _xpath_literal(value: str) -> str:
        if '"' not in value:
            return f'"{value}"'
        if "'" not in value:
            return f"'{value}'"
        parts = value.split('"')
        concat_parts = []
        for index, part in enumerate(parts):
            if part:
                concat_parts.append(f'"{part}"')
            if index != len(parts) - 1:
                concat_parts.append("'\"'")
        return "concat(" + ", ".join(concat_parts) + ")"

    @classmethod
    def back_button_xpath(cls, poi_name: str) -> str:
        return cls.BACK_BUTTON_XPATH_TEMPLATE.format(poi_name=poi_name)

    @classmethod
    def petal_map_navigation_ready_xpath(cls, poi_name: str) -> str:
        return cls.PETAL_MAP_NAVIGATION_READY_XPATH_TEMPLATE.format(
            poi_name=cls._xpath_literal(poi_name)
        )

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

    def wait_detail_loaded(self, poi_name: str, *, timeout: float = 10) -> None:
        """等待 POI 详情卡片加载完成。"""
        self.snapshot_xpaths(
            {
                "root": (self.POI_DETAIL_ROOT_XPATH, "POI详情卡片"),
                "title": (self.title_xpath(poi_name), f"POI详情标题-{poi_name}"),
                "rating": (self.RATING_XPATH, "POI详情评分"),
            },
            timeout=timeout,
        )

    def wait_detail_present(self, poi_name: str, *, timeout: float = 10) -> None:
        """等待 POI 详情仍处于打开状态，不要求评分等首屏字段当前可见。"""
        self.snapshot_xpaths(
            {
                "root": (self.POI_DETAIL_ROOT_XPATH, "POI详情卡片"),
                "title": (self.title_xpath(poi_name), f"POI详情标题-{poi_name}"),
            },
            timeout=timeout,
        )

    def wait_gallery_visible(self, *, timeout: float = 8):
        """等待 POI 详情图集展示，兼容图集在不同容器下渲染的情况。"""
        return self.wait_any_xpath(
            self.GALLERY_XPATH_CANDIDATES,
            "POI详情图集",
            timeout=timeout,
        )

    def wait_detail_closed(self, *, timeout: float = 8) -> None:
        """等待 POI 详情卡片关闭。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is None:
                return
            time.sleep(0.4)
        raise RuntimeError(f"[{self.PAGE_NAME}] POI详情卡片未关闭，timeout={timeout}s")

    @staticmethod
    def _as_list(components):
        if components is None:
            return []
        if isinstance(components, list):
            return components
        return [components]

    @staticmethod
    def _bounds_tuple(component) -> tuple[int, int, int, int]:
        bounds = component.getBounds()
        return (
            int(bounds.left),
            int(bounds.top),
            int(bounds.right),
            int(bounds.bottom),
        )

    def close_button(self, *, timeout: float = 8):
        """定位 POI 详情右上角叉号。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            detail = self.find_xpath(self.POI_DETAIL_ROOT_XPATH)
            images = self._as_list(
                self.driver.find_all_components(BY.xpath('//Image[@clickable="true"]'))
            )
            if detail is not None:
                detail_left, detail_top, detail_right, detail_bottom = self._bounds_tuple(detail)
                detail_width = max(1, detail_right - detail_left)
                candidates = []
                for image in images:
                    left, top, right, bottom = self._bounds_tuple(image)
                    if right <= left or bottom <= top:
                        continue
                    if left < detail_right - detail_width * 0.18:
                        continue
                    if top < detail_top - 380 or bottom > detail_top + 160:
                        continue
                    candidates.append((top, -left, image))
                if candidates:
                    candidates.sort(key=lambda item: (item[0], item[1]))
                    return candidates[0][2]
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到POI详情右上角叉号，timeout={timeout}s")

    def close_detail(self, *, timeout: float = 8) -> None:
        """点击 POI 详情右上角叉号并等待返回上一层。"""
        self.close_button(timeout=timeout).click()
        self.wait_detail_closed(timeout=timeout)

    def tap_add_to_trip(self) -> None:
        """点击“添加到我的行程”。"""
        self.tap_xpath(self.ADD_TO_TRIP_XPATH, "添加到我的行程")

    def tap_favorite(self) -> None:
        """点击 POI 详情页左下角收藏按钮。"""
        self.tap_xpath(self.FAVORITE_BUTTON_XPATH, "POI 收藏按钮")

    def tap_location_button(self, *, timeout: float = 8) -> None:
        """点击 POI 详情页左下角定位按钮。"""
        self.tap_xpath(self.LOCATION_BUTTON_XPATH, "POI 详情左下角定位按钮", timeout=timeout)
        time.sleep(1.5)

    def tap_book_hotel(self) -> None:
        """点击 POI 详情页右下角“订酒店”。"""
        self.tap_xpath(self.BOOK_HOTEL_BUTTON_XPATH, "订酒店按钮")
        self._continue_task_limit_prompt_if_present()

    def tap_navigation(self) -> None:
        """点击 POI 详情页右下角“导航”。"""
        self.tap_xpath(self.NAVIGATION_BUTTON_XPATH, "导航按钮")
        self._continue_task_limit_prompt_if_present()
        time.sleep(1.5)
        if self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is not None:
            self.tap_xpath(self.NAVIGATION_BUTTON_XPATH, "导航按钮")
            self._continue_task_limit_prompt_if_present()

    def wait_petal_map_navigation_loaded(self, poi_name: str, *, timeout: float = 18):
        """等待花瓣地图导航页首屏出现，不强依赖路线规划完全加载完成。"""
        navigation_xpaths = (
            self.petal_map_navigation_ready_xpath(poi_name),
            self.MAP_START_NAVIGATION_XPATH,
            self.PETAL_MAP_TITLE_XPATH,
            self.MAP_ROUTE_PANEL_XPATH,
        )
        deadline = time.time() + timeout
        while time.time() < deadline:
            component = self.driver.wait_for_component(
                BY.xpath(" | ".join(navigation_xpaths)),
                timeout=1,
            )
            if component is not None:
                return component

            # 部分设备花瓣地图首屏不暴露固定“花瓣地图”文案；只要已离开
            # POI 详情并出现服务标题，也视为跳端成功。
            if self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is None:
                title = self.find_xpath(self.SERVICE_TITLE_XPATH)
                if title is not None:
                    return title
            time.sleep(0.5)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到花瓣地图导航页-{poi_name}，timeout={timeout}s"
        )

    def tap_review_service(self) -> None:
        """点击 POI 详情页底部“看点评”。"""
        self.tap_xpath(self.REVIEW_BUTTON_XPATH, "看点评按钮")
        self._continue_task_limit_prompt_if_present()
        time.sleep(1.5)
        if self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is not None:
            button = self.find_xpath(self.REVIEW_BUTTON_XPATH)
            if button is not None:
                bounds = button.getBounds()
                self.driver.click(
                    (
                        (int(bounds.left) + int(bounds.right)) // 2,
                        (int(bounds.top) + int(bounds.bottom)) // 2,
                    )
                )
                self._continue_task_limit_prompt_if_present()

    def wait_review_service_loaded(self, *, timeout: float = 15):
        """等待点评类关联元服务打开，不强依赖固定 title id。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            title = self.find_xpath(self.SERVICE_TITLE_XPATH)
            if title is not None and self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is None:
                return title
            if self.find_xpath(self.POI_DETAIL_ROOT_XPATH) is None:
                marker = self.find_xpath(self.REVIEW_SERVICE_READY_XPATH)
                if marker is not None:
                    return marker
                marker = self.find_xpath('//Text[string-length(@text) > 0]')
                if marker is not None:
                    return marker
            time.sleep(0.5)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未进入看点评服务页，timeout={timeout}s")

    def _continue_task_limit_prompt_if_present(self) -> None:
        """兼容任务数量上限提示弹窗，出现时点击“继续”进入服务。"""
        continue_button = self.driver.wait_for_component(
            BY.xpath(self.TASK_LIMIT_CONTINUE_XPATH),
            timeout=0.8,
        )
        if continue_button is None:
            return
        continue_button.click()
        time.sleep(0.5)

    def system_gesture_back(self) -> None:
        """从屏幕右边缘左滑，执行 HarmonyOS 系统返回手势。"""
        self.driver.swipe_to_back(side="RIGHT")

    def swipe_detail_up(self, *, distance: int = 70) -> None:
        """在 POI 详情卡片内向上滑动。"""
        detail = self.wait_xpath(self.POI_DETAIL_ROOT_XPATH, "POI详情卡片")
        self.driver.swipe("UP", distance=distance, area=detail, swipe_time=0.6)
        time.sleep(0.5)

    def scroll_detail_until_xpath_visible(
        self,
        xpath: str,
        name: str,
        *,
        max_swipes: int = 5,
        timeout: float = 8,
    ):
        """在 POI 详情卡片中滚动，直到目标内容进入可见区域。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            component = self.find_xpath(xpath)
            if component is not None:
                return component
            time.sleep(0.3)

        for _ in range(max_swipes):
            self.swipe_detail_up()
            component = self.driver.wait_for_component(BY.xpath(xpath), timeout=1)
            if component is not None:
                return component

        raise RuntimeError(f"[{self.PAGE_NAME}] POI详情滚动后仍未找到{name}")

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
            time.sleep(0.6)

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
