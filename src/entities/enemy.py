import pygame


class Enemy:

    def __init__(
        self,
        x,
        y,
        left_limit,
        right_limit,
        speed=2,
        enemy_type="slime",
        platform_top=None
    ):

        # ==========================================
        # POSITION
        # ==========================================

        if enemy_type == "heavy":

            width = 60
            height = 60

        else:

            width = 32
            height = 32

        self.rect = pygame.Rect(
            x,
            y,
            width,
            height
        )

        # ==========================================
        # MOVEMENT
        # ==========================================

        self.speed = speed

        self.direction = 1
        # ==========================================
        # FAST ENEMY
        # ==========================================

        self.fast_timer = 0

        self.fast_burst_timer = 0

        self.fast_burst_duration = 12

        self.fast_burst_cooldown = 120

        self.fast_burst_speed = 2.2

        # ==========================================
        # HEAVY ENEMY
        # ==========================================

        self.heavy_timer = 0

        self.heavy_pause = 0

        self.heavy_pause_duration = 20

        self.heavy_move_duration = 90

        # ==========================================
        # PATROL LIMITS
        # ==========================================

        self.left_limit = left_limit

        self.right_limit = right_limit

        # ==========================================
        # TYPE
        # ==========================================

        self.enemy_type = enemy_type

        # ==========================================
        # STATE
        # ==========================================

        self.alive = True

        # ==========================================
        # JUMPER
        # ==========================================

        self.velocity_y = 0

        self.gravity = 0.5

        self.jump_strength = -10

        self.jump_timer = 0

        self.jump_delay = 90

        self.landing_timer = 0

        self.platform_top = platform_top

        # ==========================================
        # FLYER
        # ==========================================

        self.fly_direction = 1

        self.fly_speed = 1.5

        self.fly_top = y - 40

        self.fly_bottom = y + 40

        self.fly_time = 0

        self.fly_amplitude = 25

        self.fly_center_y = y

    # ==============================================
    # UPDATE
    # ==============================================

    def update(self):

        if not self.alive:
            return

        if self.enemy_type == "slime":

            self.move_horizontal()

        elif self.enemy_type == "fast":

            self.update_fast()

        elif self.enemy_type == "jumper":

            self.move_horizontal()

            self.update_jump()

        elif self.enemy_type == "flyer":

            self.move_horizontal()

            self.update_fly()

        elif self.enemy_type == "heavy":

            self.update_heavy()

    # ==============================================
    # HORIZONTAL MOVEMENT
    # ==============================================

    def move_horizontal(self):

        self.rect.x += (
            self.speed
            * self.direction
        )

        if self.rect.left <= self.left_limit:

            self.rect.left = self.left_limit

            self.direction = 1

        if self.rect.right >= self.right_limit:

            self.rect.right = self.right_limit

            self.direction = -1

    # ==============================================
    # FAST ENEMY
    # ==============================================

    def update_fast(self):

        self.fast_timer += 1

        # ------------------------------------------
        # START BURST
        # ------------------------------------------

        if (
            self.fast_burst_timer == 0
            and self.fast_timer >= self.fast_burst_cooldown
        ):

            self.fast_burst_timer = (
                self.fast_burst_duration
            )

            self.fast_timer = 0

        # ------------------------------------------
        # BURST MOVEMENT
        # ------------------------------------------

        if self.fast_burst_timer > 0:

            self.fast_burst_timer -= 1

            old_speed = self.speed

            self.speed = self.fast_burst_speed

            self.move_horizontal()

            self.speed = old_speed

        else:

            self.move_horizontal()

    # ==============================================
    # HEAVY ENEMY
    # ==============================================

    def update_heavy(self):

        # ------------------------------------------
        # PAUSE
        # ------------------------------------------

        if self.heavy_pause > 0:

            self.heavy_pause -= 1

            return

        # ------------------------------------------
        # MOVE
        # ------------------------------------------

        self.move_horizontal()

        self.heavy_timer += 1

        # ------------------------------------------
        # TAKE A BREAK
        # ------------------------------------------

        if (
            self.heavy_timer
            >= self.heavy_move_duration
        ):

            self.heavy_timer = 0

            self.heavy_pause = (
                self.heavy_pause_duration
            )

    # ==============================================
    # JUMPER
    # ==============================================

    def update_jump(self):

        # ------------------------------------------
        # LANDING PAUSE
        # ------------------------------------------

        if self.landing_timer > 0:
            self.landing_timer -= 1

            return

        # ------------------------------------------
        # JUMP TIMER
        # ------------------------------------------

        self.jump_timer += 1

        if (
                self.jump_timer >= self.jump_delay
                and abs(self.velocity_y) < 0.1
        ):
            self.velocity_y = (
                self.jump_strength
            )

            self.jump_timer = 0

        # ------------------------------------------
        # GRAVITY
        # ------------------------------------------

        self.velocity_y += self.gravity

        self.rect.y += int(
            self.velocity_y
        )

        # ------------------------------------------
        # LANDING
        # ------------------------------------------

        if self.platform_top is not None:

            if (
                    self.rect.bottom >= self.platform_top
                    and self.velocity_y > 0
            ):
                self.rect.bottom = (
                    self.platform_top
                )

                self.velocity_y = 0

                self.landing_timer = 8

    # ==============================================
    # FLYER
    # ==============================================

    def update_fly(self):

        self.fly_time += 1

        # ------------------------------------------
        # HORIZONTAL MOVEMENT
        # ------------------------------------------

        self.rect.x += (
                self.speed
                * self.direction
        )

        if self.rect.left <= self.left_limit:
            self.rect.left = self.left_limit

            self.direction = 1

        if self.rect.right >= self.right_limit:
            self.rect.right = self.right_limit

            self.direction = -1

        # ------------------------------------------
        # SMOOTH VERTICAL MOVEMENT
        # ------------------------------------------

        import math

        offset = (
                math.sin(
                    self.fly_time
                    * 0.025
                )
                * self.fly_amplitude
        )

        self.rect.centery = int(
            self.fly_center_y
            + offset
        )

    # ==============================================
    # PLAYER COLLISION
    # ==============================================

    def check_collision(self, player):

        if not self.alive:
            return False

        return self.rect.colliderect(
            player.rect
        )

    # ==============================================
    # DRAW
    # ==============================================

    def draw(self, screen, camera):

        if not self.alive:
            return

        camera_rect = camera.apply(
            self.rect
        )

        # ==========================================
        # BODY COLOR
        # ==========================================

        if self.enemy_type == "fast":

            body_color = (
                220,
                70,
                70
            )

        elif self.enemy_type == "jumper":

            body_color = (
                220,
                190,
                50
            )

        elif self.enemy_type == "flyer":

            body_color = (
                60,
                150,
                210
            )


        elif self.enemy_type == "heavy":
            body_color = (
                40,
                40,
                40
            )

        else:

            body_color = (
                120,
                70,
                190
            )

        # ==========================================
        # HEAVY BODY
        # ==========================================

        if self.enemy_type == "heavy":

            pygame.draw.rect(
                screen,
                body_color,
                camera_rect,
                border_radius=8
            )

        else:

            pygame.draw.ellipse(
                screen,
                body_color,
                camera_rect
            )

        # ==========================================
        # FLYER WINGS
        # ==========================================

        if self.enemy_type == "flyer":

            left_wing = pygame.Rect(
                camera_rect.x - 10,
                camera_rect.y + 10,
                15,
                20
            )

            right_wing = pygame.Rect(
                camera_rect.right - 5,
                camera_rect.y + 10,
                15,
                20
            )

            pygame.draw.ellipse(
                screen,
                body_color,
                left_wing
            )

            pygame.draw.ellipse(
                screen,
                body_color,
                right_wing
            )

        # ==========================================
        # EYES
        # ==========================================

        eye_y = (
            camera_rect.y
            + camera_rect.height // 3
        )

        left_eye = (
            camera_rect.x
            + camera_rect.width // 3,
            eye_y
        )

        right_eye = (
            camera_rect.x
            + (camera_rect.width * 2) // 3,
            eye_y
        )

        eye_size = 6

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            left_eye,
            eye_size
        )

        pygame.draw.circle(
            screen,
            (255, 255, 255),
            right_eye,
            eye_size
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            left_eye,
            3
        )

        pygame.draw.circle(
            screen,
            (0, 0, 0),
            right_eye,
            3
        )