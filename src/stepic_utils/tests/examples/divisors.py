import random

from stepic_common import nice


def generate():
    primes = [2, 3, 5, 7, 11, 13, 17]
    p = random.choice(primes)
    q = random.choice(primes)
    dataset = p * q
    clue = min(p, q), max(p, q)
    return str(dataset), clue


def solve(dataset):
    pq = int(dataset)
    for p in range(2, pq + 1):
        if pq % p == 0:
            return nice(p, pq // p)
    assert False


def check(reply, clue):
    return list(map(int, reply.split())) == clue
