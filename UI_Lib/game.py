import pygame

from UI_Lib.dice import Dice
from button import Button
from  scoreCategory import ScoreCategory
from constants import *
import pygame
# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
GRAY = (200, 200, 200)
YELLOW = (255, 215, 0)


class Game:
    """Hauptspielklasse mit neuem Layout"""

    def __init__(self, screen_width: int, screen_height: int):
        self.screen_width = screen_width
        self.screen_height = screen_height

        # Würfel initialisieren - senkrecht rechts
        dice_start_x = screen_width - 120  # 120px vom rechten Rand
        dice_start_y = (screen_height - (5 * 100 + 4 * 15)) // 2  # Zentriert vertikal
        self.dice = [
            Dice(dice_start_x, dice_start_y + i * (100 + 15))
            for i in range(5)
        ]

        # Buttons - am unteren Rand
        button_y = screen_height - 80
        self.roll_button = Button(
            screen_width // 2 - 200, button_y, 180, 50, "WÜRFELN"
        )
        self.end_turn_button = Button(
            screen_width // 2 + 20, button_y, 180, 50, "ZUG BEENDEN"
        )

        # Punktekategorien - senkrechte Tabelle links
        self.categories = []
        category_width = 350
        category_height = 35
        start_x = 50
        start_y = 150

        category_names = [
            "Nur 1er zählen", "Nur 2er zählen", "Nur 3er zählen",
            "Nur 4er zählen", "Nur 5er zählen", "Nur 6er zählen",
            "Dreierpasch", "Viererpasch", "Full House",
            "Kleine Straße", "Große Straße", "Kniffel", "Chance"
        ]

        for i, name in enumerate(category_names):
            x = start_x
            y = start_y + i * (category_height + 5)  # 5px Abstand zwischen Kategorien
            self.categories.append(
                ScoreCategory(name, x, y, category_width, category_height)
            )

        # Spielzustand
        self.rolls_left = 3
        self.current_player = "Spieler 1"
        self.game_over = False
        self.message = "Drücke 'WÜRFELN' um zu beginnen!"

        # Statistik
        self.total_score = 0
        self.turns_left = 13  # 13 Kategorien

    def roll_dice(self):
        if self.rolls_left > 0:
            for dice in self.dice:
                dice.roll()
            self.rolls_left -= 1
            self.message = f"Würfe übrig: {self.rolls_left}"

            # Werte für alle verfügbaren Kategorien berechnen
            dice_values = [d.value for d in self.dice]
            for category in self.categories:
                if category.value is None:
                    category.calculate_value(dice_values)

    def reset_round(self):
        self.rolls_left = 3
        for dice in self.dice:
            dice.held = False

    def select_category(self, category_index: int):
        category = self.categories[category_index]

        if category.value is None:  # Nur auswählen wenn noch nicht belegt
            dice_values = [d.value for d in self.dice]
            category.value = category.calculate_value(dice_values)
            self.total_score += category.value

            # Runde zurücksetzen
            self.reset_round()
            self.turns_left -= 1
            self.message = f"Kategorie '{category.name}' gewählt! Nächste Runde."

            # Prüfen ob Spiel zu Ende
            if self.turns_left <= 0:
                self.game_over = True
                self.message = f"Spiel beendet! Endstand: {self.total_score} Punkte"

    def draw(self, screen, background):
        # Hintergrund zeichnen
        screen.blit(background, (0, 0))

        # Titelbanner oben
        title_font = pygame.font.SysFont(None, 48)
        title = title_font.render("KNIFFEL", True, WHITE)
        pygame.draw.rect(screen, BLUE, (0, 0, self.screen_width, 70))
        screen.blit(title, (self.screen_width // 2 - title.get_width() // 2, 20))

        # Spielerinfo links oben
        player_font = pygame.font.SysFont(None, 32)
        player_text = player_font.render(f"Spieler: {self.current_player}", True, WHITE)
        screen.blit(player_text, (60, 85))

        # Punkteanzeige rechts oben
        score_text = player_font.render(f"Punkte: {self.total_score}", True, WHITE)
        screen.blit(score_text, (self.screen_width - 150, 85))

        # Rundeninfo
        turns_text = player_font.render(f"Runden übrig: {self.turns_left}", True, WHITE)
        screen.blit(turns_text, (self.screen_width // 2 - turns_text.get_width() // 2, 85))

        # Würfel anzeigen (rechts)
        dice_label_font = pygame.font.SysFont(None, 32)
        dice_label = dice_label_font.render("WÜRFEL", True, WHITE)
        screen.blit(dice_label, (self.screen_width - 140, 120))

        for dice in self.dice:
            dice.draw(screen)

        # Buttons anzeigen (unten)
        self.roll_button.draw(screen)
        self.end_turn_button.draw(screen)

        # Würfe übrig über Buttons
        rolls_font = pygame.font.SysFont(None, 28)
        rolls_text = rolls_font.render(f"Würfe übrig: {self.rolls_left}", True, YELLOW)
        screen.blit(rolls_text, (self.screen_width // 2 - rolls_text.get_width() // 2, self.screen_height - 120))

        # Kategorien anzeigen (links)
        category_label_font = pygame.font.SysFont(None, 32)
        category_label = category_label_font.render("PUNKTETABELLE", True, WHITE)
        screen.blit(category_label, (60, 120))

        dice_values = [d.value for d in self.dice]
        for category in self.categories:
            is_selectable = (category.value is None and self.rolls_left < 3)
            category.draw(screen, dice_values, is_selectable)

        # Nachricht am unteren Rand
        msg_font = pygame.font.SysFont(None, 28)
        msg_text = msg_font.render(self.message, True, YELLOW)
        screen.blit(msg_text, (self.screen_width // 2 - msg_text.get_width() // 2, self.screen_height - 50))

        # Spielende-Overlay
        if self.game_over:
            overlay = pygame.Surface((self.screen_width, self.screen_height), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 200))  # Halbtransparent schwarz
            screen.blit(overlay, (0, 0))

            end_font = pygame.font.SysFont(None, 64)
            end_text = end_font.render("SPIEL BEENDET!", True, YELLOW)
            screen.blit(end_text, (self.screen_width // 2 - end_text.get_width() // 2, self.screen_height // 2 - 100))

            score_font = pygame.font.SysFont(None, 48)
            score_text = score_font.render(f"Endstand: {self.total_score} Punkte", True, WHITE)
            screen.blit(score_text, (self.screen_width // 2 - score_text.get_width() // 2, self.screen_height // 2))

            restart_font = pygame.font.SysFont(None, 36)
            restart_text = restart_font.render("Leertaste drücken für neues Spiel", True, GREEN)
            screen.blit(restart_text,
                        (self.screen_width // 2 - restart_text.get_width() // 2, self.screen_height // 2 + 80))