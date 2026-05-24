# Weights

These files are the tunable priors the recipe planner samples from. Each week the planner draws
a weighted-random *pool* of ingredients and cuisines from here; an LLM then assembles coherent
dinners (plus a legume dish and a fruit dessert) out of that pool.

One file per category:

| File | What it holds |
|---|---|
| `proteins.yaml`   | Proteins (poultry, plant, egg, dairy, red meat) |
| `vegetables.yaml` | Vegetables that can anchor a dinner |
| `legumes.yaml`    | Beans, lentils, and other pulses for the weekly legume dish |
| `fruits.yaml`     | Fruits for low-added-sugar desserts |
| `cuisines.yaml`   | Cuisines, sampled as a variety axis |

Each file is a flat list of `{name, weight}` records, and the category is just the file name.

## The weight scale

`weight` runs **1–5**: 5 = feature often, 1 = feature occasionally. It's a relative sampling
probability, not a ranking — an item at weight 4 is drawn roughly twice as often as one at 2.

Each weight blends four criteria:

1. **Nutritional density** — how nutrient-rich the ingredient is.
2. **Center-of-plate ability** — can it anchor a dish, not just season it.
3. **Versatility** — does it work across many cuisines.
4. **Availability** — is it reliable year-round.

A 5 scores high on all four. A 3 usually loses a point to seasonality or a supporting role. A
1–2 flags a reason to feature it less often (red meat, starchy carbs, a concentrated sweetener).

## Why these defaults

- **Fish is left out — a personal choice.** With seafood excluded, plant proteins, poultry, and
  eggs carry the highest protein weights; add fish back to `proteins.yaml` if you eat it.
- **Red meat is held low.** It sits at weight 1–2, in line with mainstream guidance to limit
  it.
- **Soy lives in proteins.** Tofu, tempeh, and edamame are botanically legumes but function as
  proteins, so they are weighted there to avoid double-sampling.
- **Starchy roots are kept, not excluded.** Potato, sweet potato, and winter squash stay
  available but down-weighted, since they act more like a carb than a vegetable.
- **Desserts lean on fruit.** Fruits are chosen for natural sweetness; a dessert pairs well with
  an omega-3 nut or seed (walnuts, ground flax, hemp, chia) for healthy fat and micronutrients.
- **Tuned to the whole day, not just dinner.** A few items (eggs, kale, carrots, berries) are
  down-weighted because they already feature at breakfast or lunch here — the aim is a varied
  *day*, not just a varied dinner.
- **Targeted oxalate tilt (the maintainer forms calcium-oxalate stones, infrequently).** Oxalate
  load is wildly uneven across foods, so the trim is too: the megadose greens — spinach and swiss
  chard — are pushed down hardest, and cannellini (white) beans with them. Moderate sources
  (black beans, raspberries, figs) stay near their low-oxalate equivalents, since cutting them buys
  little. Diet is the secondary lever anyway — adequate calcium taken *with* these foods, plus
  fluids (2.5 L+/day) and low sodium, does more than avoidance.

These follow widely used frameworks: the Harvard Healthy Eating Plate, the Mediterranean diet
pattern, and the USDA Dietary Guidelines for Americans.

## Personalizing

This is a starting point — edit it freely:

- **Raise** the weight of ingredients you love or want more of.
- **Lower** the weight of anything you dislike, can't get locally, or already eat plenty of at
  other meals (no point having the planner push it at dinner too).
- **Add or remove items** — keep the `name` / `weight` shape so the planner can read them;
  remove an item (or set its weight to 0) to drop it from rotation entirely.

Cuisines work the same way: weight up the ones you want to explore, down the ones you don't.
