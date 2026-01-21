import pygame
import sys
import random
from typing import List, Tuple, Dict, Optional

# region Konstanten

FPS = 60
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (30, 144, 255)
GREEN = (50, 205, 50)
RED = (220, 20, 60)
GRAY = (200, 200, 200)
DARK_GRAY = (120, 120, 120)
YELLOW = (255, 215, 0)

# Würfelgröße
DICE_SIZE = 80
DICE_MARGIN = 10

# endregion Konstanten

# Initialisierung von Pygame
pygame.init()

# Konstanten

FPS = 60

# Farben
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Fenster erstellen
screen = pygame.display.set_mode()
WIDTH, HEIGHT = screen.get_size()
pygame.display.set_caption("Kniffel von Wish bestellt")
background_image = pygame.image.load("../background.jpg").convert()
background_image = pygame.transform.scale(surface=background_image, size=(WIDTH, HEIGHT))
# Spielvariablen
clock = pygame.time.Clock()
running = True

# Haupt-Spiel Schleife
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Hintergrundfarbe
    screen.blit(background_image, (0, 0))

    # Spiel-Logik hier

    # Anzeige aktualisieren
    pygame.display.flip()

    # Frame Rate steuern
    clock.tick(FPS)

# Pygame beenden
pygame.quit()
sys.exit()
