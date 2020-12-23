import itertools
from typing import List, Iterable


class Cups:
    def __init__(self, data: List[int]) -> None:
        self.cups = [0] * (len(data) + 1)
        self.current_cup = data[0]
        self.max_val = len(data)
        for val, next_val in zip(data, data[1:]):
            self.cups[val] = next_val
        self.cups[data[-1]] = self.current_cup

    def run(self, num_moves: int) -> None:
        for _ in range(num_moves):
            cup1 = self.cups[self.current_cup]
            cup2 = self.cups[cup1]
            cup3 = self.cups[cup2]

            destination = self.current_cup
            while destination in {self.current_cup, cup1, cup2, cup3}:
                destination -= 1
                if destination == 0:
                    destination = self.max_val

            new_current_cup = self.cups[cup3]
            self.cups[self.current_cup] = new_current_cup
            self.cups[cup3] = self.cups[destination]
            self.cups[destination] = cup1
            self.current_cup = new_current_cup

    def get_cups(self, starting_point: int) -> Iterable[int]:
        cup = self.cups[starting_point]
        while cup != starting_point:
            yield cup
            cup = self.cups[cup]

    def __str__(self) -> str:
        return f"{self.current_cup} {' '.join(str(x) for x in self.get_cups(self.current_cup))}"


def main() -> None:
    cups = Cups([2, 4, 7, 8, 1, 9, 3, 5, 6])
    cups.run(100)
    print("".join(str(x) for x in cups.get_cups(1)))

    part2_cups = Cups([2, 4, 7, 8, 1, 9, 3, 5, 6] + list(range(10, 1000001)))
    part2_cups.run(10000000)
    cup1, cup2 = itertools.islice(part2_cups.get_cups(1), 2)
    print(cup1 * cup2)


if __name__ == "__main__":
    main()
