import json


def parse_names(file='items.json'):
    with open(file, 'r', encoding="utf8") as f:
        return {entry['UniqueName']: entry['LocalizedNames'] for entry in json.loads(f.read())}


def example():
    """Example for the Albion Recipes project."""
    items = parse_names()
    set_of_lang = set()
    full = 'new Map(['
    for item in items:
        if items[item] is not None:  # You need to check for null objects, some items don't have 'LocalizedNames'.
            s = ''
            for k in items[item].keys():
                set_of_lang.add(k)
                local_item = items[item][k].replace('"', '\\"')
                s = s + f'["{k}", "{local_item}"],'
        else:  # For mine, I simply reused the unique name in cases where there was no localized name.
            s = ''
            for lang in set_of_lang:
                s = s + f'["{lang}", "{item}"],'
        full = full + f'["{item}",new Map([{s[:-1]}])],\n'
    return full[:-1] + "])"

with open("output.txt", 'w', encoding="utf8") as f:
    f.write(example())
