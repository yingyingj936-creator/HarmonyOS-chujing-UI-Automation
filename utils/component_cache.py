from __future__ import annotations

import time
from typing import Any


_CACHE_ATTR = "_ui_auto_component_cache"
_GENERATION_ATTR = "_ui_auto_component_generation"
_SNAPSHOT_CACHE_ATTR = "_ui_auto_snapshot_cache"


def _driver_state(driver: Any) -> dict[str, Any]:
    """绕过 Hypium 的动态 __getattr__，直接读取本地 Python 属性。"""
    return object.__getattribute__(driver, "__dict__")


def _generation(driver: Any) -> int:
    return int(_driver_state(driver).get(_GENERATION_ATTR, 0))


def component_generation(driver: Any) -> int:
    return _generation(driver)


def remember_component(driver: Any, selector: Any, component: Any) -> None:
    """缓存当前页面状态下刚定位到的组件，供紧邻的圈选或点击复用。"""
    state = _driver_state(driver)
    cache = state.get(_CACHE_ATTR)
    if cache is None:
        cache = {}
        state[_CACHE_ATTR] = cache
    cache[str(selector)] = (_generation(driver), time.monotonic(), component)


def recent_component(
    driver: Any,
    selector: Any,
    *,
    max_age_seconds: float = 5.0,
) -> Any | None:
    """返回同一页面状态下的近期组件；过期或失效时返回 None。"""
    cache = _driver_state(driver).get(_CACHE_ATTR)
    if not cache:
        return None
    cached = cache.get(str(selector))
    if cached is None:
        return None

    generation, cached_at, component = cached
    if (
        generation != _generation(driver)
        or time.monotonic() - cached_at > max_age_seconds
    ):
        cache.pop(str(selector), None)
        return None

    try:
        component.getBounds()
    except Exception:
        cache.pop(str(selector), None)
        return None
    return component


def invalidate_component_cache(driver: Any) -> None:
    """页面发生点击或输入后递增状态代次并清空组件缓存。"""
    state = _driver_state(driver)
    state[_GENERATION_ATTR] = _generation(driver) + 1
    cache = state.get(_CACHE_ATTR)
    if cache is not None:
        cache.clear()
    state.pop(_SNAPSHOT_CACHE_ATTR, None)
