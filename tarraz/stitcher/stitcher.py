import os
from abc import ABC
from typing import TYPE_CHECKING, Optional, List

from tarraz import constants
from tarraz.logger import logger
from tarraz.models import Coordinate

if TYPE_CHECKING:
    from tarraz.models import Color, ImageSize, Palette, PaletteImage, RGB


class Stitcher(ABC):
    def __init__(
        self,
        name: str,
        black_white: bool = False,
        minor_lines: bool = False,
        symbols: bool = True,
        scale: int = 20,
        save_to: "Optional[str]" = None,
        *args,
        **kwargs,
    ) -> None:
        self._black_white = black_white
        self._minor_lines = minor_lines
        self._symbols = symbols
        self._scale = scale

        self.name = name
        self.result = None

        self._dist_dir = save_to if save_to else constants.BASE_DIR / ".tmp"
        os.makedirs(self._dist_dir, exist_ok=True)

    def init(self, width: int, height: int) -> NotImplemented:
        return NotImplemented

    def finish(self) -> NotImplemented:
        return NotImplemented

    def save(self, ext: str) -> None:
        logger.debug("Create exports directory: %s...", self._dist_dir)

        file_name = f"{self._dist_dir}/{self.name}.{ext}"
        with open(file_name, "w") as f:
            logger.info(f"Saving {file_name}")
            f.write(self.result)

    def generate_key(
        self,
        colors: "Palette",
        size: int = 40,
        transparent: "Optional[List[RGB]]" = None,
    ) -> NotImplemented:
        return NotImplemented

    def draw_cell(
        self, color: "Optional[Color]", coordinate: "Coordinate", size: int
    ) -> NotImplemented:
        return NotImplemented

    def draw_cells(
        self,
        pattern: "PaletteImage",
        colors: "Palette",
        cell_size: int,
        size: "ImageSize",
        config: "Optional[dict]" = None,
        transparent: "Optional[List[RGB]]" = None,
    ):
        x = y = cell_size
        for row in pattern:
            for color_i in row:
                coordinate = Coordinate(x, y)
                color = (
                    colors[color_i] if colors[color_i].rgb not in transparent else None
                )
                self.draw_cell(color, coordinate, cell_size)
                x += cell_size
            y += cell_size
            x = cell_size

    @classmethod
    def stitch(
        cls,
        pattern: "PaletteImage",
        colors: "Palette",
        size: "ImageSize",
        cell_size: int = 10,
        configs: "Optional[dict]" = None,
        ext: "Optional[str]" = None,
        key_size: int = 40,
        save_to: "Optional[str]" = None,
        transparent: "Optional[List[RGB]]" = None,
    ):
        """Export picture with given variants.
        Supported variants:
          * Black/white.
          * Colored picture.
          * Colored with symbols.
        """
        logger.info("Stitching job started...")
        width = size.width * cell_size
        height = size.height * cell_size

        if not configs:
            configs = [{"name": "NO_CONFIG"}]

        for config in configs:
            variant = cls(**config, save_to=save_to)

            if config.get("key"):
                variant.init(key_size * 13, key_size * len(colors))
                variant.generate_key(colors, key_size, transparent=transparent)
            else:
                variant.init(width, height)
                variant.draw_cells(
                    pattern,
                    colors,
                    cell_size,
                    size,
                    config=config,
                    transparent=transparent,
                )

            variant.finish()
            variant.save(ext)

    def __str__(self):
        return f"Stitcher<{self.name}>"
