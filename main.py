import ao_recipe_parser

def print_item_recipe(item):
    """
    Example usage. Prints in the format used originally for Albion.Recipes(rip).
    :param item: The item to print.
    """
    recipe = [[k,int(item.recipe[k])] for k in item.recipe.keys()]
    nut = 0 if item.uniquename[0:2] in ['T1', 'T2'] else item.value*item.amount
    s = f'new Recipe("{item.uniquename}", new Map({recipe}),{item.exclusions},convertNut({nut}),{item.amount}),'
    print(s.replace("'", '"'))


if __name__ == '__main__':  # Blame PyCharm for the default file. That gutter run thooo
    items = items.categorized_items()
    for category in items.keys():
        itemset = set()
        print(category,':')
        for item in items[category]:
            print_item_recipe(item)
            itemset.add(item.uniquename)
            [itemset.add(comp) for comp in item.recipe]
        s = str(itemset).replace("{",'').replace("}",'').replace("'",'').replace(" ",'')
        print('\n'+s)
        print(len(s),'\n\n')


