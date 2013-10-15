import random


def generate():
    n = random.randrange(5, 10)
    return str(n), (fib_n(n), fib_n(n-1), fib_n(n+1))


def solve(dataset):
    n = int(dataset)
    return str(fib_n(n))


def check(reply, clue):
    reply = int(reply)
    if reply == clue[0]:
        return 1
    elif reply in clue:
        return 0, "Check indices. Off by one error."
    return 0


def fib_n(n):
    # 1 1 2 3 5
    # 0 1 2 3 4
    f1, f2 = 1, 1
    for _ in range(n):
        f1, f2 = f2, f1 + f2
    return f1
