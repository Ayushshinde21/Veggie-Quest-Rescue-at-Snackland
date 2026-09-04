import pygame


class NPC:
    def __init__(self, x, y, width=40, height=60, name="NPC", dialogue=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = (80, 180, 255)

        self.name = name

        self.dialogue = dialogue or [
            "Hello, Carrot!",
            "Welcome to Snackland!"
        ]

    def draw(self, screen, camera):
        screen_rect = camera.apply(self.rect)

        # Body
        pygame.draw.rect(
            screen,
            self.color,
            screen_rect
        )

        # Head
        pygame.draw.circle(
            screen,
            (255, 220, 180),
            (
                screen_rect.centerx,
                screen_rect.top - 10
            ),
            15
        )