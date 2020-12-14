from typing import Dict, List

INPUT = "input"


class BitmaskWriter:
    def __init__(self) -> None:
        self.override = 0
        self.mask = 0
        self.memory: Dict[int, int] = {}

    def update_mask(self, new_mask: str) -> None:
        self.override = 0
        self.mask = 0
        for i, c in enumerate(reversed(new_mask)):
            if c != "X":
                self.override |= int(c) << i
            else:
                self.mask |= 1 << i

    def write_value(self, address: int, value: int) -> None:
        self.memory[address] = (value & self.mask) | self.override

    def find_write_addresses(self, curr_address: int, mask: int, offset: int) -> List[int]:
        if offset < 0:
            return [curr_address]
        if mask & 1 << offset:
            result = []
            result.extend(self.find_write_addresses(curr_address, mask, offset - 1))
            result.extend(self.find_write_addresses(curr_address ^ 1 << offset, mask, offset - 1))
            return result
        else:
            return self.find_write_addresses(curr_address, mask, offset - 1)

    def write_value_part_2(self, address: int, value: int) -> None:
        for address in self.find_write_addresses(address | self.override, self.mask, 36):
            self.memory[address] = value


def main() -> None:
    writer = BitmaskWriter()
    part2 = BitmaskWriter()
    with open(INPUT, "r") as fin:
        for line in fin:
            target, arg = line.strip().split(" = ")
            if target == "mask":
                writer.update_mask(arg)
                part2.update_mask(arg)
            else:
                addr = int(target[4:-1])
                writer.write_value(addr, int(arg))
                part2.write_value_part_2(addr, int(arg))
    print(sum(writer.memory.values()))
    print(sum(part2.memory.values()))


if __name__ == "__main__":
    main()
