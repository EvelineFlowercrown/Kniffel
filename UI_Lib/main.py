import sys
import pygame
from UI_Lib.game import Game



def main():
    pygame.init()

    # Fenster erstellen (volle Bildschirmgröße oder feste Größe)
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
    WIDTH, HEIGHT = screen.get_size()
    pygame.display.set_caption("Kniffel von Wish bestellt")

    # Hintergrund laden (dein originales Hintergrundbild)
    try:
        background = pygame.image.load("background.jpg").convert()
        background = pygame.transform.scale(background, (WIDTH, HEIGHT))
    except:
        # Fallback falls Bild nicht gefunden
        background = pygame.Surface((WIDTH, HEIGHT))
        background.fill((50, 100, 150))  # Blauer Hintergrund

    clock = pygame.time.Clock()
    game = Game(WIDTH, HEIGHT)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_SPACE:
                    if game.game_over:
                        # Neues Spiel starten
                        game = Game(WIDTH, HEIGHT)
                    elif game.rolls_left > 0:
                        game.roll_dice()
                elif pygame.K_1 <= event.key <= pygame.K_5:
                    index = event.key - pygame.K_1
                    if 0 <= index < len(game.dice) and game.rolls_left < 3:
                        game.dice[index].toggle_hold()

            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()

                # Würfel klicken
                for dice in game.dice:
                    if dice.rect.collidepoint(pos) and game.rolls_left < 3:
                        dice.toggle_hold()

                # Würfeln Button
                if game.roll_button.is_clicked(pos) and game.rolls_left > 0 and not game.game_over:
                    game.roll_dice()

                # Zug beenden Button
                if game.end_turn_button.is_clicked(pos) and game.rolls_left < 3 and not game.game_over:
                    # Nur wenn mindestens 1 Wurf gemacht wurde
                    if game.rolls_left < 3:
                        game.message = "Wähle eine Kategorie aus der Tabelle!"
                    else:
                        game.message = "Du musst mindestens einmal würfeln!"

                # Kategorie auswählen
                if game.rolls_left < 3 and not game.game_over:
                    for i, category in enumerate(game.categories):
                        if category.rect.collidepoint(pos) and category.value is None:
                            game.select_category(i)

        # Spiel zeichnen
        game.draw(screen, background)

        # Anzeige aktualisieren
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()