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


def login_players():
    logged_in_players = []

    return logged_in_players


def main():
    db = Start_DB()
    players = login_players()


if __name__ == "main":
    main()
