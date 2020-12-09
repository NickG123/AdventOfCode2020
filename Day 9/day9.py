import itertools

from collections import deque
from typing import Collection, Iterator, OrderedDict

INPUT = "input"
WINDOW_SIZE = 25
ELASTIC_SUM_MIN_SIZE = 2


class SlidingWindowHashSet:
    def __init__(self, items: Iterator[int], window_size: int) -> None:
        self.items = items
        self.window = OrderedDict[int, None]((v, None) for v in itertools.islice(items, window_size))

    def slide(self) -> None:
        self.window.popitem(last=False)
        self.window[next(self.items)] = None


def two_sum(container: Collection[int], target: int) -> bool:
    for i in container:
        if target - i in container and 2 * i != target:
            return True
    return False


def find_elastic_sum(items: Iterator[int], target: int) -> Collection[int]:
    current_items = deque(itertools.islice(items, ELASTIC_SUM_MIN_SIZE))
    current_sum = sum(current_items)

    while current_sum != target:
        if current_sum > target and len(current_items) > ELASTIC_SUM_MIN_SIZE:
            current_sum -= current_items.popleft()
        else:
            new_item = next(items)
            current_items.append(new_item)
            current_sum += new_item

    return current_items


def input_generator() -> Iterator[int]:
    with open(INPUT, "r") as fin:
        for line in fin:
            yield int(line.strip())


def main() -> None:
    sliding_window_generator, iterable = itertools.tee(input_generator())
    sliding_window = SlidingWindowHashSet(sliding_window_generator, WINDOW_SIZE)

    for item in itertools.islice(iterable, WINDOW_SIZE, None):
        if not two_sum(sliding_window.window, item):
            part1 = item
            break
        sliding_window.slide()

    print(part1)
    elastic_sum = find_elastic_sum(input_generator(), part1)
    print(min(elastic_sum) + max(elastic_sum))


if __name__ == "__main__":
    main()
