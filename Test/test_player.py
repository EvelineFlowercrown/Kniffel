import unittest
from unittest.mock import patch
from Lib.player import Player
from Lib.game import GameSheet


class TestPlayer(unittest.TestCase):

    def setUp(self):
        self.player = Player("Testspieler")

    # ----------------------------
    # Test für roll_phase
    # ----------------------------
    @patch("Lib.helpers.get_integer_input_upto")
    @patch("Lib.dice_class.roll_dice")
    def test_roll_phase_keep_all(self, mock_roll_dice, mock_input_upto):
        # Simuliere, dass alle Würfel behalten werden
        mock_roll_dice.return_value = [1, 1, 5, 1, 5]
        mock_input_upto.return_value = 5  # alle behalten

        final_dice = self.player.roll_phase()
        self.assertEqual(final_dice, [1, 1, 5, 1, 5])

    #@patch("Lib.helpers.get_integer_input_upto")
    #@patch("Lib.helpers.get_integer_input")
    #@patch("Lib.dice_class.roll_dice")
    #def test_roll_phase_partial_keep(self, mock_roll_dice, mock_input, mock_input_upto):
    #    # Roll: [1,2,3,4,5], behalte die ersten 2
    #    mock_roll_dice.side_effect = [[1, 2, 3, 4, 5], [3, 4, 5]]  # zweite Runde nur die restlichen
    #    mock_input_upto.side_effect = [2, 3]  # zuerst 2 behalten, dann 3 behalten
    #    mock_input.side_effect = [1, 2, 1, 2, 3]  # Positionen zum Behalten
    #    final_dice = self.player.roll_phase()
    #    # Erwartet: alle Würfel gesammelt
    #    self.assertEqual(final_dice, [1, 2, 1, 2, 3, 4, 5])

    # ----------------------------
    # Test für calculate_options
    # ----------------------------
    def test_calculate_options(self):
        dice = [1, 1, 5, 1, 5]
        available = self.player.gameSheet.getAvailable()
        options = self.player.calculate_options(dice)
        categories = [cat for cat, _ in options]

        # Erwartet, dass Chance, Dreierpasch und nur 1er/5er dabei sind
        self.assertIn("Chance", categories)
        self.assertIn("Dreierpasch", categories)
        self.assertIn("Nur 1er zählen", categories)
        self.assertIn("Nur 5er zählen", categories)

    # ----------------------------
    # Test für apply_choice
    # ----------------------------
    def test_apply_choice_upper(self):
        self.player.apply_choice(("Nur 3er zählen", 9))
        self.assertEqual(self.player.gameSheet.obere["Nur 3er zählen"], 9)

    def test_apply_choice_lower(self):
        self.player.apply_choice(("Kniffel", 50))
        self.assertEqual(self.player.gameSheet.untere["Kniffel"], 50)

    # ----------------------------
    # Test für choose_option
    # ----------------------------
    @patch("Lib.helpers.get_integer_input")
    def test_choose_option(self, mock_input):
        options = [("Dreierpasch", 9), ("Chance", 15)]
        mock_input.return_value = 2  # wählt Chance
        choice = self.player.choose_option(options)
        self.assertEqual(choice, ("Chance", 15))

    # ----------------------------
    # Test für post_turn_menu (nur T/Ausgabe)
    # ----------------------------
    @patch("Lib.helpers.get_input")
    @patch.object(GameSheet, "printTable")
    def test_post_turn_menu(self, mock_printTable, mock_input):
        mock_input.return_value = "t"
        self.player.post_turn_menu()
        mock_printTable.assert_called_once()

    @patch("Lib.helpers.get_input")
    @patch.object(GameSheet, "printTable")
    def test_post_turn_menu_continue(self, mock_printTable, mock_input):
        mock_input.return_value = "n"
        self.player.post_turn_menu()
        mock_printTable.assert_not_called()


if __name__ == "__main__":
    unittest.main()
