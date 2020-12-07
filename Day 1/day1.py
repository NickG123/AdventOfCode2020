from typing import Iterator, Optional

TARGET = 2020
INPUT = "input"


def for_int_in_file() -> Iterator[int]:
    with open(INPUT, "r") as fin:
        for line in fin:
            yield int(line)


def part1(target: int) -> Optional[int]:
    found_numbers = set()
    for val in for_int_in_file():
        if target - val in found_numbers:
            return val * (target - val)
        found_numbers.add(val)
    return None


def part2() -> Optional[int]:
    for val in for_int_in_file():
        result = part1(TARGET - val)
        if result is not None:
            return val * result
    return None


if __name__ == "__main__":
    print(part1(TARGET))
    print(part2())
