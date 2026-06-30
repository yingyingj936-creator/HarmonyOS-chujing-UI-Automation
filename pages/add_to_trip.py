import time

from hypium import BY

from pages.base_page import BasePage


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
        self.input_xpath(
            self.TRIP_NAME_INPUT_XPATH,
            trip_name,
            "新建行程名称输入框",
        )

    def clear_and_input_trip_name(self, trip_name: str) -> None:
        component = self.wait_xpath(
            self.TRIP_NAME_INPUT_XPATH,
            "新建行程名称输入框",
        )
        component.clearText()
        component.inputText(trip_name)

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
