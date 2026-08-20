import pygame
import random

from src.settings import HEIGHT, WORLD_WIDTH
from src.entities.player import Player
from src.entities.platform import Platform
from src.world.camera import Camera
from src.world.platform_generator import PlatformGenerator


class Level:

    def __init__(self, seed=None):

        # ==========================================
        # LEVEL SEED
        # ==========================================

        # If no seed is provided, generate a random one
        if seed is None:
            seed = random.randint(
                0,
                999999999
            )

        self.seed = seed

        # Make random generation reproducible
        random.seed(self.seed)

        # ==========================================
        # WORLD
        # ==========================================

        self.width = WORLD_WIDTH

        # ==========================================
        # CAMERA
        # ==========================================

        self.camera = Camera()

        # ==========================================
        # GROUND
        # ==========================================

        self.ground = Platform(
            0,
            HEIGHT - 80,
            self.width,
            80
        )

        # ==========================================
        # RANDOM PLATFORMS
        # ==========================================

        self.generator = PlatformGenerator(
            self.width
        )

        self.platforms = self.generator.generate()

        # Add ground to collision list
        self.platforms.insert(
            0,
            self.ground
        )

        # ==========================================
        # PLAYER
        # ==========================================

        self.player = Player(
            100,
            HEIGHT - 160
        )

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self):

        self.player.update(
            self.platforms
        )

        self.camera.update(
            self.player
        )

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen):

        # ==========================================
        # DRAW GROUND
        # ==========================================

        ground_rect = self.camera.apply(
            self.ground.rect
        )

        # Main ground
        pygame.draw.rect(
            screen,
            (80, 180, 80),
            ground_rect
        )

        # Darker soil
        soil_rect = pygame.Rect(
            ground_rect.x,
            ground_rect.y + 8,
            ground_rect.width,
            ground_rect.height - 8
        )

        pygame.draw.rect(
            screen,
            (100, 70, 40),
            soil_rect
        )

        # Grass top
        pygame.draw.rect(
            screen,
            (50, 160, 50),
            (
                ground_rect.x,
                ground_rect.y,
                ground_rect.width,
                8
            )
        )

        # ==========================================
        # DRAW RANDOM PLATFORMS
        # ==========================================

        for platform in self.platforms:

            # Don't draw ground again
            if platform is self.ground:
                continue

            camera_rect = self.camera.apply(
                platform.rect
            )

            # Platform body
            pygame.draw.rect(
                screen,
                (100, 70, 40),
                camera_rect
            )

            # Grass on top
            pygame.draw.rect(
                screen,
                (70, 180, 70),
                (
                    camera_rect.x,
                    camera_rect.y,
                    camera_rect.width,
                    5
                )
            )

        # ==========================================
        # DRAW PLAYER
        # ==========================================

        player_rect = self.camera.apply(
            self.player.rect
        )

        self.player.draw(
            screen,
            player_rect
        )