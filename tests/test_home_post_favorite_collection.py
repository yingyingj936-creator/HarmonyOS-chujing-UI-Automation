import allure
from hypium import BY

from pages.bottom_navigation import BottomNavigation
from pages.mine_page import MinePage
from pages.outbound_home import HomeGuideCard, OutboundHomePage
from pages.post_detail import PostDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


MAX_CANDIDATE_FEED_SWIPES = 8


def _open_unfavorited_post_with_numeric_favorite_count(
    home: OutboundHomePage,
    detail: PostDetailPage,
) -> tuple[HomeGuideCard, int]:
    """选择收藏数可精确校验的帖子，并确保进入用例步骤前处于未收藏态。"""
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
                detail.scroll_to_like_stats(max_swipes=24)
                if not detail.favorite_count_text().isdigit():
                    raise RuntimeError("收藏数不是纯数字，无法严格断言 +1")
                original_count = detail.ensure_favorite_unselected()
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
        "浏览首页攻略流后，未找到收藏数为纯数字的帖子；"
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

    with allure.step("前置准备：进入一篇未收藏且收藏数可精确校验的帖子详情"):
        card, original_count = _open_unfavorited_post_with_numeric_favorite_count(
            home,
            detail,
        )
        assert detail.favorite_count() == original_count
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.FAVORITE_ROW_XPATH),
            f"帖子详情未收藏态-{card.title}-{original_count}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤1：点击帖子详情收藏按钮，校验按钮已收藏且数量 +1"):
        detail.tap_favorite()
        expected_count = original_count + 1
        assert detail.wait_favorite_count(expected_count) == expected_count
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.FAVORITE_ROW_XPATH),
            f"帖子详情收藏数已更新-{card.title}-{expected_count}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：进入我的页收藏区域并切换到帖子标签"):
        detail.tap_back_button()
        assert home.wait_loaded(timeout=10), "从帖子详情返回后未回到首页"
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
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(mine.favorite_post_xpath(card.title)),
            f"我的收藏帖子-{card.title}",
            timeout=8,
            attach_crop=False,
        )

