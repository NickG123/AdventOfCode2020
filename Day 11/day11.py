from __future__ import annotations

from enum import Enum
from typing import List, Optional, Set, TextIO

INPUT = "input"

NEIGHBOUR_VECTORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class SeatStatus(Enum):
    EMPTY = "L"
    FULL = "#"
    FLOOR = "."


class Cell:
    def __init__(self, status: str, x: int, y: int) -> None:
        self.status = SeatStatus(status)
        self.x = x
        self.y = y
        self.neighbours: List[Cell] = []

    @property
    def is_empty(self) -> bool:
        return self.status == SeatStatus.EMPTY

    @property
    def is_full(self) -> bool:
        return self.status == SeatStatus.FULL

    @property
    def is_floor(self) -> bool:
        return self.status == SeatStatus.FLOOR

    def toggle(self) -> None:
        if self.is_full:
            self.status = SeatStatus.EMPTY
        else:
            self.status = SeatStatus.FULL

    def compute_neighbours(self, grid: Grid, strict_adjacency: bool) -> None:
        for x_vector, y_vector in NEIGHBOUR_VECTORS:
            x_offset = 0
            y_offset = 0
            while True:
                x_offset += x_vector
                y_offset += y_vector

                point = grid.safe_get_point(self.x + x_offset, self.y + y_offset)
                if point is None:
                    break
                if not point.is_floor:
                    self.neighbours.append(point)
                    break
                if strict_adjacency:
                    break

    def __str__(self) -> str:
        return str(self.status.value)


class Grid:
    def __init__(self, fin: TextIO, strict_adjacency: bool, num_occupied_to_move: int) -> None:
        self.grid = [[Cell(val, x, y) for x, val in enumerate(line.strip())] for y, line in enumerate(fin)]
        self.num_occupied_to_move = num_occupied_to_move

        self.could_change = set()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                if not self.grid[y][x].is_floor:
                    self.grid[y][x].compute_neighbours(self, strict_adjacency)

                    self.could_change.add(self.grid[y][x])

    def safe_get_point(self, x: int, y: int) -> Optional[Cell]:
        if 0 <= y < len(self.grid):
            if 0 <= x < len(self.grid[y]):
                return self.grid[y][x]
        return None

    def step(self) -> bool:
        changes: List[Cell] = []
        new_could_change: Set[Cell] = set()
        for point in self.could_change:
            neighbours = point.neighbours
            if point.is_empty and not any(p.is_full for p in neighbours):
                changes.append(point)
            elif point.is_full and sum(p.is_full for p in neighbours) >= self.num_occupied_to_move:
                changes.append(point)
            else:
                continue
            new_could_change.update(neighbours)
            new_could_change.add(point)

        self.could_change = new_could_change
        for update in changes:
            update.toggle()
        return len(changes) > 0

    def num_occupied(self) -> int:
        return sum(p.is_full for row in self.grid for p in row)

    def __str__(self) -> str:
        return "\n".join("".join(str(x) for x in row) for row in self.grid) + "\n"


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
