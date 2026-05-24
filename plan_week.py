#!/usr/bin/env python3
"""Sample this week's ingredient pool and print an LLM prompt for finding recipes.

Draws a weighted-random pool from ingredients/ (sizes in config.yaml), folds in a digest of past
recipes from recipes/, and renders prompt_template.md to stdout. Paste the result into a Claude
web session with web search enabled.
"""
from datetime import date
from pathlib import Path
import random

import yaml

ROOT = Path(__file__).resolve().parent
INGREDIENTS_DIR = ROOT / "ingredients"
RECIPES_DIR = ROOT / "recipes"
TEMPLATE_FILE = RECIPES_DIR / "_TEMPLATE.md"


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


def read_recipes():
    """Parse the YAML frontmatter of every recipes/*.md (skipping _TEMPLATE.md)."""
    out = []
    if not RECIPES_DIR.exists():
        return out
    for path in sorted(RECIPES_DIR.glob("*.md")):
        if path.name.startswith("_"):
            continue
        text = path.read_text()
        if not text.startswith("---"):
            continue
        out.append(yaml.safe_load(text.split("---", 2)[1]) or {})
    return out


def history_block(cfg):
    """Build the past-recipes digest + history rules, or '' when there's nothing to show."""
    hist = cfg.get("history") or {}
    max_entries = hist.get("max_entries", 100)
    recent_days = hist.get("recent_days", 14)
    if max_entries <= 0:
        return ""
    recipes = read_recipes()
    if not recipes:
        return ""
    recipes.sort(key=lambda r: str(r.get("last_made") or ""), reverse=True)

    def joined(r, key):
        return ", ".join(r.get(key) or []) or "-"

    lines = []
    for r in recipes[:max_entries]:
        line = (
            f"- {r.get('title', '?')} | {r.get('type', '?')} | "
            f"{joined(r, 'proteins')} / {joined(r, 'vegetables')} / {joined(r, 'legumes')} | "
            f"{r.get('cuisine') or '-'} | {r.get('rating') or 'unrated'} | "
            f"last made {r.get('last_made') or '?'}"
        )
        if r.get("feedback"):
            line += f" | {r['feedback']}"
        lines.append(line)

    return (
        "Recipes we've cooked before (most recent first):\n"
        + "\n".join(lines)
        + "\n\nHistory rules:\n"
        "- Propose mostly NEW dishes built from this week's pool.\n"
        "- Don't repeat a logged recipe unless we ask — but you may bring back a "
        '"would-make-again" favorite if it clearly improves the week; mark it REMAKE.\n'
        f"- Don't repeat anything cooked in the last {recent_days} days.\n"
        "- Avoid dishes/directions we rated \"wouldn't\"; adjust to our feedback notes.\n\n"
    )


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
        today=date.today().isoformat(),
        history_block=history_block(cfg),
        recipe_template=TEMPLATE_FILE.read_text().strip(),
    )
    print((ROOT / "prompt_template.md").read_text().format(**fields))


if __name__ == "__main__":
    main()
