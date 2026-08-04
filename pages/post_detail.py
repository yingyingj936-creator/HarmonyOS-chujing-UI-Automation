import re
import time

from hypium import BY

from utils.allure_visual import (
    component_has_red_highlight,
    component_has_red_or_yellow_highlight,
)
from utils.component_cache import invalidate_component_cache

from pages.base_page import BasePage


class PostDetailPage(BasePage):
    """出境服务帖子详情页面对象。"""

    PAGE_NAME = "PostDetailPage"
    ROOT_XPATH = '//*[@id="ezLongTake_PostPage_StackId"]'
    CONTENT_LIST_XPATH = f'{ROOT_XPATH}//List'
    BACK_BUTTON_XPATH = f'{ROOT_XPATH}//Row[@clickable="true" and ./Image]'
    GALLERY_XPATH = f'{CONTENT_LIST_XPATH}//__Common__[@clickable="true"]'
    BODY_TEXT_XPATH = f'{CONTENT_LIST_XPATH}//Text'
    VIEW_ROW_XPATH = f'{CONTENT_LIST_XPATH}/ListItem/Row/Row[2]/Row[1]'
    VIEW_COUNT_XPATH = f'{VIEW_ROW_XPATH}/Text[1]'
    STATS_ROW_XPATH = f'{CONTENT_LIST_XPATH}/ListItem/Row/Row[2]'
    LIKE_ROW_XPATH = f'{CONTENT_LIST_XPATH}/ListItem/Row/Row[2]/Row[2]'
    LIKE_ICON_XPATH = f'{LIKE_ROW_XPATH}/Image[1]'
    LIKE_COUNT_XPATH = f'{LIKE_ROW_XPATH}/Text[1]'
    FAVORITE_ROW_XPATH = f'{CONTENT_LIST_XPATH}/ListItem/Row/Row[2]/Row[3]'
    FAVORITE_COUNT_XPATH = f'{FAVORITE_ROW_XPATH}/Text[1]'
    ACTION_BUTTON_CANDIDATE_XPATH = (
        f'{ROOT_XPATH}//*[@clickable="true" and .//Image]'
    )
    FAVORITE_TEXT_ACTION_XPATH = (
        f'{ROOT_XPATH}//*[@clickable="true" and '
        '(.//Text[contains(@text, "收藏")] '
        'or contains(@id, "collect") '
        'or contains(@id, "Collect") '
        'or contains(@key, "collect") '
        'or contains(@key, "Collect"))]'
    )
    MORE_GUIDES_TITLE_XPATH = (
        f'{CONTENT_LIST_XPATH}/ListItemGroup/Column'
        '//Text[starts-with(@text, "更多")]'
    )
    RELATED_WATERFALL_XPATH = f'{CONTENT_LIST_XPATH}//WaterFlow'
    FIRST_RELATED_CARD_XPATH = f'{RELATED_WATERFALL_XPATH}//Column[.//Text][1]'
    FIRST_RELATED_CARD_COVER_XPATH = f'{FIRST_RELATED_CARD_XPATH}//__Common__[@clickable="true"]'
    FIRST_RELATED_CARD_TITLE_XPATH = f'{FIRST_RELATED_CARD_XPATH}//Text[1]'
    PAGE_INDICATOR_PATTERN = re.compile(r"^\d+/\d+$")
    STAT_TEXT_PATTERN = re.compile(r"^\d+(?:\.\d+)?(?:万|w|W|k|K)?$")

    def wait_loaded(self, *, timeout: float = 10) -> None:
        self.wait_xpath(self.ROOT_XPATH, "帖子详情页", timeout=timeout)

    @staticmethod
    def _bounds_tuple(component) -> tuple[int, int, int, int]:
        bounds = component.getBounds()
        return (
            int(bounds.left),
            int(bounds.top),
            int(bounds.right),
            int(bounds.bottom),
        )

    @staticmethod
    def _component_text(component) -> str:
        try:
            return (component.getText() or "").strip()
        except Exception:
            return ""

    @staticmethod
    def _is_visible_bounds(bounds: tuple[int, int, int, int]) -> bool:
        left, top, right, bottom = bounds
        return right > left and bottom > top

    def _root_bounds(self) -> tuple[int, int, int, int] | None:
        root = self.find_xpath(self.ROOT_XPATH)
        if root is None:
            return None
        return self._bounds_tuple(root)

    def _click_center(self, component) -> None:
        left, top, right, bottom = self._bounds_tuple(component)
        self.driver.click(((left + right) // 2, (top + bottom) // 2))
        invalidate_component_cache(self.driver)

    def _find_back_button(self):
        root_bounds = self._root_bounds()
        components = self.driver.find_all_components(BY.xpath(self.BACK_BUTTON_XPATH))
        if components is None:
            return None
        if not isinstance(components, list):
            components = [components]

        candidates = []
        for component in components:
            bounds = self._bounds_tuple(component)
            if not self._is_visible_bounds(bounds):
                continue
            left, top, right, bottom = bounds
            width = right - left
            height = bottom - top
            if root_bounds is not None:
                root_left, root_top, root_right, root_bottom = root_bounds
                root_width = max(root_right - root_left, 1)
                root_height = max(root_bottom - root_top, 1)
                center_x = (left + right) / 2
                center_y = (top + bottom) / 2
                if center_x > root_left + root_width * 0.32:
                    continue
                if center_y > root_top + root_height * 0.18:
                    continue
                if width > root_width * 0.28 or height > root_height * 0.16:
                    continue
            candidates.append((top, left, component))

        if not candidates:
            return None
        candidates.sort(key=lambda item: (item[0], item[1]))
        return candidates[0][2]

    def back_button(self, *, timeout: float = 8):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            component = self._find_back_button()
            if component is not None:
                return component
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到帖子详情页左上角返回按钮")

    def scroll_to_top(self, *, max_swipes: int = 12) -> None:
        for swipe_count in range(max_swipes + 1):
            if (
                self.find_xpath(self.GALLERY_XPATH) is not None
                and self.gallery_page_indicator() is not None
            ):
                return
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "DOWN",
                distance=80,
                start_point=(0.5, 0.25),
                swipe_time=0.55,
            )
            time.sleep(0.5)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 滑动 {max_swipes} 次后仍未回到帖子图集区域"
        )

    def gallery_page_indicator(self):
        components = self.driver.find_all_components(BY.xpath("//Text"))
        if components is None:
            return None
        if not isinstance(components, list):
            components = [components]

        for component in components:
            text = component.getText().strip()
            if not self.PAGE_INDICATOR_PATTERN.fullmatch(text):
                continue
            left, top, right, bottom = self._bounds_tuple(component)
            if right > left and bottom > top:
                return component
        return None

    def top_gallery_component(self):
        """Return a visible gallery-like image near the top of the active detail page."""
        root = self.find_xpath(self.ROOT_XPATH)
        if root is None:
            return None
        root_left, root_top, root_right, _ = self._bounds_tuple(root)
        components = self.driver.find_all_components(BY.xpath(self.GALLERY_XPATH))
        if components is None:
            return None
        if not isinstance(components, list):
            components = [components]

        candidates = []
        for component in components:
            left, top, right, bottom = self._bounds_tuple(component)
            width = right - left
            height = bottom - top
            if width <= 100 or height <= 120:
                continue
            if right <= root_left or left >= root_right:
                continue
            # The real post gallery is rendered high on the detail page. Related
            # waterfall covers are lower and should not satisfy this proxy.
            if root_top <= top <= root_top + 650:
                candidates.append((top, component))
        if not candidates:
            return None
        candidates.sort(key=lambda item: item[0])
        return candidates[0][1]

    def wait_gallery_page_indicator(self, *, timeout: float = 8):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            component = self.gallery_page_indicator()
            if component is not None:
                return component
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到图集图片页码")

    def gallery_page_count(self) -> int:
        indicator_text = self.wait_gallery_page_indicator().getText().strip()
        _, total = indicator_text.split("/", maxsplit=1)
        return int(total)

    def visible_body_text(self, exclude_texts: tuple[str, ...] = ()):
        components = self.driver.find_all_components(BY.xpath(self.BODY_TEXT_XPATH))
        if components is None:
            return None
        if not isinstance(components, list):
            components = [components]

        for component in components:
            text = component.getText().strip()
            if not text or text == "---":
                continue
            if text in exclude_texts:
                continue
            if len(text) < 8:
                continue
            if self.PAGE_INDICATOR_PATTERN.fullmatch(text):
                continue
            if self.STAT_TEXT_PATTERN.fullmatch(text):
                continue
            if text.startswith("更多"):
                continue
            left, top, right, bottom = self._bounds_tuple(component)
            if right > left and bottom > top:
                return component
        return None

    def wait_visible_body_text(
        self,
        *,
        timeout: float = 8,
        exclude_texts: tuple[str, ...] = (),
    ):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            component = self.visible_body_text(exclude_texts=exclude_texts)
            if component is not None:
                return component
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到可见的帖子正文")

    def visible_author_info(self, author: str):
        if not author:
            return None
        component = self.driver.find_component(BY.text(author))
        if component is None:
            return None
        if self._is_visible_bounds(self._bounds_tuple(component)):
            return component
        return None

    def wait_author_avatar(self, author: str, *, timeout: float = 8):
        """优先识别作者头像；新版作者区移动时退化为作者信息可见。"""
        deadline = time.monotonic() + timeout
        last_author_component = None
        while time.monotonic() < deadline:
            author_component = self.driver.find_component(BY.text(author))
            images = self.driver.find_all_components(
                BY.xpath(f'{self.ROOT_XPATH}//Image')
            )
            if author_component is None:
                time.sleep(0.3)
                continue
            last_author_component = author_component
            if images is None:
                time.sleep(0.3)
                continue
            if not isinstance(images, list):
                images = [images]

            author_left, author_top, _, author_bottom = self._bounds_tuple(
                author_component
            )
            author_center_y = (author_top + author_bottom) / 2
            candidates = []
            for image in images:
                left, top, right, bottom = self._bounds_tuple(image)
                width = right - left
                height = bottom - top
                if (
                    40 <= width <= 160
                    and 40 <= height <= 160
                    and right <= author_left + 20
                    and top <= author_center_y <= bottom
                ):
                    candidates.append((author_left - right, image))
            if candidates:
                candidates.sort(key=lambda item: item[0])
                return candidates[0][1]
            time.sleep(0.3)

        if last_author_component is not None:
            return last_author_component

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未找到作者“{author}”左侧的可见头像"
        )

    def _visible_numeric_stat_components(self) -> list[tuple]:
        root = self.find_xpath(self.ROOT_XPATH)
        stats_left_limit = None
        if root is not None:
            root_left, _, root_right, _ = self._bounds_tuple(root)
            root_width = max(root_right - root_left, 1)
            stats_left_limit = root_left + root_width * 0.55

        texts = self.driver.find_all_components(
            BY.xpath(f'{self.CONTENT_LIST_XPATH}//Text')
        )
        if texts is None:
            return ()
        if not isinstance(texts, list):
            texts = [texts]

        numeric_texts = []
        for text_component in texts:
            text = text_component.getText().strip()
            if not self.STAT_TEXT_PATTERN.fullmatch(text):
                continue
            left, top, right, bottom = self._bounds_tuple(text_component)
            if right <= left or bottom <= top:
                continue
            if stats_left_limit is not None and left < stats_left_limit:
                continue
            numeric_texts.append((text_component, left, top, right, bottom))
        return numeric_texts

    @staticmethod
    def _best_stat_line(numeric_texts: list[tuple], *, min_count: int) -> list[tuple]:
        candidate_lines = []
        for item in numeric_texts:
            _, _, top, _, bottom = item
            center_y = (top + bottom) / 2
            same_line = [
                candidate
                for candidate in numeric_texts
                if abs(((candidate[2] + candidate[4]) / 2) - center_y) <= 35
            ]
            if len(same_line) >= min_count:
                same_line.sort(key=lambda candidate: candidate[1])
                line_bottom = max(candidate[4] for candidate in same_line)
                candidate_lines.append((line_bottom, len(same_line), same_line))
        if not candidate_lines:
            return []
        candidate_lines.sort(key=lambda item: (item[0], item[1]), reverse=True)
        return candidate_lines[0][2]

    def visible_engagement_stats(self) -> tuple:
        numeric_texts = self._visible_numeric_stat_components()
        same_line = self._best_stat_line(numeric_texts, min_count=3)
        if same_line:
            return tuple(candidate[0] for candidate in same_line[-3:])

        same_line = self._best_stat_line(numeric_texts, min_count=2)
        if same_line:
            components = [candidate[0] for candidate in same_line[-2:]]
            favorite_button = self._find_favorite_button()
            if favorite_button is not None:
                components.append(favorite_button)
            return tuple(components)
        return ()

    def wait_visible_engagement_stats(self, *, timeout: float = 8) -> tuple:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            stats = self.visible_engagement_stats()
            if len(stats) >= 2:
                return stats
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到可见的浏览/点赞/收藏数据")

    def _action_button_candidates(self) -> list:
        root_bounds = self._root_bounds()
        back_button = self._find_back_button()
        back_bounds = (
            self._bounds_tuple(back_button) if back_button is not None else None
        )
        components = self.driver.find_all_components(
            BY.xpath(self.ACTION_BUTTON_CANDIDATE_XPATH)
        )
        if components is None:
            return []
        if not isinstance(components, list):
            components = [components]

        candidates = []
        for component in components:
            bounds = self._bounds_tuple(component)
            if not self._is_visible_bounds(bounds):
                continue
            if back_bounds is not None and bounds == back_bounds:
                continue
            left, top, right, bottom = bounds
            width = right - left
            height = bottom - top
            if root_bounds is not None:
                root_left, root_top, root_right, root_bottom = root_bounds
                root_width = max(root_right - root_left, 1)
                root_height = max(root_bottom - root_top, 1)
                center_y = (top + bottom) / 2
                if center_y < root_top + root_height * 0.42:
                    continue
                if width > root_width * 0.32 or height > root_height * 0.18:
                    continue
            if width < 24 or height < 24:
                continue
            candidates.append(component)
        return candidates

    def _find_favorite_button(self):
        text_action = self.find_xpath(self.FAVORITE_TEXT_ACTION_XPATH)
        if text_action is not None and self._is_visible_bounds(
            self._bounds_tuple(text_action)
        ):
            return text_action

        old_action = self.find_xpath(self.FAVORITE_ROW_XPATH)
        if old_action is not None and self._is_visible_bounds(
            self._bounds_tuple(old_action)
        ):
            return old_action

        candidates = self._action_button_candidates()
        if not candidates:
            return None

        rows: list[tuple[float, list]] = []
        for component in candidates:
            left, top, right, bottom = self._bounds_tuple(component)
            center_y = (top + bottom) / 2
            for index, (row_y, row_components) in enumerate(rows):
                if abs(row_y - center_y) <= 80:
                    row_components.append(component)
                    rows[index] = (
                        (row_y * (len(row_components) - 1) + center_y)
                        / len(row_components),
                        row_components,
                    )
                    break
            else:
                rows.append((center_y, [component]))

        # 新版收藏和分享是并列悬浮按钮；当前布局左侧为分享，右侧为收藏。
        rows.sort(key=lambda item: (len(item[1]), item[0]), reverse=True)
        best_row = rows[0][1]
        best_row.sort(key=lambda component: self._bounds_tuple(component)[0])
        if len(best_row) >= 2:
            return best_row[-1]

        candidates.sort(key=lambda component: self._bounds_tuple(component)[1], reverse=True)
        return candidates[0]

    def favorite_button(self, *, timeout: float = 8):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            component = self._find_favorite_button()
            if component is not None:
                return component
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到帖子详情页收藏按钮")

    def _is_more_guides_visible(self) -> bool:
        return self.find_xpath(self.MORE_GUIDES_TITLE_XPATH) is not None

    def _swipe_detail_up(self) -> None:
        self.driver.swipe(
            "UP",
            distance=35,
            start_point=(0.5, 0.78),
            swipe_time=0.45,
        )
        time.sleep(0.45)

    def _swipe_detail_down(self) -> None:
        self.driver.swipe(
            "DOWN",
            distance=25,
            start_point=(0.5, 0.38),
            swipe_time=0.4,
        )
        time.sleep(0.4)

    def scroll_to_engagement_stats(self, *, max_swipes: int = 16) -> tuple:
        for swipe_count in range(max_swipes + 1):
            stats = self.visible_engagement_stats()
            if len(stats) >= 2:
                return stats
            if self._is_more_guides_visible():
                for _ in range(3):
                    self._swipe_detail_down()
                    stats = self.visible_engagement_stats()
                    if len(stats) >= 2:
                        return stats
                break
            if swipe_count == max_swipes:
                break
            self._swipe_detail_up()
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 滑动 {max_swipes} 次后仍未找到浏览/点赞/收藏数据"
        )

    def components_union_bounds(self, components: tuple) -> tuple[int, int, int, int]:
        if not components:
            raise RuntimeError(f"[{self.PAGE_NAME}] 组件列表为空，无法计算圈选区域")
        bounds = [self._bounds_tuple(component) for component in components]
        return (
            min(item[0] for item in bounds),
            min(item[1] for item in bounds),
            max(item[2] for item in bounds),
            max(item[3] for item in bounds),
        )

    def browse_gallery(self) -> tuple[str, str, bool]:
        gallery = self.wait_xpath(self.GALLERY_XPATH, "帖子图集")
        before_bounds = self._bounds_tuple(gallery)
        initial_indicator = self.wait_gallery_page_indicator().getText().strip()

        gallery.click()
        time.sleep(1)
        gallery_after_click = self.find_xpath(self.GALLERY_XPATH)
        preview_opened = self._find_back_button() is None
        if gallery_after_click is not None:
            after_bounds = self._bounds_tuple(gallery_after_click)
            preview_opened = preview_opened or (
                after_bounds[1] < before_bounds[1] - 50
                or after_bounds[3] > before_bounds[3] + 100
            )

        self.driver.swipe(
            "LEFT",
            distance=65,
            start_point=(0.82, 0.5),
            swipe_time=0.6,
        )

        deadline = time.monotonic() + 8
        current_indicator = initial_indicator
        while time.monotonic() < deadline:
            indicator = self.gallery_page_indicator()
            if indicator is not None:
                current_indicator = indicator.getText().strip()
                if current_indicator != initial_indicator:
                    return initial_indicator, current_indicator, preview_opened
            time.sleep(0.3)

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 图集滑动后页码未变化，"
            f"仍为 {current_indicator}"
        )

    def close_gallery_preview(self, preview_opened: bool) -> None:
        # 全屏预览不会移除原详情节点，不能用节点是否存在判断预览状态。
        # 点击图集后的产品行为固定为进入全屏预览，因此统一返回一次关闭。
        self.driver.press_back()
        self.wait_loaded(timeout=8)
        self.back_button(timeout=8)

    def scroll_to_article_metadata(
        self,
        title: str,
        author: str,
        *,
        max_swipes: int = 5,
    ) -> None:
        title_seen = False
        author_seen = False
        body_seen = False
        for swipe_count in range(max_swipes + 1):
            title_component = self.driver.find_component(BY.text(title))
            author_component = self.visible_author_info(author)
            body_component = self.visible_body_text(exclude_texts=(title, author))
            title_seen = title_seen or title_component is not None
            author_seen = author_seen or author_component is not None
            body_seen = body_seen or body_component is not None
            if title_seen and body_seen:
                return
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=35,
                start_point=(0.5, 0.78),
                swipe_time=0.5,
            )
            time.sleep(0.5)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 未完整找到标题和正文："
            f"title={title!r}, title_seen={title_seen}, "
            f"body_seen={body_seen}, author_seen={author_seen}, "
            f"author={author!r}"
        )

    def scroll_to_like_stats(self, *, max_swipes: int = 30) -> None:
        for swipe_count in range(max_swipes + 1):
            if (
                self.find_xpath(self.LIKE_ROW_XPATH) is not None
                or len(self.visible_engagement_stats()) >= 2
            ):
                return
            if self._is_more_guides_visible():
                for _ in range(3):
                    self._swipe_detail_down()
                    if (
                        self.find_xpath(self.LIKE_ROW_XPATH) is not None
                        or len(self.visible_engagement_stats()) >= 2
                    ):
                        return
                break
            if swipe_count == max_swipes:
                break
            self._swipe_detail_up()
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 滑动 {max_swipes} 次后仍未找到右下角点赞区域"
        )

    def try_scroll_to_more_guides(self, *, max_swipes: int = 30) -> bool:
        for swipe_count in range(max_swipes + 1):
            has_title = self.find_xpath(self.MORE_GUIDES_TITLE_XPATH) is not None
            has_card = self.find_xpath(self.FIRST_RELATED_CARD_XPATH) is not None
            if has_card:
                return True
            if has_title:
                for _ in range(4):
                    self._swipe_detail_up()
                    if self.find_xpath(self.FIRST_RELATED_CARD_XPATH) is not None:
                        return True
                return True
            if swipe_count == max_swipes:
                break
            self.driver.swipe(
                "UP",
                distance=70,
                start_point=(0.5, 0.78),
                swipe_time=0.5,
            )
            time.sleep(0.5)
        return False

    def scroll_to_more_guides(self, *, max_swipes: int = 30) -> None:
        if self.try_scroll_to_more_guides(max_swipes=max_swipes):
            return
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 滑动 {max_swipes} 次后仍未找到更多相关攻略"
        )

    def wait_related_guide_opened(self, *, timeout: float = 10) -> None:
        """Wait until the related guide opens and its top gallery is visible."""
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.top_gallery_component() is not None:
                return
            time.sleep(0.3)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] related guide top gallery did not become visible"
        )

    def tap_first_related_guide(self) -> None:
        for xpath in (
            self.FIRST_RELATED_CARD_TITLE_XPATH,
            self.FIRST_RELATED_CARD_COVER_XPATH,
            self.FIRST_RELATED_CARD_XPATH,
        ):
            component = self.find_xpath(xpath)
            if component is None:
                continue
            left, top, right, bottom = self._bounds_tuple(component)
            if right <= left or bottom <= top:
                continue
            self.driver.click(((left + right) // 2, (top + bottom) // 2))
            return
        self.wait_xpath(self.FIRST_RELATED_CARD_XPATH, "first related guide")

    def tap_back_button(self) -> None:
        self._click_center(self.back_button(timeout=8))

    @staticmethod
    def parse_like_count(value: str) -> int:
        normalized = value.replace(",", "").strip()
        multiplier = 1
        if normalized.endswith(("万", "w", "W")):
            multiplier = 10000
            normalized = normalized[:-1]
        elif normalized.endswith(("k", "K")):
            multiplier = 1000
            normalized = normalized[:-1]
        if not normalized.isdigit():
            try:
                return int(float(normalized) * multiplier)
            except ValueError as exc:
                raise RuntimeError(f"详情页点赞数格式异常：{value!r}") from exc
        return int(normalized) * multiplier

    def _icon_near_text(self, text_component):
        text_left, text_top, text_right, text_bottom = self._bounds_tuple(text_component)
        text_center_y = (text_top + text_bottom) / 2
        images = self.driver.find_all_components(BY.xpath(f'{self.ROOT_XPATH}//Image'))
        if images is None:
            return None
        if not isinstance(images, list):
            images = [images]

        candidates = []
        for image in images:
            left, top, right, bottom = self._bounds_tuple(image)
            width = right - left
            height = bottom - top
            center_y = (top + bottom) / 2
            if not (18 <= width <= 120 and 18 <= height <= 120):
                continue
            if abs(center_y - text_center_y) > 45:
                continue
            if right <= text_left + 12:
                candidates.append((text_left - right, image))
        if not candidates:
            return None
        candidates.sort(key=lambda item: item[0])
        return candidates[0][1]

    def like_action_component(self, *, timeout: float = 8):
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            old_row = self.find_xpath(self.LIKE_ROW_XPATH)
            if old_row is not None:
                return old_row
            stats = self.visible_engagement_stats()
            if len(stats) >= 2:
                icon = self._icon_near_text(stats[1])
                return icon or stats[1]
            time.sleep(0.3)
        raise RuntimeError(f"[{self.PAGE_NAME}] 未找到帖子详情页点赞区域")

    def like_count(self) -> int:
        component = self.find_xpath(self.LIKE_COUNT_XPATH)
        if component is None:
            component = self.wait_visible_engagement_stats()[1]
        return self.parse_like_count(component.getText())

    def favorite_count_text(self) -> str:
        component = self.find_xpath(self.FAVORITE_COUNT_XPATH)
        if component is not None:
            text = component.getText().strip()
            if self.STAT_TEXT_PATTERN.fullmatch(text):
                return text
        stats = self.wait_visible_engagement_stats()
        if len(stats) >= 3:
            text = self._component_text(stats[2])
            if self.STAT_TEXT_PATTERN.fullmatch(text):
                return text
        raise RuntimeError(f"[{self.PAGE_NAME}] 当前帖子详情页未展示可读取的收藏数")

    def favorite_count(self) -> int:
        return self.parse_like_count(self.favorite_count_text())

    def try_favorite_count(self) -> int | None:
        try:
            return self.favorite_count()
        except RuntimeError:
            return None

    def tap_favorite(self) -> None:
        self._click_center(self.favorite_button(timeout=8))

    def wait_favorite_count(
        self,
        expected: int,
        *,
        timeout: float = 10,
    ) -> int:
        deadline = time.monotonic() + timeout
        last_count: int | None = None
        while time.monotonic() < deadline:
            try:
                last_count = self.favorite_count()
            except RuntimeError:
                time.sleep(0.4)
                continue
            if last_count == expected:
                return last_count
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏数未变为 {expected}，最后读取={last_count}"
        )

    def wait_favorite_count_changed(
        self,
        original: int,
        *,
        timeout: float = 10,
    ) -> int:
        deadline = time.monotonic() + timeout
        last_count: int | None = None
        while time.monotonic() < deadline:
            try:
                last_count = self.favorite_count()
            except RuntimeError:
                time.sleep(0.4)
                continue
            if last_count != original:
                return last_count
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏数未从 {original} 发生变化，"
            f"最后读取={last_count}"
        )

    def ensure_favorite_unselected(self) -> int:
        """重复执行用例时，通过收藏数变化把帖子恢复为未收藏状态。"""
        current_count = self.try_favorite_count()
        if current_count is None:
            if self.is_favorite_highlighted():
                self.tap_favorite()
                self.wait_favorite_highlighted(False)
            return -1

        self.tap_favorite()
        changed_count = self.wait_favorite_count_changed(current_count)
        if changed_count < current_count:
            # 原状态为已收藏，点击后已取消收藏。
            return changed_count
        if changed_count > current_count:
            # 原状态为未收藏，点击后先收藏，再点回未收藏。
            self.tap_favorite()
            self.wait_favorite_count(current_count)
            return current_count

        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏数变化异常：{current_count} -> {changed_count}"
        )

    def is_liked(self) -> bool:
        icon = self.find_xpath(self.LIKE_ICON_XPATH)
        if icon is None:
            component = self.like_action_component(timeout=8)
            icon = self._icon_near_text(component) or component
        return component_has_red_highlight(self.driver, icon)

    def is_favorite_highlighted(self) -> bool:
        return component_has_red_or_yellow_highlight(
            self.driver,
            self.favorite_button(timeout=8),
        )

    def wait_favorite_highlighted(
        self,
        expected: bool,
        *,
        timeout: float = 10,
    ) -> bool:
        deadline = time.monotonic() + timeout
        while time.monotonic() < deadline:
            if self.is_favorite_highlighted() is expected:
                return expected
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 收藏按钮高亮状态未变为 {expected}"
        )

    def wait_like_count(
        self,
        expected: int,
        *,
        timeout: float = 10,
    ) -> int:
        deadline = time.monotonic() + timeout
        last_count: int | None = None
        while time.monotonic() < deadline:
            try:
                last_count = self.like_count()
            except RuntimeError:
                time.sleep(0.4)
                continue
            if last_count == expected:
                return last_count
            time.sleep(0.4)
        raise RuntimeError(
            f"[{self.PAGE_NAME}] 点赞数未变为 {expected}，最后读取={last_count}"
        )
