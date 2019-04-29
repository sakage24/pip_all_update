from pprint import pprint


lists: list = []
modules: str = ""

with open('sample.txt', mode='rt', encoding='utf-8') as f:
    for i in f.readlines():
        for j in i.split():
            lists.append(j)

pprint(lists)
print('-' * 20)
pprint(lists[8::4])
