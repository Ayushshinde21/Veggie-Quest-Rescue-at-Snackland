import pygame
import random

from src.settings import HEIGHT, WORLD_WIDTH
from src.entities.player import Player
from src.entities.platform import Platform
from src.entities.collectible import Collectible
from src.entities.checkpoint import Checkpoint
from src.world.camera import Camera
from src.world.platform_generator import PlatformGenerator


class Level:

    def __init__(self, seed=None):

        # ==========================================
        # LEVEL SEED
        # ==========================================

        if seed is None:
            seed = random.randint(
                0,
                999999999
            )

        self.seed = seed

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

        self.platforms.insert(
            0,
            self.ground
        )

        # ==========================================
        # PLAYER
        # ==========================================

        self.start_x = 100
        self.start_y = HEIGHT - 160

        self.player = Player(
            self.start_x,
            self.start_y
        )

        # ==========================================
        # COLLECTIBLES
        # ==========================================

        self.collectibles = []

        self.generate_collectibles()

        # ==========================================
        # SCORE
        # ==========================================

        self.score = 0

        # ==========================================
        # CHECKPOINTS
        # ==========================================

        self.checkpoints = []

        self.current_checkpoint = None

        self.generate_checkpoints()

        # ==========================================
        # FINISH
        # ==========================================

        self.level_complete = False

        self.finish_x = self.width - 300

        # ==========================================
        # UI
        # ==========================================

        self.font = pygame.font.Font(
            None,
            32
        )

        self.big_font = pygame.font.Font(
            None,
            64
        )

    # ==============================================
    # GENERATE COLLECTIBLES
    # ==============================================

    def generate_collectibles(self):

        self.collectibles.clear()

        for platform in self.platforms[1:]:

            if random.random() > 0.75:
                continue

            margin = 15

            if platform.rect.width <= (
                margin * 2 + 24
            ):
                continue

            x = random.randint(
                platform.rect.left + margin,
                platform.rect.right
                - margin
                - 24
            )

            y = platform.rect.top - 30

            collectible = Collectible(
                x,
                y
            )

            self.collectibles.append(
                collectible
            )

    # ==============================================
    # GENERATE CHECKPOINTS
    # ==============================================

    def generate_checkpoints(self):

        self.checkpoints.clear()

        checkpoint_spacing = 1800

        next_checkpoint_x = checkpoint_spacing

        for platform in self.platforms[1:]:

            if platform.rect.centerx < next_checkpoint_x:
                continue

            checkpoint_x = platform.rect.centerx
            checkpoint_y = platform.rect.top

            checkpoint = Checkpoint(
                checkpoint_x,
                checkpoint_y
            )

            self.checkpoints.append(
                checkpoint
            )

            next_checkpoint_x = (
                checkpoint_x
                + checkpoint_spacing
            )

    # ==============================================
    # RESPAWN
    # ==============================================

    def respawn_player(self):

        if self.current_checkpoint is not None:

            checkpoint = self.current_checkpoint

            self.player.rect.midbottom = (
                checkpoint.rect.centerx,
                checkpoint.rect.top
            )

        else:

            self.player.rect.x = self.start_x
            self.player.rect.y = self.start_y

        self.player.velocity_y = 0

        self.player.on_ground = False

        self.player.coyote_time = 0

    # ==============================================
    # CHECK DEATH
    # ==============================================

    def check_player_death(self):

        if self.player.rect.top > HEIGHT + 300:

            self.respawn_player()

    # ==============================================
    # CHECK LEVEL COMPLETION
    # ==============================================

    def check_level_completion(self):

        if self.player.rect.centerx >= self.finish_x:

            self.level_complete = True

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self):

        # Don't continue normal gameplay
        # after level completion

        if self.level_complete:
            return

        # ------------------------------------------
        # PLAYER
        # ------------------------------------------

        self.player.update(
            self.platforms
        )

        # ------------------------------------------
        # DEATH
        # ------------------------------------------

        self.check_player_death()

        # ------------------------------------------
        # LEVEL COMPLETE
        # ------------------------------------------

        self.check_level_completion()

        # ------------------------------------------
        # CAMERA
        # ------------------------------------------

        self.camera.update(
            self.player
        )

        # ------------------------------------------
        # COLLECTIBLES
        # ------------------------------------------

        for collectible in self.collectibles:

            if collectible.collected:
                continue

            was_collected = (
                collectible.collected
            )

            collectible.update(
                self.player
            )

            if (
                not was_collected
                and collectible.collected
            ):
                self.score += 1

        # ------------------------------------------
        # CHECKPOINTS
        # ------------------------------------------

        for checkpoint in self.checkpoints:

            checkpoint.update(
                self.player
            )

            if checkpoint.activated:

                self.current_checkpoint = (
                    checkpoint
                )

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen):

        # ==========================================
        # GROUND
        # ==========================================

        ground_rect = self.camera.apply(
            self.ground.rect
        )

        pygame.draw.rect(
            screen,
            (80, 180, 80),
            ground_rect
        )

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
        # PLATFORMS
        # ==========================================

        for platform in self.platforms:

            if platform is self.ground:
                continue

            camera_rect = self.camera.apply(
                platform.rect
            )

            pygame.draw.rect(
                screen,
                (100, 70, 40),
                camera_rect
            )

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
        # CHECKPOINTS
        # ==========================================

        for checkpoint in self.checkpoints:

            checkpoint.draw(
                screen,
                self.camera
            )

        # ==========================================
        # COLLECTIBLES
        # ==========================================

        for collectible in self.collectibles:

            collectible.draw(
                screen,
                self.camera
            )

        # ==========================================
        # FINISH FLAG
        # ==========================================

        finish_screen_x = (
            self.finish_x
            - self.camera.x
        )

        pygame.draw.rect(
            screen,
            (80, 80, 80),
            (
                finish_screen_x,
                HEIGHT - 180,
                6,
                100
            )
        )

        pygame.draw.polygon(
            screen,
            (255, 220, 50),
            [
                (
                    finish_screen_x + 6,
                    HEIGHT - 180
                ),
                (
                    finish_screen_x + 45,
                    HEIGHT - 165
                ),
                (
                    finish_screen_x + 6,
                    HEIGHT - 150
                )
            ]
        )

        # ==========================================
        # PLAYER
        # ==========================================

        player_rect = self.camera.apply(
            self.player.rect
        )

        self.player.draw(
            screen,
            player_rect
        )

        # ==========================================
        # SCORE
        # ==========================================

        score_text = self.font.render(
            f"Carrots: {self.score}",
            True,
            (255, 255, 255)
        )

        shadow_text = self.font.render(
            f"Carrots: {self.score}",
            True,
            (0, 0, 0)
        )

        screen.blit(
            shadow_text,
            (21, 21)
        )

        screen.blit(
            score_text,
            (20, 20)
        )

        # ==========================================
        # LEVEL COMPLETE SCREEN
        # ==========================================

        if self.level_complete:

            overlay = pygame.Surface(
                screen.get_size(),
                pygame.SRCALPHA
            )

            overlay.fill(
                (0, 0, 0, 150)
            )

            screen.blit(
                overlay,
                (0, 0)
            )

            complete_text = (
                self.big_font.render(
                    "LEVEL COMPLETE!",
                    True,
                    (255, 255, 255)
                )
            )

            score_complete = (
                self.font.render(
                    f"Carrots Collected: {self.score}",
                    True,
                    (255, 220, 50)
                )
            )

            screen.blit(
                complete_text,
                complete_text.get_rect(
                    center=(
                        screen.get_width() // 2,
                        screen.get_height() // 2 - 40
                    )
                )
            )

            screen.blit(
                score_complete,
                score_complete.get_rect(
                    center=(
                        screen.get_width() // 2,
                        screen.get_height() // 2 + 30
                    )
                )
            )