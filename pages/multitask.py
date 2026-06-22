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
    ENTRY_XPATH = (
        '//*[@id="TabHomeCompRoot"]'
        '//RelativeContainer[@clickable="true" and ./Text[@id="txt_num"]]'
    )
    SERVICE_ENTRY_XPATH = (
        '//Stack/Column[./Divider and ./Image[@clickable="true"]]'
        '/RelativeContainer[@clickable="true" and ./Text]'
    )
    LEGACY_SERVICE_ENTRY_XPATH = (
        '//RelativeContainer[@clickable="true" and ./Text[@id="txt_num"]]'
    )
    FLOATING_COLUMN_XPATH = '//Column[.//Text[@id="txt_num"] and ./Divider]'
    FLOATING_STACK_XPATH = '//Stack[.//Text[@id="txt_num"] and .//Divider]'
    COUNT_TEXT_XPATH = '//Text[@id="txt_num"]'
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
        for point in self._floating_entry_points_by_screen_image():
            self._touch_screen_point(point)
            if self._wait_panel_opened(timeout=4):
                self.wait_xpath(self.HEADER_XPATH, "多任务浮层标题", timeout=8)
                self.dismiss_guide_if_present()
                return

        entry_xpaths = (
            self.ENTRY_XPATH,
            self.SERVICE_ENTRY_XPATH,
            self.LEGACY_SERVICE_ENTRY_XPATH,
            self.FLOATING_COLUMN_XPATH,
            self.FLOATING_STACK_XPATH,
            self.COUNT_TEXT_XPATH,
        )
        for xpath in entry_xpaths:
            entries = self._find_all(xpath)
            if not entries:
                entry = self.driver.wait_for_component(
                    BY.xpath(xpath),
                    timeout=1,
                )
                entries = [entry] if entry is not None else []

            for entry in entries:
                self._click_multitask_entry(entry)
                if self._wait_panel_opened(timeout=3):
                    self.wait_xpath(self.HEADER_XPATH, "多任务浮层标题", timeout=8)
                    self.dismiss_guide_if_present()
                    return

        for point in self._floating_entry_points_by_screen_image():
            self._touch_screen_point(point)
            if self._wait_panel_opened(timeout=4):
                self.wait_xpath(self.HEADER_XPATH, "多任务浮层标题", timeout=8)
                self.dismiss_guide_if_present()
                return

        self.wait_xpath(self.PANEL_XPATH, "多任务浮层", timeout=8)
        self.wait_xpath(self.HEADER_XPATH, "多任务浮层标题", timeout=8)
        self.dismiss_guide_if_present()

    def _wait_panel_opened(self, *, timeout: float) -> bool:
        return (
            self.driver.wait_for_component(
                BY.xpath(self.PANEL_XPATH),
                timeout=timeout,
            )
            is not None
        )

    def _click_multitask_entry(self, entry: Any) -> None:
        """新版浮球下半部分是反馈入口，命中整条浮球时只点上半部分。"""
        bounds = entry.getBounds()
        left = int(bounds.left)
        top = int(bounds.top)
        right = int(bounds.right)
        bottom = int(bounds.bottom)
        width = max(1, right - left)
        height = max(1, bottom - top)
        if height > width * 1.2:
            self._touch_screen_point(
                (
                    (left + right) // 2,
                    top + height // 4,
                )
            )
        else:
            self._touch_screen_point(((left + right) // 2, (top + bottom) // 2))

    def _touch_screen_point(self, point: tuple[int, int]) -> None:
        """用设备级触摸事件点击系统浮球，Hypium click 对该浮层不稳定。"""
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

    @staticmethod
    def _usb_device_serial() -> str:
        """读取当前 USB 连接设备；多任务浮球属于系统层，需通过 hdc 触摸点击。"""
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
        return serials[0]

    def _floating_entry_points_by_screen_image(self) -> list[tuple[int, int]]:
        """XPath 不暴露浮球时，识别右下角黑色浮球并返回上半区候选点击点。"""
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
                min_y = int(height * 0.55)
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
            return self._right_bottom_floating_fallback_points(width, height)

        left, top, right, bottom = floating_bounds
        floating_height = max(1, bottom - top)
        floating_width = max(1, right - left)
        icon_x_offset = int(min(max(floating_width * 0.30, 55), 75))
        icon_y_offset = int(min(max(floating_height * 0.21, 70), 95))
        icon_x = right - icon_x_offset
        icon_y = top + icon_y_offset
        return [
            *self._right_bottom_floating_fallback_points(width, height),
            (icon_x, icon_y),
            (icon_x, icon_y + 20),
            (icon_x, icon_y + 40),
            (icon_x, icon_y - 15),
        ]

    @staticmethod
    def _right_bottom_floating_fallback_points(
        width: int,
        height: int,
    ) -> list[tuple[int, int]]:
        """服务页内容与黑色悬浮球合并时使用的兜底点击点。"""
        return [
            (int(width * 0.953), int(height * 0.829)),
            (int(width * 0.953), int(height * 0.845)),
            (int(width * 0.94), int(height * 0.78)),
            (int(width * 0.94), int(height * 0.80)),
            (int(width * 0.94), int(height * 0.82)),
            (int(width * 0.91), int(height * 0.80)),
        ]

    @staticmethod
    def _largest_floating_black_bounds(
        black_pixels: list[tuple[int, int]],
        *,
        width: int,
        height: int,
    ) -> tuple[int, int, int, int] | None:
        """在右下角黑色像素中找到浮球主体，排除瀑布流文字和底部导航图标。"""
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
                50 <= box_width <= 280
                and 120 <= box_height <= 520
                and right >= int(width * 0.88)
                and top >= int(height * 0.55)
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

