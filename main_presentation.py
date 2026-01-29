from Lib import Database
from Lib.helpers import GameExit
from Lib.login import login_players
from operator import itemgetter


def Start_DB():
    db = Database.SQLiteDB()
    db.create_table(table_name="player_account", columns={
        "username": "TEXT PRIMARY KEY",
        "password": "TEXT NOT NULL",
    })
    db.create_table(table_name="player_scores", columns={
        "id": "INTEGER PRIMARY KEY AUTOINCREMENT",
        "username": "TEXT NOT NULL",
        "score": "INTEGER NOT NULL",
        "datum": "TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
    })
    return db


def main():
    scores = []
    while not all(user.gameSheet.is_complete() for user in players):
        for player in players:
            if player.gameSheet.getAvailable() != 0:
                player.playerTurn()
            else:
                score = player.gameSheet.getTotal()
                scores.append((player, score))
                print(f"{player} hat das Spiel mit {score} Punkten beendet.")
    platzierung = 1
    print("Spiel Abgeschlossen.")
    for player, score in sorted(scores, key=itemgetter(1), reverse=True):
        print(platzierung, player, score)


if __name__ == "__main__":
    db = Start_DB()
    players = login_players(db)
    for player in players:
        player.gameSheet.obere.update({
            "Nur 1er zählen": None,
            "Nur 2er zählen": 2,
            "Nur 3er zählen": None,
            "Nur 4er zählen": 8,
            "Nur 5er zählen": 20,
            "Nur 6er zählen": 30,
        })
        player.gameSheet.untere.update({
            "Dreierpasch": None,
            "Viererpasch": 18,
            "Full House": None,
            "Kleine Straße": 30,
            "Große Straße": 40,
            "Kniffel": 50,
            "Chance": 12
        })
    try:
        main()
    except GameExit:
        print("Spiel beendet.")
        exit(0)
