import pygame
import random

from src.settings import HEIGHT, WORLD_WIDTH
from src.entities.player import Player
from src.entities.platform import Platform
from src.entities.collectible import Collectible
from src.entities.checkpoint import Checkpoint
from src.world.camera import Camera
from src.world.platform_generator import PlatformGenerator
from src.entities.enemy import Enemy


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
        # ==========================================
        # ENEMIES
        # ==========================================

        self.enemies = []
        self.generate_enemies()
        # ==========================================
        # ENEMY DAMAGE
        # ==========================================

        self.damage_cooldown = 0
        self.damage_cooldown_max = 60

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

        if self.damage_cooldown > 0:
            self.damage_cooldown -= 1

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
        # HEALTH DEATH
        # ------------------------------------------

        if self.player.health <= 0:
            self.respawn_player()

            self.player.health = 3

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
        # ------------------------------------------
        # ENEMIES
        # ------------------------------------------

        for enemy in self.enemies:
            enemy.update()
        self.handle_enemy_collisions()

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
        # HEALTH
        # ==========================================

        health_text = self.font.render(
            f"❤️ Health: {self.player.health}",
            True,
            (255, 255, 255)
        )

        health_shadow = self.font.render(
            f"❤️ Health: {self.player.health}",
            True,
            (0, 0, 0)
        )

        screen.blit(
            health_shadow,
            (21, 61)
        )

        screen.blit(
            health_text,
            (20, 60)
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
        # ==========================================
        # ENEMIES
        # ==========================================

        for enemy in self.enemies:
            enemy.draw(
                screen,
                self.camera
            )
    # ==============================================
    # GENERATE ENEMIES
    # ==============================================

    def generate_enemies(self):

        self.enemies.clear()

        # ==========================================
        # GO THROUGH GENERATED PLATFORMS
        # ==========================================

        for platform in self.platforms[1:]:

            width = platform.rect.width

            # ======================================
            # VERY SMALL PLATFORM
            # ======================================

            if width < 110:
                # No enemy
                continue

            # ======================================
            # ENEMY SPAWN CHANCE
            # ======================================

            # Start easier
            difficulty = min(
                platform.rect.x / self.width,
                1.0
            )

            # Base chance
            # ======================================
            # ENEMY SPAWN CHANCE
            # ======================================

            # Difficulty increases across the world.

            difficulty = min(
                platform.rect.x / self.width,
                1.0
            )

            # Start with a reasonable number of enemies
            # and gradually increase them.

            spawn_chance = (
                    0.45
                    + difficulty * 0.35
            )

            if random.random() > spawn_chance:
                continue

            # ======================================
            # PATROL AREA
            # ======================================

            margin = 20

            left_limit = (
                    platform.rect.left
                    + margin
            )

            right_limit = (
                    platform.rect.right
                    - margin
            )

            # ======================================
            # CHOOSE ENEMY SIZE
            # ======================================

            if width >= 260:

                possible_types = [
                    "slime",
                    "fast",
                    "jumper",
                    "flyer",
                    "heavy"
                ]

            elif width >= 190:

                possible_types = [
                    "slime",
                    "fast",
                    "jumper",
                    "flyer"
                ]

            elif width >= 140:

                possible_types = [
                    "slime",
                    "fast",
                    "jumper"
                ]

            else:

                possible_types = [
                    "slime",
                    "fast"
                ]

            # ======================================
            # RANDOM ENEMY TYPE
            # ======================================

            enemy_type = random.choice(
                possible_types
            )

            # ======================================
            # ENEMY SIZE
            # ======================================

            if enemy_type == "heavy":

                enemy_width = 50
                enemy_height = 50

            else:

                enemy_width = 32
                enemy_height = 32

            # ======================================
            # CHECK SPACE
            # ======================================

            if (
                    right_limit
                    - left_limit
                    < enemy_width
            ):
                continue

            # ======================================
            # RANDOM POSITION
            # ======================================

            x = random.randint(
                left_limit,
                right_limit - enemy_width
            )

            # ======================================
            # ENEMY Y POSITION
            # ======================================

            y = (
                    platform.rect.top
                    - enemy_height
            )

            # ======================================
            # SPEED
            # ======================================

            if enemy_type == "slime":

                speed = 2

            elif enemy_type == "fast":

                speed = 3

            elif enemy_type == "jumper":

                speed = 2

            elif enemy_type == "flyer":

                speed = 2

            elif enemy_type == "heavy":

                speed = 1

            else:

                speed = 2

            # ======================================
            # CREATE ENEMY
            # ======================================

            enemy = Enemy(
                x,
                y,
                left_limit,
                right_limit,
                speed,
                enemy_type,
                platform.rect.top
            )

            self.enemies.append(
                enemy
            )
        # ==========================================
        # GUARANTEE MINIMUM ENEMIES
        # ==========================================

        minimum_enemies = 8

        if len(self.enemies) < minimum_enemies:

            for platform in self.platforms[1:]:

                if len(self.enemies) >= minimum_enemies:
                    break

                # Small platforms are skipped

                if platform.rect.width < 100:
                    continue

                # ----------------------------------
                # CHECK EXISTING ENEMY
                # ----------------------------------

                already_has_enemy = False

                for enemy in self.enemies:

                    if abs(
                        enemy.rect.centerx
                        - platform.rect.centerx
                    ) < 100:

                        already_has_enemy = True
                        break

                if already_has_enemy:
                    continue

                # ----------------------------------
                # ENEMY TYPE
                # ----------------------------------

                enemy_type = random.choice([
                    "slime",
                    "fast"
                ])

                if enemy_type == "slime":
                    speed = 2
                else:
                    speed = 3

                enemy_width = 32

                # ----------------------------------
                # PATROL LIMITS
                # ----------------------------------

                margin = 20

                left_limit = (
                    platform.rect.left
                    + margin
                )

                right_limit = (
                    platform.rect.right
                    - margin
                )

                # ----------------------------------
                # CHECK SPACE
                # ----------------------------------

                if (
                    right_limit
                    - left_limit
                    < enemy_width
                ):
                    continue

                # ----------------------------------
                # POSITION
                # ----------------------------------

                x = random.randint(
                    left_limit,
                    right_limit - enemy_width
                )

                y = (
                    platform.rect.top
                    - 32
                )

                # ----------------------------------
                # CREATE ENEMY
                # ----------------------------------

                enemy = Enemy(
                    x,
                    y,
                    left_limit,
                    right_limit,
                    speed,
                    enemy_type,
                    platform.rect.top
                )

                self.enemies.append(
                    enemy
                )

    # ==============================================
    # ENEMY COLLISION
    # ==============================================

    def handle_enemy_collisions(self):

        for enemy in self.enemies:

            if not enemy.alive:
                continue

            if not enemy.check_collision(
                    self.player
            ):
                continue

            # ======================================
            # PLAYER LANDING ON ENEMY
            # ======================================

            player_bottom = self.player.rect.bottom

            enemy_top = enemy.rect.top

            # Player is falling
            if (
                    self.player.velocity_y > 0
                    and player_bottom
                    <= enemy_top + 15
            ):

                # ======================================
                # STOMP ENEMY
                # ======================================

                if enemy.enemy_type == "heavy":

                    # Heavy cannot be stomped

                    if self.damage_cooldown <= 0:
                        self.player.health -= 1

                        self.damage_cooldown = (
                            self.damage_cooldown_max
                        )

                        self.player.velocity_y = -5

                else:

                    # Normal enemies can be stomped

                    enemy.alive = False

                    self.player.rect.bottom = (
                        enemy.rect.top
                    )

                    self.player.velocity_y = (
                            self.player.jump_strength * 0.65
                    )

            # ======================================
            # SIDE COLLISION
            # ======================================

            else:

                if self.damage_cooldown > 0:
                    continue

                self.player.health = max(
                    0,
                    self.player.health - 1
                )

                self.damage_cooldown = (
                    self.damage_cooldown_max
                )

                # Push player away
                if (
                        self.player.rect.centerx
                        < enemy.rect.centerx
                ):

                    self.player.rect.right = (
                        enemy.rect.left
                    )

                else:

                    self.player.rect.left = (
                        enemy.rect.right
                    )

                # Stop downward movement
                self.player.velocity_y = -5