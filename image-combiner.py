import argparse
import math
from typing import Optional, Union

from PIL import Image, ImageOps


def combine_images(
    img_paths: Union[list[str], tuple[str]],
    n_rows: Optional[int] = None,
    n_cols: Optional[int] = None,
    resize: bool = False,
    fill: bool = False,
    background: Union[list[int], tuple[int]] = (0, 0, 0),
    cell_size: Optional[Union[list[int], tuple[int]]] = None,
    output_path: Optional[str] = None,
    show: bool = False,
) -> Image.Image:
    assert n_rows or n_cols, "n_rows and n_cols cannot be both None"
    if n_rows:
        assert n_rows > 0, "n_rows must be positive integer"
    if n_cols:
        assert n_cols > 0, "n_cols must be positive integer"
    if n_rows and n_cols:
        assert n_rows * n_cols >= len(img_paths), "# of cells (n_rows * n_cols) must be no less than # of images"
    for color in background:
        assert 0 <= color <= 255, "Each value in background (RGB) must be in [0, 255]"
    if cell_size:
        for size in cell_size:
            assert size > 0, "Each value in cell_size (width, height) must be positive integers"

    images = [Image.open(img) for img in img_paths]
    nc = math.ceil(len(img_paths) / n_rows) if n_rows and not n_cols else n_cols
    nr = math.ceil(len(img_paths) / n_cols) if n_cols and not n_rows else n_rows
    cell_width = cell_size[0] if cell_size else max([img.size[0] for img in images])
    cell_height = cell_size[1] if cell_size else max([img.size[1] for img in images])
    output_img = Image.new("RGB", (nc * cell_width, nr * cell_height), background)

    for idx, img in enumerate(images):
        if resize:
            if fill:
                img = ImageOps.fit(img, (cell_width, cell_height))
            else:
                img = ImageOps.contain(img, (cell_width, cell_height))
        width, height = img.size
        x = (idx % nc) * cell_width + (cell_width - width) // 2
        y = (idx // nc) * cell_height + (cell_height - height) // 2
        output_img.paste(img, (x, y, x + width, y + height))

    if output_path:
        output_img.save(output_path)
    if show:
        output_img.show()

    return output_img


# imgs = [
#     "images/Lycoris_Teaser_1500x2080.jpg",
#     "images/Lycoris_Twitter_01_1000x994.jpg",
#     "images/Lycoris_Twitter_04_1000x707.jpg",
#     "images/Lycoris_Twitter_05_676x1000.jpg",
#     "images/Lycoris_Twitter_06_1000x707.jpg",
# ]
# combine(imgs, 2, 2, cell_size=(2000, 2000), fill=True, output_path="output.jpeg")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Combine images in grid.")
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
        help="Crop each image to fill an entire cell (used only when resize is True)",
    )
    parser.add_argument(
        "-b", "--background", default=(0, 0, 0), type=int, nargs=3,
        help="Background color (RGB)",
    )
    parser.add_argument(
        "-cs", "--cell_size", default=None, type=int, nargs=2,
        help="Size (width, height) of each cell",
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
        background=args.background,
        cell_size=args.cell_size,
        output_path=args.output_path,
        show=args.show,
    )
