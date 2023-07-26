import json


def parse_names(file='items.json'):
    with open(file, 'r', encoding="utf8") as f:
        return {entry['UniqueName']: entry['LocalizedNames'] for entry in json.loads(f.read())}


def example():
    """Example for the Albion Recipes project."""
    items = parse_names()
    for item in items:
        if items[item] is not None:  # You need to check for null objects, some items don't have 'LocalizedNames'.
            name = items[item]["EN-US"]  # ["EN-US"] because I want English.
            if '"' in name:  # Some items, like '"Tame" Caerleon Cottontail', have quotation marks.
                name = name.replace('"', '\\"')  # So we can replace them with escaped versions of the same.
            print(f'["{item}","{name}"]', end=",\n")
        else:  # For mine, I simply reused the unique name in cases where there was no localized name.
            print(f'["{item}","{item}"]', end=",\n")


example()
