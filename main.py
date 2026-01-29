from Lib import helpers, Database, security
from Lib.helpers import GameExit
from Lib.player import Player
from operator import itemgetter


def Start_DB():
    db = Database.SQLiteDB("Datenbank")
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


def nutzer_anlegen(db, username):
    password = helpers.get_input("Lege ein passwort für dein account fest: ")
    password_hash = security.hash_password(password)
    try:
        db.insert("player_account", {"username": username, "password": password_hash})
        return True
    except:
        return False


def login_player(db, i):
    username = helpers.get_input(f"Spieler {i + 1}: Bitte gib deinen Username ein: ")
    query = db.select_where(
        table_name="player_account",
        conditions={"username": username},
        columns=["password"]
    )
    if len(query) > 0:
        try_again = False
        hashed_password = query[0]["password"]
        while not try_again:
            entered_password = helpers.get_input("Bitte gib dein passwort ein: ")
            if hashed_password == security.hash_password(entered_password):
                return Player(username)
            else:
                print("Wrong Password")
    else:
        print("Account existiert nicht. Bitte erstelle einen Account um zu spielen.")
        if nutzer_anlegen(db, username):
            return Player(username)
        else:
            raise Exception("Neuer Benutzer konnte nicht angelegt werden.")


def login_players(db):
    logged_in_players = []
    for i in range(helpers.get_integer_input_upto("Wie viele Spieler sollen mitspielen? ", 5)):
        logged_in_players.append(login_player(db, i))

    return logged_in_players


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
    try:
        main()
    except GameExit:
        print("Spiel beendet.")
        exit(0)
