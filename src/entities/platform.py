import pygame

from src.entities.game_object import GameObject


class Platform(GameObject):

    def __init__(self, x, y, width, height=20):

        super().__init__(
            x,
            y,
            width,
            height
        )

    def draw(self, screen):

        # Main platform
        pygame.draw.rect(
            screen,
            (100, 70, 40),
            self.rect
        )

        # Grass on top
        pygame.draw.rect(
            screen,
            (70, 180, 70),
            (
                self.rect.x,
                self.rect.y,
                self.rect.width,
                5
            )
        )