from pprint import pprint


def test_update(file_path: str = 'sample.txt'):
    lists: list = []
    modules: str = ""
    with open(file_path, mode='rt', encoding='utf-8') as f:
        for i in f.readlines():
            for j in i.split():
                lists.append(j)

    pprint(lists)
    print('-' * 20)
    pprint(lists[8::4])


test_update(file_path='sample.txt')

