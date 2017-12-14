def generate():
    return ['2 2\n', '5 7\n']


def solve(dataset):
    assert dataset in ['2 2\n', '5 7\n']
    return str(sum(map(int, dataset.split())))


def check(reply, clue):
    assert clue in ['4', '12']
    return reply == clue
