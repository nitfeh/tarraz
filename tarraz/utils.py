import argparse
import bisect
import math
import os
from bisect import bisect_left
from typing import TYPE_CHECKING, List

from PIL import Image, ImageColor

from tarraz.logger import logger
from tarraz.models import ImageSize, RGB

if TYPE_CHECKING:
    from PIL.Image import Image as ImageType
    from tarraz.models import Coordinate, RGBImage


parser = argparse.ArgumentParser(
    description="Generate a DMC-colored cross-stitch pattern from a given image.",
)


def color_choices(value: str) -> "RGB":
    value = value.strip()

    try:
        value = (
            ImageColor.getrgb(value)
            if value.startswith("#")
            else [int(c) for c in value.split(",")]
        )
    except ValueError:
        raise argparse.ArgumentTypeError(f"Invalid color value '{value}'")

    return RGB(*value)


def file_choices(choices: List[str], file_name: str) -> str:
    _, ext = os.path.splitext(file_name)
    if ext.upper() not in map(str.upper, choices):
        raise argparse.ArgumentTypeError(
            f"Unsupported file format '{ext}'. Available formats are: {choices}."
        )
    return file_name


def index_of(iterable, element, sort=False) -> int:
    arr = sorted(iterable) if sort else iterable

    i = bisect_left(arr, element)
    if i != len(arr) and arr[i] == element:
        return i

    return -1


def euclidean_distance(rgb_1: "RGB", rgb_2: "RGB") -> float:
    red_point = (rgb_1.red - rgb_2.red) ** 2
    green_point = (rgb_1.green - rgb_2.green) ** 2
    blue_point = (rgb_1.blue - rgb_2.blue) ** 2

    return math.sqrt(red_point + green_point + blue_point)


def generate_image(data: "RGBImage") -> "ImageType":
    """Create a resized image from a given matrix of colors."""
    size = ImageSize(len(data[0]), len(data))
    logger.info(
        f"Generating a new image [{size.width}x{size.height}] for the new colors..."
    )

    image = Image.new("RGB", size)

    data = [rgb.native for row in data for rgb in row]
    image.putdata(data)

    return image


def get_neighbours(coordinate: "Coordinate", matrix: List[List[int]]) -> List[int]:
    x, y = coordinate
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0

    width = 1
    neighbours: List[int] = []

    for i in range(max(0, x - width), min(rows, x + width + 1)):
        for j in range(max(0, y - width), min(cols, y + width + 1)):
            if not (i == x and j == y):
                # Insort neighbors sorted
                bisect.insort_left(neighbours, matrix[i][j])

    return neighbours
