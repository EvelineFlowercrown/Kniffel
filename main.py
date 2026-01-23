from Lib import point_counters as pc, helpers as h, game as g, Database
import random


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


def login_player(db):
    username = input("Bitte gib deinen Username ein")
    saved_password = db.select_where(
        table_name="player_account",
        conditions={"username": username},
        columns=["password"]
    )
    if saved_password is not None:
        try_again = False
        password = input("Bitte gib dein passwort ein")
        if saved_password == password:
            return username
        else:
            print("Wrong Password")
            input("Willst du es noch mal versuchen")



def login_players(db):
    logged_in_players = []
    for i in range(h.get_integer_input_upto("Wie viele ",5)):
        logged_in_players.append(login_player(db))

    return logged_in_players


def main():
    db = Start_DB()
    players = login_players(db)


if __name__ == "__main__":
    print("hi")
    main()
