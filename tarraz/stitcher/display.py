from typing import TYPE_CHECKING, Optional

from PIL import Image
from tarraz.stitcher import Stitcher

if TYPE_CHECKING:
    from tarraz.models import Color, Coordinate


class DisplayStitcher(Stitcher):
    def init(self, width: int, height: int) -> None:
        self.result = Image.new("RGB", (width, height))

    def draw_cell(
        self, color: "Optional[Color]", coordinate: "Coordinate", size: int
    ) -> None:
        pixels = self.result.load()

        for i in range(coordinate.x, coordinate.x + size):
            for j in range(coordinate.y, coordinate.y + size):
                pixels[i - size, j - size] = color.rgb

    def finish(self) -> None:
        self.result.show()

    def save(self, dist_dir: str, ext: str) -> None:
        return
