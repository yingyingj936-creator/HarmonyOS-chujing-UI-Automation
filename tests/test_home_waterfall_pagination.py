import allure
from hypium import BY

from pages.outbound_home import OutboundHomePage
from utils.allure_visual import assert_visible_and_attach_highlight


MINIMUM_UNIQUE_GUIDES = 50


@allure.feature("出境服务卡片")
@allure.story("首页攻略瀑布流分页加载")
def test_home_waterfall_pagination_and_card_fields(driver) -> None:
    """验证首页攻略瀑布流可分页加载，且新卡片字段展示完整。"""
    home = OutboundHomePage(driver)

    try:
        with allure.step("步骤1：在首页向下滑动到攻略瀑布流区域"):
            initial_post_ids = home.scroll_to_waterfall()
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.WATERFALL_LIST_XPATH),
                "首页攻略瀑布流区域",
                timeout=8,
                attach_crop=False,
            )

        with allure.step(
            f"步骤2：继续上拉，至少浏览{MINIMUM_UNIQUE_GUIDES}张不同攻略卡片"
        ):
            new_post_id, unique_count, swipe_count = home.load_more_guides(
                initial_post_ids,
                minimum_unique_cards=MINIMUM_UNIQUE_GUIDES,
            )
            assert new_post_id not in initial_post_ids, (
                f"分页后返回的攻略 {new_post_id} 已存在于分页前卡片中"
            )
            assert home.is_guide_card_above_bottom_navigation(new_post_id), (
                "新加载攻略卡片被底部导航遮挡"
            )
            allure.attach(
                (
                    f"分页前可见卡片数：{len(initial_post_ids)}\n"
                    f"累计不同卡片数：{unique_count}\n"
                    f"实际上拉次数：{swipe_count}\n"
                    f"新卡片帖子ID：{new_post_id}"
                ),
                name="首页攻略分页统计",
                attachment_type=allure.attachment_type.TEXT,
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.guide_card_xpath(new_post_id)),
                "分页追加的新攻略卡片",
                timeout=8,
                attach_crop=False,
            )

        with allure.step("步骤3：校验新攻略卡片的封面、标题、作者、目的地和点赞数"):
            card = home.guide_card_fields(new_post_id)
            assert card.title, "新攻略卡片标题为空"
            assert card.author, "新攻略卡片作者为空"
            assert card.destination, "新攻略卡片目的地为空"
            assert card.likes.replace(",", "").isdigit(), (
                f"新攻略卡片点赞数格式异常：{card.likes!r}"
            )
            assert_visible_and_attach_highlight(
                driver,
                BY.xpath(home.guide_card_xpath(new_post_id)),
                (
                    f"攻略字段完整-{card.title}-"
                    f"{card.author}-{card.destination}-{card.likes}"
                ),
                timeout=8,
                attach_crop=False,
            )
    finally:
        home.restore_top()
