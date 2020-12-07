import re

from dataclasses import dataclass
from typing import Dict, Iterable, Pattern, Union


@dataclass
class RangeValidator:
    min: int
    max: int

    def validate(self, contents: str) -> bool:
        try:
            return self.min <= int(contents) <= self.max
        except ValueError:
            return False


class HeightValidator:
    subvalidators = [
        ("in", RangeValidator(59, 76)),
        ("cm", RangeValidator(150, 193))
    ]

    def validate(self, contents: str) -> bool:
        for ending, validator in HeightValidator.subvalidators:
            if contents.endswith(ending):
                return validator.validate(contents[:-len(ending)])
        return False


@dataclass
class RegexValidator:
    regex: Pattern[str]

    def validate(self, contents: str) -> bool:
        return self.regex.match(contents) is not None


INPUT = "input"
REQUIRED_FIELDS: Dict[str, Union[RangeValidator, HeightValidator, RegexValidator]] = {
    "byr": RangeValidator(1920, 2002),
    "iyr": RangeValidator(2010, 2020),
    "eyr": RangeValidator(2020, 2030),
    "hgt": HeightValidator(),
    "hcl": RegexValidator(re.compile(r"^#[0-9a-f]{6}$")),
    "ecl": RegexValidator(re.compile(r"^(amb|blu|brn|gry|grn|hzl|oth)$")),
    "pid": RegexValidator(re.compile(r"^\d{9}$"))
}


def parse_passport_line(line: str) -> Dict[str, str]:
    return dict(field.split(":") for field in line.split(" "))


def is_valid(passport: Dict[str, str]) -> bool:
    return all(k in passport for k in REQUIRED_FIELDS)


def is_valid_part_2(passport: Dict[str, str]) -> bool:
    return all(validator.validate(passport[key]) for (key, validator) in REQUIRED_FIELDS.items())


def read_passports() -> Iterable[Dict[str, str]]:
    passport = {}
    with open(INPUT, "r") as fin:
        for line in (line.strip() for line in fin):
            if line:
                passport.update(parse_passport_line(line))
            else:
                yield passport
                passport = {}
    if passport:
        yield passport


def main() -> None:
    valid_passports = 0
    valid_passports_part_2 = 0

    for passport in read_passports():
        if is_valid(passport):
            valid_passports += 1
            if is_valid_part_2(passport):
                valid_passports_part_2 += 1

    print(valid_passports)
    print(valid_passports_part_2)


if __name__ == "__main__":
    main()
