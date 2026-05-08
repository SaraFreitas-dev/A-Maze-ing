from mlx import Mlx
from typing import Any


class Assets:
    """
    Loads and stores all game assets / images
    """
    def __init__(self, mlx: Mlx,
                 mlx_ptr: Any,
                 tile_size: int,
                 theme: str) -> None:
        # MENU BACKGROUND
        self.title_size = tile_size
        self.menu_background, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            "assets/imgs/menu_background.xpm"
        )

        # WALL
        self.wall, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/wall_{tile_size}.xpm"
        )

        # 42 WALL - DARKER
        self.wall_42, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/wall_42_{tile_size}.xpm"
        )

        # NORMAL THEME
        self.floor_normal, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/{theme}_floor_{tile_size}.xpm"
        )

        # GOTHIC THEME
        self.floor_gothic, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/{theme}_floor_{tile_size}.xpm"
        )

        # TRAIL
        self.trail, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/{theme}_trail_{tile_size}.xpm"
        )

        # UI HUD / BANNER
        self.banner, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            "assets/imgs/banner.xpm"
        )

        # DUCKS / PLAYER
        self.duck_normal, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/{theme}_duck_{tile_size}.xpm"
        )

        self.duck_gothic, _, _ = mlx.mlx_xpm_file_to_image(
            mlx_ptr,
            f"assets/generated/{theme}_duck_{tile_size}.xpm"
        )
