import random


def roll_dice(n):
    out = []
    for i in range(n):
        out.append(random.randint(1, 6))
    return out
