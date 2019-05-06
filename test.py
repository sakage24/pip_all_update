#! /usr/bin/python3.7
from pprint import pprint


def test_update(file_path: str = 'sample.txt') -> None:
    with open(file_path, mode='rt', encoding='utf-8') as f:
        lists: list = [j for i in f.readlines() for j in i.split()]
    print('=' * 20)
    pprint(lists[8::4])
    print('=' * 20)


test_update(file_path='sample.txt')
