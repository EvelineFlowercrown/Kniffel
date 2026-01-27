from Lib import point_counters as pc, helpers, dice_class, Database as db, helpers
from Lib.game import GameSheet


def display_endscreen():
    pass


class Player:
    def __init__(self, name):
        self.name = name
        self.gameSheet = GameSheet()

    def playerTurn(self):
        num_rolls = 0
        dice = []
        held_dice = []
        print(f"{self.name} ist am Zug.")

        while num_rolls < 3:
            dice = dice_class.roll_dice(5 - len(held_dice))
            print("dein wurf:", dice, "behaltene:", held_dice)
            if len(held_dice) < 5:
                behalten = helpers.get_integer_input_upto("wie viele würfel willst du behalten? ", len(dice))
                if behalten == len(dice):
                    for i in range(behalten):
                        held_dice.append(dice.pop(0))
                    break
                for n in range(behalten):
                    choice = dice.pop(
                        helpers.get_integer_input(f"welchen würfel möchtest du behalten? (Position: 1-{len(dice)}) ") - 1)
                    held_dice.append(choice)
                    print("dein wurf:", dice, "behaltene:", held_dice)
                num_rolls += 1
            else:
                break
        print(dice, held_dice)
        final_dice = dice + held_dice
        print("Wähle aus folgenden Optionen:")
        final_options = pc.getPointOptions(final_dice, self.gameSheet.getAvailable())
        option_counter = 1
        for name, points in final_options:
            print(f"{option_counter}. {name}:", points, "Punkte")
            option_counter += 1
        choice = final_options.pop(
            helpers.get_integer_input(f"Welches Feld möchstest du ausfüllen? (Position: 1-{len(final_options)}) ") - 1)
        if choice[0] in self.gameSheet.obere.keys():
            self.gameSheet.obere[choice[0]] = choice[1]
        if choice[0] in self.gameSheet.untere.keys():
            self.gameSheet.untere[choice[0]] = choice[1]
        self.gameSheet.calculate_extras()
        weiter = helpers.get_input("Was willst du tun? \nT = Tabelle anzeigen \nSonsige = Nächster Spieler")
        if weiter.lower() == "t":
            self.gameSheet.printTable()


    def __repr__(self):
        return self.name
