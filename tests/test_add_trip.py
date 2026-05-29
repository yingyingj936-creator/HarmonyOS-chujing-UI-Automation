import allure
from pages.outbound_home import OutboundHomePage
from pages.route_detail import RouteDetailPage
from pages.trip_detail import TripDetailPage
from pages.trip_manager import TripManagerPage

@allure.feature("出境服务")
@allure.story("行程创建与验证")
class TestHKTripPersistence:

    def test_add_hk_route_to_manager_list(self, driver):
        """
        用例：验证‘香港一日游’创建后能正确持久化到‘行程’列表
        """
        home = OutboundHomePage(driver)
        route_info = RouteDetailPage(driver)
        trip_detail = TripDetailPage(driver)
        trip_manager = TripManagerPage(driver)

        with allure.step("1. 从首页进入‘香港逛吃两日游’"):
            home.tap_hk_trip_entry()
        with allure.step("2. 加入行程并执行‘创建并添加’"):
            route_info.tap_add_to_my_trip()
            route_info.tap_create_and_add()

        with allure.step("3. 校验自动跳转到‘行程详情’页"):
            assert trip_detail.is_loaded(timeout=8), "创建后未跳转到行程详情页(route.json)"

        with allure.step("4. 侧滑返回首页"):
            # 使用 press_back 确保返回首页逻辑稳定
            driver.press_back()
            driver.press_back()
            assert home.wait_loaded(timeout=8), "返回两次后未回到首页"

        with allure.step("5. 切换到首页‘行程’页签"):
            home.tap_trip_tab()

        with allure.step("6. 校验行程管理列表中包含该行程"):
            assert trip_manager.has_trip_in_list("香港逛吃两日游"), "行程管理列表中未找到新增行程"

