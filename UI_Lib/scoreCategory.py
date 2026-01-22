import pygame

from Lib.point_counters import dreierPasch, viererPasch, fullHouse, kleineStrasse, grosseStrasse, fuenferPasch, chance, \
    counts
from constants import *
from typing import List


class ScoreCategory:
    """Klasse für eine Punktekategorie"""

    def __init__(self, name: str, x: int, y: int, width: int, height: int):
        self.name = name
        self.rect = pygame.Rect(x, y, width, height)
        self.value = None
        self.calculated_value = 0
        self.font = pygame.font.SysFont(None, 26)
        self.small_font = pygame.font.SysFont(None, 22)

    def draw(self, screen, dice_values: List[int], is_selectable: bool):
        # Hintergrund - abwechselnde Zeilenfarben für bessere Lesbarkeit
        row_index = int((self.rect.y - 150) / 40)  # Annäherung
        bg_color = (240, 240, 240) if row_index % 2 == 0 else (220, 220, 220)

        if is_selectable:
            if self.calculated_value > 0:
                bg_color = (200, 255, 200)  # Hellgrün für gute Option
            else:
                bg_color = (255, 200, 200)  # Hellrot für schlechte Option

        pygame.draw.rect(screen, bg_color, self.rect)
        pygame.draw.rect(screen, BLACK, self.rect, 1)

        # Name links
        name_text = self.font.render(self.name, True, BLACK)
        screen.blit(name_text, (self.rect.x + 10, self.rect.y + 7))

        # Wert rechts
        value_x = self.rect.right - 60

        if self.value is not None:
            # Endgültiger Wert (schwarz)
            value_text = self.font.render(str(self.value), True, BLACK)
            value_rect = value_text.get_rect(right=value_x, centery=self.rect.centery)
            screen.blit(value_text, value_rect)
        elif is_selectable:
            # Berechneten Wert für aktuelle Würfel anzeigen (blau)
            value_text = self.font.render(str(self.calculated_value), True, BLUE)
            value_rect = value_text.get_rect(right=value_x, centery=self.rect.centery)
            screen.blit(value_text, value_rect)
        else:
            # Platzhalter für noch nicht verfügbare Kategorie
            value_text = self.small_font.render("-", True, GRAY)
            value_rect = value_text.get_rect(right=value_x, centery=self.rect.centery)
            screen.blit(value_text, value_rect)

    def calculate_value(self, dice_values: List[int]):
        """Berechnet den Wert basierend auf aktuellen Würfeln"""

        dice_counts = counts(dice_values)

        if self.name == "Nur 1er zählen":
            self.calculated_value = dice_counts[1] * 1
        elif self.name == "Nur 2er zählen":
            self.calculated_value = dice_counts[2] * 2
        elif self.name == "Nur 3er zählen":
            self.calculated_value = dice_counts[3] * 3
        elif self.name == "Nur 4er zählen":
            self.calculated_value = dice_counts[4] * 4
        elif self.name == "Nur 5er zählen":
            self.calculated_value = dice_counts[5] * 5
        elif self.name == "Nur 6er zählen":
            self.calculated_value = dice_counts[6] * 6
        elif self.name == "Dreierpasch":
            self.calculated_value = dreierPasch(dice_counts, dice_values)
        elif self.name == "Viererpasch":
            self.calculated_value = viererPasch(dice_counts, dice_values)
        elif self.name == "Full House":
            self.calculated_value = fullHouse(dice_counts)
        elif self.name == "Kleine Straße":
            self.calculated_value = kleineStrasse(dice_values)
        elif self.name == "Große Straße":
            self.calculated_value = grosseStrasse(dice_values)
        elif self.name == "Kniffel":
            self.calculated_value = fuenferPasch(dice_counts)
        elif self.name == "Chance":
            self.calculated_value = chance(dice_values)

        return self.calculated_value
