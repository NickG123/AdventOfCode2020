from __future__ import annotations
from collections import defaultdict
from math import sqrt
from typing import Callable, Dict, Iterator, List, TextIO

INPUT = "input"
MONSTER_STR = [
    "                  # ",
    "#    ##    ##    ###",
    " #  #  #  #  #  #   "
]
MONSTER = [(x, y) for y, line in enumerate(MONSTER_STR) for x, s in enumerate(line) if s == '#']


def flip_image_horizontal(img: List[str]) -> List[str]:
    return [line[::-1] for line in img]


def flip_image_vertical(img: List[str]) -> List[str]:
    return img[::-1]


def rotate_image(img: List[str]) -> List[str]:
    return ["".join(row) for row in zip(*img[::-1])]


def all_image_combinations(img: List[str]) -> Iterator[List[str]]:
    for rotated in [False, True]:
        if rotated:
            img = rotate_image(img)
        for hflipped in [False, True]:
            if hflipped:
                img = flip_image_horizontal(img)
            for vflipped in [False, True]:
                if vflipped:
                    img = flip_image_vertical(img)
                yield img


class Tile:
    def __init__(self, tile_id: int, grid: List[str]) -> None:
        self.tile_id = tile_id
        self.grid = grid

    def get_row(self, index: int) -> str:
        return self.grid[index]

    def get_col(self, index: int) -> str:
        return "".join(row[index] for row in self.grid)

    def flip_horizontal(self) -> None:
        self.grid = flip_image_horizontal(self.grid)

    def flip_vertical(self) -> None:
        self.grid = flip_image_vertical(self.grid)

    def rotate(self) -> None:
        self.grid = rotate_image(self.grid)

    def make_match(self, border: str, getter: Callable[[Tile], str]) -> None:
        for opt in all_image_combinations(self.grid):
            self.grid = opt
            if border == getter(self):
                return

    def make_top_match(self, border: str) -> None:
        self.make_match(border, lambda s: s.get_row(0))

    def make_left_match(self, border: str) -> None:
        self.make_match(border, lambda s: s.get_col(0))

    def without_borders(self) -> List[str]:
        return [row[1: -1] for row in self.grid[1: -1]]

    def get_borders(self) -> List[str]:
        return [
            self.get_row(0),
            self.get_row(-1),
            self.get_col(0),
            self.get_col(-1),
            self.get_row(0)[::-1],
            self.get_row(-1)[::-1],
            self.get_col(0)[::-1],
            self.get_col(-1)[::-1]
        ]

    def __str__(self) -> str:
        grid = "\n".join(self.grid)
        return f"Tile {self.tile_id}:\n{grid}\n"


def parse_tiles(fin: TextIO) -> Iterator[Tile]:
    for header_line in fin:
        tile_id = int(header_line.split(" ")[-1].strip(":\n"))
        grid = []
        for line in fin:
            if not line.strip():
                break
            grid.append(line.strip())
        yield Tile(tile_id, grid)


def stitch_tiles(corner: Tile, side_size: int, tiles_by_border: Dict[str, List[Tile]]) -> List[str]:
    grid = {}

    def populate_cell(x: int, y: int, tile: Tile) -> None:
        grid[(x, y)] = tile.without_borders()
        if x + 1 < side_size and grid.get((x + 1, y)) is None:
            border = tile.get_col(-1)
            [neighbour] = {n for n in tiles_by_border[border] if n != tile}
            neighbour.make_left_match(border)
            populate_cell(x + 1, y, neighbour)
        if y + 1 < side_size and grid.get((x, y + 1)) is None:
            border = tile.get_row(-1)
            [neighbour] = {n for n in tiles_by_border[border] if n != tile}
            neighbour.make_top_match(border)
            populate_cell(x, y + 1, neighbour)

    if len(tiles_by_border[corner.get_col(-1)]) == 1:
        corner.flip_horizontal()
    if len(tiles_by_border[corner.get_row(-1)]) == 1:
        corner.flip_vertical()

    populate_cell(0, 0, corner)
    cell_size = len(grid[(0, 0)])

    result = []
    for vcell_num in range(side_size):
        for cell_row_num in range(cell_size):
            result.append("".join(grid[(hcell_num, vcell_num)][cell_row_num] for hcell_num in range(side_size)))
    return result


def find_monsters(img: List[str]) -> int:
    img_size = len(img)
    monster_width = len(MONSTER_STR[0])
    monster_height = len(MONSTER_STR)
    x_offsets = range(img_size - monster_width + 1)
    y_offsets = range(img_size - monster_height + 1)
    monster_positions = set()

    for opt in all_image_combinations(img):
        for x_offset in x_offsets:
            for y_offset in y_offsets:
                monster_offsets = [(x + x_offset, y + y_offset) for x, y in MONSTER]
                if all(opt[y][x] == "#" for x, y in monster_offsets):
                    monster_positions.update(monster_offsets)
        if monster_positions:
            return sum(opt[y][x] == "#" for y in range(img_size) for x in range(img_size)) - len(monster_positions)
    raise Exception("No monsters found")


def main() -> None:
    with open(INPUT, "r") as fin:
        all_tiles = list(parse_tiles(fin))

    tiles_by_border: Dict[str, List[Tile]] = defaultdict(list)
    for tile in all_tiles:
        for border in tile.get_borders():
            tiles_by_border[border].append(tile)

    corner_tiles_product = 1
    corner = None
    for tile in all_tiles:
        neighbours = set(matching_tile for border in tile.get_borders() for matching_tile in tiles_by_border[border] if matching_tile != tile)
        if len(neighbours) == 2:
            corner = tile
            corner_tiles_product *= tile.tile_id
    print(corner_tiles_product)

    assert corner is not None

    stitched = stitch_tiles(corner, int(sqrt(len(all_tiles))), tiles_by_border)
    print(find_monsters(stitched))


if __name__ == "__main__":
    main()
