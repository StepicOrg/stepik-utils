import random

from stepic_common import nice


def generate():
    numbers = [random.randrange(0, 10) for _ in range(9)]
    # ensure at least one even number
    numbers.append(random.randrange(0, 5) * 2)
    random.shuffle(numbers)
    clue = find_all_even(numbers)
    return nice(numbers), clue


def solve(dataset):
    numbers = map(int, dataset.split())
    even = find_all_even(numbers)
    return str(even[0])


def check(reply, clue):
    return int(reply) in clue


def find_all_even(numbers):
    return [x for x in numbers if x % 2 == 0]
