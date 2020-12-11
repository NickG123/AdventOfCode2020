from __future__ import annotations

from typing import Iterable, List, Optional, TextIO

INPUT = "input"
EMPTY = "L"
FULL = "#"

NEIGHBOUR_VECTORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Grid:
    def __init__(self, fin: TextIO, strict_adjacency: bool, num_occupied_to_move: int) -> None:
        self.grid = [line.strip() for line in fin]
        self.strict_adjacency = strict_adjacency
        self.num_occupied_to_move = num_occupied_to_move

    def safe_get_point(self, x: int, y: int) -> Optional[str]:
        if 0 <= y < len(self.grid):
            if 0 <= x < len(self.grid[y]):
                return self.grid[y][x]
        return None

    def neighbours(self, x: int, y: int) -> Iterable[str]:
        for x_vector, y_vector in NEIGHBOUR_VECTORS:
            x_offset = 0
            y_offset = 0
            while True:
                x_offset += x_vector
                y_offset += y_vector

                point = self.safe_get_point(x + x_offset, y + y_offset)
                if point is None:
                    break
                if point != '.':
                    yield point
                    break
                if self.strict_adjacency:
                    break

    def step(self) -> bool:
        new_grid = []
        changed = False
        for y in range(len(self.grid)):
            new_row: List[str] = []
            for x in range(len(self.grid[y])):
                point = self.grid[y][x]
                neighbours = self.neighbours(x, y)
                if point == EMPTY and not any(p == FULL for p in neighbours):
                    changed = True
                    new_row.append(FULL)
                elif point == FULL and sum(p == FULL for p in neighbours) >= self.num_occupied_to_move:
                    changed = True
                    new_row.append(EMPTY)
                else:
                    new_row.append(point)

            new_grid.append("".join(new_row))
        self.grid = new_grid
        return changed

    def num_occupied(self) -> int:
        return sum(p == FULL for row in self.grid for p in row)

    def __str__(self) -> str:
        return "\n".join(self.grid) + "\n"


def main() -> None:
    with open(INPUT, "r") as fin:
        part_1_grid = Grid(fin, True, 4)
    with open(INPUT, "r") as fin:
        part_2_grid = Grid(fin, False, 5)

    while part_1_grid.step():
        pass

    while part_2_grid.step():
        pass

    print(part_1_grid.num_occupied())
    print(part_2_grid.num_occupied())


if __name__ == "__main__":
    main()
