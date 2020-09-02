def generate():
    return ['2 2\n', '5 7\n']


def check(reply, clue):
    assert clue is None
    # Unable to check without dataset or clue
    return False
