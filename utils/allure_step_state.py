from __future__ import annotations

from contextvars import ContextVar, Token
from dataclasses import dataclass
from typing import Any

import allure


@dataclass
class _StepState:
    visual_attached: bool = False


_CURRENT_STEP: ContextVar[_StepState | None] = ContextVar(
    "allure_visual_step_state",
    default=None,
)
_ORIGINAL_STEP = allure.step
_INSTALLED = False


class _TrackedStep:
    def __init__(self, title: str) -> None:
        self._allure_context = _ORIGINAL_STEP(title)
        self._token: Token[_StepState | None] | None = None

    def __enter__(self) -> Any:
        result = self._allure_context.__enter__()
        self._token = _CURRENT_STEP.set(_StepState())
        return result

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        try:
            return self._allure_context.__exit__(exc_type, exc_val, exc_tb)
        finally:
            if self._token is not None:
                _CURRENT_STEP.reset(self._token)


def install_allure_step_tracking() -> None:
    """让视觉工具能够识别当前 Allure 步骤，限制每步一次抓屏。"""
    global _INSTALLED
    if _INSTALLED:
        return

    def tracked_step(title: Any) -> Any:
        if callable(title):
            return _ORIGINAL_STEP(title)
        return _TrackedStep(str(title))

    allure.step = tracked_step
    _INSTALLED = True


def claim_step_visual() -> bool:
    """当前步骤尚未附加视觉证据时占用名额；步骤外始终允许。"""
    state = _CURRENT_STEP.get()
    if state is None:
        return True
    if state.visual_attached:
        return False
    state.visual_attached = True
    return True
