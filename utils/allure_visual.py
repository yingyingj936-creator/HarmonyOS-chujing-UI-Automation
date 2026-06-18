from __future__ import annotations

from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Any

import allure
from PIL import Image, ImageDraw


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


def attach_fullscreen(driver: Any, name: str) -> None:
    """Capture current screen and attach it to Allure."""
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
    component = driver.wait_for_component(selector, timeout=timeout)
    if component is None:
        attach_fullscreen(driver, f"{name}-未找到-全屏")
        raise AssertionError(f"未找到组件：{name}")

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
            marked_image = raw_image.convert("RGB")
            draw = ImageDraw.Draw(marked_image)
            l = max(0, left - margin)
            t = max(0, top - margin)
            r = min(marked_image.width - 1, right + margin)
            b = min(marked_image.height - 1, bottom + margin)
            draw.rectangle([l, t, r, b], outline=outline_color, width=line_width)
            _attach_image(marked_image, f"{name}-圈选")

        if attach_crop:
            crop_jpeg_path = Path(temp_dir) / "crop.jpeg"
            saved_crop_jpeg_path = Path(
                driver.capture_screen(
                    str(crop_jpeg_path),
                    in_pc=True,
                    area=component,
                )
            )
            with Image.open(saved_crop_jpeg_path) as crop_image:
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
            l = max(0, left - margin)
            t = max(0, top - margin)
            r = min(marked_image.width - 1, right + margin)
            b = min(marked_image.height - 1, bottom + margin)
            draw.rectangle([l, t, r, b], outline=outline_color, width=line_width)
            _attach_image(marked_image, f"{name}-圈选")
