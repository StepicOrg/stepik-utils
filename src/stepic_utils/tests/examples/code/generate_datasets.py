def generate():
    return ['2 2\n', '5 7\n']


def solve(dataset):
    assert dataset in ['2 2\n', '5 7\n']
    a, b = dataset.split()
    return str(int(a) + int(b))


def check(reply, clue):
    assert clue in ['4', '12']
    return reply == clue
