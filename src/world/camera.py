import pygame

from src.settings import WIDTH, WORLD_WIDTH


class Camera:

    def __init__(self):

        self.x = 0

    def update(self, target):

        target_x = target.rect.centerx - WIDTH // 2

        # Smooth camera movement
        self.x += (target_x - self.x) * 0.1

        # Left boundary
        if self.x < 0:
            self.x = 0

        # Right boundary
        max_camera_x = WORLD_WIDTH - WIDTH

        if self.x > max_camera_x:
            self.x = max_camera_x

    def apply(self, rect):

        return pygame.Rect(
            rect.x - int(self.x),
            rect.y,
            rect.width,
            rect.height
        )