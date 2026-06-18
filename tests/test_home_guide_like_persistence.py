import allure
import time
from hypium import BY

from pages.outbound_home import OutboundHomePage
from pages.post_detail import PostDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


@allure.feature("出境服务卡片")
@allure.story("首页攻略点赞状态跨进程保持")
def test_home_guide_like_persists_after_restart(
    driver,
    restart_outbound_service,
) -> None:
    """验证首页点赞同步至详情页，并在杀进程重启后保持。"""
    home = OutboundHomePage(driver)
    detail = PostDetailPage(driver)
    target_post_id: str | None = None
    original_count: int | None = None
    liked_count: int | None = None
    should_cleanup_like = False
    test_completed = False

    try:
        with allure.step("步骤1：在首页找到未点赞攻略并点击爱心"):
            card = home.find_unliked_guide()
            target_post_id = card.post_id
            original_count = home.parse_like_count(card.likes)
            assert not home.is_guide_liked(target_post_id), (
                f"选中的攻略 {target_post_id} 在操作前已是点赞态"
            )

            home.tap_guide_like(target_post_id)
            liked_count = original_count + 1
            home.wait_guide_like_count(target_post_id, liked_count)
            should_cleanup_like = True
            assert home.is_guide_liked(target_post_id), "首页爱心未变为已点赞态"
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.guide_like_row_xpath(target_post_id)),
                f"首页攻略已点赞-{card.title}-{liked_count}",
                timeout=8,
                attach_crop=False,
            )

        with allure.step("步骤2：进入帖子详情，校验右下角点赞状态和数量同步"):
            home.tap_guide_card(target_post_id)
            detail.wait_loaded()
            detail.scroll_to_like_stats()
            assert detail.wait_like_count(liked_count) == liked_count
            assert detail.is_liked(), "帖子详情页右下角爱心不是已点赞态"
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(detail.LIKE_ROW_XPATH),
                f"帖子详情右下角点赞已同步-{liked_count}",
                timeout=8,
                attach_crop=False,
            )
            time.sleep(3)

        with allure.step("步骤3：杀掉进程并重开出境服务，校验点赞状态保持"):
            restart_outbound_service()
            home.find_guide_in_feed(target_post_id)
            actual_count = home.guide_like_count(target_post_id)
            actual_liked = home.is_guide_liked(target_post_id)
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.guide_like_row_xpath(target_post_id)),
                f"重启后攻略点赞当前状态-{actual_count}",
                timeout=8,
                attach_crop=False,
            )
            assert actual_count == liked_count, (
                f"点赞状态未跨进程保持：帖子ID={target_post_id}，"
                f"重启前点赞数={liked_count}，重启后点赞数={actual_count}"
            )
            assert actual_liked, (
                f"点赞状态未跨进程保持：帖子ID={target_post_id}，"
                "杀进程重启后爱心恢复为未点赞态"
            )
            test_completed = True
    finally:
        cleanup_errors: list[str] = []
        if (
            should_cleanup_like
            and target_post_id is not None
            and original_count is not None
        ):
            try:
                if not home.is_at_home():
                    restart_outbound_service()
                home.find_guide_in_feed(target_post_id)
                if home.is_guide_liked(target_post_id):
                    home.tap_guide_like(target_post_id)
                    home.wait_guide_like_count(target_post_id, original_count)
            except Exception as exc:
                cleanup_errors.append(f"取消点赞失败：{exc}")

        try:
            if home.is_at_home():
                home.restore_top()
        except Exception as exc:
            cleanup_errors.append(f"恢复首页顶部失败：{exc}")

        if cleanup_errors:
            allure.attach(
                "\n".join(cleanup_errors),
                name="点赞用例清理异常",
                attachment_type=allure.attachment_type.TEXT,
            )
            if test_completed:
                raise RuntimeError("; ".join(cleanup_errors))
