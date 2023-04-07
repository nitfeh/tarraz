from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
IMAGE_EXTENSIONS = (".jpeg", ".jpg", ".png", ".webp")
COLORS_EXTENSIONS = (".json",)

SVG_VARIANTS = [
    {
        "name": "key",
        "black_white": False,
        "minor_lines": True,
        "symbols": True,
        "key": True,
    },
    {
        "name": "colored_symbols",
        "black_white": False,
        "minor_lines": True,
        "symbols": True,
        "mid_arrows": True,
        "major_gridlines": True,
    },
    {
        "name": "black_white_symbols",
        "black_white": True,
        "minor_lines": True,
        "symbols": True,
        "mid_arrows": True,
        "major_gridlines": True,
    },
    {
        "name": "colored",
        "black_white": False,
        "minor_lines": False,
        "symbols": False,
        "mid_arrows": False,
        "major_gridlines": False,
    },
]
