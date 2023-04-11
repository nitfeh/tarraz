import os
from typing import TYPE_CHECKING, Optional, List

from tarraz.logger import logger
from tarraz.models import Color, Coordinate
from tarraz.stitcher import Stitcher

if TYPE_CHECKING:
    from tarraz.models import (
        ImageSize,
        Palette,
        PaletteImage,
        RGB,
        StrokeType,
        SVGAttributes,
    )


class SVGStitcher(Stitcher):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.result = ""
        self.file_name = f"{self._dist_dir}/{self.name}.svg"

        if os.path.exists(self.file_name):
            logger.debug(f"Removing {self.file_name}...")
            os.remove(self.file_name)

    def init(self, width: int, height: int) -> None:
        self._append_to_file(
            f"""
        <svg xmlns="http://www.w3.org/2000/svg"
            width="{width}"
            height="{height}"
            style ="fill:none;">
        """
        )
        self._append_to_file(
            """
            <style>
                .svg_txt    {
                    font-size:20px;
                }
                .glyph  {
                    stroke:#000000;
                    stroke-width:1;
                    stroke:1;
                }
            </style>
        """
        )

    def finish(self) -> None:
        self._append_to_file("</svg>")

    def generate_key(
        self,
        colors: "Palette",
        size: int = 40,
        transparent: "Optional[List[RGB]]" = None,
    ):
        keyed = set()
        if not transparent:
            transparent = []

        y = 0
        for i in range(len(colors)):
            if colors[i].rgb in transparent:
                continue

            color = colors[i]
            if color.code in keyed:
                continue

            self._add_key_to_svg(Coordinate(0, y), size, color)
            y += size
            keyed.add(color.code)

    def draw_cell(
        self, color: "Optional[Color]", coordinate: "Coordinate", size: int
    ) -> None:
        fill, symbols, stroke = self._get_svg_attributes(color, coordinate, size)

        self._append_to_file(
            f"""
            <rect
                x="{coordinate.x}"
                y="{coordinate.y}"
                width="{size}"
                height="{size}"
                style="{fill}{stroke}"
            />
            {symbols}
        """
        )

    def draw_cells(
        self,
        pattern: "PaletteImage",
        palette: "Palette",
        cell_size: int,
        size: "ImageSize",
        config: "Optional[dict]" = None,
        transparent: "Optional[List[RGB]]" = None,
    ):
        super().draw_cells(
            pattern,
            palette,
            cell_size,
            size,
            config=config,
            transparent=transparent,
        )

        if config.get("mid_arrows"):
            self._mid_arrows(cell_size, size.width, size.height)

        if config.get("major_gridlines"):
            self._major_gridlines(cell_size, size.width, size.height)

    def _append_to_file(self, data: str) -> None:
        logger.debug("Appending data to file: %s...", self.file_name)

        with open(self.file_name, "a") as f:
            f.write(data)

    def save(self, ext: str) -> None:
        return

    def _major_gridlines(self, size: int, width: int, height: int) -> None:
        start = size + size * 10
        step = size * 10

        for x in range(start, width, step):
            self._append_to_file(
                f"""
                <line
                    x1="{x}"
                    y1="{size}"
                    x2="{x}"
                    y2="{height}"
                    style="stroke:black; stroke-width:2"
                />
            """
            )

        for y in range(start, height, step):
            self._append_to_file(
                f"""
                <line
                    x1="{size}"
                    y1="{y}"
                    x2="{width}"
                    y2="{y}"
                    style="stroke:black; stroke-width:2"
                />
            """
            )

    def _mid_arrows(self, size: int, width: int, height: int) -> None:
        h = size // 2

        self._append_to_file(
            f"""
            <path
                d="M0 {h}L{size} {h}M{h} 0L{size} {h} {h} {size}"
                stroke="black"
                stroke-width="2"
                fill="none"
                transform="translate(0 {height // 2})"
            />
        """
        )

        self._append_to_file(
            f"""
            <path
                d="M{h} 0L{h} {size} M{size} {h}L{h} {size} 0 {h}"
                stroke="black"
                stroke-width="2"
                fill="none"
                transform="translate({width // 2} 0)"
            />
        """
        )

    @staticmethod
    def _gen_glyph(color: "Color", coordinate: "Coordinate", scale: float = 1.0) -> str:
        transform = f"translate({coordinate.x} {coordinate.y}) scale({scale})"
        fill = ""

        if not color.glyph:
            color.assign_glyph()

        if color.glyph == 0:
            # Backslash
            path = "M4 4L16 16"
        elif color.glyph == 1:
            # Forward slash
            path = "M4 16L16 4M4 10L 16 10"
        elif color.glyph == 2:
            # Black little square
            path = "M7 7L7 13 13 13 13 7Z"
            fill = "black"
        elif color.glyph == 3:
            #
            path = "M4 4L10 16L16 4 Z"
        elif color.glyph == 4:
            # Diagonal cross
            path = "M4 4L16 16M4 16 L16 4"
        elif color.glyph == 5:
            # Square
            path = "M4 4L4 16 16 16 16 4Z"
        elif color.glyph == 6:
            # Upside down black triangle
            path = "M4 4L10 16L16 4 Z"
            fill = "black"
        elif color.glyph == 7:
            # Black diamond
            path = "M10 4L6 10 10 16 14 10Z"
            fill = "black"
        elif color.glyph == 8:
            # Little square
            path = "M8 8L8 12 12 12 12 8Z"
        elif color.glyph == 9:
            # 8-way cross
            path = "M4 4L16 16M4 16 L16 4M10 4L10 16M4 10L16 10"
        elif color.glyph == 10:
            # Black Square
            path = "M4 4L4 16 16 16 16 4Z"
            fill = "black"
        else:
            return ""

        return f"""
            <path
                class="glyph"
                d="{path}"
                fill="{fill}"
                transform="{transform}"
            />
        """

    def _add_key_to_svg(
        self, coordinate: "Coordinate", size: int, color: "Color"
    ) -> None:
        fill, symbols, stroke = self._get_svg_attributes(color, coordinate, size)

        self._append_to_file(
            f"""
            <rect
                x="0"
                y="{coordinate.y}"
                width="{size}"
                height="{size}"
                style="{fill}{stroke}"
            />
            {symbols}
        """
        )

        # Color name
        self._append_to_file(
            f"""
            <rect
                x="{size}"
                y="{coordinate.y}"
                width="{size * 10}"
                height="{size}"
                style="fill: rgb(255,255,255); stroke: black; stroke-width: 1;"
            />
        """
        )
        self._append_to_file(
            f"""
            <text
                x="{coordinate.x + size * 1.5}"
                y="{coordinate.y + size / 2}"
                fill="black"
            >
                {color.name}
            </text>
        """
        )

        # Color code
        self._append_to_file(
            f"""
            <rect
                x="{size * 11}"
                y="{coordinate.y}"
                width="{size * 2}"
                height="{size}"
                style="fill: rgb(255,255,255); stroke: black; stroke-width: 1;"
            />
        """
        )
        self._append_to_file(
            f"""
            <text
                x="{size * 11 + (size / 2)}"
                y="{coordinate.y + size / 2}"
                fill="black"
            >
                {color.code}
            </text>
        """
        )

    def _get_svg_attributes(
        self, color: "Optional[Color]", coordinate: "Coordinate", size: int
    ) -> "SVGAttributes":
        fill = "fill:rgb(255,255,255);"
        stroke: "StrokeType" = "stroke:none;"
        symbols = ""

        scale = size / self._scale

        if not color:
            fill = f"fill:transparent;"
        elif not self._black_white:
            fill = f"fill:{color.rgb.css};"

        if self._minor_lines:
            stroke = "stroke:rgb(20,20,20);stroke-width:1;"

        if color and self._symbols:
            symbols = self._gen_glyph(color, coordinate, scale)

        return fill, symbols, stroke
