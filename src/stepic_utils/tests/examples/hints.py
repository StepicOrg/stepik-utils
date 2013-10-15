def generate():
    return ''


def solve(dataset):
    return '42'


def check(reply, clue):
    reply = int(reply)
    if reply < 42:
        return 0, "the answer is bigger"
    elif reply > 42:
        return 0, "the answer is smaller"
    else:
        return 1
