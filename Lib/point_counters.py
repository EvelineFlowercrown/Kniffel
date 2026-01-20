def counts(dice):
    counts = {}
    for n in range(1, 7):
        counts.update({n: dice.count(n)})
    return counts


def oberePunkte(counts):
    returnMap = {}
    for number in counts.keys():
        returnMap.update({number: counts[number] * number})
    return returnMap


def dreierPasch(counts, dice):
    if any(c >= 3 for c in counts.values()):
        return sum(dice)
    else:
        return 0


def viererPasch(counts, dice):
    if any(c >= 4 for c in counts.values()):
        return sum(dice)
    else:
        return 0


def fuenferPasch(counts):
    if any(c >= 5 for c in counts.values()):
        return 50
    else:
        return 0


def fullHouse(counts):
    if any(c == 3 for c in counts.values()) and any(c == 2 for c in counts.values()):
        return 25
    else:
        return 0


def kleineStrasse(dice):
    strassen = [{1, 2, 3, 4}, {2, 3, 4, 5}, {3, 4, 5, 6}]
    if any(strasse.issubset(set(dice)) for strasse in strassen):
        return 30
    else:
        return 0


def grosseStrasse(dice):
    if set(dice) in [{1, 2, 3, 4, 5}, {2, 3, 4, 5, 6}]:
        return 40
    else:
        return 0

def chance(dice):
    return sum(dice)

def getPointOptions(dice,available):
    diceCounts = counts(dice)
    options = {}
    if "Kniffel" in available:
        options.update({"Kniffel":fuenferPasch(diceCounts)})
    if "Große Straße" in available:
        options.update({"Große Straße":grosseStrasse(dice)})
    if "Kleine Straße" in available:
        options.update({"Kleine Straße": kleineStrasse(dice)})
    if "Full House" in available:
        options.update({"Full House": fullHouse(diceCounts)})
    if "Viererpasch" in available:
        options.update({"Viererpasch": viererPasch(diceCounts,dice)})
    if "Dreierpasch" in available:
        options.update({"Dreierpasch": dreierPasch(diceCounts,dice)})
    for number in oberePunkte(diceCounts).keys():
        if f"Nur {number}er zählen" in available:
            options.update({f"Nur {number}er zählen": oberePunkte(diceCounts)[number]})
    if "Chance" in available:
        options.update({"Chance": chance(dice)})
    return sorted(options.items(), key=lambda x: x[1],reverse=True)

