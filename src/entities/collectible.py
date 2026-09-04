import pygame


class Collectible:

    def __init__(self, x, y, size=24, value=10):

        self.rect = pygame.Rect(
            x,
            y,
            size,
            size
        )
        self.value = value
        self.collected = False

    def collect(self):
        self.collected = True

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self, player):

        if self.collected:
            return

        if self.rect.colliderect(
            player.rect
        ):
            self.collected = True

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen, camera):

        if self.collected:
            return

        screen_rect = camera.apply(
            self.rect
        )

        # Outer carrot/collectible body
        pygame.draw.circle(
            screen,
            (255, 170, 40),
            screen_rect.center,
            self.rect.width // 2
        )

        # Highlight
        pygame.draw.circle(
            screen,
            (255, 220, 80),
            (
                screen_rect.centerx - 4,
                screen_rect.centery - 4
            ),
            4
        )