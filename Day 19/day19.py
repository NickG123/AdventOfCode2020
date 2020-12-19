import regex as re
from functools import lru_cache
from typing import Any, Dict, TextIO

INPUT = "input"


def read_rules(fin: TextIO) -> Dict[int, str]:
    result = {}
    for line in fin:
        if not line.strip():
            break
        rule_num, rule_str = line.strip().split(": ")
        result[int(rule_num)] = rule_str
    return result


def parse_rule(rule: str, rules: Dict[int, str], part2: bool) -> Any:
    @lru_cache(None)
    def parse_rule_helper(rule: str) -> str:
        if part2:
            if rule == "8":
                return f"{parse_rule_helper('42')}+"
            if rule == "11":
                return f"(?P<name>{parse_rule_helper('42')}(?&name)?{parse_rule_helper('31')})"

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

        p1 = parse_rule(rules[0], rules, False)
        p2 = parse_rule(rules[0], rules, True)
        p1_total = 0
        p2_total = 0
        for line in fin:
            if p1.fullmatch(line.strip()):
                p1_total += 1
            if p2.fullmatch(line.strip()):
                p2_total += 1

        print(p1_total)
        print(p2_total)


if __name__ == "__main__":
    main()
