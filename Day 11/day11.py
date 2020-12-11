from __future__ import annotations

from typing import Iterable, List, Optional, Set, TextIO, Tuple

INPUT = "input"
EMPTY = "L"
FULL = "#"

NEIGHBOUR_VECTORS = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]


class Grid:
    def __init__(self, fin: TextIO, strict_adjacency: bool, num_occupied_to_move: int) -> None:
        self.grid = [list(line.strip()) for line in fin]
        self.strict_adjacency = strict_adjacency
        self.num_occupied_to_move = num_occupied_to_move

        self.could_change: Set[Tuple[int, int]] = set()
        for y in range(len(self.grid)):
            for x in range(len(self.grid[y])):
                self.could_change.add((x, y))

    def safe_get_point(self, x: int, y: int) -> Optional[str]:
        if 0 <= y < len(self.grid):
            if 0 <= x < len(self.grid[y]):
                return self.grid[y][x]
        return None

    def neighbours(self, x: int, y: int) -> Iterable[Tuple[str, int, int]]:
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
                    yield point, x + x_offset, y + y_offset
                    break
                if self.strict_adjacency:
                    break

    def step(self) -> bool:
        changes: List[Tuple[str, int, int]] = []
        new_could_change: Set[Tuple[int, int]] = set()
        for (x, y) in self.could_change:
            point = self.grid[y][x]
            neighbours = list(self.neighbours(x, y))
            if point == EMPTY and not any(p == FULL for p, nx, ny in neighbours):
                changes.append((FULL, x, y))
            elif point == FULL and sum(p == FULL for p, nx, ny in neighbours) >= self.num_occupied_to_move:
                changes.append((EMPTY, x, y))
            else:
                continue
            new_could_change.update((x, y) for p, x, y in neighbours)
            new_could_change.add((x, y))

        self.could_change = new_could_change
        for update, x, y in changes:
            self.grid[y][x] = update
        return len(changes) > 0

    def num_occupied(self) -> int:
        return sum(p == FULL for row in self.grid for p in row)

    def __str__(self) -> str:
        return "\n".join("".join(row) for row in self.grid) + "\n"


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
