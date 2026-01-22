from constants import *
import pygame
import random

# Würfelgröße
DICE_SIZE = 80


class Dice:
    """Klasse für einen Würfel"""

    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.value = 1
        self.held = False
        self.rect = pygame.Rect(x, y, DICE_SIZE, DICE_SIZE)
        self.dot_radius = 8

    def roll(self):
        if not self.held:
            self.value = random.randint(1, 6)

    def toggle_hold(self):
        self.held = not self.held

    def draw(self, screen):
        # Würfel hintergrund mit Schatteneffekt
        pygame.draw.rect(screen, (100, 100, 100),
                         (self.x + 3, self.y + 3, DICE_SIZE, DICE_SIZE), 0, 10)

        color = (255, 200, 100) if self.held else (255, 255, 255)  # Gold wenn gehalten
        pygame.draw.rect(screen, color, self.rect, 0, 10)
        pygame.draw.rect(screen, (0, 0, 0), self.rect, 3, 10)

        # Punkte zeichnen basierend auf Wert
        center_x = self.x + DICE_SIZE // 2
        center_y = self.y + DICE_SIZE // 2
        third = DICE_SIZE // 3

        positions = {
            1: [(center_x, center_y)],
            2: [(center_x - third, center_y - third),
                (center_x + third, center_y + third)],
            3: [(center_x - third, center_y - third),
                (center_x, center_y),
                (center_x + third, center_y + third)],
            4: [(center_x - third, center_y - third),
                (center_x + third, center_y - third),
                (center_x - third, center_y + third),
                (center_x + third, center_y + third)],
            5: [(center_x - third, center_y - third),
                (center_x + third, center_y - third),
                (center_x, center_y),
                (center_x - third, center_y + third),
                (center_x + third, center_y + third)],
            6: [(center_x - third, center_y - third),
                (center_x + third, center_y - third),
                (center_x - third, center_y),
                (center_x + third, center_y),
                (center_x - third, center_y + third),
                (center_x + third, center_y + third)]
        }

        for pos in positions.get(self.value, []):
            pygame.draw.circle(screen, (0, 0, 0), pos, self.dot_radius)

        # "Gehalten" Text unter dem Würfel
        if self.held:
            font = pygame.font.SysFont(None, 20)
            text = font.render("Gehalten", True, (200, 0, 0))
            text_rect = text.get_rect(center=(center_x, self.y + DICE_SIZE + 12))
            screen.blit(text, text_rect)