import random

from stepic_common import nice, equal_int

LOW = 1
HIGH = 10


def generate():
    a = random.randrange(LOW, HIGH)
    b = random.randrange(LOW, HIGH)
    return nice(a, b) + '\n'


def solve(dataset):
    a, b = map(int, dataset.split())
    return str(a + b)


check = equal_int
