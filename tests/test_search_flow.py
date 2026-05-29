import allure
from pages.outbound_search import OutboundSearchPage


@allure.feature("搜索功能")
@allure.story("目的地搜索流程测试")
def test_search_hongkong_disney_complete_flow(driver):
    """
    用例：从首页进入搜索，搜索香港迪士尼并校验结果分类
    """
    search_page = OutboundSearchPage(driver)

    with allure.step("1. 点击首页搜索框"):
        search_page.tap_home_search()

    with allure.step("2. 在搜索页输入'香港迪士尼'并回车"):
        # 此时 hint 可能是“在中国香港中搜索”，模糊定位依然有效
        search_page.input_and_search("香港迪士尼")

    with allure.step("3. 校验搜索结果页板块展示"):
        assert search_page.is_search_results_displayed(), "搜索结果分类板块展示不完整"

    # with allure.step("4. 侧滑返回首页"):
    #     # 执行侧滑动作
    #     search_page.swipe_to_back()
    #     time.sleep(1)

