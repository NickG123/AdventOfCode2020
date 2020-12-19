import re
from functools import lru_cache
from typing import Dict, Pattern, TextIO

INPUT = "input"


def read_rules(fin: TextIO) -> Dict[int, str]:
    result = {}
    for line in fin:
        if not line.strip():
            break
        rule_num, rule_str = line.strip().split(": ")
        result[int(rule_num)] = rule_str
    return result


def parse_rule(rule: str, rules: Dict[int, str]) -> Pattern[str]:
    @lru_cache(None)
    def parse_rule_helper(rule: str) -> str:
        if rule.startswith('"'):
            return rule.strip('"')
        if "|" in rule:
            left_rule, right_rule = rule.split("|")
            return f"({parse_rule_helper(left_rule.strip())}|{parse_rule_helper(right_rule.strip())})"
        if " " in rule:
            return "".join(parse_rule_helper(x.strip()) for x in rule.split(" "))
        return parse_rule_helper(rules[int(rule)])

    return re.compile(parse_rule_helper(rule))


def main() -> None:
    with open(INPUT, "r") as fin:
        rules = read_rules(fin)

        rule_0 = parse_rule(rules[0], rules)
        print(sum(rule_0.fullmatch(line.strip()) is not None for line in fin))


if __name__ == "__main__":
    main()
