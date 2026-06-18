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
    def trip_card_xpath(trip_name: str) -> str:
        return f'//SheetPage//Text[@text="{trip_name}"]'

    @staticmethod
    def trip_name_input_value_xpath(trip_name: str) -> str:
        return f'//Dialog//TextInput[@text="{trip_name}"]'

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

    def tap_create_and_add(self) -> None:
        self.tap_xpath(self.CREATE_AND_ADD_XPATH, "创建并添加")

    def tap_trip(self, trip_name: str) -> None:
        self.tap_xpath(self.trip_card_xpath(trip_name), f"行程“{trip_name}”")

    def tap_close(self) -> None:
        self.tap_xpath(self.CLOSE_BUTTON_XPATH, "添加至行程弹窗关闭按钮")
