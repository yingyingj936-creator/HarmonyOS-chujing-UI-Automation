from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any
import tomllib


@dataclass(frozen=True)
class AppSettings:
    target_device: str
    bundle: str
    ability: str
    default_destination: str = "中国香港"
    startup_wait_seconds: float = 4.0
    cleanup_back_steps: int = 4
    cleanup_back_interval_seconds: float = 1.0
    enable_file_order: bool = True


def _read_toml(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Config file not found: {path}")
    with path.open("rb") as f:
        return tomllib.load(f)


def load_settings(
    config_path: str | None = None,
    *,
    target_device: str | None = None,
    bundle: str | None = None,
    ability: str | None = None,
    enable_file_order: bool | None = None,
) -> AppSettings:
    root_dir = Path(__file__).resolve().parents[1]
    default_config_path = root_dir / "configs" / "default.toml"
    path = Path(config_path).resolve() if config_path else default_config_path
    data = _read_toml(path)

    app_cfg = data.get("app", {})
    run_cfg = data.get("runtime", {})
    order_cfg = data.get("execution", {})

    resolved_target_device = target_device or app_cfg.get("target_device")
    resolved_bundle = bundle or app_cfg.get("bundle")
    resolved_ability = ability or app_cfg.get("ability")
    resolved_enable_file_order = (
        enable_file_order
        if enable_file_order is not None
        else bool(order_cfg.get("enable_file_order", True))
    )

    if not resolved_target_device or not resolved_bundle or not resolved_ability:
        raise ValueError(
            "Invalid config: target_device, bundle, ability are required."
        )

    return AppSettings(
        target_device=resolved_target_device,
        bundle=resolved_bundle,
        ability=resolved_ability,
        default_destination=str(app_cfg.get("default_destination", "中国香港")),
        startup_wait_seconds=float(run_cfg.get("startup_wait_seconds", 4.0)),
        cleanup_back_steps=int(run_cfg.get("cleanup_back_steps", 4)),
        cleanup_back_interval_seconds=float(
            run_cfg.get("cleanup_back_interval_seconds", 1.0)
        ),
        enable_file_order=resolved_enable_file_order,
    )

