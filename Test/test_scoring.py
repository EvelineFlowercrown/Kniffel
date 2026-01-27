from Lib.point_counters import *


class TestKniffelFunctions:
    """Testklasse für die Kniffel/Yahtzee-Funktionen"""

    # Test für counts()
    def test_counts(self):
        """Testet die counts Funktion"""
        assert counts([1, 1, 1, 2, 3]) == {1: 3, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0}
        assert counts([5, 5, 5, 5, 5]) == {1: 0, 2: 0, 3: 0, 4: 0, 5: 5, 6: 0}
        assert counts([1, 2, 3, 4, 5]) == {1: 1, 2: 1, 3: 1, 4: 1, 5: 1, 6: 0}
        assert counts([]) == {1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0}

    # Test für oberePunkte()
    def test_oberePunkte(self):
        """Testet die oberePunkte Funktion"""
        counts_dict = {1: 3, 2: 1, 3: 1, 4: 0, 5: 0, 6: 0}
        assert oberePunkte(counts_dict) == {1: 3, 2: 2, 3: 3, 4: 0, 5: 0, 6: 0}

        counts_dict = {1: 0, 2: 0, 3: 0, 4: 0, 5: 5, 6: 0}
        assert oberePunkte(counts_dict) == {1: 0, 2: 0, 3: 0, 4: 0, 5: 25, 6: 0}

    # Test für dreierPasch()
    def test_dreierPasch(self):
        """Testet die dreierPasch Funktion"""
        # Mit Dreierpasch
        counts_dict = counts([1, 1, 1, 2, 3])
        assert dreierPasch(counts_dict, [1, 1, 1, 2, 3]) == 8

        # Ohne Dreierpasch
        counts_dict = counts([1, 1, 2, 2, 3])
        assert dreierPasch(counts_dict, [1, 1, 2, 2, 3]) == 0

        # Mit Viererpasch (sollte auch als Dreierpasch zählen)
        counts_dict = counts([1, 1, 1, 1, 3])
        assert dreierPasch(counts_dict, [1, 1, 1, 1, 3]) == 7

    # Test für viererPasch()
    def test_viererPasch(self):
        """Testet die viererPasch Funktion"""
        # Mit Viererpasch
        counts_dict = counts([1, 1, 1, 1, 3])
        assert viererPasch(counts_dict, [1, 1, 1, 1, 3]) == 7

        # Ohne Viererpasch
        counts_dict = counts([1, 1, 1, 2, 3])
        assert viererPasch(counts_dict, [1, 1, 1, 2, 3]) == 0

        # Mit Fünferpasch (sollte auch als Viererpasch zählen)
        counts_dict = counts([1, 1, 1, 1, 1])
        assert viererPasch(counts_dict, [1, 1, 1, 1, 1]) == 5

    # Test für fuenferPasch()
    def test_fuenferPasch(self):
        """Testet die fuenferPasch Funktion"""
        # Mit Fünferpasch (Kniffel)
        counts_dict = counts([1, 1, 1, 1, 1])
        assert fuenferPasch(counts_dict) == 50

        # Ohne Fünferpasch
        counts_dict = counts([1, 1, 1, 1, 2])
        assert fuenferPasch(counts_dict) == 0

    # Test für fullHouse()
    def test_fullHouse(self):
        """Testet die fullHouse Funktion"""
        # Mit Full House (3+2)
        counts_dict = counts([1, 1, 1, 2, 2])
        assert fullHouse(counts_dict) == 25

        # Ohne Full House
        counts_dict = counts([1, 1, 1, 1, 2])
        assert fullHouse(counts_dict) == 0

        # Noch ein Full House
        counts_dict = counts([3, 3, 5, 5, 5])
        assert fullHouse(counts_dict) == 25

    # Test für kleineStrasse()
    def test_kleineStrasse(self):
        """Testet die kleineStrasse Funktion"""
        # Kleine Straße vorhanden (1-2-3-4)
        assert kleineStrasse([1, 2, 3, 4, 4]) == 30

        # Kleine Straße vorhanden (2-3-4-5)
        assert kleineStrasse([2, 3, 4, 5, 1]) == 30

        # Kleine Straße vorhanden (3-4-5-6)
        assert kleineStrasse([3, 4, 5, 6, 6]) == 30

        # Kleine Straße vorhanden (3-4-5-6)
        assert kleineStrasse([1, 3, 4, 5, 6]) == 30

        # Große Straße (sollte auch kleine Straße sein)
        assert kleineStrasse([1, 2, 3, 4, 5]) == 30

        # keine Straße
        assert kleineStrasse([1, 2, 4, 5, 6]) == 0

        # keine Straße
        assert kleineStrasse([1, 2, 3, 5, 6]) == 0

        # keine Straße
        assert kleineStrasse([2, 2, 3, 3, 3]) == 0

        # keine Straße
        assert kleineStrasse([2, 2, 2, 2, 2]) == 0


    # Test für grosseStrasse()
    def test_grosseStrasse(self):
        """Testet die grosseStrasse Funktion"""
        # Große Straße (1-2-3-4-5)
        assert grosseStrasse([1, 2, 3, 4, 5]) == 40

        # Große Straße (2-3-4-5-6)
        assert grosseStrasse([2, 3, 4, 5, 6]) == 40

        # Ohne große Straße
        assert grosseStrasse([1, 2, 3, 4, 4]) == 0

        # Falsche Reihenfolge sollte trotzdem erkannt werden
        assert grosseStrasse([5, 4, 3, 2, 1]) == 40

    # Test für chance()
    def test_chance(self):
        """Testet die chance Funktion"""
        assert chance([1, 2, 3, 4, 5]) == 15
        assert chance([5, 5, 5, 5, 5]) == 25
        assert chance([1, 1, 1, 1, 1]) == 5

    # Test für getPointOptions()
    def test_getPointOptions(self):
        """Testet die getPointOptions Funktion"""
        dice = [1, 1, 1, 2, 2]
        available = ["Dreierpasch", "Full House", "Nur 1er zählen", "Chance"]

        result = getPointOptions(dice, available)

        # Überprüfe, dass alle verfügbaren Optionen enthalten sind
        option_names = [opt[0] for opt in result]
        assert "Dreierpasch" in option_names
        assert "Full House" in option_names
        assert "Nur 1er zählen" in option_names
        assert "Chance" in option_names

        # Überprüfe die Werte
        expected_values = {
            "Full House": 25,
            "Dreierpasch": 7,
            "Chance": 7,
            "Nur 1er zählen": 3
        }

        for name, value in result:
            assert value == expected_values[name]

    def test_getPointOptions_sorted_descending(self):
        """Testet, dass getPointOptions absteigend sortiert"""
        dice = [1, 1, 1, 2, 2]
        available = ["Dreierpasch", "Full House", "Nur 1er zählen", "Chance"]

        result = getPointOptions(dice, available)

        # Überprüfe Sortierung (absteigend nach Wert)
        values = [value for _, value in result]
        assert values == sorted(values, reverse=True)

    def test_getPointOptions_empty_available(self):
        """Testet getPointOptions mit leerer available-Liste"""
        dice = [1, 1, 1, 2, 2]
        available = []

        result = getPointOptions(dice, available)
        assert result == []

    def test_getPointOptions_all_options(self):
        """Testet getPointOptions mit allen möglichen Optionen"""
        dice = [1, 2, 3, 4, 5]
        available = [
            "Kniffel", "Große Straße", "Kleine Straße", "Full House",
            "Viererpasch", "Dreierpasch", "Nur 1er zählen", "Nur 2er zählen",
            "Nur 3er zählen", "Nur 4er zählen", "Nur 5er zählen", "Nur 6er zählen",
            "Chance"
        ]

        result = getPointOptions(dice, available)

        # Große Straße sollte den höchsten Wert haben (40)
        assert result[0][0] == "Große Straße"
        assert result[0][1] == 40

        # Kleine Straße sollte auch einen Wert haben (30)
        for name, value in result:
            if name == "Kleine Straße":
                assert value == 30
