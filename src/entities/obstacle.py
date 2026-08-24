import pygame


class Obstacle:

    def __init__(
        self,
        x,
        y,
        width=40,
        height=40,
        obstacle_type="rock"
    ):

        # ==========================================
        # POSITION
        # ==========================================

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        # ==========================================
        # TYPE
        # ==========================================

        self.obstacle_type = obstacle_type

        # ==========================================
        # STATE
        # ==========================================

        self.active = True

    # ==============================================
    # COLLISION
    # ==============================================

    def check_collision(self, player):

        if not self.active:
            return False

        return self.rect.colliderect(
            player.rect
        )

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen, camera):

        if not self.active:
            return

        camera_rect = camera.apply(
            self.rect
        )

        # ==========================================
        # ROCK
        # ==========================================

        if self.obstacle_type == "rock":

            pygame.draw.ellipse(
                screen,
                (90, 90, 90),
                camera_rect
            )

            # Highlight

            highlight = pygame.Rect(
                camera_rect.x + 8,
                camera_rect.y + 6,
                camera_rect.width // 3,
                camera_rect.height // 4
            )

            pygame.draw.ellipse(
                screen,
                (130, 130, 130),
                highlight
            )

            # Bottom shadow

            pygame.draw.arc(
                screen,
                (50, 50, 50),
                camera_rect,
                0,
                3.14,
                3
            )