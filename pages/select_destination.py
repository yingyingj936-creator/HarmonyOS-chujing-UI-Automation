from hypium import BY


class SelectDestinationPage:
    """选择旅行目的地页对象。"""

    PAGE_TITLE_TEXT = "选择旅行目的地"
    MACAO_TEXT = "澳门"

    def __init__(self, driver):
        self.driver = driver

    def _find_by_text(self, text: str):
        """按文本查找组件。"""
        return self.driver.find_component(BY.text(text))

    def is_loaded(self) -> bool:
        """判断‘选择旅行目的地’页面是否加载成功。"""
        return self._find_by_text(self.PAGE_TITLE_TEXT) is not None

    def choose_macao(self):
        """点击澳门选项。"""
        self._find_by_text(self.MACAO_TEXT).click()
