
def counts(dice):
    counts = {}
    for n in range(1,7):
        counts.update({n:dice.count(n)})
    return counts

def dreier(counts):
    if any(c >= 3 for c in counts.values()):
        pass
