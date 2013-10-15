import random

from stepic_common import equal_int

LOW = 1
HIGH = 10


def generate():
    a = random.randrange(LOW, HIGH)
    b = random.randrange(LOW, HIGH)
    return {'a': a, 'b': b}


def solve(dataset):
    return str(dataset['a'] + dataset['b'])


check = equal_int
