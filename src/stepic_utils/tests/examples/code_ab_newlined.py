#This is sample code challenge
import random

def generate():
    num_tests = 10
    tests = []
    for test in range(num_tests):
        a = random.randrange(10)
        b = random.randrange(10)
        test_case = "{} {}\n".format(a, b)
        tests.append(test_case)
    return tests


def solve(dataset):
    a, b = dataset.split()
    return str(int(a)+int(b))


def check(reply, clue):
    return int(reply) == int(clue)
