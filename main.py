from Lib import point_counters as pc, helpers as h, game as g
import random



def roll_dice(n):
    out = []
    for i in range(n):
        out.append(random.randint(1, 6))
    return out


def playerTurn(gameSheet):
    num_rolls = 0
    dice = []
    held_dice = []

    while num_rolls < 3:
        dice = roll_dice(5 - len(held_dice))
        print("dein wurf:", dice, "behaltene:", held_dice)
        if len(held_dice) < 5:

            behalten = None
            while behalten == None:
                behalten = h.get_integer_input("wie viele würfel willst du behalten? ")
                if behalten > len(dice):
                    print(f"{behalten} ist ungültig. wähle aus 0 -", len(dice))
                    behalten = None
            if behalten == len(dice):
                held_dice.append(dice)
                held_dice = []
                break
            for n in range(behalten):
                choice = dice.pop(
                    h.get_integer_input(f"welchen würfel möchtest du behalten? (Position: 1-{len(dice)}) ") - 1)
                held_dice.append(choice)
                print("dein wurf:", dice, "behaltene:", held_dice)
            num_rolls += 1
        else:
            break
    print(dice, held_dice)
    final_dice = dice + held_dice
    print("Wähle aus folgenden Optionen:")
    final_options = pc.getPointOptions(final_dice,gameSheet.getAvailable())
    for name, points in final_options:
        print(f"{name}:", points, "Punkte")
    choice = final_options.pop(h.get_integer_input(f"Welches Feld möchstest du ausfüllen? (Position: 1-{len(final_options)}) ") - 1)
    gameSheet.points[choice[0]] = choice[1]

gameSheet = g.GameSheet("Eveline")
if gameSheet.getAvailable() is None:
    playerTurn(gameSheet)
    gameSheet.printTable()
while len(gameSheet.getAvailable()) > 0:
    playerTurn(gameSheet)
    gameSheet.printTable()