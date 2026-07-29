import os
import subprocess
import time
from dataclasses import replace
from pathlib import Path

import pytest
from hypium import BY, UiDriver

from core.settings import AppSettings, load_settings
from pages.outbound_home import OutboundHomePage
from pages.select_destination import SelectDestinationPage
from utils.allure_step_state import install_allure_step_tracking
from utils.component_cache import invalidate_component_cache
from utils.ui_snapshot import UiSnapshot

FILE_ORDER = {
    # Read-only display and browse cases run first to avoid account-state pollution.
    "test_home_first_screen.py": 1,
    "test_bottom_navigation.py": 2,
    "test_home_waterfall_categories.py": 3,
    "test_home_waterfall_pagination.py": 4,
    "test_home_post_detail_browsing.py": 5,
    "test_home_hot_route_detail.py": 6,
    "test_home_hot_route_itinerary_tabs.py": 7,
    "test_home_hot_route_overview_card.py": 8,
    "test_home_hot_route_day1_poi_detail.py": 9,
    "test_home_hot_route_poi_surrounding.py": 10,
    "test_home_hot_route_play_mode.py": 11,
    "test_home_hot_route_play_mode_tabs.py": 12,
    "test_home_hot_route_play_mode_route_intro.py": 13,
    "test_home_hot_route_play_mode_sidebar_post.py": 14,
    "test_home_hot_route_play_mode_location.py": 15,
    "test_home_hot_route_play_mode_poi_detail.py": 16,
    "test_destination_selector_browse.py": 17,
    "test_destination_switch_refresh.py": 18,
    "test_nearby_page_default_content.py": 19,
    "test_nearby_destination_switch.py": 20,
    "test_nearby_category_switch.py": 21,
    "test_nearby_sort_priority.py": 22,
    "test_nearby_search_recommended_poi.py": 23,
    "test_nearby_search_keyword_detail_nearby.py": 24,
    "test_nearby_map_location_refresh.py": 25,
    "test_mine_page_layout_and_feedback.py": 26,
    "test_mine_favorite_detail_and_search.py": 27,
    "test_trip_page_overview.py": 28,
    "test_trip_video_tutorial.py": 29,
    "test_trip_reference_hot_routes.py": 30,
    "test_trip_detail_layout.py": 31,
    "test_trip_detail_view_map_play_mode.py": 32,
    "test_trip_detail_edit_page.py": 33,
    "test_trip_edit_tabs.py": 34,
    "test_trip_edit_select_cancel.py": 35,
    "test_trip_long_press_edit_menu.py": 36,

    # Service, search, and POI cases may affect recent-use/search/task state.
    "test_home_service_tabs.py": 37,
    "test_taxi_service_entry.py": 38,
    "test_scenic_youtube_entries.py": 39,
    "test_local_service_categories.py": 40,
    "test_local_service_search.py": 41,
    "test_food_ordering_categories.py": 42,
    "test_food_ordering_search.py": 43,
    "test_search_ai_recommend_auto_search.py": 44,
    "test_search_start_page_interactions.py": 45,
    "test_search_scope_by_destination.py": 46,
    "test_search_result_groups.py": 47,
    "test_poi_hotel_booking_and_navigation.py": 48,
    "test_poi_recommendation_post.py": 49,
    "test_nearby_poi_recommendation_review_locate.py": 50,
    "test_clear_search_history.py": 51,

    # Account-mutating cases run last: favorites, likes, recents, tasks, and trips.
    "test_favorite_poi_from_ranking.py": 52,
    "test_home_guide_like_persistence.py": 53,
    "test_home_post_favorite_collection.py": 54,
    "test_home_hot_route_play_mode_poi_favorite.py": 55,
    "test_multitask_management.py": 56,
    "test_mine_recent_service_order.py": 57,
    "test_home_hot_route_join_trip.py": 58,
    "test_trip_reference_route_join_trip.py": 59,
    "test_poi_add_to_trip.py": 60,
    "test_trip_pin_second_card.py": 61,
    "test_trip_detail_poi_light.py": 62,
    "test_trip_detail_rename.py": 63,
    "test_trip_edit_copy_poi_to_pending.py": 64,
    "test_trip_edit_add_day3_poi.py": 65,
    "test_trip_edit_move_poi_to_day2.py": 66,
    "test_trip_edit_reorder_day2_poi.py": 67,
    "test_trip_edit_delete_second_poi.py": 68,
    "test_trip_delete_card.py": 69,
}

def pytest_addoption(parser: pytest.Parser) -> None:
    parser.addoption(
        "--config",
        action="store",
        default=None,
        help="Path to TOML config file. Default: configs/default.toml",
    )
    parser.addoption(
        "--device",
        action="store",
        default=None,
        help="Override USB device serial. Use 'auto' for the only connected USB device.",
    )
    parser.addoption("--bundle", action="store", default=None, help="Override bundle")
    parser.addoption("--ability", action="store", default=None, help="Override ability")
    parser.addoption(
        "--disable-file-order",
        action="store_true",
        default=False,
        help="Disable custom FILE_ORDER and run by pytest default collection order.",
    )


def pytest_configure(config: pytest.Config) -> None:
    install_allure_step_tracking()
    config._app_settings = load_settings(
        config.getoption("--config"),
        target_device=config.getoption("--device"),
        bundle=config.getoption("--bundle"),
        ability=config.getoption("--ability"),
        enable_file_order=not config.getoption("--disable-file-order"),
    )


def _hdc_executable() -> str:
    """优先使用 CI 注入的 HDC_EXE，本地默认使用 PATH 中的 hdc。"""
    return os.environ.get("HDC_EXE", "hdc")


def _list_usb_targets() -> list[str]:
    """返回当前通过 USB 连接的 HDC 设备序列号。"""
    result = subprocess.run(
        [_hdc_executable(), "list", "targets"],
        check=True,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    targets = []
    for line in result.stdout.splitlines():
        raw_target = line.strip()
        if not raw_target or raw_target == "[Empty]":
            continue
        columns = raw_target.split()
        target = columns[0]
        # 无线目标使用 ip:port；USB 目标为设备序列号。
        is_offline = any(column.lower() == "offline" for column in columns[1:])
        if ":" not in target and not is_offline:
            targets.append(target)
    return targets


def _assert_device_ready(settings: AppSettings) -> None:
    """在创建 UiDriver 前快速确认 hdc 和 uitest 可用，避免 Hypium 内部报空指针。"""
    try:
        result = subprocess.run(
            [
                _hdc_executable(),
                "-t",
                settings.target_device,
                "shell",
                "uitest",
                "--version",
            ],
            check=False,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=10,
        )
    except subprocess.TimeoutExpired as exc:
        raise RuntimeError(
            f"设备 {settings.target_device} 的 hdc shell 无响应。"
            "请重新插拔 USB、确认设备未锁屏且 `hdc list targets` 显示 Connected 后重试。"
        ) from exc

    output = f"{result.stdout}\n{result.stderr}".strip()
    if result.returncode != 0 or not output or "[Fail]" in output:
        raise RuntimeError(
            f"设备 {settings.target_device} 当前不可用，无法获取 uitest 版本。\n"
            f"请确认 USB 连接稳定、设备在线且 `hdc -t {settings.target_device} shell uitest --version` 有输出。\n"
            f"实际输出：{output or '<空>'}"
        )


def _resolve_usb_target(configured_target: str) -> str:
    """校验并返回测试使用的 USB 设备序列号。"""
    usb_targets = _list_usb_targets()
    if not usb_targets:
        raise RuntimeError(
            "未检测到 USB 设备。请连接数据线、开启设备调试，"
            "并确认 `hdc list targets` 能显示设备序列号。"
        )

    if configured_target.lower() == "auto":
        if len(usb_targets) == 1:
            return usb_targets[0]
        raise RuntimeError(
            "检测到多台 USB 设备，请将 configs/default.toml 中的 "
            f"target_device 设置为其中一个序列号：{usb_targets}"
        )

    if configured_target not in usb_targets:
        raise RuntimeError(
            f"配置的 USB 设备 {configured_target!r} 未连接，"
            f"当前可用设备：{usb_targets}"
        )
    return configured_target


@pytest.fixture(scope="session")
def app_settings(pytestconfig: pytest.Config) -> AppSettings:
    settings = pytestconfig._app_settings
    usb_serial = _resolve_usb_target(settings.target_device)
    print(f"[Device] 使用 USB 设备：{usb_serial}")
    return replace(settings, target_device=usb_serial)


def _start_outbound_service(settings: AppSettings) -> None:
    """启动出境服务元服务并等待页面完成渲染。"""
    result = subprocess.run(
        [
            _hdc_executable(),
            "-t",
            settings.target_device,
            "shell",
            "aa",
            "start",
            "-b",
            settings.bundle,
            "-a",
            settings.ability,
        ],
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
    )
    output = f"{result.stdout}\n{result.stderr}"
    if "screen is locked" in output or "unlock screen failed" in output:
        raise RuntimeError(
            "检测到设备处于锁屏状态，无法启动出境服务。"
            "请手动解锁设备并保持屏幕常亮后重新运行用例。"
        )
    if result.returncode != 0:
        raise RuntimeError(f"启动出境服务失败：\n{output.strip()}")
    time.sleep(settings.startup_wait_seconds)


@pytest.fixture(scope="session")
def driver(app_settings: AppSettings):
    """全量会话复用同一个 UiDriver，并只在会话开始时启动一次应用。"""
    try:
        _assert_device_ready(app_settings)
        ui_driver = UiDriver.connect(device_sn=app_settings.target_device)
    except Exception as exc:
        pytest.fail(f"设备连接失败，终止当前用例：{exc}", pytrace=False)

    _start_outbound_service(app_settings)
    try:
        yield ui_driver
    finally:
        print("\n[Session Cleanup] 正在执行全量结束后的最终首页恢复...")
        try:
            if not _prepare_home(ui_driver, app_settings):
                _start_outbound_service(app_settings)
                if not _prepare_home(ui_driver, app_settings):
                    print("[Session Cleanup] 最终首页恢复失败，请手动检查设备状态")
            else:
                print(
                    "[Session Cleanup] 已恢复首页，"
                    f"目的地={app_settings.default_destination}"
                )
        except Exception as exc:
            print(f"[Session Cleanup] 最终首页恢复异常：{exc}")
        try:
            ui_driver.close()
        except Exception as exc:
            print(f"[Device] 关闭 UiDriver 失败，可能是设备已断连：{exc}")


def _inspect_home_state(
    driver,
    settings: AppSettings,
) -> tuple[bool, bool, object | None]:
    """一次查询识别首页顶部、首页页面和底部首页入口。"""
    home = OutboundHomePage(driver)
    destination = settings.default_destination.replace('"', '\\"')
    top_ready_xpath = (
        '//*[@id="TabHomeCompRoot" '
        f'and .//Row[.//Text[@text="{destination}"]]]'
        '//*[@id="home_recommends_section"]'
    )
    selector = BY.xpath(
        f"{top_ready_xpath} | {home.SEARCH_BAR_XPATH} | {home.BOTTOM_HOME_TAB_XPATH}"
    )
    components = driver.find_all_components(selector)
    if components is None:
        components = []
    elif not isinstance(components, list):
        components = [components]

    top_ready = False
    search_visible = False
    home_tab = None
    for component in components:
        properties = component.getAllProperties().to_dict()
        component_id = str(properties.get("id") or "")
        text = (component.getText() or "").strip()
        hint = str(properties.get("hint") or "")
        if component_id == "home_recommends_section":
            bounds = component.getBounds()
            top_ready = (
                int(bounds.right) > int(bounds.left)
                and int(bounds.bottom) > int(bounds.top)
                and int(bounds.bottom) > 0
            )
        elif text == "首页":
            home_tab = component
        elif "搜索服务" in text or "搜索服务" in hint:
            search_visible = True
        else:
            bounds = component.getBounds()
            search_visible = (
                int(bounds.right) > int(bounds.left)
                and int(bounds.bottom) > int(bounds.top)
            )

    return top_ready, search_visible and home_tab is not None, home_tab


def _dismiss_unsaved_edit_dialog_if_present(driver) -> bool:
    """恢复首页时处理编辑页未保存弹窗，避免污染后续用例。"""
    snapshot = UiSnapshot(driver).capture()
    dialog = snapshot.find_xpath(
        '//Dialog[.//Text[contains(@text, "保存") '
        'or contains(@text, "编辑") '
        'or contains(@text, "修改")]]'
    )
    if dialog is None:
        return False

    discard = snapshot.find_xpath(
        '//Dialog//Text[@text="不保存" '
        'or @text="放弃" '
        'or @text="离开" '
        'or @text="退出" '
        'or contains(@text, "不保存") '
        'or contains(@text, "放弃") '
        'or contains(@text, "离开") '
        'or contains(@text, "退出")]'
    )
    if discard is None:
        return False

    discard.click()
    invalidate_component_cache(driver)
    driver.wait_for_component_disappear(
        BY.xpath(
            '//Dialog[.//Text[contains(@text, "保存") '
            'or contains(@text, "编辑") '
            'or contains(@text, "修改")]]'
        ),
        timeout=2,
    )
    return True


def _return_to_home(
    driver,
    settings: AppSettings,
    *,
    initial_state: tuple[bool, bool, object | None] | None = None,
) -> bool:
    """优先通过底部导航回首页，否则逐层返回。"""
    home = OutboundHomePage(driver)
    state = initial_state

    for _ in range(settings.cleanup_back_steps):
        if state is None:
            state = _inspect_home_state(driver, settings)
        _, on_home, home_tab = state
        if on_home:
            return True

        if _dismiss_unsaved_edit_dialog_if_present(driver):
            state = None
            continue

        if home_tab is not None:
            try:
                home_tab.click()
                invalidate_component_cache(driver)
                if (
                    driver.wait_for_component(
                        BY.xpath(home.SEARCH_BAR_XPATH),
                        timeout=3,
                    )
                    is not None
                ):
                    return True
            except Exception:
                pass

        try:
            driver.press_back()
            invalidate_component_cache(driver)
            time.sleep(settings.cleanup_back_interval_seconds)
            _dismiss_unsaved_edit_dialog_if_present(driver)
            state = None
        except Exception:
            return False

    return home.is_at_home()


def _restore_default_destination(
    driver,
    settings: AppSettings,
) -> tuple[bool, bool]:
    """恢复默认目的地，返回（是否成功，是否实际发生切换）。"""
    home = OutboundHomePage(driver)
    destination_page = SelectDestinationPage(driver)
    destination_selector = BY.xpath(
        home.region_dropdown_xpath(settings.default_destination)
    )
    current_destination_xpath = home.region_dropdown_xpath(
        settings.default_destination
    )
    fallback_xpath = (
        '//*[@id="TabHomeCompRoot"]//Text'
        '[contains(@text, "香港") or contains(@text, "港澳")]'
        if settings.default_destination == "中国香港"
        else current_destination_xpath
    )
    current_components = driver.find_all_components(
        BY.xpath(f"{current_destination_xpath} | {fallback_xpath}")
    )
    if current_components:
        return True, False

    try:
        home.tap_region_selector()
        destination_page.choose_destination(settings.default_destination)
    except Exception:
        return False, False

    restored = (
        driver.wait_for_component(destination_selector, timeout=8) is not None
    )
    return restored, restored


def _prepare_home(driver, settings: AppSettings) -> bool:
    state = _inspect_home_state(driver, settings)
    if state[0]:
        return True
    if not _return_to_home(driver, settings, initial_state=state):
        return False
    if not _restore_home_top(driver):
        return False
    destination_restored, destination_changed = _restore_default_destination(
        driver,
        settings,
    )
    if not destination_restored:
        return False
    if destination_changed:
        return _restore_home_top(driver)
    return True


def _restore_home_top(driver) -> bool:
    """回到首页后统一恢复到顶部，避免上个用例的滚动位置污染金刚区/目的地用例。"""
    home = OutboundHomePage(driver)
    try:
        home.restore_top(max_swipes=18)
        return True
    except Exception:
        return False


@pytest.fixture
def restart_outbound_service(driver, app_settings: AppSettings):
    """强制结束出境服务进程后重新启动，并确认回到首页。"""

    def restart() -> None:
        subprocess.run(
            [
                _hdc_executable(),
                "-t",
                app_settings.target_device,
                "shell",
                "aa",
                "force-stop",
                app_settings.bundle,
            ],
            check=True,
        )
        time.sleep(1)
        _start_outbound_service(app_settings)
        if not _prepare_home(driver, app_settings):
            raise RuntimeError("杀掉进程并重启后未能回到出境服务首页")

    return restart


@pytest.fixture(scope="function", autouse=True)
def reset_to_home(driver, app_settings: AppSettings):
    """
    每个用例开始前恢复首页；下一条用例负责修复上一条留下的页面状态。
    """
    print("\n[Setup] 正在确认测试从首页开始...")
    if not _prepare_home(driver, app_settings):
        _start_outbound_service(app_settings)
        if not _prepare_home(driver, app_settings):
            pytest.fail("前置恢复首页失败，终止当前用例")

    yield


def _item_filename(item: pytest.Item) -> str:
    """兼容不同 pytest 版本，提取测试项所在文件名。"""
    item_path = getattr(item, "path", None)
    if item_path is not None:
        return Path(item_path).name
    return item.fspath.basename


def pytest_collection_modifyitems(
    config: pytest.Config, items: list[pytest.Item]
) -> None:
    """
    按文件优先级重排收集到的测试项：
    1) FILE_ORDER 中的文件按指定顺序执行；
    2) 未指定文件统一排在后面；
    3) 同文件内维持 pytest 原始收集顺序。
    """
    if not config._app_settings.enable_file_order:
        return

    indexed_items = list(enumerate(items))
    indexed_items.sort(
        key=lambda pair: (FILE_ORDER.get(_item_filename(pair[1]), 999), pair[0])
    )
    items[:] = [item for _, item in indexed_items]
