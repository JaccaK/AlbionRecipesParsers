import ao_journal_parser


def py_dict_to_js_map(dictionary):
    s = "new Map(["
    for k in dictionary.keys():
        s = s + f'["{k}", {dictionary[k]}],'  # string:float mapping.
    return s[:-1] + "])"


def js_journal(journal):
    return f'new Journal("{journal.unique_name}", "{journal.full()}", {py_dict_to_js_map(journal.average_loot())}),'

m = set()
l = ao_journal_parser.parse_for_journals()
l.sort(key=lambda x: x.unique_name[1])
for i in l:
    if "TROPHY" in i.unique_name:
        continue
    print(js_journal(i))
    m.add(i.unique_name)
    m.add(i.full())
    for loot in i.loot.keys():
        m.add(loot)

s = ""
for item in m:
    s = s + item + ","
print (s[:-1])