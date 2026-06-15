import re
import time
from typing import Any

from hypium import BY

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
        '//SheetWrapper//Grid/GridItem'
        '[.//Image[@clickable="true"]]//Image[@clickable="true"]'
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
        entry = self.driver.wait_for_component(
            BY.xpath(self.ENTRY_XPATH),
            timeout=2,
        )
        if entry is None:
            entry = self.driver.wait_for_component(
                BY.xpath(self.SERVICE_ENTRY_XPATH),
                timeout=4,
            )
        if entry is None:
            entry = self.wait_xpath(
                self.LEGACY_SERVICE_ENTRY_XPATH,
                "三方服务多任务数量入口",
                timeout=2,
            )
        entry.click()
        self.wait_xpath(self.PANEL_XPATH, "多任务浮层", timeout=8)
        self.wait_xpath(self.HEADER_XPATH, "多任务浮层标题", timeout=8)
        self.dismiss_guide_if_present()

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
        scroll = self.wait_xpath(
            self.TASK_SCROLL_XPATH,
            "多任务滚动列表",
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
        """点击固定的出境服务首页任务卡片。"""
        self.scroll_to_top()
        self.tap_xpath(self.HOME_CARD_XPATH, "多任务列表中的出境服务首页")

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
        return self.find_xpath(self.PANEL_XPATH) is not None

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
