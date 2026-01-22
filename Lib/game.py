class GameSheet:
    def __init__(self):
        self.points = {
            "Nur 1er zählen": None,
            "Nur 2er zählen": None,
            "Nur 3er zählen": None,
            "Nur 4er zählen": None,
            "Nur 5er zählen": None,
            "Nur 6er zählen": None,

            "Dreierpasch": None,
            "Viererpasch": None,
            "Full House": None,
            "Kleine Straße": None,
            "Große Straße": None,
            "Kniffel": None,
            "Chance": None
        }

    def getAvailable(self):
        returnList = []
        for key in self.points.keys():
            if self.points[key] is None:
                returnList.append(key)
        return returnList

    def printTable(self):
        col_width = 25
        line = "-" * (col_width + 10)

        print(f"\nPunktetafel für Spieler: {self.player}")
        print(line)
        print(f"{'Kategorie':<{col_width}} | Punkte")
        print(line)

        for category, value in self.points.items():
            display_value = "-" if value is None else value
            print(f"{category:<{col_width}} | {display_value}")

        print(line)