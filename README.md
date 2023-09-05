# Image Combiner

Combine images in grid.

## Usage

### Python

```python
combine_images(
    img_paths,
    n_rows=None,
    n_cols=None,
    resize=False,
    fill=False,
    background=(0, 0, 0),
    cell_size=None,
    output_path=None,
    show=False,
)
```

### CLI

```text
python image-combiner.py [-h] [-nr N_ROWS] [-nc N_COLS] [-r] [-f] [-b BACKGROUND BACKGROUND BACKGROUND] [-cs CELL_SIZE CELL_SIZE] [-o OUTPUT_PATH] [-s]
                         img_paths [img_paths ...]

Combine images in grid.

positional arguments:
  img_paths             Paths to images to be combined

options:
  -h, --help            show this help message and exit
  -nr N_ROWS, --n_rows N_ROWS
                        Number of rows in the grid
  -nc N_COLS, --n_cols N_COLS
                        Number of columns in the grid
  -r, --resize          Resize each image to match at least one dimension of a cell's size
  -f, --fill            Crop each image to fill an entire cell (used only when resize is True)
  -b BACKGROUND BACKGROUND BACKGROUND, --background BACKGROUND BACKGROUND BACKGROUND
                        Background color (RGB)
  -cs CELL_SIZE CELL_SIZE, --cell_size CELL_SIZE CELL_SIZE
                        Size (width, height) of each cell
  -o OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output path of the combined image
  -s, --show            Show the combined image
```
