Today is {today}. We're planning this week's dinners. Use web search to find REAL, published
recipes and link to them — do NOT invent recipes or make up URLs; only return recipes from pages
you actually found, preferably from reputable sources (NYT Cooking, Serious Eats, Bon Appetit,
BBC Good Food, Smitten Kitchen, America's Test Kitchen, established food blogs).

{history_block}This week's ingredient POOL — you choose the sensible combinations (you decide what pairs well):
  Proteins:   {proteins}
  Vegetables: {vegetables}
  Cuisines:   {cuisines}

Propose {dinner_candidates} candidate dinners (we'll cook {target_dinners}). Each is ONE protein
plus 1-2 vegetables from the pool, in ONE cuisine from the pool. Make the candidates as distinct
as possible: a different cuisine each, spread across the proteins and vegetables. For each
candidate, return:

    title - source site - link - one-line why it fits - approx active cook time

Constraints:
- No fish or seafood.
- Use red meat (beef, pork, lamb) in at most one dinner.
- Carbs are a soft preference: if a carb is essential to a dish, lean whole-grain (brown rice,
  farro, quinoa, whole-wheat); if it's just a flexible side (rice, pasta), refined is fine.

Also propose:
- 1 legume dish from: {legumes} - in whatever cuisine fits best.
- 1 fruit-sweetened dessert (minimal added sugar) from: {fruits} - pair it with an omega-3
  nut/seed (walnuts, ground flax, hemp, chia) and/or a calcium source like Greek yogurt or milk.

Once we've picked our {target_dinners} dinners, the legume dish, and the dessert, output each
chosen recipe so we can save it: a line `Filename: recipes/<slug>.md` (lowercase, hyphenated, no
date), then exactly this format with the fields filled in (set last_made to {today}; leave rating
and feedback blank):

{recipe_template}
