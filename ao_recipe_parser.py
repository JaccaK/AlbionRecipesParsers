import json


# TODO Create a main capable of fixing your website
# TODO Find cheaper hosting appropreiate for less userbase
# TODO Set up a patreon to pay for costs

class Item:
    def __init__(self, uniquename, category, subcategory):
        self.uniquename = uniquename
        self.category = category
        self.subcategory = subcategory
        self.recipe = {}
        self.exclusions = []
        self.amount = 0
        self.value = 0.0

    def add_recipe(self, recipe, exclusions, amount):
        """Sets recipe, exclusions, and amount."""
        self.amount = int(amount)
        for component in recipe:
            if 'LEVEL' in component:  # Enchant the material
                self.recipe[component + "@" + component[-1]] = recipe[component]
            else:
                self.recipe[component] = recipe[component]
        for component in exclusions:
            if 'LEVEL' in component:
                self.exclusions.append(component + '@' + component[-1])
            else:
                self.exclusions.append(component)

    def calculate_item_value(self, item_vals):
        """Calculates and sets the item value."""
        value = 0
        try:
            for component in self.recipe:
                comp = component
                if '@' in comp:  # Disenchant for item value.
                    comp = comp[:-2]
                value += item_vals[comp] * int(self.recipe[component])
        except KeyError:
            value = -1  # If the value is negative, the item_vals set was wrong and there is an error. Set manual.
        if self.uniquename in item_vals.keys():
            value = item_vals[self.uniquename]
        self.value = value

    def nutrition(self):
        """Albion nutrition formula."""
        return self.value * self.amount / 20 / 44.44

    def duplicate(self):
        """Creates a deep copy of the item."""
        return self.enchant('')

    def enchant(self, level):
        """Creates a deep copy of the item with a string appended."""
        return Item(self.uniquename + str(level), self.category, self.subcategory)


def read_file(file_name):
    """Boilerplate open file to string. Nothing to see here."""
    with open(file_name, 'r') as file:
        return file.read()


def parse_for_item_value(file_name="items.json"):
    """
    Parses a json file (items.json by default) for item values.
    :param file_name: The file name, defaults to items.json
    :return: A dictionary containing @uniquename:float(@itemvalue) pairs.
    """
    item_values = {}
    data = json.loads(read_file(file_name))["items"]
    countdown = 3
    for category in data:
        if countdown > 0:
            countdown -= 1
            continue  # Start at 3 to skip "@xmlns:xsi", "@xsi:noNamespaceSchemaLocation", "shopcategories"
        for value in data[category]:
            if '@itemvalue' in value and value != '@itemvalue':  # To avoid a stray @itemvalue, but also parse all with
                item_values[value['@uniquename']] = float(value['@itemvalue'])
    return item_values


def get_recipe(entry):
    """Gets the recipe from the entry."""
    if type(entry) is str:
        return {}, [], 0
    recipe = {}
    exclusions = []
    amount = 1
    if 'craftresource' in entry and type(entry['craftresource']) is dict:
        test = entry['craftresource']
        if '@maxreturnamount' in test:
            exclusions.append(test['@uniquename'])
        recipe[test['@uniquename']] = test['@count']
        if '@amountcrafted' in entry:
            amount = entry['@amountcrafted']
    elif 'craftresource' in entry:
        for resource in entry['craftresource']:
            if '@maxreturnamount' in resource:
                exclusions.append(resource['@uniquename'])
            recipe[resource['@uniquename']] = resource['@count']
    return recipe, exclusions, amount


def add_item_to_list(entry, base_item, items, enchant=''):
    """
    Helper for parse_for_item_recipes
    :param enchant: Enchants the item, defaults to duplication (deep copy).
    :param entry: The entry.
    :param base_item: The base item.
    :param items: Items list.
    """
    recipe, exclusions, amount = get_recipe(entry)
    if len(exclusions) > 0 and 'TOKEN_FAVOR' in exclusions[0]:
        return
    new_item = base_item.enchant(enchant)
    items.append(new_item)  #
    new_item.add_recipe(recipe, exclusions, amount)


def parse_for_item_recipes(file_name="items.json"):
    """
    Parse a JSON file for item requires for Albion Online.
    :param file_name: A json file, default is "items.json".
    :return: A list of Item objects containing recipe fields.
    """
    items = []
    data = json.loads(read_file(file_name))["items"]
    countdown = 3
    for category in data:
        if countdown > 0:
            countdown -= 1
            continue  # Start at 3 to skip "@xmlns:xsi", "@xsi:noNamespaceSchemaLocation", "shopcategories"
        for value in data[category]:
            if 'craftingrequirements' in value and value != 'craftingrequirements':
                base_item = Item(value['@uniquename'], value['@shopcategory'], value['@shopsubcategory1'])
                for entry in value['craftingrequirements']:
                    if 'craftresource' not in entry or entry == 'craftresource':
                        continue
                    add_item_to_list(entry, base_item, items)
                if type(value['craftingrequirements']) is dict:
                    entry = value['craftingrequirements']
                    if 'craftresource' not in entry or entry == 'craftresource':
                        continue
                    add_item_to_list(entry, base_item, items)
                if 'enchantments' in value and value != 'enchantments':
                    for entry in value['enchantments']['enchantment']:
                        if 'craftingrequirements' not in entry or type(entry) is str:
                            continue
                        if type(entry['craftingrequirements']) is list:
                            for requirement in entry['craftingrequirements']:
                                add_item_to_list(requirement, base_item, items, '@'+entry['@enchantmentlevel'])
                        else:
                            add_item_to_list(entry['craftingrequirements'], base_item, items, '@'+entry['@enchantmentlevel'])
    values = parse_for_item_value(file_name)
    [x.calculate_item_value(values) for x in items]  # Quick list comprehension to add values.
    return items


def add_to_category(dictionary, category, item):
    """Adds an item to a dictionary's category list, if it doesn't exist create it first."""
    if category not in dictionary.keys():
        dictionary[category] = []
    dictionary[category].append(item)


def categorized_items(category=lambda x: x.subcategory, key=lambda y: y.uniquename[1]):
    """
    Categorizes items into a dictionary based on the category parameter.
    :param key: Sort key for each individual category. Defaults to sorting by tier.
    :param category: The category function, defaults to x.subcategory to use item subcategories.
    :return: A dictionary of lists containing items under a category.
    """
    dictionary = {}
    for item in parse_for_item_recipes():
        add_to_category(dictionary, category(item), item)
    for item in dictionary:
        dictionary[item].sort(key=key)
    return dictionary
