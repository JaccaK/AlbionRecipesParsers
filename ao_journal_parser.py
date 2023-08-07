import json


class Journal:
    def __init__(self, unique_name, base_amount, loot):
        self.unique_name = unique_name + "_EMPTY"
        self.full_name = unique_name + "_FULL"
        self.base_amount = base_amount
        self.loot = loot

    def average_loot(self):
        """
        Returns the average loot for the journal.
        :return: A dictionary containing unique_name:average_amount.
        """
        adjusted_weights = {k: self.loot[k] * self.base_amount for k in self.loot.keys()}
        total = sum(self.loot.values())
        return {k: adjusted_weights[k] / total for k in adjusted_weights.keys()}

    def full(self):
        return self.full_name


def parse_for_journals(file_name="items.json"):
    """
    Parses a file (items.json by default) for all non-merc journals, turning them into Journal objects.
    :param file_name: items.json by default.
    :return: A list of Journal Objects.
    """
    data = json.loads(read_file(file_name))["items"]["journalitem"]
    journal_list = []
    for entry in data:
        if "MERCENARY" in entry["@uniquename"]:  # Skip mercenary. The data for those is easy, no calc required.
            continue
        journal_list.append(get_journal(entry))
    return journal_list


def get_journal(entry):
    """Helper for parse_for_journals. returns a Journal object given a JSON entry."""
    name = entry["@uniquename"]
    amount = float(entry["@baselootamount"])
    loot = entry["lootlist"]["loot"]
    loot_dict = {}
    if type(loot) is dict:
        loot_dict = get_journal_helper(loot)
    else:
        for item in loot:
            loot_dict.update(get_journal_helper(item))
    return Journal(name, amount, loot_dict)


def get_journal_helper(item):
    """A helper for the get_journal helper function. Given an item, returns unique_name:weight."""
    loot_dict = {}
    item_name = item["@itemname"]
    if item_name[-1] in ["1", "2", "3"]:
        item_name = item_name + "@" + item_name[-1]
    loot_dict[item_name] = int(item["@weight"])
    return loot_dict


def parse_for_merc_journals(file_name="items.json"):
    """
    Parses a file for mercenary journals. Does not have a class associated, just returns a list of dictionaries.
    :param file_name: items.json by default.
    :return: A list of mercenary journal dictionaries.
    """
    data = json.loads(read_file(file_name))["items"]["journalitem"]
    journal_list = []
    for entry in data:
        if "MERCENARY" in entry["@uniquename"]:
            journal_list.append(entry)
    return journal_list


def read_file(file_name):
    """Boilerplate open file to string. Nothing to see here."""
    with open(file_name, 'r') as file:
        return file.read()
