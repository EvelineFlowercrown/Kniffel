from Lib import helpers, security
from Lib.player import Player


def register_new_user(db, username):
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
        if register_new_user(db, username):
            return Player(username)
        else:
            raise Exception("Neuer Benutzer konnte nicht angelegt werden.")


def login_players(db):
    logged_in_players = []
    for i in range(helpers.get_integer_input_upto("Wie viele Spieler sollen mitspielen? ", 5)):
        logged_in_players.append(login_player(db, i))

    return logged_in_players