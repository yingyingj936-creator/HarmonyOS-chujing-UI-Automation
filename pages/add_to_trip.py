import time

from hypium import BY

from pages.base_page import BasePage
from utils.component_cache import invalidate_component_cache


class AddToTripPage(BasePage):
    """“添加至行程”弹窗及新建行程对话框。"""

    PAGE_NAME = "AddToTripPage"
    SHEET_TITLE_XPATH = '//SheetPage//Text[@text="添加至行程"]'
    NEW_TRIP_BUTTON_XPATH = '//SheetPage//Text[@text="新建"]'
    TRIP_NAME_INPUT_XPATH = '//Dialog//TextInput[@hint="请输入行程名称"]'
    TRIP_NAME_DIALOG_TITLE_XPATH = '//Dialog//Text[@text="请输入行程名称"]'
    CREATE_AND_ADD_XPATH = '//Dialog//Text[@text="创建并添加" and @clickable="true"]'
    CLOSE_BUTTON_XPATH = '//SheetPage/Button'

    @staticmethod
    def _text_match_condition(text: str) -> str:
        return (
            f'@text="{text}" or contains(@text, "{text}") or '
            f'(string-length(@text) > 4 and contains("{text}", @text))'
        )

    @classmethod
    def trip_card_xpath(cls, trip_name: str) -> str:
        return (
            f'//SheetPage//Text[{cls._text_match_condition(trip_name)}]'
        )

    def tap_new_trip(self) -> None:
        self.tap_xpath(self.NEW_TRIP_BUTTON_XPATH, "新建行程")

    def input_trip_name(self, trip_name: str) -> None:
        self._set_trip_name(
            trip_name,
            clear_first=False,
            action_name="输入新建行程名称",
        )

    def clear_and_input_trip_name(
        self,
        trip_name: str,
        *,
        timeout: float = 10,
    ) -> None:
        self._set_trip_name(
            trip_name,
            clear_first=True,
            timeout=timeout,
            action_name="清空并输入新建行程名称",
        )

    def _set_trip_name(
        self,
        trip_name: str,
        *,
        clear_first: bool,
        timeout: float = 10,
        action_name: str,
    ) -> object:
        """稳定设置行程名称，避免全量执行时输入框焦点或清空动作被吞。"""
        deadline = time.time() + timeout
        last_value: str | None = None
        attempt = 0

        while time.time() < deadline:
            attempt += 1
            remaining = max(0.5, deadline - time.time())
            component = self.wait_xpath(
                self.TRIP_NAME_INPUT_XPATH,
                "新建行程名称输入框",
                timeout=min(2.0, remaining),
            )
            component.click()
            time.sleep(0.2)

            if clear_first:
                component.clearText()
                self._wait_trip_name_empty(timeout=min(2.0, remaining))

            component = self.wait_xpath(
                self.TRIP_NAME_INPUT_XPATH,
                "新建行程名称输入框",
                timeout=min(2.0, remaining),
            )
            component.click()
            time.sleep(0.2)
            component.inputText(trip_name)
            invalidate_component_cache(self.driver)

            verification_timeout = min(2.0, max(0.5, deadline - time.time()))
            try:
                return self.wait_trip_name_value(
                    trip_name,
                    timeout=verification_timeout,
                )
            except RuntimeError:
                refreshed = self.driver.wait_for_component(
                    BY.xpath(self.TRIP_NAME_INPUT_XPATH),
                    timeout=0.5,
                )
                if refreshed is not None:
                    last_value = (refreshed.getText() or "").strip()
                    if self._complete_trip_name_from_prefix(
                        refreshed,
                        trip_name,
                        current_value=last_value,
                        timeout=min(2.5, max(0.5, deadline - time.time())),
                    ):
                        return self.wait_trip_name_value(
                            trip_name,
                            timeout=min(1.5, max(0.5, deadline - time.time())),
                        )
                if clear_first and last_value:
                    try:
                        refreshed.clearText()
                    except Exception:
                        pass
                time.sleep(0.3)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] {action_name}失败：期望“{trip_name}”，"
            f"实际值={last_value!r}，重试次数={attempt}，timeout={timeout}s"
        )

    def _wait_trip_name_empty(self, *, timeout: float = 2) -> None:
        """等待输入框清空生效；未清空也不立即失败，后续重试会处理。"""
        deadline = time.time() + timeout
        while time.time() < deadline:
            component = self.driver.wait_for_component(
                BY.xpath(self.TRIP_NAME_INPUT_XPATH),
                timeout=0.5,
            )
            if component is not None and not (component.getText() or "").strip():
                return
            time.sleep(0.2)

    def _complete_trip_name_from_prefix(
        self,
        component,
        trip_name: str,
        *,
        current_value: str,
        timeout: float = 2.5,
    ) -> bool:
        """输入法偶发截断尾部字符时，只补齐缺失后缀，避免整段重输再次截断。"""
        if not current_value or not trip_name.startswith(current_value):
            return False

        deadline = time.time() + timeout
        last_value = current_value
        while time.time() < deadline and last_value != trip_name:
            missing = trip_name[len(last_value):]
            if not missing:
                break
            component.click()
            time.sleep(0.1)
            component.inputText(missing[:1])
            invalidate_component_cache(self.driver)
            time.sleep(0.2)

            component = self.driver.wait_for_component(
                BY.xpath(self.TRIP_NAME_INPUT_XPATH),
                timeout=0.5,
            )
            if component is None:
                return False
            current = (component.getText() or "").strip()
            if current == last_value:
                return False
            if not trip_name.startswith(current):
                return False
            last_value = current

        return last_value == trip_name

    def wait_trip_name_value(
        self,
        trip_name: str,
        *,
        timeout: float = 8,
    ) -> object:
        """等待命名输入框完成异步回显，并校验其真实文本值。"""
        deadline = time.time() + timeout
        last_value: str | None = None
        while time.time() < deadline:
            remaining = max(0.1, deadline - time.time())
            component = self.driver.wait_for_component(
                BY.xpath(self.TRIP_NAME_INPUT_XPATH),
                timeout=min(1.0, remaining),
            )
            if component is not None:
                last_value = (component.getText() or "").strip()
                if last_value == trip_name:
                    return component
            time.sleep(0.2)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 行程名称输入框未显示期望值“{trip_name}”，"
            f"实际值={last_value!r}，timeout={timeout}s"
        )

    def tap_create_and_add(self) -> None:
        self.tap_xpath(self.CREATE_AND_ADD_XPATH, "创建并添加")

    def tap_trip(self, trip_name: str) -> None:
        self.tap_xpath(self.trip_card_xpath(trip_name), f"行程“{trip_name}”")

    def tap_close(self) -> None:
        self.tap_xpath(self.CLOSE_BUTTON_XPATH, "添加至行程弹窗关闭按钮")
