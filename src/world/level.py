import pygame
import random

from src.settings import HEIGHT, WORLD_WIDTH
from src.entities.player import Player
from src.entities.platform import Platform
from src.entities.moving_platform import MovingPlatform
from src.entities.collectible import Collectible
from src.entities.checkpoint import Checkpoint
from src.world.camera import Camera
from src.world.platform_generator import PlatformGenerator
from src.entities.obstacle import Obstacle
from src.entities.enemy import Enemy
from src.systems.save_system import save_game, load_game
from src.effects.particle import Particle
from src.entities.npc import NPC
from src.systems.dialogue import Dialogue

class Level:

    def __init__(self, seed=None, sound_manager = None):

        self.sound_manager = sound_manager

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
        # MOVING PLATFORMS
        # ==========================================

        self.moving_platforms = []

        self.generate_moving_platforms()
        # ==========================================
        # DEEP PITS
        # ==========================================

        self.pits = []
        self.generate_pits()

        # ==========================================
        # PLAYER
        # ==========================================

        self.player_start_x = 100
        self.player_start_y = HEIGHT - 160

        self.player = Player(
            self.player_start_x,
            self.player_start_y
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
        # LOAD SAVED GAME
        # ==========================================

        load_game(self)

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
        # OBSTACLES
        # ==========================================

        self.obstacles = []

        self.generate_obstacles()
        # ==========================================
        # ENEMY DAMAGE
        # ==========================================

        self.damage_cooldown = 0
        self.damage_cooldown_max = 60

        # Death screen effect
        self.death_flash_timer = 0
        self.death_flash_duration = 21

        self.particles = []

        self.npcs = [
            NPC(
                600,
                400,
                name="Snackland Guide",
                dialogue=[
                    "Welcome to Snackland!",
                    "Collect the stars and rescue your friends!",
                    "Good luck, Carrot!"
                ]
            ),

            NPC(
                1200,
                400,
                name="Chef Tomato",
                dialogue=[
                    "Hey Carrot!",
                    "The next area is dangerous.",
                    "Watch out for the enemies!"
                ]
            )
        ]

        self.dialogue = Dialogue(self.npcs[0].dialogue)
        self.current_npc = None

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
                checkpoint_y,
                len(self.checkpoints)
            )

            self.checkpoints.append(
                checkpoint
            )

            next_checkpoint_x = (
                checkpoint_x
                + checkpoint_spacing
            )
            # ==============================================

    # GENERATE DEEP PITS
    # ==============================================

    def generate_pits(self):

        self.pits.clear()

        # Need at least two platforms
        if len(self.platforms) < 3:
            return

        # Start checking after the first few platforms
        for i in range(1, len(self.platforms) - 1):

            current_platform = self.platforms[i]
            next_platform = self.platforms[i + 1]

            # ======================================
            # GAP BETWEEN PLATFORMS
            # ======================================

            gap_start = current_platform.rect.right
            gap_end = next_platform.rect.left

            gap_width = gap_end - gap_start

            # ======================================
            # GAP TOO SMALL
            # ======================================

            if gap_width < 120:
                continue

            # ======================================
            # DON'T MAKE EVERY GAP A PIT
            # ======================================

            progress = (
                    current_platform.rect.centerx
                    / self.width
            )

            if progress < 0.25:

                pit_chance = 0.25

            elif progress < 0.60:

                pit_chance = 0.40

            else:

                pit_chance = 0.55

            if random.random() > pit_chance:
                continue

            # ======================================
            # KEEP SAFE LANDING AREA
            # ======================================

            safe_margin = 25

            pit_left = gap_start + safe_margin
            pit_right = gap_end - safe_margin

            pit_width = (
                    pit_right - pit_left
            )

            # ======================================
            # PIT TOO SMALL
            # ======================================

            if pit_width < 80:
                continue

            # ======================================
            # LIMIT PIT SIZE
            # ======================================

            # ======================================
            # PIT DIFFICULTY
            # ======================================

            if progress < 0.35:

                pit_limit = random.randint(
                    140,
                    180
                )

            elif progress < 0.70:

                pit_limit = random.randint(
                    160,
                    210
                )

            else:

                pit_limit = random.randint(
                    180,
                    230
                )

            pit_width = min(
                pit_width,
                pit_limit
            )

            # Center the pit inside the gap

            pit_center = (
                    (pit_left + pit_right) // 2
            )

            pit_left = (
                    pit_center
                    - pit_width // 2
            )

            # ======================================
            # CREATE PIT
            # ======================================

            pit = pygame.Rect(
                pit_left,
                HEIGHT - 80,
                pit_width,
                80
            )

            self.pits.append(pit)

    # ==============================================
    # GENERATE MOVING PLATFORMS
    # ==============================================

    def generate_moving_platforms(self):

        self.moving_platforms.clear()

        # ==========================================
        # FIXED POSITIONS FOR NOW
        # ==========================================

        positions = [
            (1800, 420, "horizontal"),
            (3600, 350, "vertical"),
            (5400, 430, "horizontal"),
            (7200, 360, "vertical"),
            (8600, 420, "horizontal")
        ]

        for x, y, movement_type in positions:

            platform = MovingPlatform(
                x,
                y,
                140,
                20,
                movement_type=movement_type,
                movement_distance=120,
                movement_speed=1.0
            )

            self.moving_platforms.append(
                platform
            )


    # ==============================================
    # RESPAWN
    # ==============================================

    def respawn_player(self):

        # ==========================================
        # RED DEATH EFFECT
        # ==========================================

        self.death_flash_timer = (
            self.death_flash_duration
        )

        # Death particles
        self.create_particles(
            self.player.rect.centerx,
            self.player.rect.centery,
            (255, 100, 50),
            count=20
        )

        # ==========================================
        # RESPAWN POSITION
        # ==========================================

        if self.current_checkpoint is not None:

            self.player.rect.x = (
                self.current_checkpoint.respawn_x
            )

            self.player.rect.y = (
                self.current_checkpoint.respawn_y
            )

        else:

            self.player.rect.x = (
                self.player_start_x
            )

            self.player.rect.y = (
                self.player_start_y
            )

        # ==========================================
        # RESET PHYSICS
        # ==========================================

        self.player.velocity_y = 0
        self.player.on_ground = False
        self.player.current_platform = None

        # ==========================================
        # RESPAWN EFFECT
        # ==========================================

        self.player.start_respawn_effect()

    # ==============================================
    # CHECK DEATH
    # ==============================================

    def check_player_death(self):

        if self.player.rect.top > HEIGHT + 300:

            # --------------------------------------
            # DEATH SOUND
            # --------------------------------------

            if self.sound_manager is not None:
                self.sound_manager.play(
                    "death"
                )

            # --------------------------------------
            # RESPAWN EFFECT
            # --------------------------------------

            self.player.start_respawn_effect()

            # --------------------------------------
            # RESPAWN
            # --------------------------------------

            # Pit death particles
            self.create_particles(
                self.player.rect.centerx,
                self.player.rect.centery,
                (255, 100, 50),
                count=20
            )

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

        if self.death_flash_timer > 0:
            self.death_flash_timer -= 1

        # ------------------------------------------
        # MOVING PLATFORMS
        # ------------------------------------------

        for platform in self.moving_platforms:
            platform.update()

        # ------------------------------------------
        # PLAYER
        # ------------------------------------------

        collision_platforms = (
                self.platforms
                + self.moving_platforms
                + self.obstacles
        )

        # ------------------------------------------
        # REMOVE GROUND COLLISION INSIDE PITS
        # ------------------------------------------

        if self.player.rect.bottom >= HEIGHT - 100:

            collision_platforms = []

            for platform in self.platforms:

                # Never remove normal platforms

                if platform is not self.ground:
                    collision_platforms.append(
                        platform
                    )

                    continue

                # Check whether player's center
                # is inside a pit

                player_center_x = (
                    self.player.rect.centerx
                )

                inside_pit = False

                for pit in self.pits:

                    if pit.left <= player_center_x <= pit.right:
                        inside_pit = True
                        break

                if not inside_pit:
                    collision_platforms.append(
                        platform
                    )

            # --------------------------------------
            # KEEP MOVING PLATFORMS
            # --------------------------------------

            collision_platforms.extend(
                self.moving_platforms
            )

            # --------------------------------------
            # KEEP OBSTACLES
            # --------------------------------------

            collision_platforms.extend(
                self.obstacles
            )

        # ------------------------------------------
        # PLAYER
        # ------------------------------------------

        self.player.update(
            collision_platforms
        )

        # ------------------------------------------
        # ROCK COLLISION / DAMAGE
        # ------------------------------------------

        for obstacle in self.obstacles:

            if not obstacle.active:
                continue

            if not obstacle.check_collision(
                    self.player
            ):
                continue

            # --------------------------------------
            # IF STANDING ON TOP OF ROCK
            # --------------------------------------

            if (
                    self.player.rect.bottom
                    <= obstacle.rect.top + 5
            ):
                continue

            # --------------------------------------
            # DAMAGE
            # --------------------------------------

            if self.damage_cooldown > 0:
                continue

            self.player.health = max(
                0,
                self.player.health - 1
            )

            self.damage_cooldown = (
                self.damage_cooldown_max
            )

            self.player.take_damage()

            # --------------------------------------
            # PUSH PLAYER AWAY
            # --------------------------------------

            if (
                    self.player.rect.centerx
                    < obstacle.rect.centerx
            ):

                self.player.rect.right = (
                    obstacle.rect.left
                )

            else:

                self.player.rect.left = (
                    obstacle.rect.right
                )

            self.player.velocity_y = -5
        # ------------------------------------------
        # DEATH
        # ------------------------------------------

        self.check_player_death()

        # ------------------------------------------
        # HEALTH DEATH
        # ------------------------------------------

        # ------------------------------------------
        # HEALTH DEATH
        # ------------------------------------------


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
            if not collectible.collected and collectible.rect.colliderect(self.player.rect):

                # Save position before collecting
                particle_x = collectible.rect.centerx
                particle_y = collectible.rect.centery

                # Collect the item
                collectible.collect()
                self.score += collectible.value

                # Collect sound
                if self.sound_manager is not None:
                    self.sound_manager.play("collect")

                # Golden pickup particles
                self.create_particles(
                    particle_x,
                    particle_y,
                    (255, 215, 0),
                    count=10
                )

        # ------------------------------------------
        # CHECKPOINTS
        # ------------------------------------------

        for checkpoint in self.checkpoints:

            was_activated = checkpoint.activated

            checkpoint.update(
                self.player
            )

            if checkpoint.activated:

                self.current_checkpoint = checkpoint

                # ----------------------------------
                # NEW CHECKPOINT ACTIVATED
                # ----------------------------------

                if not was_activated:

                    # Save progress
                    save_game(self)

                    # Play checkpoint sound
                    if self.sound_manager is not None:
                        self.sound_manager.play(
                            "checkpoint"
                        )

                    # Checkpoint activation particles
                    self.create_particles(
                        checkpoint.rect.centerx,
                        checkpoint.rect.centery,
                        (80, 255, 120),
                        count=15
                    )


        # ------------------------------------------
        # ENEMIES
        # ------------------------------------------

        for enemy in self.enemies:
            enemy.update()

        self.handle_enemy_collisions()
        self.update_particles()
        # ------------------------------------------
        # HEALTH DEATH
        # ------------------------------------------

        if self.player.health <= 0:

            if self.sound_manager is not None:
                self.sound_manager.play(
                    "death"
                )

            self.player.health = 3

            self.respawn_player()



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
        # OBSTACLES
        # ==========================================

        for obstacle in self.obstacles:
            obstacle.draw(
                screen,
                self.camera
            )
        # ==========================================
        # MOVING PLATFORMS
        # ==========================================

        for platform in self.moving_platforms:

            platform.draw(
                screen,
                self.camera
            )
        # ==========================================
        # DEEP PITS
        # ==========================================

        for pit in self.pits:

            pit_rect = self.camera.apply(
                pit
            )

            # Dark empty area

            pygame.draw.rect(
                screen,
                (20, 20, 20),
                pit_rect
            )

            # Small warning edge

            pygame.draw.line(
                screen,
                (180, 60, 40),
                (
                    pit_rect.left,
                    pit_rect.top
                ),
                (
                    pit_rect.right,
                    pit_rect.top
                ),
                5
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
        # HEART HEALTH BAR
        # ==========================================

        max_health = 3

        for i in range(max_health):

            heart_x = 20 + i * 42
            heart_y = 62

            # --------------------------------------
            # HEART SHAPE
            # --------------------------------------

            heart_points = [
                (heart_x + 12, heart_y + 27),
                (heart_x + 2, heart_y + 15),
                (heart_x, heart_y + 8),
                (heart_x + 2, heart_y + 3),
                (heart_x + 7, heart_y),
                (heart_x + 12, heart_y + 5),
                (heart_x + 17, heart_y),
                (heart_x + 22, heart_y + 3),
                (heart_x + 24, heart_y + 8),
                (heart_x + 22, heart_y + 15)
            ]

            # --------------------------------------
            # FULL HEART
            # --------------------------------------

            if i < self.player.health:

                pygame.draw.polygon(
                    screen,
                    (220, 40, 50),
                    heart_points
                )

            # --------------------------------------
            # EMPTY HEART
            # --------------------------------------

            else:

                pygame.draw.lines(
                    screen,
                    (100, 100, 100),
                    True,
                    heart_points,
                    2
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
        # ==========================================
        # DEATH FLASH
        # ==========================================

        if self.death_flash_timer > 0:

            flash = pygame.Surface(
                screen.get_size(),
                pygame.SRCALPHA
            )

            alpha = int(
                140
                * (
                    self.death_flash_timer
                    / self.death_flash_duration
                )
            )

            flash.fill(
                (255, 60, 60, alpha)
            )

            screen.blit(
                flash,
                (0, 0)
            )

        for npc in self.npcs:

            npc.draw(
                screen,
                self.camera
            )

            # ==========================================
            # TALK PROMPT
            # ==========================================

            distance = abs(
                self.player.rect.centerx -
                npc.rect.centerx
            )

            if distance < 80 and not self.dialogue.active:
                prompt_font = pygame.font.Font(
                    None,
                    22
                )

                prompt = prompt_font.render(
                    "Press E to talk",
                    True,
                    (255, 255, 255)
                )

                prompt_rect = prompt.get_rect(
                    center=(
                        npc.rect.centerx - self.camera.x,
                        npc.rect.top - 35
                    )
                )

                # Small background
                background_rect = prompt_rect.inflate(
                    12,
                    8
                )

                pygame.draw.rect(
                    screen,
                    (30, 30, 30),
                    background_rect
                )

                screen.blit(
                    prompt,
                    prompt_rect
                )

        for particle in self.particles:
            particle.draw(
                screen,
                self.camera
            )

        self.draw_dialogue(screen)

    # ==============================================
    # GENERATE ENEMIES
    # ==============================================

    # ==============================================
    # GENERATE ENEMIES - DEBUG
    # ==============================================

    def generate_enemies(self):

        self.enemies.clear()

        total_platforms = 0
        small_platforms = 0
        chance_failed = 0
        space_failed = 0
        created = 0

        print("GENERATING ENEMIES...")
        heavy_count = 0
        for platform in self.platforms[1:]:

            total_platforms += 1

            # ======================================
            # PLATFORM SIZE
            # ======================================

            if platform.rect.width < 55:

                small_platforms += 1
                continue

            # ======================================
            # SPAWN CHANCE
            # ======================================

            progress = (
                platform.rect.centerx
                / self.width
            )

            if progress < 0.30:
                spawn_chance = 0.55
            elif progress < 0.60:
                spawn_chance = 0.65
            else:
                spawn_chance = 0.75

            if random.random() > spawn_chance:

                chance_failed += 1
                continue

            # ======================================
            # ENEMY TYPE
            # ======================================

            roll = random.random()

            if progress < 0.30:

                if roll < 0.40:
                    enemy_type = "slime"

                elif roll < 0.75:
                    enemy_type = "fast"

                else:
                    enemy_type = "jumper"

            elif progress < 0.60:

                if roll < 0.20:
                    enemy_type = "slime"

                elif roll < 0.45:
                    enemy_type = "fast"

                elif roll < 0.70:
                    enemy_type = "jumper"

                else:
                    enemy_type = "flyer"


            else:

                if roll < 0.10:

                    enemy_type = "slime"


                elif roll < 0.25:

                    enemy_type = "fast"


                elif roll < 0.40:

                    enemy_type = "jumper"


                elif roll < 0.60:

                    enemy_type = "flyer"


                else:

                    enemy_type = "heavy"

                # ======================================
                # FLYER SAFETY
                # ======================================

                if (
                        enemy_type == "flyer"
                        and platform.rect.width < 180
                ):
                    # Small platforms should not have flyers

                    enemy_type = random.choice([
                        "slime",
                        "fast",
                        "jumper"
                    ])

            # ======================================
            # ENEMY SIZE
            # ======================================

            if enemy_type == "heavy":

                # Heavy enemies need larger platforms

                if platform.rect.width < 140:
                    continue

                enemy_width = 50
                enemy_height = 50
                speed = 1

            elif platform.rect.width < 75:

                # Very small platform

                enemy_width = 24
                enemy_height = 24

                if enemy_type == "fast":
                    speed = 1.5
                else:
                    speed = 1.0

            else:

                enemy_width = 32
                enemy_height = 32

                if enemy_type == "fast":
                    speed = 1.5
                else:
                    speed = 1.0

            # ======================================
            # PATROL AREA
            # ======================================

            margin = 20

            left_limit = (
                platform.rect.left + margin
            )

            right_limit = (
                platform.rect.right - margin
            )

            if (
                right_limit - left_limit
                < enemy_width
            ):

                space_failed += 1
                continue

            # ======================================
            # POSITION
            # ======================================

            x = random.randint(
                left_limit,
                right_limit - enemy_width
            )

            y = (
                platform.rect.top
                - enemy_height
            )

            # ======================================
            # CREATE
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

            self.enemies.append(enemy)
            if enemy_type == "heavy":
                heavy_count += 1

            created += 1

        # ==========================================
        # DEBUG RESULTS
        # ==========================================

        print(
            "TOTAL PLATFORMS:",
            total_platforms
        )

        print(
            "SMALL PLATFORMS:",
            small_platforms
        )

        print(
            "CHANCE FAILED:",
            chance_failed
        )

        print(
            "SPACE FAILED:",
            space_failed
        )

        print(
            "TOTAL ENEMIES GENERATED:",
            created
        )
        print(
            "HEAVY ENEMIES:",
            heavy_count
        )

    # ==============================================
    # GENERATE OBSTACLES
    # ==============================================

    def generate_obstacles(self):

        self.obstacles.clear()

        created = 0

        print("GENERATING OBSTACLES...")

        for platform in self.platforms[1:]:

            # ======================================
            # PLATFORM SIZE
            # ======================================

            if platform.rect.width < 150:
                continue

            # ======================================
            # DON'T PUT OBSTACLE EVERYWHERE
            # ======================================

            progress = (
                    platform.rect.centerx
                    / self.width
            )

            if progress < 0.30:

                spawn_chance = 0.15

            elif progress < 0.60:

                spawn_chance = 0.25

            else:

                spawn_chance = 0.35

            if random.random() > spawn_chance:
                continue

            # ======================================
            # SIZE
            # ======================================

            obstacle_width = random.randint(
                35,
                50
            )

            obstacle_height = random.randint(
                30,
                45
            )

            # ======================================
            # SAFE MARGIN
            # ======================================

            margin = 25

            left_limit = (
                    platform.rect.left
                    + margin
            )

            right_limit = (
                    platform.rect.right
                    - margin
                    - obstacle_width
            )

            # ======================================
            # NOT ENOUGH SPACE
            # ======================================

            if right_limit <= left_limit:
                continue

            # ======================================
            # POSITION
            # ======================================

            x = random.randint(
                left_limit,
                right_limit
            )

            y = (
                    platform.rect.top
                    - obstacle_height
            )

            # ======================================
            # CREATE
            # ======================================

            obstacle = Obstacle(
                x,
                y,
                obstacle_width,
                obstacle_height,
                "rock"
            )

            self.obstacles.append(
                obstacle
            )

            created += 1

        print(
            "TOTAL OBSTACLES:",
            created
        )

    # ==============================================
    # ENEMY COLLISION
    # ==============================================
    def handle_enemy_collisions(self):

        for enemy in self.enemies:

            if not enemy.alive:
                continue

            if not enemy.check_collision(self.player):
                continue

            # ======================================
            # PLAYER LANDING ON ENEMY
            # ======================================

            player_bottom = self.player.rect.bottom
            enemy_top = enemy.rect.top

            if (
                    self.player.velocity_y > 0
                    and player_bottom <= enemy_top + 15
            ):

                # ==================================
                # HEAVY ENEMY
                # ==================================

                if enemy.enemy_type == "heavy":

                    if self.damage_cooldown > 0:
                        continue

                    # Damage player
                    self.player.health = max(
                        0,
                        self.player.health - 1
                    )

                    print(
                        "HEAVY HIT - HEALTH:",
                        self.player.health
                    )

                    self.player.take_damage()

                    # 🔊 DAMAGE SOUND
                    if self.sound_manager is not None:
                        self.sound_manager.play(
                            "damage"
                        )

                    # Damage particles
                    self.create_particles(
                        self.player.rect.centerx,
                        self.player.rect.centery,
                        (255, 80, 80),
                        count=10
                    )

                    self.damage_cooldown = (
                        self.damage_cooldown_max
                    )

                    self.player.velocity_y = -5

                # ==================================
                # NORMAL ENEMY
                # ==================================

                else:
                    enemy.alive = False
                    if self.sound_manager is not None:
                        self.sound_manager.play("stomp")

                    # Enemy stomp particles
                    self.create_particles(
                        enemy.rect.centerx,
                        enemy.rect.centery,
                        (120, 255, 120),
                        count=12

                    )
                    self.player.rect.bottom = enemy.rect.top
                    self.player.velocity_y = self.player.jump_strength * 0.65

            # ======================================
            # SIDE COLLISION
            # ======================================

            else:

                if self.damage_cooldown > 0:
                    continue

                # Damage player
                self.player.health = max(
                    0,
                    self.player.health - 1
                )

                print(
                    "ENEMY HIT - HEALTH:",
                    self.player.health
                )

                self.player.take_damage()

                # 🔊 DAMAGE SOUND
                if self.sound_manager is not None:
                    self.sound_manager.play(
                        "damage"
                    )
                # Damage particles
                self.create_particles(
                    self.player.rect.centerx,
                    self.player.rect.centery,
                    (255, 80, 80),
                    count=10
                )

                self.damage_cooldown = (
                    self.damage_cooldown_max
                )

                # ==================================
                # PUSH PLAYER AWAY
                # ==================================

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

                self.player.velocity_y = -5

    def update_particles(self):
        for particle in self.particles:
            particle.update()

        self.particles = [
            particle
            for particle in self.particles
            if particle.is_alive()
        ]

    def create_particles(self, x, y, color, count=8):
        for _ in range(count):
            self.particles.append(
                Particle(
                    x,
                    y,
                    color
                )
            )

    def interact_with_npc(self):
        if self.dialogue.active:
            self.dialogue.next_line()

            if not self.dialogue.active:
                self.current_npc = None

            return

        for npc in self.npcs:
            distance = abs(
                self.player.rect.centerx -
                npc.rect.centerx
            )

            if distance < 80:
                self.current_npc = npc
                self.dialogue = Dialogue(npc.dialogue)
                self.dialogue.start()
                break

    def draw_dialogue(self, screen):

        if not self.dialogue.active:
            return

        # ==========================================
        # DIALOGUE BOX
        # ==========================================

        box_width = 700
        box_height = 140

        box_x = (
                        screen.get_width() - box_width
                ) // 2

        box_y = (
                screen.get_height() - box_height - 40
        )

        # Background
        pygame.draw.rect(
            screen,
            (30, 30, 30),
            (
                box_x,
                box_y,
                box_width,
                box_height
            )
        )

        # Border
        pygame.draw.rect(
            screen,
            (255, 220, 80),
            (
                box_x,
                box_y,
                box_width,
                box_height
            ),
            4
        )

        # ==========================================
        # TEXT
        # ==========================================

        name_font = pygame.font.Font(None, 32)
        name_surface = name_font.render(
            self.current_npc.name,
            True,
            (255, 220, 80)
        )

        name_rect = name_surface.get_rect(
            center=(box_x + box_width // 2, box_y + 25)
        )

        screen.blit(name_surface, name_rect)

        text = self.dialogue.get_current_line()

        dialogue_font = pygame.font.Font(
            None,
            28
        )

        text_surface = dialogue_font.render(
            text,
            True,
            (255, 255, 255)
        )

        text_rect = text_surface.get_rect(
            center=(
                box_x + box_width // 2,
                box_y + 70
            )
        )

        screen.blit(
            text_surface,
            text_rect
        )

        # ==========================================
        # INSTRUCTION
        # ==========================================

        instruction = dialogue_font.render(
            "Press E to continue",
            True,
            (200, 200, 200)
        )

        instruction_rect = instruction.get_rect(
            center=(
                box_x + box_width // 2,
                box_y + 110
            )
        )

        screen.blit(
            instruction,
            instruction_rect
        )