from __future__ import annotations

import re

from typing import Dict, Iterable

INPUT = "input"
MY_BAG = "shiny gold"
BAG_REGEX = re.compile(r"^(?P<color>.*) bags contain (?P<contents>.*)\.$")
CONTENTS_REGEX = re.compile(r"^(?P<number>\d*) (?P<color>.*) bags?$")


class Bag:
    def __init__(self, description: str):
        match = BAG_REGEX.match(description)
        assert match is not None
        self.color = match.group("color")
        self.contents: Dict[str, int] = {}
        if match.group("contents") != "no other bags":
            for contents in match.group("contents").split(", "):
                contents_match = CONTENTS_REGEX.match(contents)
                assert contents_match is not None
                self.contents[contents_match.group("color")] = int(contents_match.group("number"))

        self._contains_my_bag = None
        self._total_bags = None

    def contains_my_bag(self, bag_lookup: Dict[str, Bag]) -> bool:
        if self._contains_my_bag is not None:
            return self._contains_my_bag

        if MY_BAG in self.contents:
            return True

        return any(bag_lookup[content].contains_my_bag(bag_lookup) for content in self.contents)

    def total_bags(self, bag_lookup: Dict[str, Bag]) -> int:
        if self._total_bags is not None:
            return self._total_bags

        return sum(num * (1 + bag_lookup[content].total_bags(bag_lookup)) for content, num in self.contents.items())


def read_bags() -> Iterable[Bag]:
    with open(INPUT, "r") as fin:
        for line in fin:
            yield Bag(line.strip())


def main() -> None:
    bag_lookup = {bag.color: bag for bag in read_bags()}

    print(sum(bag.contains_my_bag(bag_lookup) for bag in bag_lookup.values()))
    print(bag_lookup[MY_BAG].total_bags(bag_lookup))


if __name__ == "__main__":
    main()
