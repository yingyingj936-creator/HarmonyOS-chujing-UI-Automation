import allure
from pages.outbound_home import OutboundHomePage
from pages.post_detail import PostDetailPage
from pages.mine_page import MinePage


@allure.feature("出境服务")
@allure.story("瀑布流帖子收藏闭环")
class TestPostFavoriteLifecycle:

    def test_collect_and_remove_post(self, driver):
        """
        用例：验证帖子从瀑布流收藏到‘我的’页面帖子分类展示，并能成功取消收藏。
        """
        home = OutboundHomePage(driver)
        post_detail = PostDetailPage(driver)
        mine = MinePage(driver)

        target_title = "首次办理港澳通行证攻略（手把手教你办理）"

        with allure.step("1. 首页进入‘入境’分类并点击目标帖子"):
            home.tap_entry_category()
            driver.swipe('UP', 20)
            home.tap_target_post()

        with allure.step("2. 详情页利用绝对路径点击五角星收藏"):
            post_detail.scroll_and_tap_favorite()

        with allure.step("3. 返回首页并进入‘我的’"):
            driver.press_back()
            assert home.wait_loaded(timeout=8), "返回后未回到首页"
            home.tap_mine_tab()

        with allure.step("4. 直接点击‘帖子’页签并验证"):
            mine.tap_posts_tab()
            mine.verify_and_unfavorite(target_title)
