from __future__ import annotations

from pathlib import Path
from typing import Any
from uuid import uuid4

import allure
from PIL import Image, ImageDraw


ARTIFACT_DIR = Path("reports") / "allure_visual"


def _make_artifact_path(prefix: str, suffix: str = "png") -> Path:
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True)
    return ARTIFACT_DIR / f"{prefix}_{uuid4().hex}.{suffix}"


def _attach_png(path: Path, name: str) -> None:
    allure.attach.file(
        str(path),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


def _jpeg_to_png(jpeg_path: Path, prefix: str) -> Path:
    png_path = _make_artifact_path(prefix, "png")
    with Image.open(jpeg_path) as img:
        img.save(png_path, format="PNG")
    return png_path


def _to_rect_tuple(bounds: Any) -> tuple[int, int, int, int]:
    """
    Convert hypium bounds to (left, top, right, bottom).
    Compatible with Rect object / dict / tuple.
    """
    if hasattr(bounds, "left") and hasattr(bounds, "top"):
        return int(bounds.left), int(bounds.top), int(bounds.right), int(bounds.bottom)

    if isinstance(bounds, dict):
        left = bounds.get("left", bounds.get("leftX", 0))
        top = bounds.get("top", bounds.get("topY", 0))
        right = bounds.get("right", bounds.get("rightX", 0))
        bottom = bounds.get("bottom", bounds.get("bottomY", 0))
        return int(left), int(top), int(right), int(bottom)

    if isinstance(bounds, (list, tuple)) and len(bounds) == 4:
        return int(bounds[0]), int(bounds[1]), int(bounds[2]), int(bounds[3])

    raise ValueError(f"Unsupported bounds type: {type(bounds)}")


def attach_fullscreen(driver: Any, name: str) -> Path:
    """Capture current screen and attach it to Allure."""
    raw_jpeg_path = _make_artifact_path("full_raw", "jpeg")
    saved_jpeg_path = Path(driver.capture_screen(str(raw_jpeg_path), in_pc=True))
    full_png_path = _jpeg_to_png(saved_jpeg_path, "full")
    _attach_png(full_png_path, name)
    return full_png_path


def assert_visible_and_attach_highlight(
    driver: Any,
    selector: Any,
    name: str,
    *,
    timeout: float = 5,
    margin: int = 8,
    line_width: int = 6,
    outline_color: str = "#FF2D55",
    attach_crop: bool = True,
) -> Any:
    """
    Wait for component, then attach:
    1) full screenshot with highlighted rectangle
    2) optional cropped screenshot of target component
    """
    if not driver.wait_for_component(selector, timeout=timeout):
        attach_fullscreen(driver, f"{name}-未找到-全屏")
        raise AssertionError(f"未找到组件：{name}")

    component = driver.find_component(selector)
    if component is None:
        attach_fullscreen(driver, f"{name}-定位失败-全屏")
        raise AssertionError(f"定位组件失败：{name}")

    full_raw_jpeg_path = _make_artifact_path("raw", "jpeg")
    saved_raw_jpeg_path = Path(driver.capture_screen(str(full_raw_jpeg_path), in_pc=True))

    left, top, right, bottom = _to_rect_tuple(component.getBounds())
    with Image.open(saved_raw_jpeg_path) as img:
        draw = ImageDraw.Draw(img)
        l = max(0, left - margin)
        t = max(0, top - margin)
        r = min(img.width - 1, right + margin)
        b = min(img.height - 1, bottom + margin)
        draw.rectangle([l, t, r, b], outline=outline_color, width=line_width)
        marked_path = _make_artifact_path("marked")
        img.save(marked_path)

    _attach_png(marked_path, f"{name}-圈选")

    if attach_crop:
        crop_jpeg_path = _make_artifact_path("crop", "jpeg")
        saved_crop_jpeg_path = Path(
            driver.capture_screen(str(crop_jpeg_path), in_pc=True, area=component)
        )
        crop_png_path = _jpeg_to_png(saved_crop_jpeg_path, "crop")
        _attach_png(crop_png_path, f"{name}-局部")
    return component
