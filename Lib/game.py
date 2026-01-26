class GameSheet:
    def __init__(self):
        self.obere = {
            "Nur 1er zählen": None,
            "Nur 2er zählen": None,
            "Nur 3er zählen": None,
            "Nur 4er zählen": None,
            "Nur 5er zählen": None,
            "Nur 6er zählen": None,
        }
        self.untere = {
            "Dreierpasch": None,
            "Viererpasch": None,
            "Full House": None,
            "Kleine Straße": None,
            "Große Straße": None,
            "Kniffel": None,
            "Chance": None
        }
        self.extras = {
            "Gesamt Oberer Teil": None,
            "Bonus 63+": None,
            "Gesamt Unterer Teil": None,
            "Kniffel Bonus": None
        }

    def getAvailable(self):
        returnList = []
        for key in self.obere.keys():
            if self.obere[key] is None:
                returnList.append(key)
        for key in self.untere.keys():
            if self.untere[key] is None:
                returnList.append(key)
        return returnList

    def printTable(self):
        col_width = 25
        line = "-" * (col_width + 10)

        print(line)
        print(f"{'Kategorie':<{col_width}} | Punkte")
        print(line)

        for category, value in self.obere.items():
            display_value = "-" if value is None else value
            print(f"{category:<{col_width}} | {display_value}")

        for category, value in self.untere.items():
            display_value = "-" if value is None else value
            print(f"{category:<{col_width}} | {display_value}")

        print(line)

        print(line)

    def calculate_extras(self):
        if all(punkte is not None for punkte in self.obere):
            self.extras["Gesamt Oberer Teil"] = sum(self.obere)
        if all(punkte is not None for punkte in self.untere):
            self.extras["Gesamt Unterer Teil"] = sum(self.untere)
        self.extras["Bonus 63+"] = 35 if self.extras["Gesamt Oberer Teil"] >= 63 else 0
        return sum([self.extras["Gesamt Oberer Teil"], self.extras["Gesamt Unterer Teil"], self.extras["Bonus 63+"]])
