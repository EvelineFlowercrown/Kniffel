import helpers as h


def playerSetup():
    spieler = []
    anzahlSpieler = h.get_integer_input("wie viele spieler?")
    for i in range(anzahlSpieler):
        spieler.append(input(f"Spieler {i} Bitte gib deinen namen ein"))

    while input("start game? (y,n)") != "y":
        pass
    return  spieler
