from pages.base_page import BasePage


class TripVideoTutorialPage(BasePage):
    """行程页“查看视频教程”页面。"""

    PAGE_NAME = "TripVideoTutorialPage"

    TUTORIAL_TITLE_XPATH = '//Text[@text="视频教程"]'
    BACK_BUTTON_XPATH = '//Row[@clickable="true" and ./Image]'

    def wait_loaded(self, *, timeout: float = 10) -> None:
        """等待视频教程页展示教程相关内容，避免白屏误判。"""
        self.wait_xpath(
            self.TUTORIAL_TITLE_XPATH,
            "视频教程页标题",
            timeout=timeout,
        )

    def tap_back(self, *, timeout: float = 8) -> None:
        """点击视频教程页返回按钮。"""
        self.tap_xpath(
            self.BACK_BUTTON_XPATH,
            "视频教程页返回按钮",
            timeout=timeout,
        )
