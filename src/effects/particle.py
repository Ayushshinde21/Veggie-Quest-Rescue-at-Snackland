import pygame
import random


class Particle:
    def __init__(self, x, y, color, size=4, lifetime=30):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.lifetime = lifetime
        self.max_lifetime = lifetime

        self.velocity_x = random.uniform(-2, 2)
        self.velocity_y = random.uniform(-3, -1)

        self.gravity = 0.15

    def update(self):
        self.x += self.velocity_x
        self.y += self.velocity_y

        self.velocity_y += self.gravity

        self.lifetime -= 1

    def draw(self, screen, camera):
        if self.lifetime <= 0:
            return

        screen_x = int(self.x - camera.x)
        screen_y = int(self.y)

        progress = self.lifetime / self.max_lifetime
        current_size = max(1, int(self.size * progress))

        pygame.draw.circle(
            screen,
            self.color,
            (screen_x, screen_y),
            current_size
        )

    def is_alive(self):
        return self.lifetime > 0