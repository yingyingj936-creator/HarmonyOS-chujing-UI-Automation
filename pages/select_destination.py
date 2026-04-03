class SelectDestinationPage:
    """选择旅行目的地页对象。"""

    PAGE_TITLE_TEXT = "选择旅行目的地"
    MACAO_TEXT = "澳门"

    def __init__(self, driver):
        self.driver = driver

    def is_loaded(self) -> bool:
        """判断‘选择旅行目的地’页面是否加载成功。"""
        return self.driver(text=self.PAGE_TITLE_TEXT).exists

    def choose_macao(self):
        """点击澳门选项。"""
        self.driver(text=self.MACAO_TEXT).click()
