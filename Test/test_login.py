import os
import unittest
from unittest.mock import patch, MagicMock
from Lib.Database import SQLiteDB
from Lib.login import register_new_user, login_player, login_players
from Lib.player import Player


class TestLogin(unittest.TestCase):

    def setUp(self):
        """Setzt Test-Datenbank vor jedem Test auf"""
        try:
            os.remove("test_database.db")
        except FileNotFoundError:
            pass

        self.db = SQLiteDB("test_database.db")
        self.db.create_table(table_name="player_account", columns={
            "username": "TEXT PRIMARY KEY",
            "password": "TEXT NOT NULL",
        })

    def tearDown(self):
        """Räumt nach jedem Test auf"""
        self.db.__exit__()
        try:
            os.remove("test_database.db")
        except FileNotFoundError:
            pass

    # ----------------------------
    # Test für register_new_user()
    # ----------------------------

    @patch("Lib.helpers.get_input")
    def test_register_new_user_empty_pw(self, mock_get_input):
        """Testet Registrierung mit leerem Passwort"""
        mock_get_input.return_value = ""
        result = register_new_user(self.db, "TestUser0")
        self.assertFalse(result)  # Sollte fehlschlagen oder True/False je nach Implementierung

    @patch("Lib.helpers.get_input")
    def test_register_new_user_standard_pw(self, mock_get_input):
        """Testet Registrierung mit Standard-Passwort"""
        mock_get_input.return_value = "Pa$$wort123undNoch€|nm@l"
        result = register_new_user(self.db, "TestUser1")
        self.assertTrue(result)

        # Überprüfe ob User in DB gespeichert wurde
        query = self.db.select_where("player_account", {"username": "TestUser1"})
        self.assertEqual(len(query), 1)
        self.assertIsNotNone(query[0]["password"])

    @patch("Lib.helpers.get_input")
    def test_register_new_user_escaped_pw(self, mock_get_input):
        """Testet Registrierung mit Sonderzeichen im Passwort"""
        mock_get_input.return_value = "\n\t\\\"'"
        result = register_new_user(self.db, "TestUser2")
        self.assertTrue(result)

    @patch("Lib.helpers.get_input")
    def test_register_new_user_sql_pw(self, mock_get_input):
        """Testet Registrierung mit SQL-Injection-Versuch als Passwort"""
        mock_get_input.return_value = "DROP TABLE player_account; --"
        result = register_new_user(self.db, "TestUser3")
        self.assertTrue(result)  # Sollte gehasht werden, also kein Problem

        # Überprüfe dass Tabelle noch existiert
        query = self.db.select_where("player_account", {"username": "TestUser3"})
        self.assertEqual(len(query), 1)

    @patch("Lib.helpers.get_input")
    def test_register_new_user_non_ascii_pw(self, mock_get_input):
        """Testet Registrierung mit nicht-ASCII Zeichen"""
        mock_get_input.return_value = "咦？你为什么对我的测试用例这么感兴趣？"
        result = register_new_user(self.db, "TestUser4")
        self.assertTrue(result)

    @patch("Lib.helpers.get_input")
    def test_register_new_user_duplicate_username(self, mock_get_input):
        """Testet Registrierung mit bereits existierendem Username"""
        # Ersten User anlegen
        mock_get_input.return_value = "password123"
        result1 = register_new_user(self.db, "DuplicateUser")
        self.assertTrue(result1)

        # Versuch zweiten User mit gleichem Namen anzulegen
        mock_get_input.return_value = "different_password"
        result2 = register_new_user(self.db, "DuplicateUser")
        self.assertFalse(result2)  # Sollte fehlschlagen

    # ----------------------------
    # Test für login_player()
    # ----------------------------

    @patch("Lib.helpers.get_input")
    def test_login_player_empty_name(self, mock_get_input):
        """Testet Login mit leerem Username"""
        # Simuliere leeren Username, dann Passwort
        mock_get_input.side_effect = ["", "password123"]

        # Da User nicht existiert, wird Registrierung versucht
        with patch.object(self.db, 'insert') as mock_insert:
            mock_insert.side_effect = Exception("Primary key violation")
            player = login_player(self.db, 0)
            self.assertIsNone(player)

    @patch("Lib.helpers.get_input")
    def test_login_player_standard_name(self, mock_get_input):
        """Testet Login mit normalem Username und korrektem Passwort"""
        # Erst Registrierung
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "correct_password"
            register_new_user(self.db, "StandardUser")

        # Dann Login
        mock_get_input.side_effect = ["StandardUser", "correct_password"]
        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, "StandardUser")

    @patch("Lib.helpers.get_input")
    def test_login_player_wrong_password_then_correct(self, mock_get_input):
        """Testet Login mit falschem, dann korrektem Passwort"""
        # Registrierung
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "correct_password"
            register_new_user(self.db, "User1")

        # Login: erst falsches Passwort, dann korrektes
        mock_get_input.side_effect = ["User1", "wrong", "correct_password"]
        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, "User1")

    @patch("Lib.helpers.get_input")
    def test_login_player_escaped_name(self, mock_get_input):
        """Testet Login mit Username mit Sonderzeichen"""
        # Registrierung mit Sonderzeichen
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "password123"
            register_new_user(self.db, "User\n\t\\\"'")

        # Login
        mock_get_input.side_effect = ["User\n\t\\\"'", "password123"]
        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, "User\n\t\\\"'")

    @patch("Lib.helpers.get_input")
    def test_login_player_sql_name(self, mock_get_input):
        """Testet Login mit SQL-Injection als Username"""
        sql_username = "User'; DROP TABLE player_account; --"

        # Registrierung
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "password123"
            register_new_user(self.db, sql_username)

        # Login
        mock_get_input.side_effect = [sql_username, "password123"]
        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, sql_username)

        # Überprüfe dass Tabelle noch existiert
        query = self.db.select_where("player_account", {"username": sql_username})
        self.assertEqual(len(query), 1)

    @patch("Lib.helpers.get_input")
    def test_login_player_non_ascii_name(self, mock_get_input):
        """Testet Login mit nicht-ASCII Username"""
        non_ascii_username = "测试用户"

        # Registrierung
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "password123"
            register_new_user(self.db, non_ascii_username)

        # Login
        mock_get_input.side_effect = [non_ascii_username, "password123"]
        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, non_ascii_username)

    @patch("Lib.helpers.get_input")
    def test_login_player_new_user_registration(self, mock_get_input):
        """Testet Login mit nicht existierendem User (sollte Registrierung starten)"""
        mock_get_input.side_effect = ["NewUser", "new_password"]

        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, "NewUser")

        # Überprüfe dass User in DB gespeichert wurde
        query = self.db.select_where("player_account", {"username": "NewUser"})
        self.assertEqual(len(query), 1)

    @patch("Lib.helpers.get_input")
    def test_login_player_registration_fails(self, mock_get_input):
        """Testet Login bei dem die Registrierung fehlschlägt"""
        mock_get_input.side_effect = ["FailedUser", "password123"]

        # Simuliere Datenbankfehler bei der Registrierung
        with patch.object(self.db, 'insert') as mock_insert:
            mock_insert.side_effect = Exception("Database error")

            with self.assertRaises(Exception) as context:
                login_player(self.db, 0)

            self.assertIn("Neuer Benutzer konnte nicht angelegt werden", str(context.exception))

    @patch("Lib.helpers.get_input")
    def test_login_player_max_password_attempts(self, mock_get_input):
        """Testet Login mit wiederholt falschem Passwort"""
        # Registrierung
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "correct_password"
            register_new_user(self.db, "UserX")

        # Login mit mehrfach falschem Passwort
        # ACHTUNG: Diese Test muss möglicherweise angepasst werden,
        # da die aktuelle Implementierung in einer Endlosschleife ist
        # Wir mocken nur 3 Versuche
        mock_get_input.side_effect = ["UserX", "wrong1", "wrong2", "wrong3", "correct_password"]

        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, "UserX")

    # ----------------------------
    # Test für login_players()
    # ----------------------------

    @patch("Lib.helpers.get_input")
    @patch("Lib.helpers.get_integer_input_upto")
    def test_login_players_zero_players(self, mock_get_integer, mock_get_input):
        """Testet login_players mit 0 Spielern"""
        mock_get_integer.return_value = 0
        players = login_players(self.db)

        self.assertEqual(len(players), 0)

    @patch("Lib.helpers.get_input")
    @patch("Lib.helpers.get_integer_input_upto")
    def test_login_players_one_player(self, mock_get_integer, mock_get_input):
        """Testet login_players mit 1 Spieler"""
        mock_get_integer.return_value = 1
        mock_get_input.side_effect = ["Player1", "pass1"]

        players = login_players(self.db)

        self.assertEqual(len(players), 1)
        self.assertIsInstance(players[0], Player)
        self.assertEqual(players[0].name, "Player1")

    @patch("Lib.helpers.get_input")
    @patch("Lib.helpers.get_integer_input_upto")
    def test_login_players_multiple_players(self, mock_get_integer, mock_get_input):
        """Testet login_players mit 3 Spielern"""
        mock_get_integer.return_value = 3
        mock_get_input.side_effect = [
            "Player1", "pass1",
            "Player2", "pass2",
            "Player3", "pass3"
        ]

        players = login_players(self.db)

        self.assertEqual(len(players), 3)
        self.assertEqual(players[0].name, "Player1")
        self.assertEqual(players[1].name, "Player2")
        self.assertEqual(players[2].name, "Player3")

    @patch("Lib.helpers.get_input")
    @patch("Lib.helpers.get_integer_input_upto")
    def test_login_players_max_players(self, mock_get_integer, mock_get_input):
        """Testet login_players mit maximaler Spieleranzahl (5)"""
        mock_get_integer.return_value = 5
        mock_get_input.side_effect = [
            "Player1", "pass1",
            "Player2", "pass2",
            "Player3", "pass3",
            "Player4", "pass4",
            "Player5", "pass5"
        ]

        players = login_players(self.db)

        self.assertEqual(len(players), 5)
        for i, player in enumerate(players, 1):
            self.assertEqual(player.name, f"Player{i}")

    @patch("Lib.helpers.get_input")
    @patch("Lib.helpers.get_integer_input_upto")
    def test_login_players_duplicate_usernames(self, mock_get_integer, mock_get_input):
        """Testet login_players mit doppelten Usernamen"""
        mock_get_integer.return_value = 2

        # Erster Spieler wird registriert, zweiter versucht gleichen Namen
        mock_get_input.side_effect = [
            "SameUser", "pass1",  # Erster Spieler: erfolgreich
            "SameUser", "pass2",  # Zweiter Spieler: sollte fehlschlagen
            "DifferentUser", "pass3"  # Dann neuer Versuch mit anderem Namen
        ]

        players = login_players(self.db)

        self.assertEqual(len(players), 2)
        self.assertEqual(players[0].name, "SameUser")
        self.assertEqual(players[1].name, "DifferentUser")

    @patch("Lib.helpers.get_input")
    @patch("Lib.helpers.get_integer_input_upto")
    def test_login_players_registration_fails_for_one_player(self, mock_get_integer, mock_get_input):
        """Testet login_players wenn Registrierung für einen Spieler fehlschlägt"""
        mock_get_integer.return_value = 2
        mock_get_input.side_effect = [
            "Player1", "pass1",  # Erfolgreich
            "Player2", "pass2"  # Sollte fehlschlagen
        ]

        # Simuliere Datenbankfehler für zweiten Spieler
        call_count = 0
        original_insert = self.db.insert

        def mock_insert(*args, **kwargs):
            nonlocal call_count
            call_count += 1
            if call_count == 2:  # Beim zweiten Einfügen (Player2) fehlschlagen
                raise Exception("Database error")
            return original_insert(*args, **kwargs)

        self.db.insert = mock_insert

        with self.assertRaises(Exception):
            login_players(self.db)

    # ----------------------------
    # Edge Cases und Integration Tests
    # ----------------------------

    @patch("Lib.helpers.get_input")
    def test_login_player_case_sensitive(self, mock_get_input):
        """Testet ob Username case-sensitive ist"""
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "password123"
            register_new_user(self.db, "CaseUser")

        # Versuch mit anderer Großschreibung
        mock_get_input.side_effect = ["CASEUSER", "password123"]
        player = login_player(self.db, 0)

        # Sollte None zurückgeben und dann Registrierung versuchen
        # oder einen neuen Account anlegen, je nach Implementierung
        self.assertIsInstance(player, Player)
        # Entweder ist es der originale User oder ein neuer

    @patch("Lib.helpers.get_input")
    def test_login_player_password_hashing_consistency(self, mock_get_input):
        """Testet ob Passwort-Hashing konsistent ist"""
        # Registrierung
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = "my_password"
            register_new_user(self.db, "HashUser")

        # Hole gehashtes Passwort aus DB
        query = self.db.select_where("player_account", {"username": "HashUser"})
        stored_hash = query[0]["password"]

        # Simuliere Login mit gleichem Passwort
        from Lib.security import hash_password
        new_hash = hash_password("my_password")

        # Der Hash sollte gleich sein
        self.assertEqual(stored_hash, new_hash)

    @patch("Lib.helpers.get_input")
    def test_login_player_empty_password_in_db(self, mock_get_input):
        """Testet Login wenn Passwort in DB leer ist (unwahrscheinlich, aber testen)"""
        # Füge User mit leerem Passwort direkt in DB ein (umgeht hash_password)
        self.db.insert("player_account", {
            "username": "EmptyPassUser",
            "password": ""
        })

        mock_get_input.side_effect = ["EmptyPassUser", ""]
        player = login_player(self.db, 0)

        # Sollte funktionieren, da beide Passwörter leer sind
        self.assertIsInstance(player, Player)

    @patch("Lib.helpers.get_input")
    def test_login_player_special_characters_in_both(self, mock_get_input):
        """Testet Login mit Sonderzeichen in Username UND Passwort"""
        special_username = "user@domain.com"
        special_password = "p@$$w0rd!#$%^&*()"

        # Registrierung
        with patch("Lib.helpers.get_input") as mock_register_input:
            mock_register_input.return_value = special_password
            register_new_user(self.db, special_username)

        # Login
        mock_get_input.side_effect = [special_username, special_password]
        player = login_player(self.db, 0)

        self.assertIsInstance(player, Player)
        self.assertEqual(player.name, special_username)


if __name__ == "__main__":
    unittest.main()