import sqlite3
from typing import List, Optional, Any, Dict, Tuple


class SQLiteDB:
    def __init__(self, db_name: str = "database.db"):
        """Initialisiert die Datenbankverbindung"""
        self.db_name = db_name
        self.connection = None
        self.cursor = None
        self.connect()

    def connect(self):
        """Stellt die Verbindung zur Datenbank her"""
        try:
            self.connection = sqlite3.connect(self.db_name)
            self.connection.row_factory = sqlite3.Row  # Ermöglicht Spaltenzugriff per Name
            self.cursor = self.connection.cursor()
            print(f"✓ Verbindung zu '{self.db_name}' hergestellt")
        except sqlite3.Error as e:
            print(f"✗ Verbindungsfehler: {e}")

    def create_table(self, table_name: str, columns: Dict[str, str]):
        """
        Erstellt eine Tabelle

        Args:
            table_name: Name der Tabelle
            columns: Dictionary mit Spaltennamen und Datentypen
                Beispiel: {"id": "INTEGER PRIMARY KEY", "name": "TEXT", "age": "INTEGER"}
        """
        if not columns:
            raise ValueError("Mindestens eine Spalte muss definiert werden")

        columns_def = ", ".join([f"{col} {dtype}" for col, dtype in columns.items()])
        sql = f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_def})"

        try:
            self.cursor.execute(sql)
            self.connection.commit()
            print(f"✓ Tabelle '{table_name}' erstellt/geprüft")
        except sqlite3.Error as e:
            print(f"✗ Fehler beim Erstellen der Tabelle: {e}")

    def insert(self, table_name: str, data: Dict[str, Any]) -> int:
        """
        Fügt einen Datensatz ein

        Args:
            table_name: Name der Tabelle
            data: Dictionary mit Spaltennamen und Werten

        Returns:
            ID des eingefügten Datensatzes
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?"] * len(data))
        values = list(data.values())

        sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            last_id = self.cursor.lastrowid
            print(f"✓ Datensatz in '{table_name}' eingefügt (ID: {last_id})")
            return last_id
        except sqlite3.Error as e:
            print(f"✗ Fehler beim Einfügen: {e}")
            return -1

    def select_all(self, table_name: str, columns: List[str] = None) -> List[sqlite3.Row]:
        """
        Liest alle Datensätze einer Tabelle

        Args:
            table_name: Name der Tabelle
            columns: Liste der abzufragenden Spalten (None für alle)

        Returns:
            Liste der Datensätze
        """
        cols = "*" if columns is None else ", ".join(columns)
        sql = f"SELECT {cols} FROM {table_name}"

        try:
            self.cursor.execute(sql)
            rows = self.cursor.fetchall()
            print(f"✓ {len(rows)} Datensätze aus '{table_name}' gelesen")
            return rows
        except sqlite3.Error as e:
            print(f"✗ Fehler beim Lesen: {e}")
            return []

    def select_where(self, table_name: str,
                     conditions: Dict[str, Any] = None,
                     columns: List[str] = None) -> List[sqlite3.Row]:
        """
        Liest Datensätze mit WHERE-Bedingungen

        Args:
            table_name: Name der Tabelle
            conditions: Dictionary mit WHERE-Bedingungen
            columns: Liste der abzufragenden Spalten

        Returns:
            Liste der gefundenen Datensätze
        """
        cols = "*" if columns is None else ", ".join(columns)

        if conditions:
            where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
            values = list(conditions.values())
            sql = f"SELECT {cols} FROM {table_name} WHERE {where_clause}"
        else:
            sql = f"SELECT {cols} FROM {table_name}"
            values = []

        try:
            self.cursor.execute(sql, values)
            rows = self.cursor.fetchall()
            print(f"✓ {len(rows)} Datensätze mit Bedingungen gefunden")
            return rows
        except sqlite3.Error as e:
            print(f"✗ Fehler bei selektiver Abfrage: {e}")
            return []

    def update(self, table_name: str,
               data: Dict[str, Any],
               conditions: Dict[str, Any]) -> int:
        """
        Aktualisiert Datensätze

        Args:
            table_name: Name der Tabelle
            data: Dictionary mit zu aktualisierenden Spalten und Werten
            conditions: Dictionary mit WHERE-Bedingungen

        Returns:
            Anzahl der aktualisierten Zeilen
        """
        set_clause = ", ".join([f"{k} = ?" for k in data.keys()])
        where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])

        values = list(data.values()) + list(conditions.values())
        sql = f"UPDATE {table_name} SET {set_clause} WHERE {where_clause}"

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            affected = self.cursor.rowcount
            print(f"✓ {affected} Datensätze in '{table_name}' aktualisiert")
            return affected
        except sqlite3.Error as e:
            print(f"✗ Fehler beim Aktualisieren: {e}")
            return 0

    def delete(self, table_name: str, conditions: Dict[str, Any]) -> int:
        """
        Löscht Datensätze

        Args:
            table_name: Name der Tabelle
            conditions: Dictionary mit WHERE-Bedingungen

        Returns:
            Anzahl der gelöschten Zeilen
        """
        where_clause = " AND ".join([f"{k} = ?" for k in conditions.keys()])
        values = list(conditions.values())
        sql = f"DELETE FROM {table_name} WHERE {where_clause}"

        try:
            self.cursor.execute(sql, values)
            self.connection.commit()
            affected = self.cursor.rowcount
            print(f"✓ {affected} Datensätze aus '{table_name}' gelöscht")
            return affected
        except sqlite3.Error as e:
            print(f"✗ Fehler beim Löschen: {e}")
            return 0

    def execute_custom(self, sql: str, params: Tuple = ()) -> List[sqlite3.Row]:
        """
        Führt eine benutzerdefinierte SQL-Abfrage aus

        Args:
            sql: SQL-Befehl
            params: Parameter für Platzhalter

        Returns:
            Ergebnis der Abfrage
        """
        try:
            self.cursor.execute(sql, params)

            if sql.strip().upper().startswith("SELECT"):
                result = self.cursor.fetchall()
                print(f"✓ Benutzerdefinierte SELECT-Abfrage ausgeführt")
                return result
            else:
                self.connection.commit()
                affected = self.cursor.rowcount
                print(f"✓ Benutzerdefinierte Abfrage ausgeführt ({affected} Zeilen betroffen)")
                return []
        except sqlite3.Error as e:
            print(f"✗ Fehler bei benutzerdefinierter Abfrage: {e}")
            return []

    def get_table_info(self, table_name: str) -> List[sqlite3.Row]:
        """Gibt Informationen über die Tabellenstruktur zurück"""
        return self.execute_custom(f"PRAGMA table_info({table_name})")

    def drop_table(self, table_name: str):
        """Löscht eine Tabelle"""
        self.execute_custom(f"DROP TABLE IF EXISTS {table_name}")
        print(f"✓ Tabelle '{table_name}' gelöscht (falls vorhanden)")

    def close(self):
        """Schließt die Datenbankverbindung"""
        if self.connection:
            self.connection.close()
            print("✓ Datenbankverbindung geschlossen")

    def __enter__(self):
        """Unterstützung für with-Kontextmanager"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Automatisches Schließen im with-Block"""
        self.close()
