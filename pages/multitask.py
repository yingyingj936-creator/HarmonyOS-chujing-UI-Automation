import os
import re
import subprocess
import time
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

from hypium import BY
from PIL import Image

from pages.base_page import BasePage


class MultiTaskPage(BasePage):
    """出境服务卡片内的多任务管理浮层。"""

    PAGE_NAME = "MultiTaskPage"
    _CACHED_USB_SERIAL: str | None = None
    _CACHED_UITEST_VERSION: str | None = None
    DIGIT_TEXT_CONDITION = (
        '@text="1" or @text="2" or @text="3" or @text="4" or @text="5" '
        'or @text="6" or @text="7" or @text="8" or @text="9"'
    )
    ENTRY_XPATH = (
        '//*[@id="TabHomeCompRoot"]'
        '//RelativeContainer[@clickable="true" and ./Text[@id="txt_num"]]'
    )
    CLICKABLE_ENTRY_XPATH = (
        '//RelativeContainer[@clickable="true" and .//Text[@id="txt_num"]]'
    )
    LEGACY_SERVICE_ENTRY_XPATH = (
        '//RelativeContainer[@clickable="true" and ./Text[@id="txt_num"]]'
    )
    FLOATING_COLUMN_XPATH = '//Column[.//Text[@id="txt_num"] and ./Divider]'
    FLOATING_STACK_XPATH = '//Stack[.//Text[@id="txt_num"] and .//Divider]'
    COUNT_TEXT_XPATH = '//Text[@id="txt_num"]'
    COUNT_TEXT_NO_ID_XPATH = (
        '//Stack[@clickable="true"]'
        f'//Text[{DIGIT_TEXT_CONDITION}]'
    )
    COUNT_STACK_NO_ID_XPATH = (
        '//Stack[@clickable="true" '
        f'and .//Text[{DIGIT_TEXT_CONDITION}] '
        'and .//RelativeContainer[@clickable="true"]]'
    )
    COUNT_CONTAINER_NO_ID_XPATH = (
        '//RelativeContainer[@clickable="true" '
        f'and .//Text[{DIGIT_TEXT_CONDITION}]]'
    )
    PANEL_XPATH = '//SheetWrapper/SheetPage'
    HEADER_XPATH = '//SheetWrapper//Text[starts-with(@text, "多任务")]'
    TASK_SCROLL_XPATH = '//SheetWrapper//Grid'
    TASK_GRID_XPATH = '//SheetWrapper//Grid'
    TASK_TITLE_XPATH = (
        '//SheetWrapper//Grid/GridItem/Column/Row/Text'
    )
    HOME_CARD_XPATH = (
        '//SheetWrapper//Grid/GridItem'
        '[.//Text[@text="出境服务首页"]]'
    )
    DELETABLE_TASK_TITLE_XPATH = (
        '//SheetWrapper//Grid/GridItem'
        '[.//Image[@clickable="true"]]/Column/Row/Text'
    )
    DELETE_BUTTON_XPATH = (
        '(//SheetWrapper//Grid/GridItem'
        '[.//Image[@clickable="true"]]/Column/Row'
        '/Image[@clickable="true"][last()])[1]'
    )
    CLEAR_ALL_XPATH = (
        '//SheetWrapper//Row'
        '[@clickable="true" and ./Text[@text="一键清除"]]'
    )
    CLOSE_BUTTON_XPATH = (
        '//SheetWrapper/SheetPage/Button[@clickable="true"]'
    )
    GUIDE_CONFIRM_XPATH = '//Text[@text="知道了"]'
    HOME_TITLE = "出境服务首页"
    COUNT_PATTERN = re.compile(r"多任务(?:窗口|列表)[（(](\d+)[）)]")

    def _find_all(self, xpath: str) -> list[Any]:
        components = self.driver.find_all_components(BY.xpath(xpath))
        if components is None:
            return []
        if isinstance(components, list):
            return components
        return [components]

    def open(self) -> None:
        """从首页或三方服务的任务数量入口打开多任务浮层。"""
        if self._finish_opened_panel(timeout=0.5):
            return

        # 优先走 UI 树定位；服务内浮窗不暴露时再用截图识别黑色浮窗。
        if self._open_from_visible_entry(timeout=8):
            return

        if self._open_from_screen_image(timeout=3):
            return

        if self._expand_collapsed_entry():
            if self._finish_opened_panel(timeout=0.5):
                return
            if self._open_from_visible_entry(timeout=4):
                return
            if self._open_from_screen_image(timeout=2):
                return

        # 三方服务刚进入时浮窗存在 5 秒默认展开态；前面若正好遇到过渡
        # 动画，这里再轮询一次入口，避免错过自动展开窗口。
        if self._open_from_visible_entry(timeout=6):
            return
        if self._open_from_screen_image(timeout=2):
            return
        if self._open_from_service_title_bar_image(timeout=2):
            return

        if self._expand_collapsed_entry():
            if self._finish_opened_panel(timeout=0.5):
                return
            if self._open_from_visible_entry(timeout=4):
                return
            if self._open_from_screen_image(timeout=2):
                return
            if self._open_from_service_title_bar_image(timeout=2):
                return

        self.wait_xpath(self.PANEL_XPATH, "多任务浮层", timeout=8)
        self.wait_xpath(self.HEADER_XPATH, "多任务浮层标题", timeout=8)
        self.dismiss_guide_if_present()

    def _entry_xpaths(self) -> tuple[str, ...]:
        """可通过 UI 树定位到的展开态多任务入口。"""
        return (
            self.COUNT_TEXT_XPATH,
            self.COUNT_TEXT_NO_ID_XPATH,
            self.COUNT_CONTAINER_NO_ID_XPATH,
            self.COUNT_STACK_NO_ID_XPATH,
            self.FLOATING_COLUMN_XPATH,
            self.FLOATING_STACK_XPATH,
            self.ENTRY_XPATH,
            self.LEGACY_SERVICE_ENTRY_XPATH,
            self.CLICKABLE_ENTRY_XPATH,
        )

    def _open_from_visible_entry(self, *, timeout: float) -> bool:
        """优先通过 UI 树中的多任务入口打开浮层，不依赖固定坐标。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            for xpath in self._entry_xpaths():
                for entry in self._find_all(xpath):
                    if self._click_visible_entry(entry):
                        return True
            time.sleep(0.3)
        return False

    def _click_visible_entry(self, entry: Any) -> bool:
        """点击已展开的多任务入口；只允许点击 txt_num 本身或其小型父容器。"""
        if not self._is_safe_multitask_entry(entry):
            return False

        try:
            entry.click()
        except Exception:
            pass
        else:
            if self._finish_opened_panel(timeout=1):
                return True

        for point in self._entry_touch_points(entry):
            if self._tap_point_and_finish(point, timeout=1.5):
                return True

        return False

    def _is_safe_multitask_entry(self, entry: Any) -> bool:
        """过滤掉误匹配到的业务页面大容器，避免在三方服务页乱点。"""
        bounds = entry.getBounds()
        left = int(bounds.left)
        top = int(bounds.top)
        right = int(bounds.right)
        bottom = int(bounds.bottom)
        width = max(1, right - left)
        height = max(1, bottom - top)

        # 多任务入口是右侧小浮层的一部分；全屏业务容器或页面卡片不能点击。
        if width > 320 or height > 560:
            return False
        if left < 0:
            return False
        screen_width, screen_height = self._screen_size()
        if screen_width and right < int(screen_width * 0.68):
            return False
        if self._is_home_top_entry(
            left=left,
            top=top,
            right=right,
            bottom=bottom,
            width=width,
            height=height,
            screen_width=screen_width,
            screen_height=screen_height,
        ):
            return True
        if screen_height and bottom < int(screen_height * 0.55):
            return False
        return True

    def _is_home_top_entry(
        self,
        *,
        left: int,
        top: int,
        right: int,
        bottom: int,
        width: int,
        height: int,
        screen_width: int,
        screen_height: int,
    ) -> bool:
        """首页多任务入口在右上角，不套用服务内浮窗的下半屏限制。"""
        if self.find_xpath('//*[@id="TabHomeCompRoot"]') is None:
            return False
        if not screen_width or not screen_height:
            return False
        return (
            right >= int(screen_width * 0.82)
            and int(screen_height * 0.08) <= top <= int(screen_height * 0.25)
            and bottom <= int(screen_height * 0.35)
            and width <= 180
            and height <= 180
        )

    def _open_from_screen_image(self, *, timeout: float) -> bool:
        """UI 树点击失败时，只根据截图识别出的黑色浮窗区域点击，不使用固定坐标。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            for point in self._floating_entry_points_by_screen_image():
                if self._tap_point_and_finish(point, timeout=1):
                    return True
            time.sleep(0.4)
        return False

    def _open_from_service_title_bar_image(self, *, timeout: float) -> bool:
        """从三方服务顶部标题栏右侧“四点”按钮打开多任务。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            for point in self._service_title_bar_multitask_points_by_screen_image():
                if self._tap_point_and_finish(point, timeout=1):
                    return True
            time.sleep(0.4)
        return False

    def _expand_collapsed_entry(self) -> bool:
        """UI 树没有入口时，用截图识别黑色浮窗本体并点击展开。"""
        for point in self._floating_entry_points_by_screen_image():
            if self._tap_point_and_finish(point, timeout=1):
                return True
            if self.find_xpath(self.COUNT_TEXT_XPATH) is not None:
                return True
            time.sleep(0.4)
        return False

    def _finish_opened_panel(self, *, timeout: float) -> bool:
        if not self._wait_panel_opened(timeout=timeout):
            return False

        self.dismiss_guide_if_present()
        if self._wait_task_panel_ready(timeout=max(1.5, timeout)):
            return True

        # 顶部服务胶囊的四点按钮也会打开 Sheet，但不是多任务列表。
        # 这里主动关闭错误 Sheet，继续尝试右侧黑色多任务浮窗。
        if self._wait_panel_opened(timeout=0.3):
            self.driver.press_back()
            self.wait_closed(timeout=2)
        return False

    def _wait_panel_opened(self, *, timeout: float) -> bool:
        return (
            self.driver.wait_for_component(
                BY.xpath(self.PANEL_XPATH),
                timeout=timeout,
            )
            is not None
        )

    def _wait_task_panel_ready(self, *, timeout: float) -> bool:
        ready_xpath = f"{self.HOME_CARD_XPATH} | {self.HEADER_XPATH}"
        return (
            self.driver.wait_for_component(
                BY.xpath(ready_xpath),
                timeout=timeout,
            )
            is not None
        )

    def _entry_touch_points(self, entry: Any) -> list[tuple[int, int]]:
        """从 UI 树控件边界推导多任务入口候选点，避免只点到数字文本。"""
        bounds = entry.getBounds()
        left = int(bounds.left)
        top = int(bounds.top)
        right = int(bounds.right)
        bottom = int(bounds.bottom)
        width = max(1, right - left)
        height = max(1, bottom - top)
        if self._is_count_text_entry(entry, width=width, height=height):
            return self._points_around_count_text(left, top, right, bottom)

        if height > width * 1.2:
            return self._points_in_floating_bounds(left, top, right, bottom)

        center_x = (left + right) // 2
        center_y = (top + bottom) // 2
        points = [
            (center_x, center_y),
            (center_x, int(top + height * 0.32)),
            (center_x, int(top + height * 0.45)),
            (int(left + width * 0.42), int(top + height * 0.35)),
            (int(left + width * 0.62), int(top + height * 0.35)),
            (int(right - max(2, width * 0.15)), int(top + height * 0.38)),
        ]
        return self._unique_points(points)

    def _is_count_text_entry(self, entry: Any, *, width: int, height: int) -> bool:
        """识别浮窗内的任务数量 Text，基于它反推上半区多任务按钮。"""
        try:
            properties = entry.getAllProperties().to_dict()
        except Exception:
            properties = {}
        if properties.get("id") == "txt_num":
            return True

        try:
            text = entry.getText().strip()
        except Exception:
            text = ""
        return bool(text.isdigit() and width <= 120 and height <= 120)

    @staticmethod
    def _points_around_count_text(
        left: int,
        top: int,
        right: int,
        bottom: int,
    ) -> list[tuple[int, int]]:
        """从 txt_num 边界推导顶部多任务图标点击点，避免误点下方反馈入口。"""
        width = max(1, right - left)
        height = max(1, bottom - top)
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        points = [
            (int(center_x + max(6, width * 0.15)), int(center_y - height * 0.35)),
            (center_x, int(center_y - height * 0.35)),
            (center_x, center_y),
            (int(center_x + max(6, width * 0.15)), center_y),
            (int(center_x + max(10, width * 0.25)), int(center_y - height * 0.35)),
        ]
        return MultiTaskPage._unique_points(
            (max(1, x), max(1, y)) for x, y in points
        )

    def _tap_point_and_finish(
        self,
        point: tuple[int, int],
        *,
        timeout: float,
    ) -> bool:
        """同一候选点用多种点击方式尝试，兼容不同 HarmonyOS 版本。"""
        point = self._clamp_point_to_screen(point)
        for click_method in (
            self._click_with_driver,
            self._click_with_mouse,
            self._click_with_uitest,
            self._click_with_uinput,
        ):
            try:
                click_method(point)
            except Exception:
                continue
            if self._finish_opened_panel(timeout=timeout):
                return True

        if self._should_use_uinput_swipe_tap():
            try:
                self._click_with_uinput_swipe_tap(point)
            except Exception:
                return False
            if self._finish_opened_panel(timeout=timeout):
                return True
        return False

    def _click_with_uinput_swipe_tap(self, point: tuple[int, int]) -> None:
        """用极短滑动模拟点击；部分系统浮窗对普通 click 不响应。"""
        x, y = point
        subprocess.run(
            [
                os.environ.get("HDC_EXE", "hdc"),
                "-t",
                self._usb_device_serial(),
                "shell",
                "uinput",
                "-T",
                "-m",
                str(int(x)),
                str(int(y)),
                str(int(x)),
                str(int(y)),
                "100",
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def _click_with_uitest(self, point: tuple[int, int]) -> None:
        """使用 Harmony uitest 坐标点击，优先处理系统浮窗。"""
        x, y = point
        subprocess.run(
            [
                os.environ.get("HDC_EXE", "hdc"),
                "-t",
                self._usb_device_serial(),
                "shell",
                "uitest",
                "uiInput",
                "click",
                str(int(x)),
                str(int(y)),
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def _click_with_uinput(self, point: tuple[int, int]) -> None:
        """使用设备级触摸事件兜底点击系统浮窗。"""
        x, y = point
        subprocess.run(
            [
                os.environ.get("HDC_EXE", "hdc"),
                "-t",
                self._usb_device_serial(),
                "shell",
                "uinput",
                "-T",
                "-c",
                str(int(x)),
                str(int(y)),
            ],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )

    def _click_with_driver(self, point: tuple[int, int]) -> None:
        """使用 Hypium 坐标点击兜底，兼容部分 UI 层可点击浮窗。"""
        self.driver.click(point)

    def _click_with_mouse(self, point: tuple[int, int]) -> None:
        """部分系统浮层对普通触摸不响应，尝试鼠标输入通道。"""
        self.driver.mouse_click(point)

    def _screen_size(self) -> tuple[int, int]:
        """从根节点边界获取当前屏幕尺寸，用于过滤状态栏数字等误匹配。"""
        try:
            root = self.driver.wait_for_component(BY.xpath("/*"), timeout=0.5)
            if root is None:
                return 0, 0
            bounds = root.getBounds()
            return (
                max(0, int(bounds.right) - int(bounds.left)),
                max(0, int(bounds.bottom) - int(bounds.top)),
            )
        except Exception:
            return 0, 0

    def _clamp_point_to_screen(self, point: tuple[int, int]) -> tuple[int, int]:
        """候选点来自截图或 UI 边界推导，点击前收敛到屏幕内，避免越界误点。"""
        x, y = point
        screen_width, screen_height = self._screen_size()
        if screen_width:
            x = min(max(1, int(x)), screen_width - 1)
        else:
            x = max(1, int(x))
        if screen_height:
            y = min(max(1, int(y)), screen_height - 1)
        else:
            y = max(1, int(y))
        return x, y

    def _should_use_uinput_swipe_tap(self) -> bool:
        """5.x 设备会把短滑点击识别成拖动浮窗；仅在 6.x 及以上作为最后兜底。"""
        version = self._uitest_version()
        match = re.match(r"^(\d+)", version)
        if match is None:
            return False
        return int(match.group(1)) >= 6

    @classmethod
    def _usb_device_serial(cls) -> str:
        """读取当前 USB 连接设备；多任务浮球属于系统层，需通过 hdc 触摸点击。"""
        if cls._CACHED_USB_SERIAL is not None:
            return cls._CACHED_USB_SERIAL

        result = subprocess.run(
            [os.environ.get("HDC_EXE", "hdc"), "list", "targets"],
            check=True,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
        )
        serials = []
        for line in result.stdout.splitlines():
            stripped = line.strip()
            if not stripped or stripped == "[Empty]" or "Offline" in stripped:
                continue
            serial = stripped.split()[0]
            if ":" not in serial:
                serials.append(serial)
        if len(serials) != 1:
            raise RuntimeError(
                "多任务浮球点击需要唯一 USB 设备，"
                f"当前 hdc USB 设备：{serials}"
            )
        cls._CACHED_USB_SERIAL = serials[0]
        return cls._CACHED_USB_SERIAL

    @classmethod
    def _uitest_version(cls) -> str:
        if cls._CACHED_UITEST_VERSION is not None:
            return cls._CACHED_UITEST_VERSION

        try:
            result = subprocess.run(
                [
                    os.environ.get("HDC_EXE", "hdc"),
                    "-t",
                    cls._usb_device_serial(),
                    "shell",
                    "uitest",
                    "--version",
                ],
                check=False,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                timeout=10,
            )
        except Exception:
            cls._CACHED_UITEST_VERSION = ""
            return cls._CACHED_UITEST_VERSION

        cls._CACHED_UITEST_VERSION = (
            result.stdout.strip() or result.stderr.strip()
        )
        return cls._CACHED_UITEST_VERSION

    def _floating_entry_points_by_screen_image(self) -> list[tuple[int, int]]:
        """XPath 不暴露浮球时，识别右侧黑色浮球并返回上半区候选点击点。"""
        with TemporaryDirectory() as temp_dir:
            screenshot_path = Path(temp_dir) / "multitask_entry.jpeg"
            saved_path = Path(
                self.driver.capture_screen(str(screenshot_path), in_pc=True)
            )
            with Image.open(saved_path) as screenshot:
                screenshot = screenshot.convert("RGB")
                width, height = screenshot.size
                black_pixels = []
                min_x = int(width * 0.72)
                min_y = int(height * 0.18)
                for y in range(min_y, height):
                    for x in range(min_x, width):
                        red, green, blue = screenshot.getpixel((x, y))
                        if red < 70 and green < 70 and blue < 70:
                            black_pixels.append((x, y))
                floating_bounds = self._largest_floating_black_bounds(
                    black_pixels,
                    width=width,
                    height=height,
                )
                if floating_bounds is None:
                    return []

                icon_points = self._white_top_icon_points(
                    screenshot,
                    floating_bounds,
                )
                top_area_points = self._points_in_floating_bounds(
                    *floating_bounds,
                )
                if icon_points:
                    return self._unique_points(
                        [*top_area_points, *icon_points]
                    )

        left, top, right, bottom = floating_bounds
        return self._points_in_floating_bounds(left, top, right, bottom)

    def _service_title_bar_multitask_points_by_screen_image(
        self,
    ) -> list[tuple[int, int]]:
        """识别服务页顶部标题栏右侧四点图标，作为服务内多任务入口。"""
        if self.find_xpath('//Text[@id="title"]') is None:
            return []

        with TemporaryDirectory() as temp_dir:
            screenshot_path = Path(temp_dir) / "service_title_bar.jpeg"
            saved_path = Path(
                self.driver.capture_screen(str(screenshot_path), in_pc=True)
            )
            with Image.open(saved_path) as screenshot:
                screenshot = screenshot.convert("RGB")
                width, height = screenshot.size
                left = int(width * 0.62)
                right = int(width * 0.86)
                top = int(height * 0.055)
                bottom = int(height * 0.13)
                dark_pixels = []
                for y in range(top, bottom):
                    for x in range(left, right):
                        red, green, blue = screenshot.getpixel((x, y))
                        if red < 85 and green < 85 and blue < 85:
                            dark_pixels.append((x, y))

        if not dark_pixels:
            return []

        min_x = min(x for x, _ in dark_pixels)
        icon_pixels = [(x, y) for x, y in dark_pixels if x <= min_x + 90]
        if not icon_pixels:
            return []

        icon_left = min(x for x, _ in icon_pixels)
        icon_right = max(x for x, _ in icon_pixels)
        icon_top = min(y for _, y in icon_pixels)
        icon_bottom = max(y for _, y in icon_pixels)
        center_x = (icon_left + icon_right) // 2
        center_y = (icon_top + icon_bottom) // 2
        return self._unique_points(
            (
                (center_x, center_y),
                (center_x + 8, center_y),
                (center_x - 8, center_y),
                (center_x, center_y + 8),
            )
        )

    @staticmethod
    def _white_top_icon_points(
        screenshot: Image.Image,
        bounds: tuple[int, int, int, int],
    ) -> list[tuple[int, int]]:
        left, top, right, bottom = bounds
        floating_height = max(1, bottom - top)
        floating_width = max(1, right - left)
        min_icon_top = int(top + floating_height * 0.16)
        max_icon_bottom = int(top + floating_height * 0.52)
        white_pixels = []
        for y in range(top, bottom + 1):
            for x in range(left, right + 1):
                red, green, blue = screenshot.getpixel((x, y))
                if red > 180 and green > 180 and blue > 180:
                    white_pixels.append((x, y))

        candidates = set(white_pixels)
        best_bounds = None
        best_area = 0
        while candidates:
            start = candidates.pop()
            stack = [start]
            c_left = c_right = start[0]
            c_top = c_bottom = start[1]
            area = 1
            while stack:
                x, y = stack.pop()
                for neighbor in (
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ):
                    if neighbor not in candidates:
                        continue
                    candidates.remove(neighbor)
                    stack.append(neighbor)
                    nx, ny = neighbor
                    c_left = min(c_left, nx)
                    c_right = max(c_right, nx)
                    c_top = min(c_top, ny)
                    c_bottom = max(c_bottom, ny)
                    area += 1

            c_width = c_right - c_left
            c_height = c_bottom - c_top
            is_top_icon = (
                area >= 30
                and min_icon_top <= c_top
                and c_bottom <= max_icon_bottom
                and c_width <= floating_width * 0.75
                and c_height <= floating_height * 0.35
            )
            if is_top_icon and area > best_area:
                best_area = area
                best_bounds = (c_left, c_top, c_right, c_bottom)

        if best_bounds is None:
            return []

        c_left, c_top, c_right, c_bottom = best_bounds
        center_x = (c_left + c_right) // 2
        center_y = (c_top + c_bottom) // 2
        return MultiTaskPage._unique_points(
            (
                (center_x, center_y),
                (center_x, center_y + 8),
                (center_x, center_y - 8),
                (min(right - 4, center_x + 10), center_y),
            )
        )

    @staticmethod
    def _points_in_floating_bounds(
        left: int,
        top: int,
        right: int,
        bottom: int,
    ) -> list[tuple[int, int]]:
        floating_height = max(1, bottom - top)
        floating_width = max(1, right - left)
        center_x = (left + right) // 2
        center_y = (top + bottom) // 2

        if floating_height > floating_width * 1.2:
            # 贴右边显示时，可见黑色区域的中心可能偏离真实按钮中心；
            # 同时点可见区域中心和右侧，优先覆盖上半区多任务图标。
            x_candidates = [
                center_x,
                int(right - min(max(floating_width * 0.12, 4), 12)),
            ]
            y_candidates = [
                int(top + floating_height * 0.26),
                int(top + floating_height * 0.34),
            ]
            return MultiTaskPage._unique_points(
                (x, y) for y in y_candidates for x in x_candidates
            )

        return MultiTaskPage._unique_points(
            (
                (center_x, center_y),
                (int(left + floating_width * 0.65), center_y),
                (int(right - min(max(floating_width * 0.12, 4), 12)), center_y),
                (center_x, int(center_y - floating_height * 0.12)),
                (center_x, int(center_y + floating_height * 0.12)),
            )
        )

    @staticmethod
    def _unique_points(points: Any) -> list[tuple[int, int]]:
        unique = []
        seen = set()
        for x, y in points:
            point = (int(x), int(y))
            if point in seen:
                continue
            seen.add(point)
            unique.append(point)
        return unique

    @staticmethod
    def _largest_floating_black_bounds(
        black_pixels: list[tuple[int, int]],
        *,
        width: int,
        height: int,
    ) -> tuple[int, int, int, int] | None:
        """在右侧黑色像素中找到浮球主体，排除正文文字和底部导航图标。"""
        candidates = set(black_pixels)
        best_bounds = None
        best_area = 0
        while candidates:
            start = candidates.pop()
            stack = [start]
            left = right = start[0]
            top = bottom = start[1]
            area = 1
            while stack:
                x, y = stack.pop()
                for neighbor in (
                    (x + 1, y),
                    (x - 1, y),
                    (x, y + 1),
                    (x, y - 1),
                ):
                    if neighbor not in candidates:
                        continue
                    candidates.remove(neighbor)
                    stack.append(neighbor)
                    nx, ny = neighbor
                    left = min(left, nx)
                    right = max(right, nx)
                    top = min(top, ny)
                    bottom = max(bottom, ny)
                    area += 1

            box_width = right - left
            box_height = bottom - top
            is_floating_shape = (
                45 <= box_width <= 320
                and 45 <= box_height <= 560
                and right >= int(width * 0.82)
                and top >= int(height * 0.18)
            )
            if is_floating_shape and area > best_area:
                best_area = area
                best_bounds = (left, top, right, bottom)
        return best_bounds

    def dismiss_guide_if_present(self) -> None:
        """关闭账号首次打开多任务时出现的固定首页说明。"""
        confirm = self.driver.wait_for_component(
            BY.xpath(self.GUIDE_CONFIRM_XPATH),
            timeout=1,
        )
        if confirm is None:
            return
        confirm.click()
        deadline = time.time() + 3
        while time.time() < deadline:
            if self.find_xpath(self.GUIDE_CONFIRM_XPATH) is None:
                return
            time.sleep(0.2)
        raise RuntimeError(f"[{self.PAGE_NAME}] 多任务首次使用引导未关闭")

    def header_count(self) -> int:
        """读取“多任务窗口（N）”中的任务数量。"""
        header = self.find_xpath(self.HEADER_XPATH)
        if header is None:
            return -1
        matched = self.COUNT_PATTERN.fullmatch(header.getText().strip())
        return int(matched.group(1)) if matched else -1

    def visible_task_titles(self) -> tuple[str, ...]:
        """读取当前已渲染的任务卡片标题，包含固定首页。"""
        titles = []
        for component in self._find_all(self.TASK_TITLE_XPATH):
            title = component.getText().strip()
            if title:
                titles.append(title)
        return tuple(titles)

    def _swipe_task_list(self, direction: str) -> None:
        scroll = self.find_xpath(self.TASK_SCROLL_XPATH)
        if scroll is None and self.find_xpath(self.HOME_CARD_XPATH) is not None:
            return
        if scroll is None:
            scroll = self.wait_xpath(
                self.TASK_SCROLL_XPATH,
                "multitask scroll list",
                timeout=3,
            )
        self.driver.swipe(direction, distance=75, area=scroll)
        time.sleep(0.5)

    def scroll_to_top(self) -> None:
        """将虚拟任务列表滚动到顶部。"""
        previous = ()
        for _ in range(6):
            current = self.visible_task_titles()
            if current == previous:
                return
            previous = current
            self._swipe_task_list("DOWN")

    def all_task_titles(self, *, expected_count: int) -> tuple[str, ...]:
        """滚动虚拟列表并汇总所有任务标题。"""
        initial_titles = self.visible_task_titles()
        if len(initial_titles) >= expected_count:
            return initial_titles

        self.scroll_to_top()
        titles = []
        unchanged_rounds = 0
        for _ in range(10):
            previous_count = len(titles)
            for title in self.visible_task_titles():
                if title not in titles:
                    titles.append(title)
            if len(titles) >= expected_count:
                break
            if len(titles) == previous_count:
                unchanged_rounds += 1
                if unchanged_rounds >= 2:
                    break
            else:
                unchanged_rounds = 0
            self._swipe_task_list("UP")
        return tuple(titles)

    def wait_count_consistent(
        self,
        *,
        expected_count: int | None = None,
        timeout: float = 8,
    ) -> tuple[int, tuple[str, ...]]:
        """等待标题计数与滚动遍历得到的实际任务数保持一致。"""
        deadline = time.time() + timeout
        latest = (-1, ())
        while time.time() < deadline:
            count = self.header_count()
            if count < 1 or (
                expected_count is not None and count != expected_count
            ):
                time.sleep(0.4)
                continue
            titles = self.all_task_titles(expected_count=count)
            latest = (count, titles)
            if (
                count == len(titles)
                and (expected_count is None or count == expected_count)
            ):
                return latest
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 多任务计数不一致，"
            f"期望={expected_count}，实际标题计数/任务标题={latest}"
        )

    def first_deletable_task_title(self) -> str:
        """返回第一个带删除按钮的三方服务标题。"""
        components = self._find_all(self.DELETABLE_TASK_TITLE_XPATH)
        if not components:
            raise RuntimeError(f"[{self.PAGE_NAME}] 未找到可删除的三方服务")
        return components[0].getText().strip()

    def delete_first_external_task(self) -> str:
        """删除第一个三方服务任务，固定首页不会被选择。"""
        self.scroll_to_top()
        task_title = self.first_deletable_task_title()
        self.tap_xpath(
            self.DELETE_BUTTON_XPATH,
            f"三方服务“{task_title}”右上角删除按钮",
        )
        time.sleep(0.8)
        return task_title

    def tap_clear_all(self) -> None:
        """清除所有三方服务任务。"""
        for _ in range(8):
            button = self.find_xpath(self.CLEAR_ALL_XPATH)
            if button is not None:
                button.click()
                return
            self._swipe_task_list("UP")
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到一键清除按钮")

    def tap_home_card(self) -> None:
        """点击固定首页任务卡片。"""
        if self.find_xpath(self.HOME_CARD_XPATH) is None:
            self.scroll_to_top()
        self.tap_xpath(self.HOME_CARD_XPATH, "固定首页任务卡片")

    def wait_only_home(self, *, timeout: float = 8) -> None:
        """等待所有三方任务清除，仅保留固定首页。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            titles = self.visible_task_titles()
            if (
                self.header_count() == 1
                and titles == (self.HOME_TITLE,)
                and not self._find_all(self.DELETABLE_TASK_TITLE_XPATH)
            ):
                return
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 一键清除后未仅保留固定首页，"
            f"标题计数={self.header_count()}，任务标题={self.visible_task_titles()}"
        )

    def close(self) -> None:
        """点击浮层右上角叉号。"""
        self.tap_xpath(self.CLOSE_BUTTON_XPATH, "多任务浮层右上角关闭按钮")

    def is_open(self) -> bool:
        return self._wait_panel_opened(timeout=0.8)

    def reopen_if_closed(self) -> None:
        """兼容一键清除后自动收起浮层的设备版本。"""
        if not self.is_open():
            self.open()

    def wait_closed(self, *, timeout: float = 8) -> None:
        """等待多任务浮层关闭。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            if self.find_xpath(self.PANEL_XPATH) is None:
                return
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 多任务浮层未关闭")

