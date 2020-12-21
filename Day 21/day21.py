from collections import Counter
from dataclasses import dataclass
from typing import Dict, Iterable, List, Set

INPUT = "input"


@dataclass
class Food:
    ingredients: List[str]
    allergens: List[str]


def read_foods() -> Iterable[Food]:
    with open(INPUT, "r") as fin:
        for line in fin:
            ingredients, allergens = line.strip().strip(")").split(" (contains ")
            yield Food(ingredients.split(" "), allergens.split(", "))


def remove_food_possibility(allergen: str, possible_allergens: Dict[str, Set[str]]) -> None:
    [containing_food] = possible_allergens[allergen]
    for other_allergen, foods in possible_allergens.items():
        if other_allergen == allergen:
            continue
        if containing_food in foods:
            foods.remove(containing_food)
            if len(foods) == 1:
                remove_food_possibility(other_allergen, possible_allergens)


def main() -> None:
    ingredient_counts: Dict[str, int] = Counter()
    possible_allergens = {}
    for food in read_foods():
        ingredient_counts.update(food.ingredients)
        for allergen in food.allergens:
            if allergen not in possible_allergens:
                possible_allergens[allergen] = set(food.ingredients)
            else:
                possible_allergens[allergen] &= set(food.ingredients)
            if len(possible_allergens[allergen]) == 1:
                remove_food_possibility(allergen, possible_allergens)

    all_possible_allergenic_foods = {ingredient for ingredients in possible_allergens.values() for ingredient in ingredients}
    print(sum(count for ingredient, count in ingredient_counts.items() if ingredient not in all_possible_allergenic_foods))
    print(",".join(food for allergen, [food] in sorted(possible_allergens.items())))


if __name__ == "__main__":
    main()
