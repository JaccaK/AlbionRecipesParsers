# AlbionRecipesParsers
Parsers created for updating Albion Recipes

## ao_name_parser.py
This parses for localized item names given an item id such as "T4_PLANK."

This parser is pretty simple, 2 lines of code that will parse through the formatted item json found here: https://github.com/ao-data/ao-bin-dumps/tree/master/formatted

Included, if run on it's own, is an example of how I might use it to get an updated list of elements for my name map for Albion Recipes.


## ao_recipe_parser.py
This parses for recipes, and attempts to parse for item value. I had it skip favor tokens.

Less simple, a solid 180 line file. This parses the items.json found in the root of the ao-bin-dumps repo: https://github.com/ao-data/ao-bin-dumps/tree/master

Included is a main.py that is an example of how I might use it to get a list of recipes that can be used for my Albion Recipes repo.


## ao_journal_parser.py
This parses for journals' average loot return. It might be a bit messed up, I used it to get my laborer calc made.
