import time

import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.mine_page import MinePage
from pages.outbound_home import HomeGuideCard, OutboundHomePage
from pages.post_detail import PostDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


MAX_CANDIDATE_FEED_SWIPES = 8


def _return_from_post_detail(driver, detail: PostDetailPage, wait_target, message: str) -> None:
    """从帖子详情返回目标页：页面内返回优先，失败后用侧滑和系统返回兜底。"""
    actions = (
        detail.tap_back_button,
        lambda: driver.swipe_to_back(side="RIGHT"),
        driver.press_back,
    )
    for action in actions:
        try:
            action()
        except RuntimeError:
            pass
        time.sleep(1)
        try:
            result = wait_target(timeout=4)
        except RuntimeError:
            continue
        if result is not False:
            return
    raise AssertionError(message)


def _open_unfavorited_post(
    home: OutboundHomePage,
    detail: PostDetailPage,
) -> tuple[HomeGuideCard, int | None]:
    """选择可收藏的帖子，并确保进入用例步骤前处于未收藏态。"""
    checked_post_ids: set[str] = set()
    home.select_guide_category("发现")
    home.scroll_to_waterfall()

    for feed_swipe in range(MAX_CANDIDATE_FEED_SWIPES + 1):
        candidates = home.visible_fully_visible_guides(checked_post_ids)
        for card in candidates:
            checked_post_ids.add(card.post_id)
            home.tap_guide_card(card.post_id)

            try:
                detail.wait_loaded(timeout=10)
                detail.scroll_to_like_stats(max_swipes=12)
                cleaned_count = detail.ensure_favorite_unselected()
                original_count = None if cleaned_count < 0 else cleaned_count
                return card, original_count
            except RuntimeError:
                pass

            if detail.find_xpath(detail.ROOT_XPATH) is not None:
                detail.tap_back_button()
            else:
                detail.driver.press_back()
            if not home.wait_loaded(timeout=10):
                raise RuntimeError("检查候选帖子后未能返回首页")

        if feed_swipe < MAX_CANDIDATE_FEED_SWIPES:
            home.scroll_guide_feed_once()

    raise RuntimeError(
        "浏览首页攻略流后，未找到可收藏的帖子；"
        "当前测试数据不满足本用例前置条件"
    )


@allure.feature("收藏管理")
@allure.story("帖子详情收藏后在我的收藏帖子中展示")
def test_post_favorite_appears_in_mine_collection(driver) -> None:
    """验证帖子详情收藏状态、收藏数同步，以及我的收藏帖子列表展示。"""
    home = OutboundHomePage(driver)
    detail = PostDetailPage(driver)
    mine = MinePage(driver)
    navigation = BottomNavigation(driver)

    with allure.step("前置准备：进入一篇未收藏的帖子详情"):
        card, original_count = _open_unfavorited_post(
            home,
            detail,
        )
        if original_count is not None:
            assert detail.favorite_count() == original_count
        assert not detail.is_favorite_highlighted(), "前置准备后帖子仍是已收藏态"
        assert_visible_and_attach_highlight(
            driver,
            detail.favorite_button(timeout=8),
            f"帖子详情未收藏态-{card.title}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击帖子详情收藏按钮，校验按钮已收藏；若展示收藏数则校验数量 +1"):
        detail.tap_favorite()
        favorite_confirmed_by_count = False
        if original_count is not None:
            expected_count = original_count + 1
            assert detail.wait_favorite_count(expected_count) == expected_count
            favorite_confirmed_by_count = True
        if not favorite_confirmed_by_count:
            try:
                detail.wait_favorite_highlighted(True, timeout=4)
            except RuntimeError as exc:
                allure.attach(
                    (
                        "帖子详情新版收藏按钮颜色状态不稳定，"
                        "本步骤改由后续“我的收藏帖子列表展示该帖子”作为最终断言。\n"
                        f"{exc}"
                    ),
                    name="收藏按钮高亮辅助校验未命中",
                    attachment_type=allure.attachment_type.TEXT,
                )
        assert_visible_and_attach_highlight(
            driver,
            detail.favorite_button(timeout=8),
            f"帖子详情收藏按钮已高亮-{card.title}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：进入我的页收藏区域并切换到帖子标签"):
        _return_from_post_detail(
            driver,
            detail,
            home.wait_loaded,
            "从帖子详情返回后未回到首页",
        )
        navigation.tap_mine()
        mine.wait_content_loaded()
        assert_visible_and_attach_highlight(
            driver,
            BY.text("小星星的旅程"),
            "我的页-小星星的旅程",
            timeout=8,
            attach_crop=False,
        )
        mine.tap_favorite_posts_tab()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.FAVORITE_POSTS_TAB_XPATH),
            "我的收藏-帖子Tab",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：在我的收藏帖子标签查找该帖子"):
        mine.scroll_favorite_post_into_view(card.title, max_swipes=10)
        post_component = assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.favorite_post_xpath(card.title)),
            f"我的收藏帖子-{card.title}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("用例清理：取消本次新增收藏并恢复收藏地点默认页"):
        mine.tap_favorite_item(card.title, post_component)
        detail.wait_loaded(timeout=10)
        detail.scroll_to_like_stats(max_swipes=12)
        current_count = detail.try_favorite_count()
        if original_count is not None and current_count != original_count:
            detail.tap_favorite()
            assert detail.wait_favorite_count(original_count) == original_count
        elif original_count is None:
            detail.tap_favorite()
            try:
                detail.wait_favorite_highlighted(False, timeout=4)
            except RuntimeError:
                pass
        _return_from_post_detail(
            driver,
            detail,
            mine.wait_content_loaded,
            "清理收藏后未回到我的页",
        )
        mine.restore_favorites_default_state()

