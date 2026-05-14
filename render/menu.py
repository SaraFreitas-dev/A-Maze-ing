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
    """Pre-loaded MLX image pointers for menu background and banner."""
    bg: Any = None
    banner: Any = None


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

        # Updated from convert to magick for modern ImageMagick
        os.system(f"magick {bg_png} {bg_xpm}")
    imgs.bg, _, _ = mlx.mlx_xpm_file_to_image(mlx_ptr, bg_xpm)

    # Load banner image
    banner_height = 180
    banner_xpm = f"assets/generated/banner_{WINDOW_WIDTH}x{banner_height}.xpm"
    if not os.path.exists(banner_xpm):
        banner_png = banner_xpm.replace(".xpm", ".png")
        if not os.path.exists(banner_png):
            src = Image.open("assets/imgs/banner.jpeg")

            # Smart crop to remove black borders
            # Convert to RGB if needed for consistency
            if src.mode != "RGB":
                src = src.convert("RGB")  # type: ignore

            # Manual crop based on the banner layout we can see
            # The content appears to be in the middle horizontal band
            width, height = src.size

            # From the image, the useful content is roughly in the middle third
            crop_top = int(height * 0.35)  # Start from about 35% down
            crop_bottom = int(height * 0.65)  # End at about 65% down
            crop_left = 0  # Keep full width
            crop_right = width

            cropped_src = src.crop((crop_left, crop_top,
                                    crop_right, crop_bottom))

            # Resize with high quality resampling
            resized_src = cropped_src.resize(
                (WINDOW_WIDTH, banner_height),
                Image.Resampling.LANCZOS  # High quality resampling
            )
            resized_src.save(banner_png)
        os.system(f"magick {banner_png} {banner_xpm}")
    imgs.banner, _, _ = mlx.mlx_xpm_file_to_image(mlx_ptr, banner_xpm)

    return imgs


# ── Menu rendering ────────────────────────────────────────
def _draw_menu(
    mlx: Mlx, mlx_ptr: Any, win_ptr: Any, imgs: MenuImages
) -> None:
    """Render the menu background image."""
    if imgs.bg is None:
        return
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, imgs.bg, 0, 0)


def _draw_banner(
    mlx: Mlx, mlx_ptr: Any, win_ptr: Any, imgs: MenuImages
) -> None:
    """Render the banner at the bottom of the window."""
    if imgs.banner is None:
        return
    banner_y = WINDOW_HEIGHT - 180  # Position at bottom
    mlx.mlx_put_image_to_window(mlx_ptr, win_ptr, imgs.banner, 0, banner_y)
