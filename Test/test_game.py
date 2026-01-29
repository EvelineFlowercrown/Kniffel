import unittest
from Lib import game


class TestGame(unittest.TestCase):

    def setUp(self):
        self.game_sheet = game.GameSheet()

    # ----------------------------
    # Test für getAvailable()
    # ----------------------------

    def test_getAvailable_empty(self):
        self.assertEqual(self.game_sheet.getAvailable(),[
            "Nur 1er zählen",
            "Nur 2er zählen",
            "Nur 3er zählen",
            "Nur 4er zählen",
            "Nur 5er zählen",
            "Nur 6er zählen",
            "Dreierpasch",
            "Viererpasch",
            "Full House",
            "Kleine Straße",
            "Große Straße",
            "Kniffel",
            "Chance",
        ])

    def test_getAvailable_standard(self):
            self.game_sheet.obere.update({
                "Nur 1er zählen": 2,
                "Nur 2er zählen": 6,
                "Nur 3er zählen": 9,
            })
            self.game_sheet.untere.update({
                "Chance": 21,
                "Große Straße": 0,
                "Viererpasch": 22,
            })
            self.assertEqual(self.game_sheet.getAvailable(), [
                "Nur 4er zählen",
                "Nur 5er zählen",
                "Nur 6er zählen",
                "Dreierpasch",
                "Full House",
                "Kleine Straße",
                "Kniffel",
            ])

    def test_getAvailable_full(self):
        self.game_sheet.obere.update({
            "Nur 1er zählen": 1,
            "Nur 2er zählen": 2,
            "Nur 3er zählen": 3,
            "Nur 4er zählen": 4,
            "Nur 5er zählen": 5,
            "Nur 6er zählen": 6,
        })
        self.game_sheet.untere.update({
            "Dreierpasch": 7,
            "Viererpasch": 8,
            "Full House": 9,
            "Kleine Straße": 0,
            "Große Straße": 10,
            "Kniffel": 11,
            "Chance": 12
        })

        self.assertEqual(self.game_sheet.getAvailable(), [])

    # ----------------------------
    # Test für calculate_extras()
    # ----------------------------

    def test_calculate_extras_no_bonus(self):
        self.game_sheet.obere.update({
            "Nur 1er zählen": 1,
            "Nur 2er zählen": 2,
            "Nur 3er zählen": 3,
            "Nur 4er zählen": 4,
            "Nur 5er zählen": 5,
            "Nur 6er zählen": 6,
        })
        self.game_sheet.untere.update({
            "Dreierpasch": 7,
            "Viererpasch": 8,
            "Full House": 9,
            "Kleine Straße": 0,
            "Große Straße": 10,
            "Kniffel": 11,
            "Chance": 12
        })

        self.game_sheet.calculate_extras()

        self.assertEqual(self.game_sheet.extras,{
            "Gesamt Oberer Teil": 21,
            "Bonus 63+": 0,
            "Gesamt Unterer Teil": 57
        })

    def test_calculate_extras_Bonus(self):
        self.game_sheet.obere.update({
            "Nur 1er zählen": 5,
            "Nur 2er zählen": 10,
            "Nur 3er zählen": 15,
            "Nur 4er zählen": 20,
            "Nur 5er zählen": 25,
            "Nur 6er zählen": 30,
        })
        self.game_sheet.untere.update({
            "Dreierpasch": 0,
            "Viererpasch": 0,
            "Full House": 0,
            "Kleine Straße": 0,
            "Große Straße": 0,
            "Kniffel": 0,
            "Chance": 0
        })

        self.game_sheet.calculate_extras()

        self.assertEqual(self.game_sheet.extras, {
            "Gesamt Oberer Teil": 105,
            "Bonus 63+": 35,
            "Gesamt Unterer Teil": 0
        })


    def test_calculate_extras_None(self):
        self.game_sheet.obere.update({
            "Nur 1er zählen": 5,
            "Nur 2er zählen": None,
            "Nur 3er zählen": 15,
            "Nur 4er zählen": 20,
            "Nur 5er zählen": 25,
            "Nur 6er zählen": 30,
        })
        self.game_sheet.untere.update({
            "Dreierpasch": 0,
            "Viererpasch": 0,
            "Full House": None,
            "Kleine Straße": 0,
            "Große Straße": 0,
            "Kniffel": 0,
            "Chance": 0
        })

        self.game_sheet.calculate_extras()

        self.assertEqual(self.game_sheet.extras, {
            "Gesamt Oberer Teil": None,
            "Bonus 63+": None,
            "Gesamt Unterer Teil": None
        })

    # ----------------------------
    # Test für get_total()
    # ----------------------------

    def test_get_total_low(self):
        self.game_sheet.extras.update({
            "Gesamt Oberer Teil": 0,
            "Bonus 63+": 0,
            "Gesamt Unterer Teil": 0
        })
        self.assertEqual(self.game_sheet.get_total(),0)

    def test_get_total_high(self):
        self.game_sheet.extras.update({
            "Gesamt Oberer Teil": 65,
            "Bonus 63+": 35,
            "Gesamt Unterer Teil": 150
        })
        self.assertEqual(self.game_sheet.get_total(),250)

    def test_get_total_none(self):
        self.game_sheet.extras.update({
            "Gesamt Oberer Teil": 65,
            "Bonus 63+": None,
            "Gesamt Unterer Teil": 150
        })
        self.assertRaises(ValueError)
    # ----------------------------
    # Test für is_complete()
    # ----------------------------

    def test_is_complete_empty(self):
        self.assertEqual(self.game_sheet.is_complete(),False)



    def test_is_complete_standard(self):
        self.game_sheet.obere.update({
            "Nur 1er zählen": 2,
            "Nur 2er zählen": 6,
            "Nur 3er zählen": 9,
        })
        self.game_sheet.untere.update({
            "Chance": 21,
            "Große Straße": 0,
            "Viererpasch": 22,
        })
        self.assertEqual(self.game_sheet.is_complete(),False)

    def test_is_complete_full(self):
        self.game_sheet.obere.update({
            "Nur 1er zählen": 1,
            "Nur 2er zählen": 2,
            "Nur 3er zählen": 3,
            "Nur 4er zählen": 4,
            "Nur 5er zählen": 5,
            "Nur 6er zählen": 6,
        })
        self.game_sheet.untere.update({
            "Dreierpasch": 7,
            "Viererpasch": 8,
            "Full House": 9,
            "Kleine Straße": 0,
            "Große Straße": 10,
            "Kniffel": 11,
            "Chance": 12
        })

        self.assertEqual(self.game_sheet.is_complete(),True)