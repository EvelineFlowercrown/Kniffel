import user
import point_counters as pc
import helpers as h
import random

players = ["eve"]
#user.playerSetup()


def roll_dice(n):
    out = []
    for i in range(n):
        out.append(random.randint(1, 6))
    return out


def playerTurn():
    num_rolls = 0
    dice = []
    held_dice = []

    while num_rolls < 3:
        dice = roll_dice(5 - len(held_dice))
        print("dein wurf:", dice, "behaltene:", held_dice)
        if len(held_dice) < 5:
            for n in range(h.get_integer_input("wie viele würfel willst du behalten")):
                choice = dice.pop(h.get_integer_input(f"welchen würfel möchtest du behalten? (Position: 0-{len(dice) - 1})"))
                held_dice.append(choice)
                print("dein wurf:", dice, "behaltene:", held_dice)
            num_rolls += 1
    print(dice,held_dice)
    final_dice = dice+held_dice
    print(pc.counts(final_dice))


playerTurn()