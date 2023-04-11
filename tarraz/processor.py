from PIL import Image
from typing import List, TYPE_CHECKING, Union

from tarraz.logger import logger
from tarraz.models import Color, Coordinate, ImageSize, RGB
from tarraz.providers import DMCProvider
from tarraz.utils import generate_image, get_neighbours, index_of

if TYPE_CHECKING:
    from tarraz.models import (
        Palette,
        PaletteImage,
        PaletteImageRow,
        RGBImage,
        RGBImageRow,
    )
    from tarraz.providers import ColorProvider


class Tarraz(object):
    def __init__(
        self,
        image_path: str,
        provider: "ColorProvider" = DMCProvider(),
        cleanup: bool = True,
        colors_num: int = 3,
        result_width: int = 1000,
        x_count: int = 50,
    ) -> None:
        self.new_width = result_width

        self._cleanup = cleanup
        self._colors_num = colors_num
        self._image = Image.open(image_path)
        self._provider = provider
        self._x_count = x_count

    @property
    def pixel_size(self) -> int:
        return self.new_width // int(self._x_count)

    @property
    def size(self) -> "ImageSize":
        return ImageSize(*self._image.size)

    def process(self) -> tuple["PaletteImage", List[Color]]:
        """Create a resized image with the translated colors."""
        logger.info("Processing image started...")

        self._resize_image()
        translated_image = self._translate_image()
        colored_image = generate_image(translated_image)

        # Translate pixels through the palette using the required number of colors.
        self._image = colored_image.convert(
            "P", palette=Image.ADAPTIVE, colors=self._colors_num
        )

        pattern = self._create_pattern()
        colors = self._generate_palette()

        if self._cleanup:
            self._clean_up(pattern)
        else:
            logger.info("Bypassing cleanup job!")

        return pattern, colors

    def _get_pixel(self, x: int, y: int, palette=False) -> Union[int, "RGB"]:
        coordinate = Coordinate(x, y)
        pixel_data = self._image.getpixel(coordinate)

        if palette:
            return pixel_data

        # Ignore alpha value incase we have a png
        return RGB(*pixel_data[:3])

    def _resize_image(self):
        scale = self.new_width / self.size.width
        new_height = int(self.size.height * scale)
        new_size = ImageSize(self.new_width, new_height)

        self._image = self._image.resize(new_size, Image.NEAREST)

    def _translate_image(self) -> "RGBImage":
        """Convert image pixels colors to match the provider colors."""
        logger.info(f"Translating image colors to {self._provider}...")

        colors: "RGBImage" = []
        for y in range(0, self.size.height, self.pixel_size):
            row: "RGBImageRow" = []
            for x in range(0, self.size.width, self.pixel_size):
                pixel = self._get_pixel(x, y)
                matching_color = self._provider.get_matching_color(pixel)
                row.append(matching_color.rgb)
            colors.append(row)

        return colors

    def _create_pattern(self) -> "PaletteImage":
        """Create an image with the information from the new image."""
        logger.info("Generating SVG information...")
        pattern: "PaletteImage" = []

        for y in range(self.size.height):
            row: "PaletteImageRow" = []
            for x in range(self.size.width):
                color_index = self._get_pixel(x, y, palette=True)
                row.append(color_index)
            pattern.append(row)

        return pattern

    def _generate_palette(self) -> "Palette":
        """Creates a new palette with the dmc objects"""
        logger.info("Generating SVG palette...")
        image_palette = self._image.getpalette()

        palette = []
        for i in range(self._colors_num):
            r = i * 3
            red, green, blue = image_palette[r : r + 3]

            color = RGB(red, green, blue)
            matching_color = self._provider.get_matching_color(color)
            palette.append(matching_color)

        return palette

    def _clean_up(self, pattern: "PaletteImage") -> None:
        """Perform extra jobs like cleaning the image  removing isolated pixels."""
        logger.info("Cleaning up proces started...")

        for x in range(self.size.width):
            for y in range(self.size.height):
                coordinate = Coordinate(y, x)
                neighbours = get_neighbours(coordinate, pattern)

                if index_of(neighbours, pattern[y][x]) == -1:
                    mode = max(neighbours, key=neighbours.count)
                    pattern[y][x] = mode
