from typing import List, Literal, NamedTuple, TypeVar, Optional


class RGB(NamedTuple):
    red: int
    green: int
    blue: int

    def __str__(self) -> str:
        return f"{self.red}, {self.green}, {self.blue}"

    @property
    def native(self):
        return self.red, self.green, self.blue

    @property
    def css(self):
        return f"rgb({self.red}, {self.green}, {self.blue})"


class Color(object):
    _glyphs_count = 0

    def __init__(self, code: str, rgb: RGB, name: str) -> None:
        self.code = code
        self.rgb = rgb
        self.name = name
        self._glyph: "Optional[int]" = None

    @property
    def glyph(self):
        return self._glyph

    def assign_glyph(self, number: "Optional[int]" = None):
        self._glyph = number if number else Color._glyphs_count + 1
        Color._glyphs_count += 1

    def __str__(self) -> str:
        return self.name

    @classmethod
    def create(
        cls, raw_colors: "List[dict]", extras: "Optional[List[RGB, RGB]]" = None
    ) -> List["Color"]:
        result = []
        processed = set()
        for raw_color in raw_colors:
            rgb = RGB(*raw_color["rgb"])
            if str(rgb) in processed:
                continue

            processed.add(str(rgb))
            result.append(
                cls(
                    code=raw_color["code"],
                    rgb=RGB(*raw_color["rgb"]),
                    name=raw_color["name"],
                )
            )

        extras = extras or []
        for i, extra in enumerate(extras):
            if str(extra) in processed:
                continue

            processed.add(str(extra))
            result.append(
                cls(
                    code=f"{i}",
                    rgb=extra,
                    name=f"extra_{i}",
                )
            )

        return result


class Coordinate(NamedTuple):
    x: int
    y: int


class ImageSize(NamedTuple):
    width: int
    height: int


T = TypeVar("T")

Palette = List["Color"]
ImageRow = List[T]

RGBImageRow = ImageRow[RGB]
PaletteImageRow = ImageRow[int]

RGBImage = List[RGBImageRow]
PaletteImage = List[ImageRow[int]]

StrokeType = Literal["stroke:rgb(20,20,20);stroke-width:1;", "stroke:none;"]
SVGAttributes = tuple[str, str, StrokeType]
