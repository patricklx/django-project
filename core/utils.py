
def median(l):
    half = len(l) // 2
    l.sort()
    if not len(l) % 2:
        return (float(l[half - 1]) + float(l[half])) / 2.0
    return l[half]