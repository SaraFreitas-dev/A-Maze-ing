from __future__ import annotations
import os
from dataclasses import dataclass
from typing import Any
from PIL import Image
from mlx import Mlx

# ── Window ────────────────────────────────────────────────
WINDOW_WIDTH: int = 1600
WINDOW_HEIGHT: int = 900

# ── Key codes ─────────────────────────────────────────────
KEY_ESC: int = 65307
KEY_1: int = 49
KEY_2: int = 50


@dataclass
class MenuImages:
    """Pre-loaded MLX image pointer for the menu background."""
    bg: Any = None


# ── Asset helpers ─────────────────────────────────────────

def _prepare_menu_images(mlx: Mlx, mlx_ptr: Any) -> MenuImages:
    """Load the menu background XPM, generating it from PNG if needed."""
    os.makedirs("assets/generated", exist_ok=True)
    imgs = MenuImages()

    bg_xpm = (
        f"assets/generated/"
        f"menu_bgnew_{WINDOW_WIDTH}x{WINDOW_HEIGHT}.xpm"
    )
    if not os.path.exists(bg_xpm):
        bg_png = bg_xpm.replace(".xpm", ".png")
        if not os.path.exists(bg_png):
            src = Image.open("assets/imgs/menu_background.png")
            resized_src = src.resize(
                (WINDOW_WIDTH, WINDOW_HEIGHT),
                Image.Resampling.LANCZOS
            )
            resized_src.save(bg_png)
        os.system(f"convert {bg_png} {bg_xpm}")
    imgs.bg, _, _ = mlx.mlx_xpm_file_to_image(mlx_ptr, bg_xpm)

    return imgs


# ── Menu rendering ────────────────────────────────────────
def _draw_menu(
    mlx: Mlx, mlx_ptr: Any, win_ptr: Any, imgs: MenuImages
) -> None:
    """Render the menu background image."""
    if imgs.bg is None:
        return
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, imgs.bg, 0, 0)
