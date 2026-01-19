import pygame
import sys

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
background_image = pygame.image.load("background.jpg").convert()
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
