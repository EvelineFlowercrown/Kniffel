import pygame
from constants import *

class Button:
    """Klasse für einen Button"""

    def __init__(self, x: int, y: int, width: int, height: int, text: str):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = BLUE
        self.hover_color = (70, 130, 180)
        self.current_color = self.color
        self.font = pygame.font.SysFont(None, 32)

    def draw(self, screen):
        # Hover-Effekt
        mouse_pos = pygame.mouse.get_pos()
        if self.rect.collidepoint(mouse_pos):
            self.current_color = self.hover_color
        else:
            self.current_color = self.color

        pygame.draw.rect(screen, self.current_color, self.rect, 0, 5)
        pygame.draw.rect(screen, BLACK, self.rect, 2, 5)

        text_surf = self.font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)