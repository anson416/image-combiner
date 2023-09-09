import argparse
import math
from typing import List, Optional, Tuple, Union

from PIL import Image, ImageOps


def combine_images(
    img_paths: Union[List[str], Tuple[str, ...]],
    n_rows: Optional[int] = None,
    n_cols: Optional[int] = None,
    resize: bool = False,
    fill: bool = False,
    background: Tuple[int, int, int] = (0, 0, 0),
    cell_width: Optional[int] = None,
    cell_height: Optional[int] = None,
    output_path: Optional[str] = None,
    show: bool = False,
) -> Image.Image:
    """
    Combine images in grid.

    Args:
        img_paths (Union[List[str], Tuple[str, ...]]): Paths to images to be combined
        n_rows (Optional[int], optional): Number of rows in the grid. Defaults to None.
        n_cols (Optional[int], optional): Number of columns in the grid. Defaults to None.
        resize (bool, optional): If True, resize each image to match at least one dimension of a cell's size. Defaults to False.
        fill (bool, optional): If True, crop each image to fill an entire cell. Defaults to False.
        background (Tuple[int, int, int], optional): Background color (RGB). Defaults to (0, 0, 0).
        cell_width (Optional[int], optional): Width of each cell in the grid. Defaults to None.
        cell_height (Optional[int], optional): Height of each cell in the grid. Defaults to None.
        output_path (Optional[str], optional): If not None, the combined image will be saved as `output_path`. Defaults to None.
        show (bool, optional): If True, show the combined image. Defaults to False.

    Returns:
        PIL.Image.Image: The combined image

    Raises:
        AssertionError: Raise if `n_rows` is not None and `n_rows` <= 0
        AssertionError: Raise if `n_cols` is not None and `n_cols` <= 0
        AssertionError: Raise if both `n_rows` and `n_cols` are not None and `n_rows` * `n_cols` < len(`img_paths`)
        AssertionError: Raise if any value in `background` is not in [0, 255]
        AssertionError: Raise if `cell_width` is not None and `cell_width` <= 0
        AssertionError: Raise if `cell_height` is not None and `cell_height` <= 0
    """

    # Check arguments
    if n_rows:
        assert n_rows > 0, "`n_rows` must be positive integer"
    if n_cols:
        assert n_cols > 0, "`n_cols` must be positive integer"
    if n_rows and n_cols:
        assert n_rows * n_cols >= len(img_paths), "# of cells (`n_rows` * `n_cols`) must be no less than # of images"
    for color in background:
        assert 0 <= color <= 255, "Each value in background (RGB) must be an integer in [0, 255]"
    if cell_width:
        assert cell_width > 0, "`cell_width` must be a positive integer"
    if cell_height:
        assert cell_height > 0, "`cell_height` must be a positive integer"

    # Read images from `img_paths` and store them to a list called `images`
    images = [Image.open(img) for img in img_paths]

    # Compute `n_rows` and/or `n_cols`
    if not (n_rows or n_cols):
        n_rows = n_cols = math.ceil(math.sqrt(len(images)))
    elif n_cols and not n_rows:
        n_rows = math.ceil(len(img_paths) / n_cols)
    elif n_rows and not n_cols:
        n_cols = math.ceil(len(img_paths) / n_rows)

    # Compute `cell_width` and/or `cell_height`
    cell_width = max([img.size[0] for img in images]) if not cell_width else cell_width
    cell_height = max([img.size[1] for img in images]) if not cell_height else cell_height

    # Create a new blank image called `output_img`
    output_img = Image.new("RGB", (n_cols * cell_width, n_rows * cell_height), background)

    # Paste all images in `images` into `output_img`
    for idx, img in enumerate(images):
        # Resize image
        if fill:
            img = ImageOps.fit(img, (cell_width, cell_height))
        elif resize or (img.size[0] > cell_width or img.size[1] > cell_height):
            img = ImageOps.contain(img, (cell_width, cell_height))
        
        # Paste image in the center of the cell
        width, height = img.size
        x = (idx % n_cols) * cell_width + (cell_width - width) // 2
        y = (idx // n_cols) * cell_height + (cell_height - height) // 2
        output_img.paste(img, (x, y, x + width, y + height))

    # Save the combined image
    if output_path:
        output_img.save(output_path)

    # Show the combined image
    if show:
        output_img.show()

    return output_img


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        description="Combine images in grid.",
    )
    parser.add_argument(
        "img_paths", type=str, nargs="+",
        help="Paths to images to be combined",
    )
    parser.add_argument(
        "-nr", "--n_rows", default=None, type=int,
        help="Number of rows in the grid",
    )
    parser.add_argument(
        "-nc", "--n_cols", default=None, type=int,
        help="Number of columns in the grid",
    )
    parser.add_argument(
        "-r", "--resize", action="store_true",
        help="Resize each image to match at least one dimension of a cell's size",
    )
    parser.add_argument(
        "-f", "--fill", action="store_true",
        help="Crop each image to fill an entire cell",
    )
    parser.add_argument(
        "-b", "--background", default=(0, 0, 0), type=int, nargs=3,
        help="Background color (RGB)",
    )
    parser.add_argument(
        "-cw", "--cell_width", default=None, type=int,
        help="Width of each cell in the grid",
    )
    parser.add_argument(
        "-ch", "--cell_height", default=None, type=int,
        help="Height of each cell in the grid",
    )
    parser.add_argument(
        "-o", "--output_path", default=None, type=str,
        help="Output path of the combined image",
    )
    parser.add_argument(
        "-s", "--show", action="store_true",
        help="Show the combined image",
    )
    args = parser.parse_args()

    combine_images(
        args.img_paths,
        n_rows=args.n_rows,
        n_cols=args.n_cols,
        resize=args.resize,
        fill=args.fill,
        background=tuple(args.background),
        cell_width=args.cell_width,
        cell_height=args.cell_height,
        output_path=args.output_path,
        show=args.show,
    )
