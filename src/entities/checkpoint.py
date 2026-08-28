import pygame


class Checkpoint:

    def __init__(self, x, y, checkpoint_id=0):

        # ==========================================
        # POSITION
        # ==========================================

        self.x = x
        self.y = y

        self.checkpoint_id = checkpoint_id

        self.respawn_x = x
        self.respawn_y = y

        # ==========================================
        # CHECKPOINT COLLISION
        # ==========================================

        self.rect = pygame.Rect(
            x,
            y - 50,
            20,
            50
        )

        # ==========================================
        # RESPAWN POSITION
        # ==========================================

        # Player will appear slightly above
        # the bottom of the checkpoint.

        self.respawn_x = x
        self.respawn_y = y - 60

        # ==========================================
        # STATE
        # ==========================================

        self.activated = False

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self, player):

        if self.activated:
            return

        if self.rect.colliderect(player.rect):

            self.activated = True

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen, camera):

        screen_rect = camera.apply(
            self.rect
        )

        # ==========================================
        # POLE
        # ==========================================

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            screen_rect
        )

        # ==========================================
        # FLAG COLOR
        # ==========================================

        if self.activated:

            flag_color = (
                80,
                200,
                80
            )

        else:

            flag_color = (
                200,
                80,
                80
            )

        # ==========================================
        # FLAG
        # ==========================================

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