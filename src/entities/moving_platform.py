import pygame

from src.entities.platform import Platform


class MovingPlatform(Platform):

    def __init__(
        self,
        x,
        y,
        width,
        height=20,
        movement_type="horizontal",
        movement_distance=120,
        movement_speed=1.0
    ):

        super().__init__(
            x,
            y,
            width,
            height
        )

        # ==========================================
        # MOVEMENT SETTINGS
        # ==========================================

        self.movement_type = movement_type
        self.movement_distance = movement_distance
        self.movement_speed = movement_speed

        # ==========================================
        # ORIGINAL POSITION
        # ==========================================

        self.start_x = x
        self.start_y = y

        # ==========================================
        # DIRECTION
        # ==========================================

        self.direction = 1

        # ==========================================
        # OFFSET
        # ==========================================

        self.offset = 0.0
        self.previous_x = self.rect.x
        self.previous_y = self.rect.y

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self):

        self.previous_x = self.rect.x
        self.previous_y = self.rect.y

        self.offset += (
            self.movement_speed
            * self.direction
        )

        # ==========================================
        # HORIZONTAL ONLY
        # ==========================================

        if self.movement_type == "horizontal":

            self.rect.x = int(
                self.start_x + self.offset
            )

            # Keep Y completely fixed

            self.rect.y = self.start_y

        # ==========================================
        # VERTICAL ONLY
        # ==========================================

        elif self.movement_type == "vertical":

            self.rect.y = int(
                self.start_y + self.offset
            )

            # Keep X completely fixed

            self.rect.x = self.start_x

        # ==========================================
        # REVERSE
        # ==========================================

        if abs(self.offset) >= self.movement_distance:

            self.offset = (
                self.movement_distance
                * self.direction
            )

            self.direction *= -1

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen, camera):

        camera_rect = camera.apply(
            self.rect
        )

        # Platform body

        pygame.draw.rect(
            screen,
            (90, 90, 100),
            camera_rect
        )

        # Platform top

        pygame.draw.rect(
            screen,
            (180, 190, 200),
            (
                camera_rect.x,
                camera_rect.y,
                camera_rect.width,
                5
            )
        )