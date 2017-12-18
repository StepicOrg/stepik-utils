def generate():
    return [('2 2\n', 'clue:4'), ('5 7\n', 'clue:12')]


def solve(dataset):
    assert dataset in ['2 2\n', '5 7\n']
    a, b = dataset.split()
    return str(int(a) + int(b))


def check(reply, clue):
    assert clue in ['clue:4', 'clue:12']
    return reply == clue[5:]
