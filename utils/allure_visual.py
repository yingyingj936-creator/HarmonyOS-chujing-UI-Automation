from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import allure
from PIL import Image, ImageDraw

from utils.allure_step_state import claim_step_visual
from utils.component_cache import recent_component, remember_component


def _attach_image(image: Image.Image, name: str) -> None:
    buffer = BytesIO()
    image.save(buffer, format="PNG")
    allure.attach(
        buffer.getvalue(),
        name=name,
        attachment_type=allure.attachment_type.PNG,
    )


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


def _normalize_rect(
    left: int,
    top: int,
    right: int,
    bottom: int,
    *,
    width: int,
    height: int,
    margin: int,
) -> tuple[int, int, int, int]:
    """Normalize possibly reversed or out-of-screen bounds before drawing."""
    x0, x1 = sorted((left, right))
    y0, y1 = sorted((top, bottom))

    x0 = max(0, min(width - 1, x0))
    x1 = max(0, min(width - 1, x1))
    y0 = max(0, min(height - 1, y0))
    y1 = max(0, min(height - 1, y1))

    l = max(0, x0 - margin)
    t = max(0, y0 - margin)
    r = min(width - 1, x1 + margin)
    b = min(height - 1, y1 + margin)
    if r <= l:
        l = max(0, min(width - 2, l))
        r = min(width - 1, l + 1)
    if b <= t:
        t = max(0, min(height - 2, t))
        b = min(height - 1, t + 1)
    return l, t, r, b


def attach_fullscreen(driver: Any, name: str, *, force: bool = False) -> None:
    """Capture current screen and attach it to Allure."""
    if not force and not claim_step_visual():
        return
    with TemporaryDirectory() as temp_dir:
        raw_jpeg_path = Path(temp_dir) / "fullscreen.jpeg"
        saved_jpeg_path = Path(
            driver.capture_screen(str(raw_jpeg_path), in_pc=True)
        )
        with Image.open(saved_jpeg_path) as image:
            _attach_image(image, name)


def component_has_red_highlight(
    driver: Any,
    component: Any,
    *,
    minimum_red_pixels: int = 20,
) -> bool:
    """通过组件截图中的红色像素判断爱心等图标是否处于高亮态。"""
    with TemporaryDirectory() as temp_dir:
        crop_jpeg_path = Path(temp_dir) / "state.jpeg"
        saved_crop_jpeg_path = Path(
            driver.capture_screen(
                str(crop_jpeg_path),
                in_pc=True,
                area=component,
            )
        )
        with Image.open(saved_crop_jpeg_path) as image:
            red_pixels = 0
            rgb_image = image.convert("RGB")
            pixels = (
                rgb_image.get_flattened_data()
                if hasattr(rgb_image, "get_flattened_data")
                else rgb_image.getdata()
            )
            for red, green, blue in pixels:
                if (
                    red >= 175
                    and green <= 145
                    and blue <= 155
                    and red - green >= 50
                    and red - blue >= 35
                ):
                    red_pixels += 1
                    if red_pixels >= minimum_red_pixels:
                        return True
    return False


def component_has_red_or_yellow_highlight(
    driver: Any,
    component: Any,
    *,
    minimum_colored_pixels: int = 20,
) -> bool:
    """识别红色或黄色高亮态，兼容点赞、收藏等图标按钮。"""
    with TemporaryDirectory() as temp_dir:
        crop_jpeg_path = Path(temp_dir) / "state.jpeg"
        saved_crop_jpeg_path = Path(
            driver.capture_screen(
                str(crop_jpeg_path),
                in_pc=True,
                area=component,
            )
        )
        with Image.open(saved_crop_jpeg_path) as image:
            colored_pixels = 0
            rgb_image = image.convert("RGB")
            pixels = (
                rgb_image.get_flattened_data()
                if hasattr(rgb_image, "get_flattened_data")
                else rgb_image.getdata()
            )
            for red, green, blue in pixels:
                is_red = (
                    red >= 175
                    and green <= 145
                    and blue <= 155
                    and red - green >= 50
                    and red - blue >= 35
                )
                is_yellow = (
                    red >= 175
                    and green >= 135
                    and blue <= 90
                    and red - blue >= 80
                    and green - blue >= 55
                )
                if is_red or is_yellow:
                    colored_pixels += 1
                    if colored_pixels >= minimum_colored_pixels:
                        return True
    return False


def assert_visible_and_attach_highlight(
    driver: Any,
    selector: Any,
    name: str,
    *,
    timeout: float = 5,
    margin: int = 8,
    line_width: int = 6,
    outline_color: str = "#FF2D55",
    attach_crop: bool = False,
) -> Any:
    """
    Wait for a selector, or reuse an existing component, then attach:
    1) full screenshot with highlighted rectangle
    2) optional cropped screenshot of target component
    """
    if hasattr(selector, "getBounds"):
        component = selector
    else:
        component = recent_component(driver, selector)
        if component is None:
            component = driver.wait_for_component(selector, timeout=timeout)
            if component is not None:
                remember_component(driver, selector, component)
    if component is None:
        attach_fullscreen(driver, f"{name}-未找到-全屏", force=True)
        raise AssertionError(f"未找到组件：{name}")

    if not claim_step_visual():
        return component

    left, top, right, bottom = _to_rect_tuple(component.getBounds())
    with TemporaryDirectory() as temp_dir:
        full_raw_jpeg_path = Path(temp_dir) / "fullscreen.jpeg"
        saved_raw_jpeg_path = Path(
            driver.capture_screen(
                str(full_raw_jpeg_path),
                in_pc=True,
            )
        )
        with Image.open(saved_raw_jpeg_path) as raw_image:
            source_image = raw_image.convert("RGB")
            marked_image = source_image.copy()
            draw = ImageDraw.Draw(marked_image)
            l, t, r, b = _normalize_rect(
                left,
                top,
                right,
                bottom,
                width=marked_image.width,
                height=marked_image.height,
                margin=margin,
            )
            draw.rectangle([l, t, r, b], outline=outline_color, width=line_width)
            _attach_image(marked_image, f"{name}-圈选")

            if attach_crop:
                crop_l, crop_t, crop_r, crop_b = _normalize_rect(
                    left,
                    top,
                    right,
                    bottom,
                    width=source_image.width,
                    height=source_image.height,
                    margin=0,
                )
                crop_image = source_image.crop(
                    (crop_l, crop_t, crop_r + 1, crop_b + 1)
                )
                _attach_image(crop_image, f"{name}-局部")
    return component


def attach_highlighted_bounds(
    driver: Any,
    bounds: Any,
    name: str,
    *,
    margin: int = 8,
    line_width: int = 6,
    outline_color: str = "#FF2D55",
) -> None:
    """Attach a full screenshot with a highlighted arbitrary bounds rectangle."""
    if not claim_step_visual():
        return
    left, top, right, bottom = _to_rect_tuple(bounds)
    with TemporaryDirectory() as temp_dir:
        full_raw_jpeg_path = Path(temp_dir) / "fullscreen.jpeg"
        saved_raw_jpeg_path = Path(
            driver.capture_screen(
                str(full_raw_jpeg_path),
                in_pc=True,
            )
        )
        with Image.open(saved_raw_jpeg_path) as raw_image:
            marked_image = raw_image.convert("RGB")
            draw = ImageDraw.Draw(marked_image)
            l, t, r, b = _normalize_rect(
                left,
                top,
                right,
                bottom,
                width=marked_image.width,
                height=marked_image.height,
                margin=margin,
            )
            draw.rectangle([l, t, r, b], outline=outline_color, width=line_width)
            _attach_image(marked_image, f"{name}-圈选")
