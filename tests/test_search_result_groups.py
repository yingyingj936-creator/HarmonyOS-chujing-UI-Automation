import allure
from hypium import BY

from pages.ai_chat import AiChatPage
from pages.outbound_search import OutboundSearchPage
from pages.poi_detail import PoiDetailPage
from pages.post_detail import PostDetailPage
from pages.route_detail import RouteDetailPage
from pages.service_detail import ServiceDetailPage
from utils.allure_visual import assert_visible_and_attach_highlight


KEYWORD = "香港"
SERVICE_NAME = "香港迪士尼"
ROUTE_NAME = "香港经典一日游"
PLACE_NAME = "香港大会堂"
RESULT_GROUPS = ("服务", "路线", "地点", "最新攻略")
MINIMUM_GUIDE_INDEX = 25


@allure.feature("搜索功能")
@allure.story("搜索结果分组跳转")
def test_search_result_group_navigation(driver) -> None:
    """验证搜索结果AI总结、各分组内容及深分页攻略均可进入对应详情页。"""
    ai_chat = AiChatPage(driver)
    search_page = OutboundSearchPage(driver)
    service_page = ServiceDetailPage(driver)
    route_page = RouteDetailPage(driver)
    poi_page = PoiDetailPage(driver)
    post_page = PostDetailPage(driver)

    with allure.step("前置准备：从首页进入搜索页"):
        search_page.tap_home_search()
        search_page.wait_search_start_loaded(timeout=8)

    with allure.step("步骤1：在搜索框输入“香港”，搜索按钮可点击"):
        search_page.input_keyword(KEYWORD)
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.input_value_xpath(KEYWORD)),
            "搜索框输入内容-香港",
            timeout=8,
            attach_crop=False,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.SEARCH_BUTTON_XPATH),
            "搜索按钮-可点击",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤2：点击搜索，展示AI总结、服务、路线、地点和最新攻略分组"):
        search_page.tap_search_button()
        search_page.wait_result_ready_with_ai_summary(
            KEYWORD,
            RESULT_GROUPS,
            timeout=12,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.ai_summary_card_xpath(KEYWORD)),
            "搜索结果页-AI总结模块",
            timeout=8,
            attach_crop=False,
        )

    with allure.step("步骤3：点击AI总结“查看详情”，校验进入AI对话页"):
        search_page.tap_ai_summary_detail(timeout=8)
        ai_ready = ai_chat.wait_loaded(
            previous_root_xpath=search_page.RESULT_ROOT_XPATH,
            timeout=15,
        )
        assert_visible_and_attach_highlight(
            driver,
            ai_ready,
            "AI对话页-搜索查看详情",
            timeout=8,
            attach_crop=False,
        )
        ai_chat.press_system_back()
        search_page.wait_result_loaded(timeout=10)

    with allure.step("步骤4.1：点击服务“香港迪士尼”，进入服务详情页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.result_item_xpath(SERVICE_NAME)),
            f"服务结果-{SERVICE_NAME}",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_result_item(SERVICE_NAME)
        assert search_page.wait_result_hidden(timeout=8), (
            "点击香港迪士尼后仍停留在搜索结果页"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(service_page.title_xpath(SERVICE_NAME)),
            f"服务详情页-{SERVICE_NAME}",
            timeout=15,
            attach_crop=False,
        )
        service_page.press_system_back()
        search_page.wait_result_loaded(timeout=10)

    with allure.step("步骤4.2：点击路线“香港经典一日游”，进入路线详情页"):
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.result_item_xpath(ROUTE_NAME)),
            f"路线结果-{ROUTE_NAME}",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_result_item(ROUTE_NAME)
        assert search_page.wait_result_hidden(timeout=8), (
            "点击香港经典一日游后仍停留在搜索结果页"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(route_page.overview_title_xpath(ROUTE_NAME)),
            f"路线详情页-{ROUTE_NAME}",
            timeout=12,
            attach_crop=False,
        )
        route_page.tap_back_button()
        search_page.wait_result_loaded(timeout=10)

    with allure.step("步骤4.3：点击地点“香港大会堂”，进入地点详情页"):
        search_page.browse_result_group_to_right_until_visible(
            3,
            PLACE_NAME,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(search_page.result_item_xpath(PLACE_NAME)),
            f"地点结果-{PLACE_NAME}",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_result_item(PLACE_NAME)
        assert search_page.wait_result_hidden(timeout=8), (
            "点击香港大会堂后仍停留在搜索结果页"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(poi_page.title_xpath(PLACE_NAME)),
            f"地点详情页-{PLACE_NAME}",
            timeout=10,
            attach_crop=False,
        )
        # 返回仅用于继续验证下一个搜索分组，系统返回比 POI 顶部按钮稳定。
        poi_page.press_system_back()
        search_page.wait_result_loaded(timeout=10)

    with allure.step(
        "步骤4.4：连续向下滑动最新攻略，点击至少第25篇之后的帖子"
    ):
        search_page.scroll_result_text_into_view("最新攻略")
        title_xpath, browsed_count, swipe_count = (
            search_page.browse_latest_guides(
                minimum_browsed_cards=MINIMUM_GUIDE_INDEX,
            )
        )
        allure.attach(
            (
                f"实际滑动次数：{swipe_count}\n"
                f"累计浏览不同帖子标题数：{browsed_count}"
            ),
            name="最新攻略实际滑动统计",
            attachment_type=allure.attachment_type.TEXT,
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(title_xpath),
            f"实际浏览{browsed_count}篇后的最新攻略帖子",
            timeout=8,
            attach_crop=False,
        )
        search_page.tap_latest_guide(title_xpath)
        assert search_page.wait_result_hidden(timeout=8), (
            "点击深分页攻略帖子后仍停留在搜索结果页"
        )
        assert_visible_and_attach_highlight(
            driver,
            BY.xpath(post_page.CONTENT_LIST_XPATH),
            "帖子详情页-正文内容",
            timeout=10,
            attach_crop=False,
        )
