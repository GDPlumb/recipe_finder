#!/usr/bin/env python3
"""Sample this week's ingredient pool and print an LLM prompt for finding recipes.

Draws a weighted-random pool (without replacement) from ingredients/ using the sizes in
config.yaml, then renders prompt_template.md to stdout. Paste the result into a Claude web
session with web search enabled.
"""
from pathlib import Path
import random

import yaml

ROOT = Path(__file__).resolve().parent
INGREDIENTS_DIR = ROOT / "ingredients"


def load_items(category):
    """Load ingredients/<category>.yaml as a list of {name, weight} records."""
    data = yaml.safe_load((INGREDIENTS_DIR / f"{category}.yaml").read_text())
    if not isinstance(data, list):
        raise ValueError(f"ingredients/{category}.yaml should be a flat list of items")
    return data


def weighted_sample(items, k):
    """Pick k distinct names by weight (weighted sampling without replacement)."""
    pool = [(i["name"], float(i["weight"])) for i in items]
    chosen = []
    for _ in range(min(k, len(pool))):
        idx = random.choices(range(len(pool)), weights=[w for _, w in pool], k=1)[0]
        chosen.append(pool.pop(idx)[0])
    return chosen


def main():
    cfg = yaml.safe_load((ROOT / "config.yaml").read_text())
    pool = cfg["pool"]
    fields = dict(
        proteins=", ".join(weighted_sample(load_items("proteins"), pool["proteins"])),
        vegetables=", ".join(weighted_sample(load_items("vegetables"), pool["vegetables"])),
        cuisines=", ".join(weighted_sample(load_items("cuisines"), pool["cuisines"])),
        legumes=", ".join(weighted_sample(load_items("legumes"), cfg["legume_options"])),
        fruits=", ".join(weighted_sample(load_items("fruits"), cfg["dessert_options"])),
        dinner_candidates=cfg["dinner_candidates"],
        target_dinners=cfg["target_dinners"],
    )
    template = (ROOT / "prompt_template.md").read_text()
    print(template.format(**fields))


if __name__ == "__main__":
    main()
