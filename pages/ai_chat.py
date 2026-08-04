import time
from typing import Any

from hypium import BY

from pages.base_page import BasePage


class AiChatPage(BasePage):
    """AI 对话页公共页面对象。"""

    PAGE_NAME = "AiChatPage"
    PAGE_READY_XPATH = (
        '//Text[contains(@text, "AI")]'
        ' | //Text[contains(@text, "智能")]'
        ' | //Text[contains(@text, "助手")]'
        ' | //Text[contains(@text, "对话")]'
        ' | //Text[contains(@text, "发送")]'
        ' | //Text[contains(@text, "继续提问")]'
        ' | //Text[contains(@text, "重新生成")]'
        ' | //TextInput'
    )
    OVERLAY_READY_XPATH = (
        '//Text[contains(@text, "助手")]'
        ' | //Text[contains(@text, "对话")]'
        ' | //Text[contains(@text, "发送")]'
        ' | //Text[contains(@text, "继续提问")]'
        ' | //Text[contains(@text, "重新生成")]'
        ' | //TextInput[contains(@hint, "问") or contains(@hint, "输入")]'
    )
    FALLBACK_READY_XPATH = (
        '//*[not(@id="GlobalSearchResultComp") '
        'and not(@id="mapPageRoot") '
        'and not(@id="TabHomeCompRoot") '
        'and (self::Web '
        'or self::XComponent '
        'or self::Text '
        'or self::TextInput '
        'or self::List '
        'or self::Column '
        'or self::Row '
        'or self::Stack '
        'or @clickable="true" '
        'or @scrollable="true")]'
    )

    def wait_loaded(
        self,
        *,
        previous_root_xpath: str | None = None,
        timeout: float = 12,
    ) -> Any:
        """
        等待 AI 对话页加载。

        如果来源页根节点仍在 UI 树里，只接受更像对话页的控件，避免把来源页
        里的“AI总结/问一问”误判成已跳转。
        """
        deadline = time.monotonic() + timeout
        latest_state = "未检测到 AI 对话页特征"
        source_hidden_since: float | None = None

        while time.monotonic() < deadline:
            previous_visible = False
            if previous_root_xpath:
                previous_visible = (
                    self.driver.wait_for_component(
                        BY.xpath(previous_root_xpath),
                        timeout=0.2,
                    )
                    is not None
                )
                if previous_visible:
                    source_hidden_since = None
                elif source_hidden_since is None:
                    source_hidden_since = time.monotonic()

            ready_xpath = (
                self.OVERLAY_READY_XPATH
                if previous_visible
                else self.PAGE_READY_XPATH
            )
            ready = self.driver.wait_for_component(
                BY.xpath(ready_xpath),
                timeout=0.5,
            )
            if ready is not None:
                return ready

            if source_hidden_since and time.monotonic() - source_hidden_since >= 1:
                fallback_ready = self.driver.wait_for_component(
                    BY.xpath(self.FALLBACK_READY_XPATH),
                    timeout=0.5,
                )
                if fallback_ready is not None:
                    return fallback_ready

            latest_state = (
                "来源页仍可见，未检测到对话页输入/发送类控件"
                if previous_visible
                else "来源页已退出，未检测到 AI 对话页内容"
            )
            time.sleep(0.3)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] AI 对话页未加载完成，最后状态：{latest_state}"
        )

    def press_system_back(self) -> None:
        """使用系统返回键离开 AI 对话页。"""
        self.driver.press_back()
        time.sleep(1.5)
