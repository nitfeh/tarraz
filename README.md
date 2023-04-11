# Tarraz | طرّاز
A cross-stitch image generator.
Generates a cross stitch pattern from an image of your choice. The generated pattern is DMC colored.

Takes an image file and generates a cross stitch pattern using a user specified color..

## Supported image extensions
1. JPEG (.jpg, .jpeg)
2. PNG (.png)
3. WebP (.webp)

## Current color providers
1. DMC

## Results

Photo by [Kiki Siepel](https://unsplash.com/@studiokiek?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText) on [Unsplash](https://unsplash.com/images/nature/flower?utm_source=unsplash&utm_medium=referral&utm_content=creditCopyText)
<img src="https://github.com/nitfe/tarraz/raw/v0.0.1/images/flower.jpg" alt="Alt text" style="display: inline-block; margin: 0 auto; max-width: 600px"/>

<img src="https://github.com/nitfe/tarraz/raw/v0.0.1/images/colored_symbols.jpg" alt="Colored with Symbols" style="display: inline-block; margin: 0 auto; max-width: 300px"/>
<img src="https://github.com/nitfe/tarraz/raw/v0.0.1/images/black_white_symbols.jpg" alt="Black White with Symbols" style="display: inline-block; margin: 0 auto; max-width: 300px"/>
<img src="https://github.com/nitfe/tarraz/raw/v0.0.1/images/colored.jpg" alt="Colored" style="display: inline-block; margin: 0 auto; max-width: 300px"/>
<img src="https://github.com/nitfe/tarraz/raw/v0.0.1/images/key.jpg" alt="Keys" style="display: inline-block; margin: 0 auto; max-width: 300px; height: 256px"/>


## Usage
### Installation
```
pip install tarraz
```

### CLI Example
```shell
tarraz .tmp/palestinian_flag.jpg --colors 6 --stitches-count 100
```

### Python Example
```python
from tarraz import constants
from tarraz.processor import Tarraz
from tarraz.providers import DMCProvider
from tarraz.stitcher import SVGStitcher
from tarraz.models import RGB


# Choose a color provider
image_path = ".tmp/flower.jpg"
provider = DMCProvider()

tarraz = Tarraz(
    image_path,
    provider=provider,  # Optional if not using a custom provider
    x_count=100,        # Default 50
    colors_num=6,       # default 3
    result_width=200,   # Default 1000
    cleanup=True,       # Default True
)

# Process the image
pattern, colors = tarraz.process()

# Stitch the result
SVGStitcher.stitch(
    pattern,
    colors,
    tarraz.size,
    transparent=[RGB(255,255,255)],
    configs=constants.SVG_VARIANTS,
    cell_size=10,
    save_to="/tmp/test/",
)

```

### Options
```shell
$ tarraz --help
usage: tarraz [-h] [-v] [-c COLORS] [-n STITCHES_COUNT] [-w WIDTH] [-m DMC] [-t TRANSPARENT [TRANSPARENT ...]] [-s DIST] [-z CELL_SIZE] [--no-cleanup] [--svg] image

Generate a DMC-colored cross-stitch pattern from a given image.

positional arguments:
  image                 Input image

optional arguments:
  -h, --help            show this help message and exit
  -v, --version         show program's version number and exit
  -c COLORS, --colors COLORS
                        Number of colors to use in the pattern.
  -n STITCHES_COUNT, --stitches-count STITCHES_COUNT
                        Number of stitches to use in the x axis.
  -w WIDTH, --width WIDTH
                        Result pattern width.
  -m DMC, --dmc DMC     DMC json color path.
  -t TRANSPARENT [TRANSPARENT ...], --transparent TRANSPARENT [TRANSPARENT ...]
                        A Color to ignore from the end result.
  -s DIST, --dist DIST  DMC json color path.
  -z CELL_SIZE, --cell-size CELL_SIZE
                        The size of the generated Aida fabric cell.
  --no-cleanup          Don't run cleanup job on generated image.
  --svg                 Export result to svg files.
```
 

## Development
make sure to add the project to your `PYTHONPATH`

```shell
$ export PYTHONPATH="${PYTHONPATH}:/path/to/tarraz"
```