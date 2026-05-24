# recipe_finder

A small tool to fight dinner decision-fatigue. Each week it samples a weighted-random *pool* of
core ingredients and cuisines; you paste the generated prompt into a Claude web session (with web
search on), and it finds real, published recipes for you to choose from.

## Setup

```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## Usage

```sh
python plan_week.py
```

On macOS you can instead double-click **`plan_week.command`** in Finder — it runs the planner and
copies the prompt straight to your clipboard.

Then:

1. Paste the prompt into a Claude session **with web search enabled**.
2. Pick the dinners, legume dish, and dessert you like from the recipe links it returns.
3. Save each recipe block Claude outputs to the `recipes/<filename>` it suggests — that's your
   library, and later prompts draw on it (what you've made, liked, and disliked).

## Config

Three places to tune behavior:

- **[ingredients/](ingredients/)** — the weighted ingredient lists, one file per category. See
  [ingredients/README.md](ingredients/README.md) for the weight scale and how to personalize.
- **[config.yaml](config.yaml)** — the numbers: pool sizes (the variety dial), how many dinners
  to cook and candidates to propose, and the legume/dessert options.
- **[prompt_template.md](prompt_template.md)** — the dietary rules and instructions sent to the
  LLM: no fish, red meat at most once, whole-grain carbs, an omega-3 nut/seed with dessert, and
  the preferred recipe sources.
