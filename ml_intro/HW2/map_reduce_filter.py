import re
import operator
from itertools import starmap
from functools import reduce

def solution1(arg):
    return list(map(lambda item: int(re.sub(r'[\s|,|\-|.]', '', item)[::-1]), arg))

def solution2(arg):
    return list(starmap(operator.mul, arg))

def solution3(arg):
    return list(filter(lambda item: item % 6 == 2 or item % 6 == 5 or item % 6 == 0, arg))

def solution4(arg):
    return list(filter(None, arg))

def solution5(arg):
    return list(map(lambda item: operator.setitem(item, 'square', item['width']*item['length']), arg))

def solution6(arg):
    return list(map(lambda item: operator.setitem(item, 'square', item['width']*item['length']) or item, arg))

def solution7(arg):
    return list(map(lambda item: dict(item, square= item['width'] * item['length']), arg))

def solution8(arg):
    return (reduce(lambda x, y: x + y['height'], arg, 0), len(arg))

def solution9(arg):
    return list(map(lambda item: item['name'],filter(lambda item: item['gpa'] > 4.5, arg)))

def solution10(arg):
    return list(
        filter(
            lambda str: 
                sum(map(lambda x: int(x[1]), filter(lambda x: x[0]%2, enumerate(str))), 0) ==
                sum(map(lambda x: int(x[1]), filter(lambda x: x[0]%2 == 0, enumerate(str))), 0),
            arg
        )
    )

solutions = {
    'solution1': solution1,
    'solution2': solution2,
    'solution3': solution3,
    'solution4': solution4,
    'solution5': solution5,
    'solution6': solution6,
    'solution7': solution7,
    'solution8': solution8,
    'solution9': solution9,
    'solution10': solution10,
}