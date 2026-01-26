from sqlalchemy.dialects.mssql.information_schema import columns

from Lib import helpers as h, Database
import random

from Lib.player import Player


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
    password = input("Lege ein passwort für dein account fest: ")
    try:
        db.insert("player_account", {"username": username, "password": password})
        return True
    except:
        return False


def login_player(db, i):
    username = input(f"Spieler {i + 1}: Bitte gib deinen Username ein: ")
    saved_password = db.select_where(
        table_name="player_account",
        conditions={"username": username},
        columns=["password"]
    )
    if len(saved_password) > 0:
        try_again = False
        while not try_again:
            password = input("Bitte gib dein passwort ein: ")
            if saved_password[0]["password"] == password:
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
    for i in range(h.get_integer_input_upto("Wie viele Spieler sollen mitspielen? ", 5)):
        logged_in_players.append(login_player(db, i))

    return logged_in_players


def main():
    db = Start_DB()
    players = login_players(db)
    print(players)
    while not all(user.gameSheet.getAvailable() == 0 for user in players):
        for player in players:
            if player.gameSheet.getAvailable() != 0:
                player.playerTurn()
            else:
                score = player.gameSheet.getTotal()


if __name__ == "__main__":
    main()
