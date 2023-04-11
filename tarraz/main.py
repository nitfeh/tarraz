import os
import argparse

from tarraz import version
from tarraz import constants
from tarraz.logger import logger
from tarraz.processor import Tarraz
from tarraz.providers import DMCProvider
from tarraz.stitcher import DisplayStitcher, SVGStitcher
from tarraz.utils import parser, file_choices, color_choices


def init_argparse() -> argparse.ArgumentParser:
    parser.add_argument(
        "-v",
        "--version",
        action="version",
        version=f"{parser.prog} version {version.__version__}",
    )
    parser.add_argument(
        "image",
        type=lambda f: file_choices(constants.IMAGE_EXTENSIONS, f),
        help="Input image",
    )
    parser.add_argument(
        "-c",
        "--colors",
        type=int,
        default=3,
        help="Number of colors to use in the pattern.",
    )
    parser.add_argument(
        "-n",
        "--stitches-count",
        type=int,
        default=50,
        help="Number of stitches to use in the x axis.",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=1000,
        help="Result pattern width.",
    )
    parser.add_argument(
        "-m",
        "--dmc",
        type=lambda f: file_choices(constants.COLORS_EXTENSIONS, f),
        default="tarraz/assets/dmc.json",
        help="DMC json color path.",
    )
    parser.add_argument(
        "-t",
        "--transparent",
        nargs="+",
        type=lambda f: color_choices(f),
        help="A Color to ignore from the end result.",
    )
    parser.add_argument(
        "-s",
        "--dist",
        type=str,
        default=constants.BASE_DIR / ".tmp/",
        help="DMC json color path.",
    )
    parser.add_argument(
        "-z",
        "--cell-size",
        type=int,
        default=10,
        help="The size of the generated Aida fabric cell.",
    )
    parser.add_argument(
        "--no-cleanup",
        action="store_true",
        help="Don't run cleanup job on generated image.",
    )
    parser.add_argument(
        "--svg",
        action="store_true",
        help="Export result to svg files.",
    )
    return parser


def main() -> None:
    p = init_argparse()
    args = p.parse_args()

    base_file_name = os.path.basename(args.image).split(".")[0]

    logger.info("Generating pattern for %s...", base_file_name)
    logger.debug("\t File path: %s", args.image)
    logger.debug("\t X count: %s", args.stitches_count)
    logger.debug("\t Colors number: %s", args.colors)
    logger.debug("\t Result width: %s", args.width)
    logger.debug("\t DMC path: %s", args.dmc)
    logger.debug("\t No cleanup: %s", args.no_cleanup)
    logger.debug("\t SVG cell size: %s", args.cell_size)
    logger.debug("\t Destination: %s", args.dist)

    if args.transparent:
        logger.info("Transparent colors: %s", args.transparent)

    provider = DMCProvider(args.dmc)
    tarraz = Tarraz(
        args.image,
        provider=provider,
        x_count=args.stitches_count,
        colors_num=args.colors,
        result_width=args.width,
        cleanup=not args.no_cleanup,
    )

    pattern, colors = tarraz.process()

    if args.svg:
        SVGStitcher.stitch(
            pattern,
            colors,
            tarraz.size,
            transparent=args.transparent,
            configs=constants.SVG_VARIANTS,
            cell_size=args.cell_size,
            save_to=f"{args.dist}/{base_file_name}",
        )
    else:
        DisplayStitcher.stitch(
            pattern,
            colors,
            tarraz.size,
            transparent=args.transparent,
            cell_size=args.cell_size,
            save_to=f"{args.dist}/{base_file_name}",
        )

    logger.info("Tarraz process finished successfully!")


if __name__ == "__main__":
    exit(main())
