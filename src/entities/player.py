import pygame

from src.settings import (
    WIDTH,
    WORLD_WIDTH,
    PLAYER_SPEED,
    PLAYER_GRAVITY,
    PLAYER_JUMP_STRENGTH
)

from src.settings import WIDTH, WORLD_WIDTH
from src.entities.game_object import GameObject
LANDING_TOLERANCE = 15

class Player(GameObject):

    def __init__(self, x, y):

        super().__init__(x, y, 40, 60)

        # Movement
        self.speed = PLAYER_SPEED

        # Physics
        self.velocity_y = 0
        self.gravity = PLAYER_GRAVITY
        self.jump_strength = PLAYER_JUMP_STRENGTH

        # State
        self.on_ground = False
        self.facing_right = True

        # Health
        self.health = 3

        # Animation
        self.animation_timer = 0
        self.animation_frame = 0

        # Coyote time
        self.coyote_time = 0
        self.coyote_time_max = 8

    # --------------------------------------------------
    # INPUT
    # --------------------------------------------------

    def handle_input(self):

        keys = pygame.key.get_pressed()

        moving = False

        # Move left
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:

            self.rect.x -= self.speed

            self.facing_right = False

            moving = True

        # Move right
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:

            self.rect.x += self.speed

            self.facing_right = True

            moving = True

        return moving

    # --------------------------------------------------
    # JUMP
    # --------------------------------------------------

    def jump(self):

        if self.on_ground or self.coyote_time > 0:
            self.velocity_y = self.jump_strength

            self.on_ground = False

            self.coyote_time = 0

    # --------------------------------------------------
    # GRAVITY
    # --------------------------------------------------

    def apply_gravity(self):

        self.velocity_y += self.gravity

        self.rect.y += self.velocity_y

    # --------------------------------------------------
    # COLLISION
    # --------------------------------------------------

    def handle_platform_collision(self, platforms, previous_rect):

        was_on_ground = self.on_ground

        self.on_ground = False

        for platform in platforms:

            landing_rect = platform.rect.inflate(
                LANDING_TOLERANCE * 2,
                0
            )

            if self.velocity_y >= 0:

                if (previous_rect.bottom <= platform.rect.top and self.rect.bottom >= platform.rect.top and self.rect.colliderect(landing_rect) ):
                    self.rect.bottom = platform.rect.top

                    self.velocity_y = 0

                    self.on_ground = True

                    break

        # Update coyote timer
        if self.on_ground:

            self.coyote_time = self.coyote_time_max

        elif was_on_ground and self.coyote_time > 0:

            self.coyote_time -= 1

        elif self.coyote_time > 0:

            self.coyote_time -= 1
    # --------------------------------------------------
    # ANIMATION
    # --------------------------------------------------

    def update_animation(self, moving):

        if moving and self.on_ground:

            self.animation_timer += 1

            if self.animation_timer >= 10:

                self.animation_timer = 0

                self.animation_frame += 1

                if self.animation_frame > 1:

                    self.animation_frame = 0

        else:

            self.animation_frame = 0

            self.animation_timer = 0

    # --------------------------------------------------
    # UPDATE
    # --------------------------------------------------

    def update(self, platforms):

        previous_rect = self.rect.copy()

        moving = self.handle_input()

        # Screen boundaries
        if self.rect.left < 0:
            self.rect.left = 0

        if self.rect.right > WORLD_WIDTH:
            self.rect.right = WORLD_WIDTH

        self.apply_gravity()

        self.handle_platform_collision(
            platforms,
            previous_rect
        )

        self.update_animation(moving)

    # --------------------------------------------------
    # DRAW
    # --------------------------------------------------

    def draw(self, screen, camera_rect=None):

        if camera_rect is None:
            camera_rect = self.rect

        x = camera_rect.x
        y = camera_rect.y

        # ---------------------------------------------
        # CARROT BODY
        # ---------------------------------------------

        body = pygame.Rect(
            x + 8,
            y + 15,
            24,
            40
        )

        pygame.draw.ellipse(
            screen,
            (255, 140, 0),
            body
        )

        # ---------------------------------------------
        # CARROT LEAVES
        # ---------------------------------------------

        pygame.draw.ellipse(
            screen,
            (50, 180, 70),
            (x + 5, y, 15, 18)
        )

        pygame.draw.ellipse(
            screen,
            (70, 200, 80),
            (x + 15, y - 4, 15, 20)
        )

        pygame.draw.ellipse(
            screen,
            (40, 160, 60),
            (x + 23, y + 2, 12, 15)
        )

        # ---------------------------------------------
        # EYES
        # ---------------------------------------------

        if self.facing_right:

            left_eye_x = x + 17
            right_eye_x = x + 27

        else:

            left_eye_x = x + 13
            right_eye_x = x + 23

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (left_eye_x, y + 25),
            5
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            (right_eye_x, y + 25),
            5
        )

        # Pupils
        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (left_eye_x, y + 25),
            2
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            (right_eye_x, y + 25),
            2
        )

        # ---------------------------------------------
        # SMILE
        # ---------------------------------------------

        pygame.draw.arc(
            screen,
            (0, 0, 0),
            (x + 13, y + 28, 18, 12),
            0,
            3.14,
            2
        )

        # ---------------------------------------------
        # WALKING EFFECT
        # ---------------------------------------------

        if self.animation_frame == 1 and self.on_ground:

            pygame.draw.circle(
                screen,
                (255, 200, 150),
                (x + 5, y + 57),
                3
            )