import functools
import itertools
from collections import Counter
from typing import Iterable, List, Optional, Tuple

INPUT = "input"
SORT_SIZE = 200


def pidgeonhole_sort(iterable: Iterable[int], size: int) -> List[int]:
    holes: List[Optional[int]] = [None] * size
    for adapter in iterable:
        holes[adapter] = adapter

    return [v for v in holes if v is not None]


def read_input() -> Iterable[int]:
    with open(INPUT, "r") as fin:
        for line in fin:
            yield int(line)


@functools.lru_cache(maxsize=None)
def num_combinations(current_adapter: int, list_remainder: Tuple[int]) -> int:
    if len(list_remainder) == 0:
        return 1
    combinations = 0
    for i, adapter in enumerate(list_remainder):
        if adapter - current_adapter < 4:
            combinations += num_combinations(adapter, list_remainder[i + 1:])
    return combinations


def main() -> None:
    adapters = pidgeonhole_sort(read_input(), SORT_SIZE)

    all_diffs = itertools.chain(
        [3, adapters[0]],
        (next_elem - elem for elem, next_elem in zip(adapters, adapters[1:]))
    )
    counter = Counter(all_diffs)
    print(counter[1] * counter[3])
    print(num_combinations(0, tuple(adapters)))


if __name__ == "__main__":
    main()
