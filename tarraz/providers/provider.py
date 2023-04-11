import json
from abc import ABC
from typing import List, Optional

from tarraz.logger import logger
from tarraz.models import Color, RGB
from tarraz.utils import euclidean_distance


class ColorProvider(ABC):
    def __init__(
        self,
        data_path: Optional[str] = None,
        colors: Optional[List["Color"]] = None,
    ) -> None:
        if not data_path and not colors:
            raise ValueError(
                "You need to supply either a data path or a colors list..."
            )

        self.matching_colors = {}
        self._data_path = data_path
        self.colors = colors if colors else self._read_colors()

        logger.debug("%d colors successfully processed.", len(self.colors))

    def _read_colors(self) -> "List[Color]":
        logger.info("Reading colors from %s", self._data_path)

        with open(self._data_path, mode="r") as data_file:
            colors = Color.create(json.load(data_file))

        return colors

    def get_matching_color(self, rgb_color: "RGB") -> "Optional[Color]":
        logger.debug("Getting a matching color for color %s.", rgb_color.css)

        if rgb_color in self.matching_colors:
            logger.debug("Loading matching color from cache...")
            return self.matching_colors[rgb_color]

        best_matching_index = self._get_best_color_index(rgb_color)

        if best_matching_index >= 0:
            matching_color = self.colors[best_matching_index]
            logger.debug(
                "Found %s as matching color for color %s.",
                matching_color.rgb.css,
                rgb_color.css,
            )
        else:
            matching_color = None
            logger.debug("No matching color found for %s color.", rgb_color.css)

        logger.debug("Storing matching color in cache...")
        self.matching_colors[rgb_color] = matching_color

        return matching_color

    def _get_best_color_index(self, rgb_color: "RGB") -> int:
        min_distance = float("inf")
        min_distance_index = float("-inf")

        for i, provider_color in enumerate(self.colors):
            dist = euclidean_distance(provider_color.rgb, rgb_color)

            if dist < min_distance:
                min_distance = dist
                min_distance_index = i

        return min_distance_index

    def index(self, rgb_color: "RGB") -> int:
        for i, c in enumerate(self.colors):
            if c.rgb == rgb_color:
                return i
        return -1

    def get(self, rgb_color: "RGB", default: "Optional" = None) -> "Optional[Color]":
        index = self.index(rgb_color)

        if index < 0:
            return default

        return self.colors[index]

    def __str__(self):
        name = self.__class__.__name__
        if "Provider" in name:
            name = name.split("Provider")[0]

        return f"{name}"
