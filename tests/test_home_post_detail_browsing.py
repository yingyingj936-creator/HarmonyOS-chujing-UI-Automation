import allure
import pytest
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.post_detail import PostDetailPage
from utils.allure_visual import (
    assert_visible_and_attach_highlight,
    attach_highlighted_bounds,
)


MAX_CANDIDATE_FEED_SWIPES = 6


def _open_guide_with_gallery_and_recommendations(
    home: OutboundHomePage,
    detail: PostDetailPage,
):
    """动态选择同时具备多图图集和更多攻略的帖子。"""
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
                detail.scroll_to_top()
                has_multiple_images = detail.gallery_page_count() > 1
                has_recommendations = False
                if has_multiple_images:
                    has_recommendations = detail.try_scroll_to_more_guides(
                        max_swipes=12
                    )
                if has_multiple_images and has_recommendations:
                    detail.scroll_to_top()
                    return card
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
        "浏览首页攻略流后，未找到同时包含多图图集和更多攻略的帖子；"
        "当前测试数据不满足本用例前置条件"
    )


@allure.feature("首页攻略")
@allure.story("攻略详情完整展示、图集浏览及更多攻略跳转")
def test_home_post_detail_browsing(driver) -> None:
    """验证首页攻略详情内容、图集、更多攻略和返回位置。"""
    home = OutboundHomePage(driver)
    detail = PostDetailPage(driver)

    with allure.step(
        "步骤1：选择一篇包含多图和更多攻略的首页攻略卡片，进入详情页"
    ):
        try:
            card = _open_guide_with_gallery_and_recommendations(
                home,
                detail,
            )
        except RuntimeError as exc:
            pytest.skip(str(exc))
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.ROOT_XPATH),
            f"已进入攻略详情-{card.title}",
            timeout=8,
            attach_crop=False,
        )

    with allure.step(
        "步骤2：查看返回按钮、图集页码、标题、作者头像、正文、"
        "浏览数、点赞数、收藏数和更多攻略"
    ):
        detail.scroll_to_top()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.BACK_BUTTON_XPATH),
            "帖子详情页-返回按钮",
            timeout=8,
            attach_crop=False,
        )
        indicator = detail.wait_gallery_page_indicator()
        assert_visible_and_attach_highlight(
            driver,
            BY.text(indicator.getText().strip()),
            "帖子详情页-图集及图片页码",
            timeout=8,
            attach_crop=False,
        )

        detail.scroll_to_article_metadata(card.title, card.author)
        detail.wait_text(card.title, "帖子标题")
        detail.wait_text(card.author, "作者昵称")
        detail.wait_author_avatar(card.author)
        body_text = detail.wait_visible_body_text().getText().strip()
        assert_visible_and_attach_highlight(
            driver,
            BY.text(body_text),
            "帖子详情页-标题作者正文区域",
            timeout=8,
            attach_crop=False,
        )

        engagement_stats = detail.scroll_to_engagement_stats()
        attach_highlighted_bounds(
            driver,
            detail.components_union_bounds(engagement_stats),
            "帖子详情页-浏览点赞收藏数据",
        )

        detail.scroll_to_more_guides()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.MORE_GUIDES_TITLE_XPATH),
            "帖子详情页-更多相关攻略",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击图集并横向滑动，校验图片页码发生变化"):
        detail.scroll_to_top()
        before_page, after_page, preview_opened = detail.browse_gallery()
        assert before_page != after_page, (
            f"图集滑动前后页码未变化：{before_page}"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.text(after_page),
            f"图集放大浏览-{before_page}到{after_page}",
            timeout=8,
            attach_crop=False,
        )
        detail.close_gallery_preview(preview_opened)

    with allure.step("步骤4：向下滑动并点击更多攻略中的第一篇帖子"):
        detail.scroll_to_more_guides()
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.FIRST_RELATED_CARD_XPATH),
            "更多攻略-第一篇帖子",
            timeout=8,
            attach_crop=False,
        )
        detail.tap_first_related_guide()
        detail.wait_related_guide_opened(timeout=10)
        detail.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.ROOT_XPATH),
            "已跳转到更多攻略帖子详情",
            timeout=10,
            attach_crop=False,
        )

    with allure.step("步骤5：点击页面返回按钮，回到上一篇攻略详情"):
        detail.tap_back_button()
        detail.wait_loaded(timeout=10)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(detail.FIRST_RELATED_CARD_XPATH),
            "已回到上一篇攻略详情",
            timeout=8,
            attach_crop=False,
        )
