import pygame


class Checkpoint:

    def __init__(self, x, y):

        self.x = x
        self.y = y

        self.rect = pygame.Rect(
            x,
            y - 50,
            20,
            50
        )

        self.activated = False

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self, player):

        if self.rect.colliderect(
            player.rect
        ):
            self.activated = True

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen, camera):

        screen_rect = self.rect.copy()

        screen_rect = camera.apply(
            screen_rect
        )

        # Pole
        pygame.draw.rect(
            screen,
            (80, 80, 80),
            screen_rect
        )

        # Flag
        flag_color = (
            (80, 200, 80)
            if self.activated
            else (200, 80, 80)
        )

        pygame.draw.polygon(
            screen,
            flag_color,
            [
                (
                    screen_rect.right,
                    screen_rect.top
                ),
                (
                    screen_rect.right + 25,
                    screen_rect.top + 10
                ),
                (
                    screen_rect.right,
                    screen_rect.top + 20
                )
            ]
        )