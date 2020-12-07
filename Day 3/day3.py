from __future__ import annotations
from dataclasses import dataclass
from typing import TextIO

INPUT = "input"
TREE = "#"


@dataclass
class Pair:
    x: int
    y: int

    def __iadd__(self, other: Pair) -> Pair:
        self.x += other.x
        self.y += other.y
        return self


class Grid:
    def __init__(self, fin: TextIO):
        self.grid = [line.strip() for line in fin]
        self.width = len(self.grid[0])
        self.height = len(self.grid)

    def get_point(self, point: Pair) -> str:
        return self.grid[point.y][point.x % self.width]

    def is_tree(self, point: Pair) -> bool:
        return self.get_point(point) == TREE


def main() -> None:
    with open(INPUT, "r") as fin:
        grid = Grid(fin)

    vectors = [Pair(1, 1), Pair(3, 1), Pair(5, 1), Pair(7, 1), Pair(1, 2)]
    tree_product = 1
    for vector in vectors:
        position = Pair(0, 0)
        trees = 0
        while position.y < grid.height:
            if grid.is_tree(position):
                trees += 1
            position += vector

        if vector == Pair(3, 1):
            print(trees)
        tree_product *= trees
    print(tree_product)


if __name__ == "__main__":
    main()
